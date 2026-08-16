import logging
from typing import Optional

logger = logging.getLogger("livechat.user_manager")


class RoomUserManager:
    """
    Manages active connected users in chat rooms.
    Supports in-memory tracking with optional Redis synchronization.
    """
    def __init__(self, redis_client=None):
        self._redis = redis_client
        # Memory storage: sid -> {"username": str, "room": str, "color": str, "status": str, "sid": str}
        self._sessions: dict[str, dict[str, str]] = {}
        # Memory storage: room -> set of sids
        self._room_members: dict[str, set[str]] = {}

    def set_redis_client(self, redis_client):
        self._redis = redis_client

    def add_user(self, sid: str, username: str, room: str, color: str, status: str = "online") -> None:
        """Add or update a user session in a room."""
        # Remove from previous room if existed
        if sid in self._sessions:
            old_room = self._sessions[sid]["room"]
            if old_room in self._room_members and sid in self._room_members[old_room]:
                self._room_members[old_room].remove(sid)

        # Store in local memory
        user_data = {
            "username": username,
            "room": room,
            "color": color,
            "status": status,
            "sid": sid
        }
        self._sessions[sid] = user_data

        if room not in self._room_members:
            self._room_members[room] = set()
        self._room_members[room].add(sid)

        # Sync to Redis if available
        if self._redis:
            try:
                self._redis.hset(f"chat:session:{sid}", mapping=user_data)
                self._redis.sadd(f"chat:room:{room}:members", sid)
            except Exception as e:
                logger.warning(f"Failed to sync user addition to Redis: {e}")

    def set_user_status(self, sid: str, status: str) -> Optional[dict[str, str]]:
        """Update a connected user's presence status ('online' or 'away')."""
        if sid in self._sessions:
            self._sessions[sid]["status"] = status
            if self._redis:
                try:
                    self._redis.hset(f"chat:session:{sid}", "status", status)
                except Exception as e:
                    logger.warning(f"Failed to sync user status update to Redis: {e}")
            return self._sessions[sid]
        return None

    def remove_user(self, sid: str) -> Optional[dict[str, str]]:
        """Remove a user by socket ID and return their last session data if found."""
        session = self._sessions.pop(sid, None)
        if session:
            room = session.get("room")
            if room and room in self._room_members:
                self._room_members[room].discard(sid)
                if not self._room_members[room]:
                    self._room_members.pop(room, None)

            if self._redis:
                try:
                    self._redis.delete(f"chat:session:{sid}")
                    if room:
                        self._redis.srem(f"chat:room:{room}:members", sid)
                except Exception as e:
                    logger.warning(f"Failed to sync user removal to Redis: {e}")

        return session

    def get_user(self, sid: str) -> Optional[dict[str, str]]:
        """Get session data for a socket ID."""
        return self._sessions.get(sid)

    def get_room_users(self, room: str) -> list[dict[str, str]]:
        """
        Get unique list of online users in a room.
        Deduplicates by username if the same user has multiple tabs open.
        """
        sids = self._room_members.get(room, set())
        users_by_name: dict[str, dict[str, str]] = {}

        for sid in sids:
            session = self._sessions.get(sid)
            if session:
                username = session["username"]
                if username not in users_by_name:
                    users_by_name[username] = {
                        "username": username,
                        "color": session.get("color", "#4f46e5"),
                        "status": session.get("status", "online"),
                        "online": True,
                    }

        return list(users_by_name.values())

    def get_user_count(self, room: str) -> int:
        """Get count of active unique users in a room."""
        return len(self.get_room_users(room))

    def get_all_room_counts(self) -> dict[str, int]:
        """Get online user counts for all active rooms."""
        counts = {}
        for room in list(self._room_members.keys()):
            counts[room] = self.get_user_count(room)
        return counts


# Global instance
user_manager = RoomUserManager()
