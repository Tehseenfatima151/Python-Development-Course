import logging
from flask_socketio import SocketIO
from config import Config

logger = logging.getLogger("livechat.sockets")

# Module-level SocketIO instance (used by app.py and tests)
socketio = SocketIO()


def init_socketio(app):
    """
    Initialize SocketIO with optional Redis message queue support.
    Redis is only used when REDIS_URL is set to a non-empty string in config.
    """
    redis_url = app.config.get("REDIS_URL") or ""
    require_redis = app.config.get("REQUIRE_REDIS", False)

    # Only attempt Redis when a URL is actually configured
    redis_available = False
    redis_msg = "REDIS_URL not configured — running in standalone mode."

    if redis_url:
        redis_available, redis_msg = Config.check_redis_connection(redis_url)
    elif require_redis:
        raise RuntimeError("REQUIRE_REDIS is True but REDIS_URL is not set.")

    app.config["REDIS_CONNECTED"] = redis_available
    app.config["REDIS_STATUS_MESSAGE"] = redis_msg

    socketio_kwargs = {
        "cors_allowed_origins": app.config.get("CORS_ALLOWED_ORIGINS", "*"),
        "async_mode": "threading",
        "logger": False,
        "engineio_logger": False,
    }

    if redis_available:
        logger.info(f"Redis available — using message queue: {redis_url}")
        socketio_kwargs["message_queue"] = redis_url
        try:
            import redis as redis_lib
            from models.user import user_manager
            user_manager.set_redis_client(redis_lib.from_url(redis_url))
        except Exception as e:
            logger.warning(f"Could not bind Redis to user manager: {e}")
    else:
        if require_redis:
            raise RuntimeError(f"Strict Redis requirement failed: {redis_msg}")
        logger.warning(
            f"Redis unavailable ({redis_msg}). Running in standalone in-memory mode."
        )
        # Explicitly clear any previously set message_queue so that calling
        # init_app() a second time (e.g. in tests after a production init)
        # does NOT inherit the Redis PubSubManager from the first call.
        socketio.server_options.pop("message_queue", None)
        socketio.server_options.pop("client_manager", None)
        socketio_kwargs["message_queue"] = None  # forces url=None → no queue

    socketio.init_app(app, **socketio_kwargs)

    # Register chat event handlers
    from sockets import chat_events
    chat_events.register_events(socketio, app)

    return socketio
