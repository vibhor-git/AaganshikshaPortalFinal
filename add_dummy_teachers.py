
from app import app, db
from models import User, Center
from werkzeug.security import generate_password_hash
import random

def add_dummy_teachers():
    """Add 10 dummy teachers to the database, one per center."""
    print("Adding 10 dummy teachers...")
    
    # Get centers that don't have teachers assigned yet
    centers = Center.query.outerjoin(User, Center.id == User.center_id)\
                  .filter(User.id == None)\
                  .limit(10).all()
    
    if not centers:
        print("No centers available without assigned teachers!")
        return False
    
    # Teacher names
    first_names = [
        "Rajesh", "Sunita", "Amit", "Priya", "Vikram", 
        "Ananya", "Deepak", "Meena", "Sanjay", "Kavita"
    ]
    
    last_names = [
        "Sharma", "Patel", "Singh", "Gupta", "Reddy", 
        "Verma", "Kumar", "Joshi", "Mishra", "Pandey"
    ]
    
    for i, center in enumerate(centers):
        # Create a unique name
        name = f"{first_names[i]} {last_names[random.randint(0, len(last_names)-1)]}"
        
        # Generate a unique 12-digit Aadhar number
        aadhar = f"444455{i:02d}{random.randint(100000, 999999):06d}"[:12]
        
        # Create email from first name
        email = f"{first_names[i].lower()}@aaganshiksha.org"
        
        # Generate random phone and address
        phone = f"98{random.randint(1000000000, 9999999999):10d}"
        city = center.address.split(",")[-1].strip()
        address = f"{random.randint(1, 100)}, Teachers Colony, {city}"
        
        # Create teacher
        teacher = User(
            username=f"teacher{center.id}",
            email=email,
            role='teacher',
            aadhar_number=aadhar,
            phone_number=phone,
            address=address,
            center_id=center.id
        )
        teacher.set_password(f"teacher{center.id}")
        
        db.session.add(teacher)
    
    db.session.commit()
    print(f"✅ {len(centers)} dummy teachers added successfully!")
    return True

if __name__ == "__main__":
    with app.app_context():
        add_dummy_teachers()
