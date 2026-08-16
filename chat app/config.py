import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
base_dir = Path(__file__).resolve().parent
load_dotenv(base_dir / ".env")

logger = logging.getLogger("livechat.config")


class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-livechat-secret-key-change-in-prod")

    # Instance path setup
    INSTANCE_DIR = base_dir / "instance"
    INSTANCE_DIR.mkdir(parents=True, exist_ok=True)

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        db_path = INSTANCE_DIR / "chat.db"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.as_posix()}"
    elif DATABASE_URL.startswith("sqlite:///") and not os.path.isabs(DATABASE_URL[10:]):
        # Resolve relative sqlite paths relative to instance dir
        rel_path = DATABASE_URL.replace("sqlite:///", "")
        db_path = INSTANCE_DIR / rel_path
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path.as_posix()}"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Redis configuration
    REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    REQUIRE_REDIS = os.getenv("REQUIRE_REDIS", "false").lower() in ("true", "1", "yes")

    # Real-time chat limits & constraints
    MESSAGE_HISTORY_LIMIT = int(os.getenv("MESSAGE_HISTORY_LIMIT", "50"))
    MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "1000"))
    MAX_USERNAME_LENGTH = int(os.getenv("MAX_USERNAME_LENGTH", "30"))
    MAX_ROOM_LENGTH = int(os.getenv("MAX_ROOM_LENGTH", "50"))
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "*")

    @classmethod
    def check_redis_connection(cls, url: str = None) -> tuple[bool, str]:
        """
        Check if Redis is reachable.
        Returns:
            (is_connected: bool, status_message: str)
        """
        target_url = url or cls.REDIS_URL or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
        if not target_url:
            return False, "REDIS_URL is not configured"
        try:
            import redis
            client = redis.from_url(target_url, socket_connect_timeout=2.0, socket_timeout=2.0)
            client.ping()
            client.close()
            return True, "Redis connected successfully"
        except Exception as e:
            return False, f"Redis connection failed: {str(e)}"
