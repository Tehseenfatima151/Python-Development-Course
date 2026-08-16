import pytest
from app import create_app
from config import Config
from models import db, Message, Room, MessageReaction
from models.user import user_manager
from sockets import socketio
from utils.helpers import (
    get_username_color,
    sanitize_text,
    validate_username,
    validate_room,
    validate_message,
    validate_reaction,
)


class TestConfig(Config):
    __test__ = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    REQUIRE_REDIS = False
    REDIS_URL = None
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    """Create a clean Flask test application with in-memory database."""
    test_app = create_app(TestConfig)
    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """HTTP test client."""
    return app.test_client()


@pytest.fixture
def socket_client(app):
    """Flask-SocketIO test client fixture."""
    return socketio.test_client(app)


# ============================================================================
# 1. Helper and Sanitization Unit Tests
# ============================================================================

def test_color_determinism():
    """Test that username colors are deterministic and consistent."""
    color1 = get_username_color("Sarah")
    color2 = get_username_color("Sarah")
    color3 = get_username_color("sarah")
    assert color1 == color2
    assert color1 == color3
    assert color1.startswith("#")


def test_sanitize_text():
    """Test string sanitization stripping control characters while preserving emojis."""
    raw = "  Hello \x00\x08World! 🚀   "
    cleaned = sanitize_text(raw)
    assert cleaned == "Hello World! 🚀"


def test_validations():
    """Test validation helpers for username, room, message, and reactions."""
    # Username
    assert validate_username("Alex")[0] is True
    assert validate_username("A")[0] is False  # Too short
    assert validate_username("")[0] is False  # Empty
    assert validate_username("a" * 35)[0] is False  # Too long
    assert validate_username("<script>")[0] is False  # Invalid chars

    # Room
    assert validate_room("general")[0] is True
    assert validate_room("dev-team")[0] is True
    assert validate_room("")[0] is False

    # Message
    assert validate_message("Hello there!")[0] is True
    assert validate_message("   ")[0] is False
    assert validate_message("m" * 1005)[0] is False

    # Reaction
    assert validate_reaction("👍")[0] is True
    assert validate_reaction("❤️")[0] is True
    assert validate_reaction("")[0] is False
    assert validate_reaction("invalid_emoji")[0] is False


# ============================================================================
# 2. Database & Model Tests
# ============================================================================

def test_message_model_persistence(app):
    """Test that messages are saved in SQLite and can be retrieved chronologically."""
    with app.app_context():
        msg1 = Message(username="Alice", room="general", content="First message", username_color="#3b82f6")
        msg2 = Message(username="Bob", room="general", content="Second message", username_color="#10b981")
        msg_other = Message(username="Charlie", room="random", content="Random message", username_color="#8b5cf6")

        db.session.add_all([msg1, msg2, msg_other])
        db.session.commit()

        messages = Message.query.filter_by(room="general").order_by(Message.timestamp.asc()).all()
        assert len(messages) == 2
        assert messages[0].username == "Alice"
        assert messages[0].content == "First message"
        assert messages[1].username == "Bob"

        d = messages[0].to_dict()
        assert d["username"] == "Alice"
        assert d["message"] == "First message"
        assert d["room"] == "general"
        assert "timestamp" in d
        assert "reactions" in d
        assert "reply_to" in d
        assert "is_pinned" in d


# ============================================================================
# 3. HTTP Route & Dynamic Room Tests
# ============================================================================

def test_index_route(client):
    """Test that the index route loads correctly with 200 OK."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"LiveChat" in response.data
    assert b"join-screen" in response.data


def test_health_route(client):
    """Test health check route."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["components"]["database"]["status"] == "connected"


def test_room_messages_api(client, app):
    """Test REST API endpoint for room message history."""
    with app.app_context():
        msg = Message(username="Tester", room="dev", content="Test message API", username_color="#3b82f6")
        db.session.add(msg)
        db.session.commit()

    response = client.get("/api/rooms/dev/messages")
    assert response.status_code == 200
    data = response.get_json()
    assert data["room"] == "dev"
    assert data["count"] == 1
    assert data["messages"][0]["content"] == "Test message API"


def test_dynamic_room_creation_and_listing(client, app):
    """Test creating a dynamic room via POST and listing it via GET."""
    # List initial default rooms
    get_res = client.get("/api/rooms")
    assert get_res.status_code == 200
    init_data = get_res.get_json()
    assert init_data["count"] >= 4
    default_names = [r["name"] for r in init_data["rooms"]]
    assert "general" in default_names

    # Create new custom room
    post_res = client.post(
        "/api/rooms",
        json={"name": "ai-lab", "description": "Machine learning collaboration", "created_by": "fatima"}
    )
    assert post_res.status_code == 201
    post_data = post_res.get_json()
    assert post_data["success"] is True
    assert post_data["room"]["name"] == "ai-lab"
    assert post_data["room"]["description"] == "Machine learning collaboration"

    # Verify presence in list
    get_res2 = client.get("/api/rooms")
    rooms2 = get_res2.get_json()["rooms"]
    assert any(r["name"] == "ai-lab" for r in rooms2)


def test_duplicate_and_invalid_room_rejection(client, app):
    """Test that duplicate and invalid room creations are properly rejected."""
    # Duplicate room creation
    res_dup = client.post(
        "/api/rooms",
        json={"name": "general", "description": "Duplicate room test"}
    )
    assert res_dup.status_code == 409
    assert "already exists" in res_dup.get_json()["error"]

    # Invalid room name (too short)
    res_short = client.post(
        "/api/rooms",
        json={"name": "a", "description": "Too short"}
    )
    assert res_short.status_code == 400


# ============================================================================
# 4. Real-Time Socket.IO Multi-Client & Collaboration Tests
# ============================================================================

def test_socketio_join_and_history(app):
    """Test join_room event loads existing history and broadcasts user_joined."""
    with app.app_context():
        # Pre-populate history
        msg = Message(username="PriorUser", room="tech", content="Existing note", username_color="#f59e0b")
        db.session.add(msg)
        db.session.commit()

    client1 = socketio.test_client(app)
    assert client1.is_connected()

    # Join room
    client1.emit("join_room", {"username": "Sarah", "room": "tech"})
    received = client1.get_received()

    event_names = [e["name"] for e in received]
    assert "room_joined" in event_names
    assert "message_history" in event_names
    assert "user_joined" in event_names
    assert "room_users_updated" in event_names

    # Check history payload
    history_event = next(e for e in received if e["name"] == "message_history")
    assert len(history_event["args"][0]["messages"]) == 1
    assert history_event["args"][0]["messages"][0]["message"] == "Existing note"

    client1.disconnect()


def test_socketio_multi_client_messaging(app):
    """
    Test real-time messaging between two clients in the same room.
    Messages sent by Client 1 must be received by Client 2 and saved in SQLite.
    """
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    # Both join the same room
    client1.emit("join_room", {"username": "UserOne", "room": "lobby"})
    client2.emit("join_room", {"username": "UserTwo", "room": "lobby"})

    # Flush join events
    client1.get_received()
    client2.get_received()

    # Client 1 sends a message
    client1.emit("send_message", {"message": "Hello from UserOne!", "room": "lobby"})

    # Check Client 2 received the message
    c2_events = client2.get_received()
    new_msg_events = [e for e in c2_events if e["name"] == "new_message"]
    assert len(new_msg_events) == 1
    payload = new_msg_events[0]["args"][0]
    assert payload["username"] == "UserOne"
    assert payload["message"] == "Hello from UserOne!"
    assert payload["room"] == "lobby"

    # Check SQLite persistence
    with app.app_context():
        saved = Message.query.filter_by(room="lobby").all()
        assert len(saved) == 1
        assert saved[0].content == "Hello from UserOne!"

    client1.disconnect()
    client2.disconnect()


def test_socketio_room_isolation(app):
    """
    Test room isolation: Client in Room A must NOT receive messages sent to Room B.
    """
    client_a = socketio.test_client(app)
    client_b = socketio.test_client(app)

    client_a.emit("join_room", {"username": "Alice", "room": "room-alpha"})
    client_b.emit("join_room", {"username": "Bob", "room": "room-beta"})

    client_a.get_received()
    client_b.get_received()

    # Alice sends message in room-alpha
    client_a.emit("send_message", {"message": "Confidential Alpha", "room": "room-alpha"})

    # Bob in room-beta must NOT receive it
    c_b_events = client_b.get_received()
    new_msgs_for_b = [e for e in c_b_events if e["name"] == "new_message"]
    assert len(new_msgs_for_b) == 0

    client_a.disconnect()
    client_b.disconnect()


def test_socketio_typing_indicator(app):
    """Test typing start and stop events between clients."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    client1.emit("join_room", {"username": "TyperUser", "room": "chat-room"})
    client2.emit("join_room", {"username": "WatcherUser", "room": "chat-room"})

    client1.get_received()
    client2.get_received()

    # Client 1 starts typing
    client1.emit("typing_start", {"room": "chat-room"})

    c2_events = client2.get_received()
    typing_events = [e for e in c2_events if e["name"] == "typing_update"]
    assert len(typing_events) == 1
    assert typing_events[0]["args"][0]["username"] == "TyperUser"
    assert typing_events[0]["args"][0]["is_typing"] is True

    # Client 1 stops typing
    client1.emit("typing_stop", {"room": "chat-room"})
    c2_events = client2.get_received()
    typing_events = [e for e in c2_events if e["name"] == "typing_update"]
    assert len(typing_events) == 1
    assert typing_events[0]["args"][0]["is_typing"] is False

    client1.disconnect()
    client2.disconnect()


def test_socketio_leave_room(app):
    """Test voluntary leave_room event."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    client1.emit("join_room", {"username": "LeavingUser", "room": "meeting"})
    client2.emit("join_room", {"username": "RemainingUser", "room": "meeting"})

    client1.get_received()
    client2.get_received()

    # Client 1 leaves room
    client1.emit("leave_room", {"room": "meeting"})
    c1_events = client1.get_received()
    assert any(e["name"] == "room_left" for e in c1_events)

    # Client 2 should receive user_left notification
    c2_events = client2.get_received()
    user_left_events = [e for e in c2_events if e["name"] == "user_left"]
    assert len(user_left_events) == 1
    assert user_left_events[0]["args"][0]["username"] == "LeavingUser"

    client1.disconnect()
    client2.disconnect()


def test_socketio_validation_errors(app):
    """Test invalid payloads are rejected with error events."""
    client = socketio.test_client(app)

    # Empty join payload
    client.emit("join_room", {"username": "", "room": "general"})
    events = client.get_received()
    error_events = [e for e in events if e["name"] == "error"]
    assert len(error_events) >= 1
    assert "Username is required" in error_events[0]["args"][0]["message"]

    client.disconnect()


# ============================================================================
# 5. Advanced Collaboration Feature Tests: Replies, Reactions, Pins, Search
# ============================================================================

def test_message_reply_thread(app):
    """Test sending a message with reply_to_id and verifying reply preview structure."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    client1.emit("join_room", {"username": "Alice", "room": "collab"})
    client2.emit("join_room", {"username": "Bob", "room": "collab"})
    client1.get_received()
    client2.get_received()

    # Alice sends parent message
    client1.emit("send_message", {"message": "Original query from Alice", "room": "collab"})
    client1.get_received()  # Flush Alice's received events
    events = client2.get_received()
    parent_msg = next(e["args"][0] for e in events if e["name"] == "new_message")
    parent_id = parent_msg["id"]

    # Bob replies to Alice's message
    client2.emit("send_message", {
        "message": "Bob's reply answer",
        "room": "collab",
        "reply_to_id": parent_id
    })

    c1_events = client1.get_received()
    reply_msg = next(e["args"][0] for e in c1_events if e["name"] == "new_message")

    assert reply_msg["username"] == "Bob"
    assert reply_msg["message"] == "Bob's reply answer"
    assert reply_msg["reply_to"] is not None
    assert reply_msg["reply_to"]["id"] == parent_id
    assert reply_msg["reply_to"]["username"] == "Alice"
    assert reply_msg["reply_to"]["content"] == "Original query from Alice"

    client1.disconnect()
    client2.disconnect()


def test_message_reaction_toggle(app):
    """Test adding and toggling emoji reactions on messages."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    client1.emit("join_room", {"username": "Alice", "room": "design-review"})
    client2.emit("join_room", {"username": "Bob", "room": "design-review"})
    client1.get_received()
    client2.get_received()

    # Alice posts a message
    client1.emit("send_message", {"message": "Look at the new design mockups!", "room": "design-review"})
    msg_id = next(e["args"][0]["id"] for e in client2.get_received() if e["name"] == "new_message")

    # Bob reacts with 🔥
    client2.emit("toggle_reaction", {"message_id": msg_id, "reaction": "🔥", "room": "design-review"})

    c1_events = client1.get_received()
    rx_event = next(e["args"][0] for e in c1_events if e["name"] == "reaction_updated")
    assert rx_event["message_id"] == msg_id
    assert rx_event["action"] == "added"
    assert len(rx_event["reactions"]) == 1
    assert rx_event["reactions"][0]["reaction"] == "🔥"
    assert rx_event["reactions"][0]["count"] == 1
    assert "Bob" in rx_event["reactions"][0]["users"]

    # Bob clicks 🔥 again to toggle off
    client2.emit("toggle_reaction", {"message_id": msg_id, "reaction": "🔥", "room": "design-review"})
    c1_events2 = client1.get_received()
    rx_event2 = next(e["args"][0] for e in c1_events2 if e["name"] == "reaction_updated")
    assert rx_event2["action"] == "removed"
    assert len(rx_event2["reactions"]) == 0

    client1.disconnect()
    client2.disconnect()


def test_message_pin_unpin_and_api(client, app):
    """Test pinning and unpinning messages and retrieving pinned list via API."""
    with app.app_context():
        m1 = Message(username="Alice", room="sprint", content="Demo is on Friday 10 AM", username_color="#3b82f6")
        m2 = Message(username="Bob", room="sprint", content="Normal message", username_color="#10b981")
        db.session.add_all([m1, m2])
        db.session.commit()
        m1_id = m1.id

    sc = socketio.test_client(app)
    sc.emit("join_room", {"username": "Alice", "room": "sprint"})
    sc.get_received()

    # Pin message
    sc.emit("pin_message", {"message_id": m1_id, "room": "sprint"})
    events = sc.get_received()
    pin_event = next(e["args"][0] for e in events if e["name"] == "message_pinned")
    assert pin_event["message_id"] == m1_id
    assert pin_event["pinned_by"] == "Alice"

    # Verify REST endpoint returns pinned message
    res = client.get("/api/rooms/sprint/pinned")
    assert res.status_code == 200
    data = res.get_json()
    assert data["count"] == 1
    assert data["pinned_messages"][0]["id"] == m1_id
    assert data["pinned_messages"][0]["content"] == "Demo is on Friday 10 AM"

    # Unpin message
    sc.emit("unpin_message", {"message_id": m1_id, "room": "sprint"})
    events2 = sc.get_received()
    unpin_event = next(e["args"][0] for e in events2 if e["name"] == "message_unpinned")
    assert unpin_event["message_id"] == m1_id

    # Verify REST endpoint returns 0 pinned messages
    res2 = client.get("/api/rooms/sprint/pinned")
    assert res2.get_json()["count"] == 0

    sc.disconnect()


def test_in_room_message_search_isolation(client, app):
    """
    Test that message search queries return matching messages strictly from the current room
    and NEVER expose messages from another room.
    """
    with app.app_context():
        m_alpha = Message(username="Fatima", room="alpha", content="KeywordRedisSecret in Alpha", username_color="#3b82f6")
        m_beta = Message(username="Ali", room="beta", content="KeywordRedisSecret in Beta", username_color="#10b981")
        db.session.add_all([m_alpha, m_beta])
        db.session.commit()

    # Search in 'alpha' for 'KeywordRedisSecret'
    res_alpha = client.get("/api/rooms/alpha/search?q=KeywordRedisSecret")
    assert res_alpha.status_code == 200
    data_alpha = res_alpha.get_json()
    assert data_alpha["count"] == 1
    assert data_alpha["results"][0]["room"] == "alpha"
    assert data_alpha["results"][0]["username"] == "Fatima"

    # Search in 'beta' for 'KeywordRedisSecret'
    res_beta = client.get("/api/rooms/beta/search?q=KeywordRedisSecret")
    assert res_beta.status_code == 200
    data_beta = res_beta.get_json()
    assert data_beta["count"] == 1
    assert data_beta["results"][0]["room"] == "beta"
    assert data_beta["results"][0]["username"] == "Ali"

    # Search in 'gamma' (empty room)
    res_gamma = client.get("/api/rooms/gamma/search?q=KeywordRedisSecret")
    assert res_gamma.status_code == 200
    assert res_gamma.get_json()["count"] == 0


def test_user_presence_status_update(app):
    """Test updating user presence status (Online / Away) and broadcasting to room."""
    client1 = socketio.test_client(app)
    client2 = socketio.test_client(app)

    client1.emit("join_room", {"username": "Alice", "room": "lounge"})
    client2.emit("join_room", {"username": "Bob", "room": "lounge"})
    client1.get_received()
    client2.get_received()

    # Alice toggles status to 'away'
    client1.emit("user_status", {"status": "away"})

    c2_events = client2.get_received()
    status_event = next(e["args"][0] for e in c2_events if e["name"] == "user_status_updated")
    assert status_event["username"] == "Alice"
    assert status_event["status"] == "away"

    # Alice toggles back to 'online'
    client1.emit("user_status", {"status": "online"})
    c2_events2 = client2.get_received()
    status_event2 = next(e["args"][0] for e in c2_events2 if e["name"] == "user_status_updated")
    assert status_event2["username"] == "Alice"
    assert status_event2["status"] == "online"

    client1.disconnect()
    client2.disconnect()
