
from app import app, db
from models import Center
import random

def add_dummy_centers():
    """Add 10 dummy centers to the database."""
    print("Adding 10 dummy centers...")
    
    # Center names and cities
    center_names = [
        "Digital Aaganwadi", "Smart Learning Center", "Child Development Hub", 
        "Future Minds Center", "Early Education Point", "Little Stars Aaganwadi", 
        "Happy Kids Center", "Growing Minds", "Sunshine Aaganwadi", "Rainbow Learning Hub"
    ]
    
    cities = [
        "Nagpur", "Indore", "Surat", "Bhopal", "Kanpur", 
        "Patna", "Ludhiana", "Varanasi", "Agra", "Visakhapatnam"
    ]
    
    areas = [
        "Gandhi Nagar", "Civil Lines", "Model Town", "Saket Colony", "New Market",
        "MG Road", "Railway Colony", "Sector 9", "Lake View", "Green Park"
    ]
    
    for i in range(10):
        address = f"{random.randint(1, 100)}, {random.choice(areas)}, {cities[i]}"
        phone = f"98{random.randint(1000000000, 9999999999):10d}"
        
        center = Center(
            name=center_names[i],
            address=address,
            contact_number=phone,
            email=f"center{i+11}@aaganshiksha.org"
        )
        db.session.add(center)
    
    db.session.commit()
    print("✅ 10 dummy centers added successfully!")
    return True

if __name__ == "__main__":
    with app.app_context():
        add_dummy_centers()
