
from app import app, db
from models import Student, Attendance, User
import random
from datetime import datetime, timedelta

def add_dummy_attendance():
    """Add attendance records for all students for the past 2 months."""
    print("Adding dummy attendance records for the past 2 months...")
    
    # Get all students
    students = Student.query.all()
    
    if not students:
        print("No students found in the database!")
        return False
    
    # Generate dates for the past 2 months (weekdays only)
    today = datetime.utcnow().date()
    two_months_ago = today - timedelta(days=60)
    
    # Get all days between two_months_ago and today
    attendance_days = []
    current_date = two_months_ago
    
    while current_date <= today:
        # Only include weekdays (Monday to Friday)
        if current_date.weekday() < 5:  # 0-4 are Monday to Friday
            attendance_days.append(current_date)
        current_date = current_date + timedelta(days=1)
    
    print(f"Generating attendance for {len(attendance_days)} school days")
    
    # For each student, create attendance records for all days
    total_records = 0
    
    for student in students:
        # Get the teacher assigned to this student's center
        teacher = User.query.filter_by(center_id=student.center_id, role='teacher').first()
        
        if not teacher:
            print(f"Warning: No teacher found for center {student.center_id}, using first admin")
            teacher = User.query.filter_by(role='admin').first()
        
        if not teacher:
            print(f"Error: No teachers or admins found to mark attendance!")
            return False
        
        for day in attendance_days:
            # First check if attendance already exists for this student on this day
            existing = Attendance.query.filter_by(
                student_id=student.id,
                date=day
            ).first()
            
            if existing:
                continue  # Skip if attendance already recorded
                
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
            total_records += 1
            
            # Commit in batches to avoid memory issues
            if total_records % 1000 == 0:
                print(f"Processed {total_records} attendance records...")
                db.session.commit()
    
    # Final commit
    db.session.commit()
    print(f"✅ Added {total_records} attendance records for {len(students)} students across {len(attendance_days)} days!")
    return True

if __name__ == "__main__":
    with app.app_context():
        add_dummy_attendance()
