import os
import logging
from flask import Flask
from config import Config
from models import db
from models.migration import run_database_migrations
from sockets import init_socketio, socketio
from routes import main_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(name)s: %(message)s",
)
# Keep third-party loggers quiet
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logging.getLogger("engineio").setLevel(logging.WARNING)
logging.getLogger("socketio").setLevel(logging.WARNING)
logger = logging.getLogger("livechat")


def create_app(config_class=Config):
    """Application factory for LiveChat Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Safely migrate schema and seed default data
    run_database_migrations(app)

    # Register Blueprints
    app.register_blueprint(main_bp)

    # Initialize Flask-SocketIO
    init_socketio(app)

    return app


# Create global app instance
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "yes")
    
    print("\n" + "=" * 60)
    print(" [*] LiveChat Real-Time Collaboration Platform Starting")
    print(f" [*] URL: http://127.0.0.1:{port}")
    print(f" [*] Database: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
    print(f" [*] Redis Status: {app.config.get('REDIS_STATUS_MESSAGE')}")
    print("=" * 60 + "\n")
    
    socketio.run(app, host="0.0.0.0", port=port, debug=debug, allow_unsafe_werkzeug=True)
