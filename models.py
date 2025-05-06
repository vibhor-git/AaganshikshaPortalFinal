from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'teacher'
    aadhar_number = db.Column(db.String(12), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'), nullable=True)  # Only required for teachers
    
    # Relationships
    center = db.relationship('Center', backref='teachers', lazy=True)
    complaints = db.relationship('Complaint', backref='author', lazy=True)
    nutrition_tips = db.relationship('NutritionTip', backref='created_by', lazy=True)
    activities = db.relationship('Activity', backref='created_by', lazy=True)
    inventory_requests = db.relationship('InventoryRequest',
                                      foreign_keys='InventoryRequest.user_id',
                                      backref=db.backref('requested_by', lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all, delete-orphan')
    
    @validates('aadhar_number')
    def validate_aadhar_number(self, key, aadhar_number):
        if not aadhar_number.isdigit() or len(aadhar_number) != 12:
            raise ValueError('Aadhar number must be exactly 12 digits')
        return aadhar_number
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_teacher(self):
        return self.role == 'teacher'

class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_number = db.Column(db.String(15))
    email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    students = db.relationship('Student', backref='center', lazy=True)
    inventory_items = db.relationship('Inventory', backref='center', lazy=True)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    parent_name = db.Column(db.String(100))
    parent_contact = db.Column(db.String(15))
    address = db.Column(db.String(200))
    aadhar_number = db.Column(db.String(12), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)
    
    @validates('aadhar_number')
    def validate_aadhar_number(self, key, aadhar_number):
        if not aadhar_number.isdigit() or len(aadhar_number) != 12:
            raise ValueError('Aadhar number must be exactly 12 digits')
        return aadhar_number

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20))
    description = db.Column(db.Text)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class NutritionTip(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'present', 'absent', 'late'
    remarks = db.Column(db.Text)
    marked_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with user who marked attendance
    teacher = db.relationship('User', foreign_keys=[marked_by])

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Optional, if complaint by logged-in user
    status = db.Column(db.String(20), default='pending')  # 'pending', 'resolved', 'in-progress'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class InventoryRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(20))
    description = db.Column(db.Text)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    center = db.relationship('Center', backref='inventory_requests')
    requested_by = db.relationship('User', foreign_keys=[user_id])
