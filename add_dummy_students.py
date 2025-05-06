
from app import app, db
from models import Student, Center
import random
from datetime import datetime, timedelta

def add_dummy_students():
    """Add 20 dummy students to each center in the database."""
    print("Adding dummy students to centers...")
    
    # Get all centers
    centers = Center.query.all()
    
    if not centers:
        print("No centers found in the database!")
        return False
    
    # Boy and girl names for variety
    boy_names = [
        "Aarav", "Vihaan", "Arjun", "Reyansh", "Ayaan", "Atharva", "Krishna", 
        "Ishaan", "Shaurya", "Dhruv", "Kabir", "Ritvik", "Aarush", "Veer", 
        "Ronith", "Krish", "Rohan", "Arnav", "Aditya", "Yash", "Shivam", "Rudra",
        "Ansh", "Vivaan", "Dev", "Devansh", "Abhimanyu", "Shreshth", "Parth"
    ]
    
    girl_names = [
        "Aadhya", "Ananya", "Pari", "Aanya", "Aaradhya", "Anvi", "Myra", 
        "Siya", "Diya", "Kiara", "Avni", "Anika", "Navya", "Riya", "Ahana", 
        "Ishita", "Saanvi", "Nisha", "Shreya", "Tara", "Meera", "Ira", "Zara", 
        "Kyra", "Advika", "Sara", "Avantika", "Prisha", "Khushi"
    ]
    
    last_names = [
        "Sharma", "Patel", "Singh", "Kumar", "Verma", "Gupta", "Malhotra", 
        "Reddy", "Iyer", "Joshi", "Shah", "Das", "Rao", "Chopra", "Kohli", 
        "Jain", "Agarwal", "Mishra", "Nair", "Menon", "Khanna", "Bose", "Sen", 
        "Kapoor", "Malik", "Chaudhary", "Chawla", "Pillai", "Desai"
    ]
    
    total_added = 0
    
    for center in centers:
        print(f"Adding students to center: {center.name}")
        
        # Add 20 students to each center (10 boys, 10 girls)
        for i in range(20):
            # Decide gender (alternate)
            gender = "male" if i < 10 else "female"
            
            # Select appropriate name based on gender
            if gender == "male":
                first_name = random.choice(boy_names)
            else:
                first_name = random.choice(girl_names)
                
            last_name = random.choice(last_names)
            full_name = f"{first_name} {last_name}"
            
            # Age between 5-12
            age = random.randint(5, 12)
            
            # Generate parent name (Mr/Mrs + last_name)
            parent_prefix = "Mr." if random.random() < 0.7 else "Mrs."
            parent_name = f"{parent_prefix} {last_name}"
            
            # Generate unique Aadhar number
            # Format: center_id(3 digits) + sequential number(3 digits) + random(6 digits)
            aadhar = f"{center.id:03d}{i:03d}{random.randint(100000, 999999):06d}"[:12]
            
            # Generate address based on center's city
            city = center.address.split(",")[-1].strip()
            area = random.choice(["Gandhi Nagar", "Model Town", "Civil Lines", "New Colony", 
                                 "Green Park", "Sector 12", "Lake View", "Old City", "Central Area"])
            address = f"{random.randint(1, 200)}, {area}, {city}"
            
            # Generate parent contact
            contact = f"9{random.randint(700000000, 999999999):09d}"
            
            # Generate enrollment date (between 30-365 days ago)
            enrollment_date = datetime.utcnow().date() - timedelta(days=random.randint(30, 365))
            
            # Create student
            student = Student(
                name=full_name,
                age=age,
                gender=gender,
                parent_name=parent_name,
                parent_contact=contact,
                address=address,
                aadhar_number=aadhar,
                enrollment_date=enrollment_date,
                center_id=center.id
            )
            
            db.session.add(student)
            total_added += 1
        
        # Commit after each center to prevent large transaction
        db.session.commit()
    
    print(f"✅ Added {total_added} students across {len(centers)} centers!")
    return True

if __name__ == "__main__":
    with app.app_context():
        add_dummy_students()
