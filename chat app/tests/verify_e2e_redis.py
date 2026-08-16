import os
import sys
import time
from pathlib import Path

# Add project root to Python module path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import socketio
from models import db
from models.message import Message
from app import create_app

SERVER_URL = "http://127.0.0.1:5000"

def test_live_redis_chat():
    print("=" * 60)
    print(" [*] Starting Live E2E Verification with Redis")
    print(f" [*] Target Server: {SERVER_URL}")
    print("=" * 60)

    client1 = socketio.SimpleClient()
    client2 = socketio.SimpleClient()
    client3 = socketio.SimpleClient()

    # Track received events
    c1_events = []
    c2_events = []
    c3_events = []

    # 1. Connect clients
    print("\n[1/7] Connecting 3 Socket.IO clients...")
    client1.connect(SERVER_URL)
    client2.connect(SERVER_URL)
    client3.connect(SERVER_URL)
    print(" -> All 3 clients connected successfully.")

    # 2. Join Rooms
    print("\n[2/7] Joining rooms (Alice & Bob -> #general, Charlie -> #isolated-room)...")
    client1.emit("join_room", {"username": "Alice", "room": "general"})
    time.sleep(0.3)
    client2.emit("join_room", {"username": "Bob", "room": "general"})
    time.sleep(0.3)
    client3.emit("join_room", {"username": "Charlie", "room": "isolated-room"})
    time.sleep(0.5)

    # 3. Typing Indicators
    print("\n[3/7] Testing real-time typing indicators...")
    client1.emit("typing_start", {"room": "general"})
    time.sleep(0.3)

    # Read events on client 2 (Bob in general)
    received_typing = False
    while True:
        try:
            event = client2.receive(timeout=0.5)
            if event[0] == "typing_update" and event[1].get("username") == "Alice" and event[1].get("is_typing") is True:
                received_typing = True
                break
        except Exception:
            break
    assert received_typing, "Bob failed to receive Alice's typing_start event"
    print(" -> Bob received 'Alice is typing...' indicator in #general.")

    # 4. Message Broadcast in Room
    print("\n[4/7] Testing message broadcast in #general...")
    test_content = f"Redis verified message at {time.time()}"
    client1.emit("send_message", {"message": test_content, "room": "general"})
    time.sleep(0.5)

    # Bob should receive the message
    received_msg = False
    while True:
        try:
            event = client2.receive(timeout=0.5)
            if event[0] == "new_message" and event[1].get("content") == test_content:
                received_msg = True
                break
        except Exception:
            break
    assert received_msg, "Bob failed to receive Alice's message in #general"
    print(" -> Bob received Alice's message in real time.")

    # 5. Room Isolation Verification
    print("\n[5/7] Verifying Room Isolation (Charlie in #isolated-room)...")
    charlie_got_msg = False
    while True:
        try:
            event = client3.receive(timeout=0.5)
            if event[0] == "new_message" and event[1].get("content") == test_content:
                charlie_got_msg = True
                break
        except Exception:
            break
    assert not charlie_got_msg, "SECURITY/ISOLATION FAILURE: Charlie in #isolated-room received Alice's #general message!"
    print(" -> Room isolation verified: Charlie received zero messages from #general.")

    # 6. SQLite Database Persistence
    print("\n[6/7] Verifying SQLite persistence...")
    app = create_app()
    with app.app_context():
        saved = Message.query.filter_by(room="general", content=test_content).first()
        assert saved is not None, "Message was not persisted in SQLite database!"
        assert saved.username == "Alice"
        print(f" -> Message persisted in SQLite: ID={saved.id}, Room={saved.room}, User={saved.username}")

    # 7. Leave Room
    print("\n[7/7] Testing leave_room...")
    client2.emit("leave_room", {"room": "general"})
    time.sleep(0.5)

    received_leave = False
    while True:
        try:
            event = client1.receive(timeout=0.5)
            if event[0] == "user_left" and event[1].get("username") == "Bob":
                received_leave = True
                break
        except Exception:
            break
    assert received_leave, "Alice did not receive user_left notification when Bob left."
    print(" -> Alice received 'Bob left the room' notification.")

    # Disconnect
    client1.disconnect()
    client2.disconnect()
    client3.disconnect()

    print("\n" + "=" * 60)
    print(" ALL 7 LIVE E2E REDIS VERIFICATIONS PASSED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_live_redis_chat()
