
from app import app, db
from models import NutritionTip, User
from datetime import datetime

def add_nutrition_tips():
    with app.app_context():
        # Get admin user for assigning the tips
        admin = User.query.filter_by(role='admin').first()
        
        if not admin:
            print("No admin user found. Please create an admin user first.")
            return
        
        # List of nutrition tips
        nutrition_tips = [
            ("Protein-Rich Breakfast", "Start the day with protein-rich foods like eggs, paneer, or sprouted legumes to improve concentration and energy levels throughout the day."),
            ("Iron-Rich Foods", "Include iron-rich foods like spinach, beetroot, and jaggery to prevent anemia and boost cognitive development in growing children."),
            ("Calcium for Growth", "Ensure daily intake of milk, curd, or cheese to support bone development and growth in children under 6 years."),
            ("Nuts and Seeds", "A small handful of mixed nuts and seeds provides essential fatty acids that support brain development and immune function."),
            ("Vitamin C Sources", "Include amla, orange, or guava daily to enhance immunity and iron absorption from plant-based foods."),
            ("Limit Processed Foods", "Replace packaged snacks with fresh fruits, vegetable sticks, or homemade snacks to reduce excess sugar and salt intake."),
            ("Balanced Thali", "Ensure each meal contains a grain, protein, vegetable, and dairy component for complete nutrition."),
            ("Mindful Eating", "Teach children to eat slowly and recognize hunger cues to prevent overeating and promote healthy eating habits."),
            ("Hydration Importance", "Ensure children drink water regularly throughout the day, not just when they feel thirsty, to maintain optimal hydration."),
            ("Traditional Superfoods", "Incorporate traditional foods like millets, turmeric, and indigenous vegetables which are rich in micronutrients and adapted to local conditions.")
        ]
        
        # Add each tip to the database
        for title, content in nutrition_tips:
            tip = NutritionTip(
                title=title,
                content=content,
                is_active=True,
                user_id=admin.id,
                created_at=datetime.utcnow()
            )
            db.session.add(tip)
        
        # Commit changes
        db.session.commit()
        print("Successfully added 10 nutrition tips to the database!")

if __name__ == "__main__":
    add_nutrition_tips()
