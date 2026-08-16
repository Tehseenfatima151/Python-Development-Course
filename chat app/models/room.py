from datetime import datetime, timezone
from models import db


class Room(db.Model):
    """Chat room persistent storage in SQLite."""
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=False, default="")
    created_by = db.Column(db.String(50), nullable=False, default="system")
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )
    is_default = db.Column(db.Boolean, nullable=False, default=False)

    def to_dict(self, online_count: int = 0) -> dict:
        """Convert room model to dictionary format for JSON responses and SocketIO events."""
        ts = self.created_at
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_by": self.created_by,
            "created_at": ts.isoformat(),
            "is_default": self.is_default,
            "online_count": online_count,
        }

    def __repr__(self) -> str:
        return f"<Room id={self.id} name='{self.name}' default={self.is_default}>"
