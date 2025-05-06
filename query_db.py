from app import app
from models import User, Center, Student, Inventory, NutritionTip, Activity, Attendance, Complaint

# This script demonstrates querying database tables through Flask models

with app.app_context():
    print("\n===== Users =====")
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")

    print("\n===== Centers =====")
    centers = Center.query.all()
    for center in centers:
        print(f"ID: {center.id}, Name: {center.name}, Address: {center.address}, Contact: {center.contact_number}")
        print(f"- Students: {len(center.students)}")
        print(f"- Inventory items: {len(center.inventory_items)}")

    print("\n===== Students =====")
    students = Student.query.all()
    for student in students:
        print(f"ID: {student.id}, Name: {student.name}, Age: {student.age}, Center: {student.center.name if student.center else 'None'}")

    print("\n===== Inventory Items =====")
    items = Inventory.query.all()
    for item in items:
        print(f"ID: {item.id}, Name: {item.item_name}, Quantity: {item.quantity}, Center: {item.center.name if item.center else 'None'}")

    print("\n===== Nutrition Tips =====")
    tips = NutritionTip.query.all()
    for tip in tips:
        print(f"ID: {tip.id}, Title: {tip.title}, Created by: {tip.created_by.username}")

    print("\n===== Activities =====")
    activities = Activity.query.all()
    for activity in activities:
        print(f"ID: {activity.id}, Title: {activity.title}, Date: {activity.date}, Created by: {activity.created_by.username}")

    print("\n===== Attendance Records =====")
    records = Attendance.query.all()
    for record in records:
        print(f"ID: {record.id}, Student: {record.student.name}, Date: {record.date}, Status: {record.status}")

    print("\n===== Complaints =====")
    complaints = Complaint.query.all()
    for complaint in complaints:
        print(f"ID: {complaint.id}, Subject: {complaint.subject}, Status: {complaint.status}")