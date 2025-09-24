from .app import app
from .models import db, User, Session, UserSession, Reflection
from datetime import datetime

def seed_database():
    with app.app_context():
    
        user1 = User(name="John Doe", email="john@example.com")
        user1.set_password("password123")
        
        user2 = User(name="Jane Smith", email="jane@example.com")
        user2.set_password("password123")
        
        user3 = User(name="Bob Johnson", email="bob@example.com")
        user3.set_password("password123")
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        
      
        session1 = Session(
            title="Bible Study on Faith",
            theme="Faith in Action",
            date=datetime(2024, 9, 25, 10, 0, 0),
            facilitator_id=user1.id
        )
        db.session.add(session1)
        db.session.commit()
        
        # Add users to session
        user_session1 = UserSession(user_id=user1.id, session_id=session1.id, role="facilitator")
        user_session2 = UserSession(user_id=user2.id, session_id=session1.id, role="participant")
        user_session3 = UserSession(user_id=user3.id, session_id=session1.id, role="participant")
        
        db.session.add_all([user_session1, user_session2, user_session3])
        db.session.commit()
        
        # Create sample reflections
        reflection1 = Reflection(
            content="This session helped me understand faith better.",
            user_id=user2.id,
            session_id=session1.id
        )
        
        reflection2 = Reflection(
            content="Great discussion on applying faith in daily life.",
            user_id=user3.id,
            session_id=session1.id
        )
        
        db.session.add_all([reflection1, reflection2])
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()