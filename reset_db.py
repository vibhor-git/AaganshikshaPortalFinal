
import os
import sys
from app import app, db
from models import User, Center, Student, Inventory, NutritionTip, Activity, Attendance, Complaint, InventoryRequest
from utils import initialize_demo_data

def reset_database():
    """
    Resets the database by dropping all tables and recreating them.
    WARNING: This will delete all data in the database!
    """
    print("⚠️ WARNING: This will delete ALL existing data in the database! ⚠️")
    print("Automatic confirmation: Database will be reset now.")
    
    # Skip confirmation for automated reset
    confirm = "YES"
    
    try:
        # Drop all tables
        with app.app_context():
            db.drop_all()
            print("✓ All tables dropped successfully.")
            
            # Create new tables
            db.create_all()
            print("✓ New tables created successfully.")
            
            # Initialize demo data
            result = initialize_demo_data()
            if result:
                print("✓ Demo data initialized successfully.")
            else:
                print("× Demo data initialization failed.")
                
        print("\n✅ Database reset and rebuilt successfully with the new schema.")
        print("The new schema includes:")
        print("- Aadhar number fields for users and students")
        print("- Auto-generated IDs for nutrition tips, activities, and inventory requests")
        return True
        
    except Exception as e:
        print(f"× An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    reset_database()
