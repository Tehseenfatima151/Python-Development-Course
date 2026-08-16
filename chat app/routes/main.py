import logging
from datetime import datetime, timezone
from flask import render_template, jsonify, request, current_app
from sqlalchemy import text, or_
from routes import main_bp
from models import db, Message, Room, MessageReaction
from models.user import user_manager
from sockets import socketio
from utils.helpers import (
    validate_room,
    validate_room_description,
    validate_username,
    sanitize_text,
    get_utc_now_iso,
)

logger = logging.getLogger("livechat.routes")


@main_bp.route("/")
def index():
    """Render the primary Single-Page Real-Time Collaboration Platform."""
    initial_room = request.args.get("room", "").strip()
    initial_username = request.args.get("username", "").strip()
    return render_template(
        "index.html",
        initial_room=initial_room,
        initial_username=initial_username,
        max_message_len=current_app.config.get("MAX_MESSAGE_LENGTH", 1000),
        max_username_len=current_app.config.get("MAX_USERNAME_LENGTH", 30),
        max_room_len=current_app.config.get("MAX_ROOM_LENGTH", 50),
    )


@main_bp.route("/health")
def health_check():
    """
    Health check endpoint returning the status of database,
    Redis connection, and active platform stats.
    """
    # 1. Check SQLite Database
    db_healthy = False
    db_error = None
    try:
        db.session.execute(text("SELECT 1"))
        db_healthy = True
    except Exception as e:
        db_error = str(e)
        logger.error(f"Database health check failed: {e}")

    # 2. Check Redis Status
    redis_connected = current_app.config.get("REDIS_CONNECTED", False)
    redis_status_msg = current_app.config.get(
        "REDIS_STATUS_MESSAGE",
        "Redis connected successfully" if redis_connected else "Redis disconnected"
    )

    status_code = 200 if db_healthy else 500

    return (
        jsonify({
            "status": "healthy" if db_healthy else "unhealthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "components": {
                "database": {
                    "status": "connected" if db_healthy else "error",
                    "type": "SQLite",
                    "error": db_error,
                },
                "redis": {
                    "status": "connected" if redis_connected else "disconnected",
                    "mode": "message_queue" if redis_connected else "local_in_memory_fallback",
                    "message": redis_status_msg,
                },
            },
        }),
        status_code,
    )


@main_bp.route("/api/rooms", methods=["GET"])
def list_rooms():
    """List all available rooms with their online member counts and metadata."""
    rooms = Room.query.order_by(Room.is_default.desc(), Room.name.asc()).all()
    room_counts = user_manager.get_all_room_counts()

    return jsonify({
        "count": len(rooms),
        "rooms": [r.to_dict(online_count=room_counts.get(r.name, 0)) for r in rooms],
    })


@main_bp.route("/api/rooms", methods=["POST"])
def create_room():
    """
    Create a new dynamic chat room.
    Validates room name, ensures uniqueness, persists in database,
    and broadcasts the newly created room to all connected clients.
    """
    data = request.get_json() or {}
    raw_name = data.get("name", "")
    raw_desc = data.get("description", "")
    raw_creator = data.get("created_by", "anonymous")

    # Validate room name
    is_valid_room, room_err = validate_room(raw_name, current_app.config.get("MAX_ROOM_LENGTH", 50))
    if not is_valid_room:
        return jsonify({"error": room_err, "field": "name"}), 400

    # Validate description
    is_valid_desc, desc_err = validate_room_description(raw_desc)
    if not is_valid_desc:
        return jsonify({"error": desc_err, "field": "description"}), 400

    name = sanitize_text(raw_name).lower()
    description = sanitize_text(raw_desc)
    creator = sanitize_text(raw_creator) or "anonymous"

    # Check for existing duplicate room
    existing_room = Room.query.filter_by(name=name).first()
    if existing_room:
        return jsonify({"error": f"A room named '{name}' already exists.", "field": "name"}), 409

    try:
        new_room = Room(
            name=name,
            description=description,
            created_by=creator,
            is_default=False,
        )
        db.session.add(new_room)
        db.session.commit()

        room_dict = new_room.to_dict(online_count=0)

        # Broadcast room creation to all connected WebSocket clients in real time
        try:
            socketio.emit("room_created", room_dict)
        except Exception as e:
            logger.warning(f"Could not broadcast room_created via socketio: {e}")

        return jsonify({"success": True, "room": room_dict}), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating room: {e}", exc_info=True)
        return jsonify({"error": "Failed to create room due to a server error."}), 500


@main_bp.route("/api/rooms/<room_name>/info", methods=["GET"])
def get_room_info(room_name):
    """Get metadata for a specific room including member count and pinned messages count."""
    cleaned_room = sanitize_text(room_name).lower()
    room = Room.query.filter_by(name=cleaned_room).first()

    # If not registered in Room table yet, dynamically register it
    if not room:
        is_valid, _ = validate_room(cleaned_room)
        if is_valid:
            room = Room(name=cleaned_room, description="Dynamic collaboration room", is_default=False)
            db.session.add(room)
            db.session.commit()
        else:
            return jsonify({"error": "Room not found."}), 404

    online_count = user_manager.get_user_count(cleaned_room)
    pinned_count = Message.query.filter_by(room=cleaned_room, is_pinned=True).count()
    total_messages = Message.query.filter_by(room=cleaned_room).count()

    room_data = room.to_dict(online_count=online_count)
    room_data["pinned_count"] = pinned_count
    room_data["total_messages"] = total_messages
    room_data["members"] = user_manager.get_room_users(cleaned_room)

    return jsonify({"room": room_data})


@main_bp.route("/api/rooms/<room_name>/messages", methods=["GET"])
def get_room_messages(room_name):
    """REST endpoint to fetch recent message history for a room."""
    is_valid, err = validate_room(room_name)
    if not is_valid:
        return jsonify({"error": err}), 400

    cleaned_room = sanitize_text(room_name)
    limit = min(
        request.args.get("limit", current_app.config.get("MESSAGE_HISTORY_LIMIT", 50), type=int),
        100,
    )

    messages = (
        Message.query.filter_by(room=cleaned_room)
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .all()
    )

    return jsonify({
        "room": cleaned_room,
        "count": len(messages),
        "messages": [m.to_dict() for m in reversed(messages)],
    })


@main_bp.route("/api/rooms/<room_name>/pinned", methods=["GET"])
def get_pinned_messages(room_name):
    """REST endpoint to fetch all pinned messages in a specific room."""
    is_valid, err = validate_room(room_name)
    if not is_valid:
        return jsonify({"error": err}), 400

    cleaned_room = sanitize_text(room_name)
    pinned = (
        Message.query.filter_by(room=cleaned_room, is_pinned=True)
        .order_by(Message.pinned_at.desc())
        .all()
    )

    return jsonify({
        "room": cleaned_room,
        "count": len(pinned),
        "pinned_messages": [m.to_dict() for m in pinned],
    })


@main_bp.route("/api/rooms/<room_name>/search", methods=["GET"])
def search_room_messages(room_name):
    """
    Search messages inside the current room only.
    Strictly prevents cross-room message exposure using parameterized queries.
    """
    is_valid, err = validate_room(room_name)
    if not is_valid:
        return jsonify({"error": err}), 400

    cleaned_room = sanitize_text(room_name)
    query_str = request.args.get("q", "").strip()

    if not query_str:
        return jsonify({"room": cleaned_room, "query": "", "count": 0, "results": []})

    cleaned_query = sanitize_text(query_str)
    limit = min(request.args.get("limit", 25, type=int), 50)

    # Search strictly in the specified room matching content or username
    search_pattern = f"%{cleaned_query}%"
    results = (
        Message.query.filter(
            Message.room == cleaned_room,
            or_(
                Message.content.ilike(search_pattern),
                Message.username.ilike(search_pattern),
            )
        )
        .order_by(Message.timestamp.desc())
        .limit(limit)
        .all()
    )

    return jsonify({
        "room": cleaned_room,
        "query": cleaned_query,
        "count": len(results),
        "results": [m.to_dict() for m in results],
    })
