import uuid
from datetime import datetime
from database.models import Base, engine, SessionLocal, User, Document, Chunk, Conversation, Message

def seed_database():
    session = SessionLocal()
    try:
        # Clear existing data
        session.query(Message).delete()
        session.query(Conversation).delete()
        session.query(Chunk).delete()
        session.query(Document).delete()
        session.query(User).delete()

        # Seed Users
        user1 = User(
            id=str(uuid.uuid4()),
            email="alice@example.com",
            password_hash="hashed_password_1",
            role="admin",
            created_at=datetime.utcnow()
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="bob@example.com",
            password_hash="hashed_password_2",
            role="user",
            created_at=datetime.utcnow()
        )

        session.add_all([user1, user2])
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()