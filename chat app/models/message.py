from datetime import datetime, timezone
from models import db


class Message(db.Model):
    """Chat message persistent storage in SQLite with reply, reaction, and pin support."""
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    room = db.Column(db.String(50), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    username_color = db.Column(db.String(20), nullable=False, default="#4f46e5")

    # Reply reference (nullable)
    reply_to_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Pin status
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    pinned_by = db.Column(db.String(50), nullable=True)
    pinned_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    reactions = db.relationship(
        "MessageReaction",
        backref="message",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="MessageReaction.created_at.asc()"
    )
    reply_to = db.relationship(
        "Message",
        remote_side=[id],
        foreign_keys=[reply_to_id],
        lazy="joined"
    )

    def get_reactions_summary(self) -> list[dict]:
        """Aggregate reactions by emoji with counts and list of user names."""
        summary = {}
        for r in self.reactions:
            if r.reaction not in summary:
                summary[r.reaction] = {
                    "reaction": r.reaction,
                    "count": 0,
                    "users": []
                }
            summary[r.reaction]["count"] += 1
            summary[r.reaction]["users"].append(r.username)
        return list(summary.values())

    def to_dict(self) -> dict:
        """Convert message model to dictionary format for WebSocket/JSON serialization."""
        ts = self.timestamp
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)

        pinned_ts = None
        if self.pinned_at:
            p_ts = self.pinned_at
            if p_ts.tzinfo is None:
                p_ts = p_ts.replace(tzinfo=timezone.utc)
            pinned_ts = p_ts.isoformat()

        reply_preview = None
        if self.reply_to:
            reply_preview = {
                "id": self.reply_to.id,
                "username": self.reply_to.username,
                "message": self.reply_to.content,
                "content": self.reply_to.content,
                "username_color": self.reply_to.username_color,
            }
        elif self.reply_to_id:
            # Fallback if parent message was deleted
            reply_preview = {
                "id": self.reply_to_id,
                "username": "Original message",
                "message": "This message was deleted or is no longer available.",
                "content": "This message was deleted or is no longer available.",
                "username_color": "#94a3b8",
            }

        return {
            "id": self.id,
            "username": self.username,
            "room": self.room,
            "message": self.content,
            "content": self.content,
            "timestamp": ts.isoformat(),
            "username_color": self.username_color,
            "reply_to_id": self.reply_to_id,
            "reply_to": reply_preview,
            "reactions": self.get_reactions_summary(),
            "is_pinned": bool(self.is_pinned),
            "pinned_by": self.pinned_by,
            "pinned_at": pinned_ts,
        }

    def __repr__(self) -> str:
        return f"<Message id={self.id} room='{self.room}' user='{self.username}'>"
