import logging
from sqlalchemy import text
from models import db, Room

logger = logging.getLogger("livechat.migration")

DEFAULT_ROOMS = [
    {
        "name": "general",
        "description": "Main collaboration space for announcements, general discussion, and team updates.",
        "is_default": True,
        "created_by": "system",
    },
    {
        "name": "developers",
        "description": "Engineering discussions, code reviews, architectural planning, and debugging.",
        "is_default": True,
        "created_by": "system",
    },
    {
        "name": "design",
        "description": "UI/UX design, visual systems, component patterns, and styling ideas.",
        "is_default": True,
        "created_by": "system",
    },
    {
        "name": "random",
        "description": "Casual chatter, team banter, coffee break discussions, and interesting links.",
        "is_default": True,
        "created_by": "system",
    },
]


def run_database_migrations(app):
    """
    Safely initialize and migrate SQLite database schema without data loss.
    - Creates missing tables (rooms, message_reactions, messages).
    - Safely adds missing columns to existing messages table.
    - Seeds default rooms if the rooms table is empty.
    """
    with app.app_context():
        try:
            # 1. Create tables if they do not exist
            db.create_all()

            # 2. Check and migrate columns on existing messages table
            inspector = db.inspect(db.engine)
            if inspector.has_table("messages"):
                existing_columns = {col["name"] for col in inspector.get_columns("messages")}

                migrations = []
                if "reply_to_id" not in existing_columns:
                    migrations.append("ALTER TABLE messages ADD COLUMN reply_to_id INTEGER REFERENCES messages(id)")
                if "is_pinned" not in existing_columns:
                    migrations.append("ALTER TABLE messages ADD COLUMN is_pinned BOOLEAN DEFAULT 0 NOT NULL")
                if "pinned_by" not in existing_columns:
                    migrations.append("ALTER TABLE messages ADD COLUMN pinned_by VARCHAR(50)")
                if "pinned_at" not in existing_columns:
                    migrations.append("ALTER TABLE messages ADD COLUMN pinned_at DATETIME")

                for sql in migrations:
                    logger.info(f"Executing migration: {sql}")
                    db.session.execute(text(sql))

                if migrations:
                    db.session.commit()
                    logger.info(f"Applied {len(migrations)} schema migration(s) to 'messages' table.")

            # 3. Seed default rooms if empty
            existing_room_count = Room.query.count()
            if existing_room_count == 0:
                logger.info("Seeding default rooms into database...")
                for r_data in DEFAULT_ROOMS:
                    room = Room(
                        name=r_data["name"],
                        description=r_data["description"],
                        is_default=r_data["is_default"],
                        created_by=r_data["created_by"],
                    )
                    db.session.add(room)
                db.session.commit()
                logger.info("Default rooms seeded successfully.")
            else:
                # Ensure default rooms exist even if other rooms are present
                for r_data in DEFAULT_ROOMS:
                    r_exists = Room.query.filter_by(name=r_data["name"]).first()
                    if not r_exists:
                        db.session.add(
                            Room(
                                name=r_data["name"],
                                description=r_data["description"],
                                is_default=r_data["is_default"],
                                created_by=r_data["created_by"],
                            )
                        )
                db.session.commit()

            logger.info("Database migration and initialization completed successfully.")

        except Exception as e:
            db.session.rollback()
            logger.error(f"Database migration error: {e}", exc_info=True)
            raise e
