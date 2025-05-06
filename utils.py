from datetime import datetime, timedelta
from models import User, Student, Center, Inventory, NutritionTip, Activity, Attendance, Complaint
from app import db
from werkzeug.security import generate_password_hash
import random
import string

def format_date(date):
    """Format a date object to string in the format 'YYYY-MM-DD'"""
    if date:
        return date.strftime('%Y-%m-%d')
    return None

def format_datetime(dt):
    """Format a datetime object to string in the format 'YYYY-MM-DD HH:MM'"""
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M')
    return None

def get_week_dates():
    """Get the dates for the current week (Monday to Sunday)"""
    today = datetime.utcnow().date()
    monday = today - timedelta(days=today.weekday())
    
    week_dates = []
    for i in range(7):
        week_dates.append(monday + timedelta(days=i))
    
    return week_dates

def initialize_demo_data():
    """Initialize demo data for the application."""
    # Only initialize if no data exists
    if User.query.first() is not None:
        return False
    
    # Create admin and teacher users
    admin = User(
        username='admin',
        email='admin@aaganshiksha.org',
        role='admin',
        aadhar_number='123456789012'
    )
    admin.password_hash = generate_password_hash('admin123')
    
    teacher = User(
        username='teacher',
        email='teacher@aaganshiksha.org',
        role='teacher',
        aadhar_number='987654321012'
    )
    teacher.password_hash = generate_password_hash('teacher123')
    
    db.session.add(admin)
    db.session.add(teacher)
    
    # Create centers
    centers = [
        Center(name='Aaganwadi Center 1', address='123 Main St, City 1', contact_number='1234567890', email='center1@aaganshiksha.org'),
        Center(name='Aaganwadi Center 2', address='456 Elm St, City 2', contact_number='0987654321', email='center2@aaganshiksha.org')
    ]
    
    for center in centers:
        db.session.add(center)
    
    # Commit to get center IDs
    db.session.commit()
    
    # Create students
    student_names = [
        'Aarav Sharma', 'Aditi Patel', 'Arjun Singh', 'Diya Kumar', 'Ishaan Gupta',
        'Kavya Desai', 'Neha Reddy', 'Rohan Mehta', 'Sanya Verma', 'Vihaan Joshi'
    ]
    
    for i, name in enumerate(student_names):
        center_id = centers[i % 2].id  # Alternate between centers
        # Generate a unique 12-digit Aadhar number for each student
        aadhar = f'{(i+1):012d}'
        student = Student(
            name=name,
            age=random.randint(3, 6),
            gender='male' if i % 2 == 0 else 'female',
            parent_name=f'Parent of {name}',
            parent_contact=f'98765{i:05d}',
            address=f'{i+100} Park Avenue, City {i%3 + 1}',
            aadhar_number=aadhar,
            center_id=center_id,
            enrollment_date=datetime.utcnow().date() - timedelta(days=random.randint(10, 100))
        )
        db.session.add(student)
    
    # Create inventory items
    inventory_items = [
        ('Rice', 50, 'kg', 'Basmati rice for meals'),
        ('Milk', 20, 'liters', 'Toned milk for children'),
        ('Notebooks', 100, 'pieces', 'Basic ruled notebooks'),
        ('Pencils', 200, 'pieces', 'HB pencils for writing'),
        ('Toys', 30, 'sets', 'Educational toys for learning')
    ]
    
    for i, (name, qty, unit, desc) in enumerate(inventory_items):
        center_id = centers[i % 2].id  # Alternate between centers
        inventory = Inventory(
            item_name=name,
            quantity=qty,
            unit=unit,
            description=desc,
            center_id=center_id
        )
        db.session.add(inventory)
    
    # Create nutrition tips
    nutrition_tips = [
        ('Importance of Protein', 'Protein is essential for growing children. Include eggs, milk, and pulses in daily diet.'),
        ('Fruits for Immunity', 'Fresh fruits provide essential vitamins that boost immunity.'),
        ('Hydration', 'Ensure children drink at least 5-6 glasses of water daily for proper hydration.'),
        ('Avoid Junk Food', 'Limit consumption of processed foods high in salt, sugar, and unhealthy fats.')
    ]
    
    for title, content in nutrition_tips:
        tip = NutritionTip(
            title=title,
            content=content,
            is_active=True,
            user_id=random.choice([admin.id, teacher.id])
        )
        db.session.add(tip)
    
    # Create activities
    activities = [
        ('Story Telling Session', 'Interactive storytelling session for cognitive development', datetime.utcnow().date() + timedelta(days=5)),
        ('Art and Craft', 'Creative art and craft activities using recycled materials', datetime.utcnow().date() + timedelta(days=7)),
        ('Sports Day', 'Fun outdoor activities and games for physical development', datetime.utcnow().date() + timedelta(days=10)),
        ('Parents Meeting', 'Meeting with parents to discuss child development', datetime.utcnow().date() + timedelta(days=15))
    ]
    
    for title, desc, date in activities:
        activity = Activity(
            title=title,
            description=desc,
            date=date,
            is_active=True,
            user_id=random.choice([admin.id, teacher.id])
        )
        db.session.add(activity)
    
    # Commit all changes
    db.session.commit()
    
    # Mark attendance for past 7 days for all students
    students = Student.query.all()
    today = datetime.utcnow().date()
    
    for i in range(7):
        date = today - timedelta(days=i)
        
        for student in students:
            # Randomly mark as present (70% chance), absent (20% chance), or late (10% chance)
            rand = random.random()
            if rand < 0.7:
                status = 'present'
            elif rand < 0.9:
                status = 'absent'
            else:
                status = 'late'
            
            attendance = Attendance(
                student_id=student.id,
                date=date,
                status=status,
                remarks='Regular attendance' if status == 'present' else ('Sick' if status == 'absent' else 'Transport issue'),
                marked_by=teacher.id
            )
            db.session.add(attendance)
    
    # Create sample complaints
    for i in range(3):
        complaint = Complaint(
            name=f'Parent {i+1}',
            email=f'parent{i+1}@example.com',
            subject=f'Complaint about {["food", "facilities", "teaching"][i%3]}',
            message=f'This is a sample complaint message about {["food quality", "center facilities", "teaching methods"][i%3]}.',
            status=['pending', 'in-progress', 'resolved'][i%3]
        )
        db.session.add(complaint)
    
    # Commit all changes
    db.session.commit()
    
    return True
