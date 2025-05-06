
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Student, Center, Attendance, NutritionTip, Activity, Inventory
from forms import StudentForm, AttendanceForm, InventoryRequestForm
from app import db
from datetime import datetime, date
from functools import wraps

teacher_bp = Blueprint('teacher', __name__)

# Teacher access decorator
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('You need to be a teacher to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/api/teacher/search-suggestions')
@login_required
@teacher_required
def search_suggestions_api():
    query = request.args.get('query', '')
    if not query or len(query) < 3:
        return jsonify([])
    
    # Teachers can only search students in their center
    if not current_user.center_id:
        return jsonify([])
    
    suggestions = []
    
    # Search for students in teacher's center
    students = Student.query.filter(
        Student.center_id == current_user.center_id,
        db.or_(
            Student.name.ilike(f'%{query}%'),
            Student.aadhar_number.ilike(f'%{query}%'),
            Student.parent_contact.ilike(f'%{query}%'),
            Student.parent_name.ilike(f'%{query}%')
        )
    ).limit(10).all()
    
    for student in students:
        suggestions.append({
            'id': student.id,
            'name': student.name,
            'aadhar': "XXXX-XXXX-" + student.aadhar_number[-4:] if student.aadhar_number else 'N/A',
            'parent': student.parent_name
        })
    
    return jsonify(suggestions)

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import Student, Center, Inventory, NutritionTip, Activity, Attendance, User, InventoryRequest
from forms import StudentForm, InventoryForm, NutritionTipForm, ActivityForm, AttendanceForm, StudentAttendanceForm, InventoryRequestForm
from app import db
from datetime import datetime
from functools import wraps
from sqlalchemy import or_ # Added or_ import


teacher_bp = Blueprint('teacher', __name__)

# Teacher access decorator
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'teacher':
            flash('You need to be a teacher to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@teacher_bp.route('/dashboard')
@login_required
@teacher_required
def dashboard():
    # Check if teacher has an assigned center
    center_id = current_user.center_id
    center_name = "Not Assigned"

    if center_id:
        center = Center.query.get(center_id)
        center_name = center.name if center else "Unknown"

        # Count statistics for dashboard (center-specific)
        students_count = Student.query.filter_by(center_id=center_id).count()
        inventory_count = Inventory.query.filter_by(center_id=center_id).count()
    else:
        students_count = 0
        inventory_count = 0

    centers_count = 1  # Teacher only has one center
    tips_count = NutritionTip.query.count()
    activities_count = Activity.query.count()

    # Get recent activities and nutrition tips
    recent_activities = Activity.query.order_by(Activity.created_at.desc()).limit(5).all()
    recent_tips = NutritionTip.query.order_by(NutritionTip.created_at.desc()).limit(5).all()

    return render_template('teacher/dashboard.html', 
                           students_count=students_count,
                           centers_count=centers_count,
                           inventory_count=inventory_count,
                           tips_count=tips_count,
                           activities_count=activities_count,
                           recent_activities=recent_activities,
                           recent_tips=recent_tips,
                           center_name=center_name)

# Student Management
@teacher_bp.route('/students')
@login_required
@teacher_required
def students():
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to view students.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    # Only get students from the teacher's center
    students = Student.query.filter_by(center_id=current_user.center_id).all()
    return render_template('teacher/students.html', students=students)

@teacher_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_student():
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to add students.', 'danger')
        return redirect(url_for('teacher.dashboard'))

    form = StudentForm()

    # Only allow teacher to add students to their own center
    center = Center.query.get(current_user.center_id)
    form.center_id.choices = [(center.id, center.name)]

    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            age=form.age.data,
            gender=form.gender.data,
            parent_name=form.parent_name.data,
            parent_contact=form.parent_contact.data,
            address=form.address.data,
            center_id=form.center_id.data,
            enrollment_date=datetime.utcnow().date()
        )

        db.session.add(student)
        db.session.commit()

        flash('Student added successfully!', 'success')
        return redirect(url_for('teacher.students'))

    return render_template('teacher/students.html', form=form, is_add=True)

@teacher_bp.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_student(id):
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to edit students.', 'danger')
        return redirect(url_for('teacher.dashboard'))

    student = Student.query.get_or_404(id)

    # Verify student belongs to teacher's center
    if student.center_id != current_user.center_id:
        flash('You can only edit students from your own center.', 'danger')
        return redirect(url_for('teacher.students'))

    form = StudentForm()

    # Only allow teacher to assign students to their own center
    center = Center.query.get(current_user.center_id)
    form.center_id.choices = [(center.id, center.name)]

    if form.validate_on_submit():
        student.name = form.name.data
        student.age = form.age.data
        student.gender = form.gender.data
        student.parent_name = form.parent_name.data
        student.parent_contact = form.parent_contact.data
        student.address = form.address.data
        student.center_id = form.center_id.data

        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('teacher.students'))

    elif request.method == 'GET':
        form.name.data = student.name
        form.age.data = student.age
        form.gender.data = student.gender
        form.parent_name.data = student.parent_name
        form.parent_contact.data = student.parent_contact
        form.address.data = student.address
        form.center_id.data = student.center_id

    return render_template('teacher/students.html', form=form, student=student, is_edit=True)

@teacher_bp.route('/students/delete/<int:id>', methods=['POST'])
@login_required
@teacher_required
def delete_student(id):
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to delete students.', 'danger')
        return redirect(url_for('teacher.dashboard'))

    student = Student.query.get_or_404(id)

    # Verify student belongs to teacher's center
    if student.center_id != current_user.center_id:
        flash('You can only delete students from your own center.', 'danger')
        return redirect(url_for('teacher.students'))

    # Check if student has attendance records
    if student.attendance_records:
        flash('Cannot delete student with attendance records!', 'danger')
        return redirect(url_for('teacher.students'))

    db.session.delete(student)
    db.session.commit()

    flash('Student deleted successfully!', 'success')
    return redirect(url_for('teacher.students'))

# Attendance Management
@teacher_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
@teacher_required
def attendance():
    form = AttendanceForm()
    students = []
    date = datetime.utcnow().date()

    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to mark attendance.', 'danger')
        return redirect(url_for('teacher.dashboard'))

    if form.validate_on_submit():
        date = form.date.data
        # Only get students from the teacher's center
        students = Student.query.filter_by(center_id=current_user.center_id).all()

        # Check if attendance is already marked for this date for the teacher's center
        student_ids = [student.id for student in students]
        if student_ids:  # Only check if there are students
            existing_attendance = Attendance.query.filter(
                Attendance.date == date,
                Attendance.student_id.in_(student_ids)
            ).first()

            if existing_attendance:
                flash(f'Attendance for {date.strftime("%Y-%m-%d")} has already been marked!', 'info')

    elif request.method == 'GET':
        form.date.data = date

    return render_template('teacher/attendance.html', form=form, students=students, date=date)

@teacher_bp.route('/mark-attendance', methods=['POST'])
@login_required
@teacher_required
def mark_attendance():
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to mark attendance.', 'danger')
        return redirect(url_for('teacher.dashboard'))

    date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    student_ids = request.form.getlist('student_id')
    statuses = request.form.getlist('status')
    remarks_list = request.form.getlist('remarks')

    # Get all students from teacher's center
    center_students = Student.query.filter_by(center_id=current_user.center_id).all()
    center_student_ids = [str(student.id) for student in center_students]

    # Validate that all student_ids belong to teacher's center
    for student_id in student_ids:
        if student_id not in center_student_ids:
            flash('Unauthorized attempt to mark attendance for students outside your center!', 'danger')
            return redirect(url_for('teacher.attendance'))

    # Delete existing attendance for this date and only for students in teacher's center
    Attendance.query.filter(
        Attendance.date == date,
        Attendance.student_id.in_(center_student_ids)
    ).delete(synchronize_session=False)

    # Add new attendance records
    for i in range(len(student_ids)):
        attendance = Attendance(
            student_id=student_ids[i],
            date=date,
            status=statuses[i],
            remarks=remarks_list[i] if i < len(remarks_list) else None,
            marked_by=current_user.id
        )
        db.session.add(attendance)

    db.session.commit()
    flash('Attendance marked successfully!', 'success')
    return redirect(url_for('teacher.attendance'))

# Inventory Management
@teacher_bp.route('/inventory')
@login_required
@teacher_required
def inventory():
    inventory_items = Inventory.query.all()
    return render_template('teacher/inventory.html', inventory_items=inventory_items)

@teacher_bp.route('/inventory/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_inventory():
    form = InventoryForm()

    # Populate center choices
    form.center_id.choices = [(c.id, c.name) for c in Center.query.all()]

    if form.validate_on_submit():
        inventory = Inventory(
            item_name=form.item_name.data,
            quantity=form.quantity.data,
            unit=form.unit.data,
            description=form.description.data,
            center_id=form.center_id.data
        )

        db.session.add(inventory)
        db.session.commit()

        flash('Inventory item added successfully!', 'success')
        return redirect(url_for('teacher.inventory'))

    return render_template('teacher/inventory.html', form=form, is_add=True)

@teacher_bp.route('/inventory/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_inventory(id):
    inventory = Inventory.query.get_or_404(id)
    form = InventoryForm()

    # Populate center choices
    form.center_id.choices = [(c.id, c.name) for c in Center.query.all()]

    if form.validate_on_submit():
        inventory.item_name = form.item_name.data
        inventory.quantity = form.quantity.data
        inventory.unit = form.unit.data
        inventory.description = form.description.data
        inventory.center_id = form.center_id.data
        inventory.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Inventory item updated successfully!', 'success')
        return redirect(url_for('teacher.inventory'))

    elif request.method == 'GET':
        form.item_name.data = inventory.item_name
        form.quantity.data = inventory.quantity
        form.unit.data = inventory.unit
        form.description.data = inventory.description
        form.center_id.data = inventory.center_id

    return render_template('teacher/inventory.html', form=form, inventory=inventory, is_edit=True)

@teacher_bp.route('/inventory-request', methods=['GET', 'POST'])
@login_required
@teacher_required
def request_inventory():
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to request inventory items.', 'danger')
        return redirect(url_for('teacher.dashboard'))
    
    form = InventoryRequestForm()
    
    # Set the center_id field to the teacher's center only
    center = Center.query.get(current_user.center_id)
    if center:
        form.center_id.choices = [(center.id, center.name)]
    else:
        form.center_id.choices = []
    
    if form.validate_on_submit():
        try:
            # Set center_id directly from current_user
            inventory_request = InventoryRequest(
                item_name=form.item_name.data,
                quantity=form.quantity.data,
                unit=form.unit.data,
                description=form.description.data,
                center_id=current_user.center_id,  # Use teacher's center directly
                user_id=current_user.id,
                status='pending'
            )
            
            db.session.add(inventory_request)
            db.session.commit()
            
            # Update pending_requests_count in admin dashboard
            pending_requests_count = InventoryRequest.query.filter_by(status='pending').count()
            print(f"Created inventory request: {inventory_request.id}, {inventory_request.item_name}, User: {inventory_request.user_id}, Center: {inventory_request.center_id}")
            print(f"Current pending requests: {pending_requests_count}")
            
            flash('Inventory request submitted successfully! It will be reviewed by an admin.', 'success')
            return redirect(url_for('teacher.inventory'))
        except Exception as e:
            db.session.rollback()
            print(f"Error creating inventory request: {str(e)}")
            flash(f'Error submitting request: {str(e)}', 'danger')
            
    return render_template('teacher/inventory_request.html', form=form)

# Nutrition Tips Management
@teacher_bp.route('/nutrition')
@login_required
@teacher_required
def nutrition():
    nutrition_tips = NutritionTip.query.all()
    return render_template('teacher/nutrition.html', nutrition_tips=nutrition_tips)

@teacher_bp.route('/nutrition/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_nutrition():
    form = NutritionTipForm()

    if form.validate_on_submit():
        nutrition_tip = NutritionTip(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            user_id=current_user.id
        )

        db.session.add(nutrition_tip)
        db.session.commit()

        flash('Nutrition tip added successfully!', 'success')
        return redirect(url_for('teacher.nutrition'))

    return render_template('teacher/nutrition.html', form=form, is_add=True)

@teacher_bp.route('/nutrition/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_nutrition(id):
    nutrition_tip = NutritionTip.query.get_or_404(id)

    # Only allow editing tips created by the current user
    if nutrition_tip.user_id != current_user.id:
        flash('You can only edit nutrition tips that you created!', 'danger')
        return redirect(url_for('teacher.nutrition'))

    form = NutritionTipForm()

    if form.validate_on_submit():
        nutrition_tip.title = form.title.data
        nutrition_tip.content = form.content.data
        nutrition_tip.is_active = form.is_active.data
        nutrition_tip.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Nutrition tip updated successfully!', 'success')
        return redirect(url_for('teacher.nutrition'))

    elif request.method == 'GET':
        form.title.data = nutrition_tip.title
        form.content.data = nutrition_tip.content
        form.is_active.data = nutrition_tip.is_active

    return render_template('teacher/nutrition.html', form=form, nutrition_tip=nutrition_tip, is_edit=True)

# Activities Management
@teacher_bp.route('/activities')
@login_required
@teacher_required
def activities():
    activities = Activity.query.all()
    return render_template('teacher/activities.html', activities=activities)

@teacher_bp.route('/activities/add', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_activity():
    form = ActivityForm()

    if form.validate_on_submit():
        activity = Activity(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            is_active=form.is_active.data,
            user_id=current_user.id
        )

        db.session.add(activity)
        db.session.commit()

        flash('Activity added successfully!', 'success')
        return redirect(url_for('teacher.activities'))

    return render_template('teacher/activities.html', form=form, is_add=True)

@teacher_bp.route('/activities/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@teacher_required
def edit_activity(id):
    activity = Activity.query.get_or_404(id)

    # Only allow editing activities created by the current user
    if activity.user_id != current_user.id:
        flash('You can only edit activities that you created!', 'danger')
        return redirect(url_for('teacher.activities'))

    form = ActivityForm()

    if form.validate_on_submit():
        activity.title = form.title.data
        activity.description = form.description.data
        activity.date = form.date.data
        activity.is_active = form.is_active.data
        activity.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Activity updated successfully!', 'success')
        return redirect(url_for('teacher.activities'))

    elif request.method == 'GET':
        form.title.data = activity.title
        form.description.data = activity.description
        form.date.data = activity.date
        form.is_active.data = activity.is_active

    return render_template('teacher/activities.html', form=form, activity=activity, is_edit=True)

# Search functionality
@teacher_bp.route('/search')
@login_required
@teacher_required
def search():
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to search students.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    query = request.args.get('query', '')
    if not query or len(query) < 3:
        return render_template('teacher/search.html', results=None, query=query)

    # Search for students only from teacher's center
    students = Student.query.filter(
        Student.center_id == current_user.center_id,
        or_(
            Student.name.ilike(f'%{query}%'),
            Student.aadhar_number.ilike(f'%{query}%')
        )
    ).all()

    return render_template('teacher/search.html', results=students, query=query)

@teacher_bp.route('/search/student/<int:id>')
@login_required
@teacher_required
def search_student_details(id):
    # Check if teacher has an assigned center
    if not current_user.center_id:
        flash('You need to be assigned to a center to view student details.', 'warning')
        return redirect(url_for('teacher.dashboard'))

    student = Student.query.get_or_404(id)

    # Verify student belongs to teacher's center
    if student.center_id != current_user.center_id:
        flash('You can only view details for students from your own center.', 'danger')
        return redirect(url_for('teacher.search'))

    # Get attendance records for this student
    attendance_records = Attendance.query.filter_by(
        student_id=student.id
    ).order_by(Attendance.date.desc()).all()

    return render_template('teacher/student_details.html', student=student, attendance_records=attendance_records)

# API routes for search suggestions
@teacher_bp.route('/api/teacher/search-suggestions')
@login_required
@teacher_required
def search_suggestions_api():
    query = request.args.get('query', '')
    if not query or len(query) < 3:
        return jsonify([])

    # Get teacher's center
    teacher_center_id = User.query.get(current_user.id).center_id

    # Search students from teacher's center only (limit 8)
    students = Student.query.filter(
        Student.center_id == teacher_center_id,
        or_(
            Student.name.ilike(f'%{query}%'),
            Student.aadhar_number.ilike(f'%{query}%')
        )
    ).limit(8).all()

    suggestions = []
    for student in students:
        suggestions.append({
            'id': student.id,
            'name': student.name,
            'type': 'student',
            'age': student.age
        })

    return jsonify(suggestions)