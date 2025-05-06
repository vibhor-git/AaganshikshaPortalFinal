
from app import app, db
from models import User, Center, Student, Inventory, NutritionTip, Activity, Attendance, Complaint, InventoryRequest
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample data for the application."""
    print("Generating sample data...")
    
    # Clear existing data first to prevent duplicates
    print("Clearing existing data...")
    # We're not deleting users to preserve the admin account
    # but will clear centers which will cascade to related data
    Center.query.delete()
    db.session.commit()
    
    # Check if admin user exists, create if not
    if User.query.filter_by(role='admin').first() is None:
        # Create admin user if it doesn't exist
        admin = User(
            username='admin',
            email='admin@aaganshiksha.org',
            role='admin',
            aadhar_number='111122223333'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    # Create exactly 10 centers - one for each teacher
    centers = []
    center_names = [f"Center {chr(65+i)}" for i in range(10)]  # Center A to Center J
    
    for i, name in enumerate(center_names):
        center = Center(
            name=name,
            address=f"{random.randint(1, 100)} {['Main', 'Park', 'Gandhi', 'Nehru', 'Patel'][i % 5]} Road, {['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'][i]}",
            contact_number=f"99{i}0{i}0{i}0{i}0{i}",
            email=f"center{chr(97+i)}@aaganshiksha.org"
        )
        db.session.add(center)
        centers.append(center)
    
    db.session.commit()
    
    # Create 10 teachers (1 per center)
    teacher_names = [
        "Rahul Sharma", "Priya Patel", "Amit Kumar", "Neha Singh", "Vikram Malhotra",
        "Anjali Desai", "Suresh Verma", "Kavita Gupta", "Rajesh Reddy", "Meena Iyer"
    ]
    
    teachers = []
    for i, name in enumerate(teacher_names):
        # Get first name for email
        first_name = name.split()[0].lower()
        
        # Generate a unique 12-digit Aadhar number for each teacher
        aadhar = f"222233{i:02d}{i+10:02d}{random.randint(10000, 99999):05d}"
        
        teacher = User(
            username=f"teacher{i+1}",
            email=f"{first_name}@aaganshiksha.org",
            role='teacher',
            aadhar_number=aadhar,
            center_id=centers[i].id  # Each teacher is assigned to a unique center
        )
        teacher.set_password(f"teacher{i+1}")
        db.session.add(teacher)
        teachers.append(teacher)
    
    db.session.commit()
    
    # Create 20 students per center (200 total)
    first_names_boys = [
        "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Reyansh", "Ayaan", "Atharva", 
        "Krishna", "Ishaan", "Shaurya", "Dhruv", "Kabir", "Ritvik", "Aarush", "Kayaan", 
        "Darsh", "Veer", "Samar", "Shivansh", "Ivaan", "Ronith", "Krish", "Ranbir", "Naksh"
    ]
    
    first_names_girls = [
        "Aadhya", "Ananya", "Pari", "Aanya", "Aaradhya", "Anvi", "Myra", "Sara", 
        "Siya", "Diya", "Kiara", "Avni", "Anika", "Navya", "Riya", "Ahana", "Ishita", 
        "Saanvi", "Nisha", "Shreya", "Tara", "Meera", "Ira", "Zara", "Kyra"
    ]
    
    last_names = [
        "Sharma", "Patel", "Singh", "Kumar", "Verma", "Gupta", "Malhotra", "Desai",
        "Reddy", "Iyer", "Joshi", "Shah", "Das", "Rao", "Chopra", "Kohli", "Jain",
        "Agarwal", "Mishra", "Nair", "Menon", "Khanna", "Bose", "Sen", "Kapoor"
    ]
    
    students = []
    for center in centers:
        for i in range(20):  # 20 students per center
            # Determine gender (alternating)
            gender = "male" if i % 2 == 0 else "female"
            
            # Choose name based on gender
            if gender == "male":
                first_name = random.choice(first_names_boys)
            else:
                first_name = random.choice(first_names_girls)
            
            last_name = random.choice(last_names)
            name = f"{first_name} {last_name}"
            
            # Generate a unique 12-digit Aadhar number for each student
            center_index = centers.index(center)
            aadhar = f"3333{center_index:02d}{i:02d}{random.randint(100000, 999999):06d}"[:12]
            
            # Create student
            student = Student(
                name=name,
                age=random.randint(3, 6),
                gender=gender,
                parent_name=f"Parent of {name}",
                parent_contact=f"98765{random.randint(10000, 99999):05d}",
                address=f"{random.randint(1, 100)} {['Main', 'Park', 'Gandhi', 'Nehru', 'Patel'][i % 5]} Street, {['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow'][center_index]}",
                aadhar_number=aadhar,
                center_id=center.id,
                enrollment_date=datetime.utcnow().date() - timedelta(days=random.randint(30, 365))
            )
            db.session.add(student)
            students.append(student)
    
    db.session.commit()
    
    # Create 2 nutrition tips per teacher (20 total)
    nutrition_tips_data = [
        "Balanced Diet for Children", "Include fruits, vegetables, proteins, and carbohydrates in children's meals for optimal growth.",
        "Hydration Importance", "Ensure children drink at least 6-8 glasses of water daily, especially during summer.",
        "Protein-Rich Foods", "Include eggs, milk, pulses, and nuts in daily diet to support muscle development.",
        "Iron-Rich Diet", "Serve green leafy vegetables, beans, and jaggery to prevent anemia in growing children.",
        "Healthy Snacks", "Replace packaged snacks with fruits, sprouts, and homemade options to avoid excess sugar and salt.",
        "Calcium Sources", "Regular intake of milk, curd, and cheese helps in bone development for children.",
        "Vitamin C Foods", "Include citrus fruits, amla, and guava to boost immunity and fight infections.",
        "Whole Grains", "Choose brown rice, whole wheat bread, and millets over refined grains for better nutrition.",
        "Limit Sugar Intake", "Reduce consumption of candies, chocolates, and sugary drinks to prevent dental issues and obesity.",
        "Meal Timing", "Maintain regular meal times to establish healthy eating patterns in children.",
        "Mindful Eating", "Encourage children to eat slowly and focus on their food without distractions.",
        "Rainbow Plate", "Include colorful fruits and vegetables to ensure diverse nutrient intake.",
        "Omega-3 Rich Foods", "Include flaxseeds, walnuts, and fatty fish for brain development.",
        "Probiotics", "Regular consumption of curd and fermented foods improves gut health.",
        "Avoid Processed Foods", "Limit packaged and processed foods high in preservatives and artificial colors.",
        "Seasonal Fruits", "Prioritize locally grown seasonal fruits for maximum nutritional benefits.",
        "Homemade Meals", "Prefer homemade meals over outside food to ensure hygiene and nutrition.",
        "Portion Control", "Serve age-appropriate portions to avoid overeating and food wastage.",
        "Protein at Breakfast", "Include protein-rich foods at breakfast for sustained energy throughout the day.",
        "Cooking Methods", "Prefer steaming, boiling, and baking over deep-frying for healthier meal preparation."
    ]
    
    for i, teacher in enumerate(teachers):
        # Create 2 nutrition tips per teacher
        for j in range(2):
            index = i*2 + j
            tip = NutritionTip(
                title=nutrition_tips_data[index*2],
                content=nutrition_tips_data[index*2 + 1],
                user_id=teacher.id,
                is_active=True
            )
            db.session.add(tip)
    
    db.session.commit()
    
    # Create 2 activities per teacher (20 total)
    activities_data = [
        "Story Telling Session", "Interactive storytelling to enhance language skills and imagination.",
        "Art and Craft Workshop", "Creative activities using recycled materials to develop fine motor skills.",
        "Nature Walk", "Guided walk to observe local plants and insects, promoting environmental awareness.",
        "Group Games", "Team-based games to foster cooperation and social skills.",
        "Music and Dance", "Rhythmic activities to develop coordination and cultural appreciation.",
        "Simple Science Experiments", "Age-appropriate experiments to encourage curiosity and logical thinking.",
        "Yoga for Kids", "Basic yoga poses and breathing exercises for physical and mental well-being.",
        "Kitchen Garden Project", "Planting and tending to vegetable seeds to understand plant growth.",
        "Puppet Show", "Educational puppet performances about health, hygiene, and social values.",
        "Clay Modeling", "Creating shapes and objects with clay to enhance creativity and dexterity.",
        "Number Games", "Fun activities with counting and basic mathematics for cognitive development.",
        "Traditional Games", "Teaching indigenous games like Lagori, Kho-Kho to preserve cultural heritage.",
        "Drawing and Painting", "Free-form art expression using various colors and techniques.",
        "Book Reading Club", "Regular reading sessions to develop language skills and love for books.",
        "Role Play", "Enacting common scenarios to understand social roles and responsibilities.",
        "Community Helpers Visit", "Interaction with local professionals like doctors, firefighters for awareness.",
        "Nutrition Workshop", "Learning about healthy foods through interactive demonstrations.",
        "Hygiene Awareness", "Fun activities to teach personal hygiene habits like handwashing.",
        "Physical Exercise Session", "Age-appropriate exercises for physical fitness and energy release.",
        "Show and Tell", "Children bringing and describing personal items to improve communication skills."
    ]
    
    today = datetime.utcnow().date()
    for i, teacher in enumerate(teachers):
        # Create 2 activities per teacher
        for j in range(2):
            index = i*2 + j
            activity_date = today + timedelta(days=random.randint(1, 30))
            
            activity = Activity(
                title=activities_data[index*2],
                description=activities_data[index*2 + 1],
                date=activity_date,
                user_id=teacher.id,
                is_active=True
            )
            db.session.add(activity)
    
    db.session.commit()
    
    # Create 1 inventory request per center (10 total)
    inventory_items = [
        "Books and Educational Materials", "30", "sets", "New learning materials for preschool education",
        "Sports Equipment", "5", "sets", "Balls, skipping ropes, and other outdoor play equipment",
        "Art Supplies", "20", "kits", "Crayons, sketch pens, colored paper, and craft materials",
        "Furniture", "10", "pieces", "Child-sized tables and chairs for activities",
        "Drinking Water Filters", "2", "units", "Water purification systems for safe drinking water",
        "First Aid Kits", "5", "kits", "Medical supplies for emergency treatment",
        "Stationery", "50", "sets", "Notebooks, pencils, erasers, and sharpeners",
        "Storage Units", "4", "pieces", "Cabinets and shelves for organizing materials",
        "Mats and Carpets", "10", "pieces", "Floor coverings for sitting and activities",
        "Nutritional Supplements", "100", "packs", "Protein and vitamin supplements for children"
    ]
    
    for i, center in enumerate(centers):
        # Get the teacher assigned to this center
        teacher = User.query.filter_by(center_id=center.id).first()
        
        # Create inventory request
        request = InventoryRequest(
            item_name=inventory_items[i*4],
            quantity=int(inventory_items[i*4 + 1]),
            unit=inventory_items[i*4 + 2],
            description=inventory_items[i*4 + 3],
            center_id=center.id,
            user_id=teacher.id,
            status=random.choice(['pending', 'approved', 'rejected'])
        )
        db.session.add(request)
    
    db.session.commit()
    
    # Create 2 months of attendance (June & July 2024)
    # Define school days (Monday to Friday)
    june_2024_days = []
    july_2024_days = []
    
    # June 2024 (weekdays only)
    june_start = datetime(2024, 6, 1).date()
    for i in range(30):  # June has 30 days
        day = june_start + timedelta(days=i)
        if day.weekday() < 5:  # 0-4 are Monday to Friday
            june_2024_days.append(day)
    
    # July 2024 (weekdays only)
    july_start = datetime(2024, 7, 1).date()
    for i in range(31):  # July has 31 days
        day = july_start + timedelta(days=i)
        if day.weekday() < 5:  # 0-4 are Monday to Friday
            july_2024_days.append(day)
    
    # Limit to 20 days per month
    june_2024_days = june_2024_days[:20]
    july_2024_days = july_2024_days[:20]
    
    # Combine all days
    all_days = june_2024_days + july_2024_days
    
    for student in students:
        # Get the teacher assigned to this student's center
        teacher = User.query.filter_by(center_id=student.center_id).first()
        
        for day in all_days:
            # Randomly mark as present (85% chance), absent (10% chance), or late (5% chance)
            rand = random.random()
            if rand < 0.85:
                status = 'present'
                remarks = 'Regular attendance'
            elif rand < 0.95:
                status = 'absent'
                if random.random() < 0.7:
                    remarks = 'Sick leave'
                else:
                    remarks = 'Family function'
            else:
                status = 'late'
                remarks = 'Transport issue'
            
            attendance = Attendance(
                student_id=student.id,
                date=day,
                status=status,
                remarks=remarks,
                marked_by=teacher.id
            )
            db.session.add(attendance)
    
    # Commit in batches to avoid memory issues
    db.session.commit()
    
    # Create 3 complaints
    complaints_data = [
        "Broken Furniture", "Several chairs in Center A are broken and need immediate repair.",
        "Poor Meal Quality", "Parents have complained about the quality of meals served last week.",
        "Water Leakage", "There is water leakage in the classroom during rainy days."
    ]
    
    statuses = ['pending', 'in-progress', 'resolved']
    
    for i in range(3):
        # Randomly select a center and student from that center
        center = random.choice(centers)
        student = random.choice([s for s in students if s.center_id == center.id])
        
        complaint = Complaint(
            name=f"Parent of {student.name}",
            email=f"parent{i+1}@example.com",
            subject=complaints_data[i*2],
            message=complaints_data[i*2 + 1],
            status=statuses[i],
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
        )
        
        if statuses[i] == 'resolved':
            complaint.resolved_at = datetime.utcnow() - timedelta(days=random.randint(1, 10))
        
        db.session.add(complaint)
    
    db.session.commit()
    
    print("Sample data generation complete!")
    print("Created:")
    print(f"- 10 centers")
    print(f"- 10 teachers (1 per center)")
    print(f"- 200 students (20 per center)")
    print(f"- 20 nutrition tips (2 per teacher)")
    print(f"- 20 activities (2 per teacher)")
    print(f"- 10 inventory requests (1 per center)")
    print(f"- {len(all_days)} days of attendance for 200 students ({len(all_days)*200} records)")
    print(f"- 3 complaints")
    
    return True

if __name__ == "__main__":
    with app.app_context():
        generate_sample_data()
