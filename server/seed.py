from app import app, db
from models import User, Session, UserSession, Reflection
from datetime import datetime

def seed_database():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Clear existing data
        db.session.query(Reflection).delete()
        db.session.query(UserSession).delete()
        db.session.query(Session).delete()
        db.session.query(User).delete()
        db.session.commit()

        # users
        user1 = User(name="John Doe", email="john@example.com")
        user1.set_password("password123")
        user2 = User(name="Jane Smith", email="jane@example.com")
        user2.set_password("password123")
        user3 = User(name="Bob Johnson", email="bob@example.com")
        user3.set_password("password123")

        db.session.add_all([user1, user2, user3])
        db.session.commit()

        # sessions
        session1 = Session(title="Faith Study", theme="Faith", facilitator_id=user1.id)
        session2 = Session(title="Prayer Meeting", theme="Prayer", facilitator_id=user2.id)
        session3 = Session(title="Bible Reading", theme="Scripture", facilitator_id=user3.id)

        db.session.add_all([session1, session2, session3])
        db.session.commit()

        #  user-session relationships
        user_session1 = UserSession(role="facilitator", user_id=user1.id, session_id=session1.id)
        user_session2 = UserSession(role="participant", user_id=user2.id, session_id=session1.id)
        user_session3 = UserSession(role="facilitator", user_id=user2.id, session_id=session2.id)
        user_session4 = UserSession(role="participant", user_id=user3.id, session_id=session2.id)
        user_session5 = UserSession(role="facilitator", user_id=user3.id, session_id=session3.id)
        user_session6 = UserSession(role="participant", user_id=user1.id, session_id=session3.id)

        db.session.add_all([user_session1, user_session2, user_session3, user_session4, user_session5, user_session6])
        db.session.commit()

        # reflections
        reflection1 = Reflection(content="This session deepened my faith.", user_id=user1.id, session_id=session1.id)
        reflection2 = Reflection(content="Great prayer time today.", user_id=user2.id, session_id=session2.id)
        reflection3 = Reflection(content="The Bible reading was enlightening.", user_id=user3.id, session_id=session3.id)

        db.session.add_all([reflection1, reflection2, reflection3])
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()