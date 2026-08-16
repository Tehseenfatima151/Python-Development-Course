import logging
from datetime import datetime, timezone
from flask import request
from flask_socketio import (
    emit,
    join_room as socketio_join_room,
    leave_room as socketio_leave_room,
)
from models import db, Message, Room, MessageReaction
from models.user import user_manager
from utils.helpers import (
    validate_username,
    validate_room,
    validate_room_description,
    validate_message,
    validate_reaction,
    sanitize_text,
    get_username_color,
    get_utc_now_iso,
)

logger = logging.getLogger("livechat.events")


def register_events(socketio, app):
    """Register all Socket.IO chat events with the SocketIO instance."""

    @socketio.on("connect")
    def handle_connect():
        """Handle client connection."""
        sid = request.sid
        logger.info(f"Client connected: SID {sid}")
        emit(
            "connection_status",
            {
                "status": "connected",
                "sid": sid,
                "redis_connected": app.config.get("REDIS_CONNECTED", False),
            },
        )

    @socketio.on("disconnect")
    def handle_disconnect():
        """Handle client disconnection and clean up room membership."""
        sid = request.sid
        logger.info(f"Client disconnected: SID {sid}")
        session = user_manager.remove_user(sid)
        if session:
            room = session.get("room")
            username = session.get("username")
            if room and username:
                now_iso = get_utc_now_iso()
                # Broadcast that user left
                emit(
                    "user_left",
                    {
                        "username": username,
                        "room": room,
                        "timestamp": now_iso,
                        "message": f"{username} left the room",
                    },
                    to=room,
                )
                # Broadcast updated user list
                emit(
                    "room_users_updated",
                    {
                        "room": room,
                        "users": user_manager.get_room_users(room),
                        "count": user_manager.get_user_count(room),
                    },
                    to=room,
                )
                # Clear typing state
                emit(
                    "typing_update",
                    {"username": username, "room": room, "is_typing": False},
                    to=room,
                    include_self=False,
                )

    @socketio.on("join_room")
    def handle_join_room(data):
        """
        Handle a user joining a chat room.
        Expected data: {'username': str, 'room': str}
        """
        try:
            if not isinstance(data, dict):
                emit("error", {"message": "Invalid join request payload."})
                return

            raw_username = data.get("username", "")
            raw_room = data.get("room", "")

            # Validate username
            is_valid_user, user_err = validate_username(
                raw_username, app.config.get("MAX_USERNAME_LENGTH", 30)
            )
            if not is_valid_user:
                emit("error", {"message": user_err, "field": "username"})
                return

            # Validate room
            is_valid_room, room_err = validate_room(
                raw_room, app.config.get("MAX_ROOM_LENGTH", 50)
            )
            if not is_valid_room:
                emit("error", {"message": room_err, "field": "room"})
                return

            username = sanitize_text(raw_username)
            room_name = sanitize_text(raw_room).lower()
            color = get_username_color(username)
            sid = request.sid

            # Ensure room exists in database
            room_obj = Room.query.filter_by(name=room_name).first()
            if not room_obj:
                room_obj = Room(
                    name=room_name,
                    description="Dynamic collaboration channel",
                    is_default=False,
                    created_by=username,
                )
                db.session.add(room_obj)
                db.session.commit()
                # Broadcast room creation to all clients
                try:
                    emit("room_created", room_obj.to_dict(), broadcast=True)
                except Exception as e:
                    logger.warning(f"Could not broadcast new room: {e}")

            # Join the Socket.IO room
            socketio_join_room(room_name)

            # Record user in manager
            user_manager.add_user(sid, username, room_name, color, status="online")
            logger.info(f"User '{username}' joined room '{room_name}' (SID: {sid})")

            # Fetch recent message history from SQLite
            limit = app.config.get("MESSAGE_HISTORY_LIMIT", 50)
            messages = (
                Message.query.filter_by(room=room_name)
                .order_by(Message.timestamp.desc())
                .limit(limit)
                .all()
            )
            # Order chronologically for the UI
            history = [m.to_dict() for m in reversed(messages)]

            # Acknowledge join to current user
            emit(
                "room_joined",
                {
                    "success": True,
                    "username": username,
                    "room": room_name,
                    "room_description": room_obj.description,
                    "username_color": color,
                    "timestamp": get_utc_now_iso(),
                },
            )

            # Send message history strictly to joining user
            emit("message_history", {"room": room_name, "messages": history})

            # Broadcast user_joined notification to room
            now_iso = get_utc_now_iso()
            emit(
                "user_joined",
                {
                    "username": username,
                    "username_color": color,
                    "room": room_name,
                    "timestamp": now_iso,
                    "message": f"{username} joined the room",
                },
                to=room_name,
            )

            # Broadcast updated room users list to room
            emit(
                "room_users_updated",
                {
                    "room": room_name,
                    "users": user_manager.get_room_users(room_name),
                    "count": user_manager.get_user_count(room_name),
                },
                to=room_name,
            )

        except Exception as e:
            logger.error(f"Error in handle_join_room: {e}", exc_info=True)
            emit("error", {"message": "An internal error occurred while joining the room."})

    @socketio.on("leave_room")
    def handle_leave_room(data=None):
        """Handle a user voluntarily leaving a chat room."""
        try:
            sid = request.sid
            session = user_manager.remove_user(sid)
            if not session:
                emit("room_left", {"success": True})
                return

            room = session.get("room")
            username = session.get("username")

            if room:
                socketio_leave_room(room)
                now_iso = get_utc_now_iso()

                # Broadcast user left to remaining room members
                emit(
                    "user_left",
                    {
                        "username": username,
                        "room": room,
                        "timestamp": now_iso,
                        "message": f"{username} left the room",
                    },
                    to=room,
                )

                # Broadcast updated online users
                emit(
                    "room_users_updated",
                    {
                        "room": room,
                        "users": user_manager.get_room_users(room),
                        "count": user_manager.get_user_count(room),
                    },
                    to=room,
                )

                # Broadcast stop typing
                emit(
                    "typing_update",
                    {"username": username, "room": room, "is_typing": False},
                    to=room,
                    include_self=False,
                )

            # Confirm leaving to user
            emit("room_left", {"success": True, "room": room})
            logger.info(f"User '{username}' left room '{room}' (SID: {sid})")

        except Exception as e:
            logger.error(f"Error in handle_leave_room: {e}", exc_info=True)
            emit("error", {"message": "An error occurred while leaving the room."})

    @socketio.on("send_message")
    def handle_send_message(data):
        """
        Handle receiving a new message from a client with optional reply reference,
        persisting in SQLite, and broadcasting to room participants.
        """
        try:
            sid = request.sid
            user_session = user_manager.get_user(sid)
            if not user_session:
                emit("error", {"message": "You must join a room before sending messages."})
                return

            if not isinstance(data, dict):
                emit("error", {"message": "Invalid message format."})
                return

            raw_content = data.get("message") or data.get("content") or ""
            reply_to_id = data.get("reply_to_id")
            max_len = app.config.get("MAX_MESSAGE_LENGTH", 1000)

            # Validate message
            is_valid, msg_err = validate_message(raw_content, max_len)
            if not is_valid:
                emit("error", {"message": msg_err, "field": "message"})
                return

            content = sanitize_text(raw_content)
            username = user_session["username"]
            room = user_session["room"]
            color = user_session["color"]

            # Validate reply_to_id belongs to the same room if provided
            valid_reply_id = None
            if reply_to_id:
                try:
                    parent_msg = Message.query.filter_by(id=int(reply_to_id), room=room).first()
                    if parent_msg:
                        valid_reply_id = parent_msg.id
                except (ValueError, TypeError):
                    valid_reply_id = None

            # Save message permanently in SQLite
            new_msg = Message(
                username=username,
                room=room,
                content=content,
                username_color=color,
                reply_to_id=valid_reply_id,
            )
            db.session.add(new_msg)
            db.session.commit()

            message_payload = new_msg.to_dict()

            # Broadcast new message to everyone in the room
            emit("new_message", message_payload, to=room)
            logger.debug(f"Message {new_msg.id} sent to room '{room}' by '{username}'")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in handle_send_message: {e}", exc_info=True)
            emit("error", {"message": "Failed to deliver message."})

    @socketio.on("toggle_reaction")
    def handle_toggle_reaction(data):
        """
        Handle toggling an emoji reaction on a message.
        If the user has already reacted with this emoji, remove it. Otherwise, add it.
        Broadcasts reaction update in real time.
        """
        try:
            sid = request.sid
            user_session = user_manager.get_user(sid)
            if not user_session:
                emit("error", {"message": "Must be connected to react."})
                return

            if not isinstance(data, dict):
                return

            message_id = data.get("message_id")
            raw_reaction = data.get("reaction")

            if not message_id or not raw_reaction:
                return

            is_valid_rx, rx_err = validate_reaction(raw_reaction)
            if not is_valid_rx:
                emit("error", {"message": rx_err})
                return

            username = user_session["username"]
            room = user_session["room"]
            reaction = sanitize_text(raw_reaction)

            # Find the message in the user's current room
            msg = Message.query.filter_by(id=int(message_id), room=room).first()
            if not msg:
                emit("error", {"message": "Message not found in this room."})
                return

            existing_rx = MessageReaction.query.filter_by(
                message_id=msg.id,
                username=username,
                reaction=reaction
            ).first()

            if existing_rx:
                db.session.delete(existing_rx)
                action = "removed"
            else:
                new_rx = MessageReaction(
                    message_id=msg.id,
                    username=username,
                    reaction=reaction
                )
                db.session.add(new_rx)
                action = "added"

            db.session.commit()

            # Re-fetch reactions summary
            reactions_summary = msg.get_reactions_summary()

            # Broadcast reaction update to the room
            emit(
                "reaction_updated",
                {
                    "message_id": msg.id,
                    "room": room,
                    "reactions": reactions_summary,
                    "username": username,
                    "reaction": reaction,
                    "action": action,
                },
                to=room,
            )

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in handle_toggle_reaction: {e}", exc_info=True)
            emit("error", {"message": "Failed to update reaction."})

    @socketio.on("pin_message")
    def handle_pin_message(data):
        """Pin a message in the current room."""
        try:
            sid = request.sid
            user_session = user_manager.get_user(sid)
            if not user_session:
                emit("error", {"message": "Must be connected to pin messages."})
                return

            message_id = data.get("message_id") if isinstance(data, dict) else None
            if not message_id:
                return

            username = user_session["username"]
            room = user_session["room"]

            msg = Message.query.filter_by(id=int(message_id), room=room).first()
            if not msg:
                emit("error", {"message": "Message not found in this room."})
                return

            msg.is_pinned = True
            msg.pinned_by = username
            msg.pinned_at = datetime.now(timezone.utc)
            db.session.commit()

            # Broadcast pin event to the room
            emit(
                "message_pinned",
                {
                    "message_id": msg.id,
                    "room": room,
                    "pinned_by": username,
                    "pinned_at": msg.pinned_at.isoformat(),
                    "message": msg.to_dict(),
                },
                to=room,
            )

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in handle_pin_message: {e}", exc_info=True)
            emit("error", {"message": "Failed to pin message."})

    @socketio.on("unpin_message")
    def handle_unpin_message(data):
        """Unpin a message in the current room."""
        try:
            sid = request.sid
            user_session = user_manager.get_user(sid)
            if not user_session:
                emit("error", {"message": "Must be connected to unpin messages."})
                return

            message_id = data.get("message_id") if isinstance(data, dict) else None
            if not message_id:
                return

            username = user_session["username"]
            room = user_session["room"]

            msg = Message.query.filter_by(id=int(message_id), room=room).first()
            if not msg:
                emit("error", {"message": "Message not found in this room."})
                return

            msg.is_pinned = False
            msg.pinned_by = None
            msg.pinned_at = None
            db.session.commit()

            # Broadcast unpin event to the room
            emit(
                "message_unpinned",
                {
                    "message_id": msg.id,
                    "room": room,
                    "unpinned_by": username,
                    "message": msg.to_dict(),
                },
                to=room,
            )

        except Exception as e:
            db.session.rollback()
            logger.error(f"Error in handle_unpin_message: {e}", exc_info=True)
            emit("error", {"message": "Failed to unpin message."})

    @socketio.on("user_status")
    def handle_user_status(data):
        """Update user presence status ('online' or 'away') and broadcast to room."""
        try:
            sid = request.sid
            user_session = user_manager.get_user(sid)
            if not user_session or not isinstance(data, dict):
                return

            status = data.get("status", "online")
            if status not in ("online", "away"):
                status = "online"

            updated = user_manager.set_user_status(sid, status)
            if updated:
                room = updated["room"]
                username = updated["username"]
                emit(
                    "user_status_updated",
                    {
                        "username": username,
                        "room": room,
                        "status": status,
                        "users": user_manager.get_room_users(room),
                    },
                    to=room,
                )

        except Exception as e:
            logger.error(f"Error in handle_user_status: {e}", exc_info=True)

    @socketio.on("typing_start")
    def handle_typing_start(data=None):
        """Handle typing start indicator."""
        sid = request.sid
        user_session = user_manager.get_user(sid)
        if user_session:
            room = user_session["room"]
            username = user_session["username"]
            emit(
                "typing_update",
                {"username": username, "room": room, "is_typing": True},
                to=room,
                include_self=False,
            )

    @socketio.on("typing_stop")
    def handle_typing_stop(data=None):
        """Handle typing stop indicator."""
        sid = request.sid
        user_session = user_manager.get_user(sid)
        if user_session:
            room = user_session["room"]
            username = user_session["username"]
            emit(
                "typing_update",
                {"username": username, "room": room, "is_typing": False},
                to=room,
                include_self=False,
            )
