from datetime import datetime, timezone
from models import db


class MessageReaction(db.Model):
    """Emoji reactions attached to chat messages."""
    __tablename__ = "message_reactions"
    __table_args__ = (
        db.UniqueConstraint("message_id", "username", "reaction", name="uq_message_user_reaction"),
    )

    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(
        db.Integer,
        db.ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    username = db.Column(db.String(50), nullable=False)
    reaction = db.Column(db.String(20), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self) -> dict:
        ts = self.created_at
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return {
            "id": self.id,
            "message_id": self.message_id,
            "username": self.username,
            "reaction": self.reaction,
            "created_at": ts.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<MessageReaction id={self.id} msg={self.message_id} user='{self.username}' emoji='{self.reaction}'>"
