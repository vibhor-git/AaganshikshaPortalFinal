
from app import app, db
from models import Activity, User
from datetime import datetime, timedelta

def add_activities():
    with app.app_context():
        # Get admin user for assigning the activities
        admin = User.query.filter_by(role='admin').first()
        
        if not admin:
            print("No admin user found. Please create an admin user first.")
            return
        
        # Today's date for reference
        today = datetime.utcnow().date()
        
        # List of activities with title, description, and days from today
        activities = [
            ("Garden to Plate", "Children will plant seeds in recycled containers and learn about plant growth and nutrition while tending to their own mini garden.", 7),
            ("Traditional Games Day", "Introducing children to traditional Indian games like Pitthu, Gilli-Danda, and Kho-Kho to promote physical activity and cultural heritage.", 14),
            ("Storytime with Puppets", "Interactive storytelling using hand-made puppets to enhance listening skills, imagination, and emotional development.", 21),
            ("Healthy Cooking Workshop", "Simple food preparation activities where children learn to make nutritious snacks like sprout chaat and fruit salad.", 28),
            ("Nature Explorer Walk", "Guided walk around the locality to observe plants, insects, and birds, fostering environmental awareness and curiosity.", 10),
            ("Clay Modeling Session", "Using natural clay to create shapes and objects, developing fine motor skills and artistic expression.", 17),
            ("Music and Movement", "Rhythmic activities and simple dance movements to improve coordination, balance, and cultural appreciation.", 24),
            ("Parent-Child Day", "Collaborative activities for parents and children to strengthen bonds and demonstrate home-based learning techniques.", 31),
            ("Science Fun Day", "Age-appropriate experiments with water, colors, and everyday materials to introduce basic scientific concepts.", 12),
            ("Numbers and Counting Games", "Interactive games using natural materials like stones and leaves to develop early mathematical skills in a playful manner.", 19)
        ]
        
        # Add each activity to the database
        for title, description, days_ahead in activities:
            activity_date = today + timedelta(days=days_ahead)
            activity = Activity(
                title=title,
                description=description,
                date=activity_date,
                is_active=True,
                user_id=admin.id,
                created_at=datetime.utcnow()
            )
            db.session.add(activity)
        
        # Commit changes
        db.session.commit()
        print("Successfully added 10 activities to the database!")

if __name__ == "__main__":
    add_activities()
