from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Student, Attendance, Center
from forms import AttendanceForm
from app import db
from datetime import datetime, timedelta
from functools import wraps

attendance_bp = Blueprint('attendance', __name__)

def authorized_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['admin', 'teacher']:
            flash('You need to be an admin or teacher to access this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@attendance_bp.route('/')
@login_required
@authorized_user
def index():
    form = AttendanceForm()
    
    # Default to today's date
    today = datetime.utcnow().date()
    form.date.data = today
    
    # Get week offset from query parameters (for previous and next week navigation)
    week_offset = request.args.get('week_offset', 0)
    try:
        week_offset = int(week_offset)
    except ValueError:
        week_offset = 0
    
    # Calculate start and end of the week based on offset
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=week_offset)
    end_of_week = start_of_week + timedelta(days=6)
    
    # Get list of centers
    centers = Center.query.all()
    
    # Prepare data for attendance report
    center_data = []
    for center in centers:
        students = Student.query.filter_by(center_id=center.id).all()
        attendance_data = db.session.query(
            Attendance.date, 
            db.func.count(Attendance.id).label('total'), 
            db.func.sum(db.case((Attendance.status == 'present', 1), else_=0)).label('present')
        ).filter(
            Attendance.student_id.in_([s.id for s in students]),
            Attendance.date.between(start_of_week, end_of_week)
        ).group_by(Attendance.date).all()
        
        # Convert to a dict for easier access
        attendance_by_date = {row.date: {'total': row.total, 'present': row.present} for row in attendance_data}
        
        # Calculate totals
        total_students = len(students)
        days_data = []
        
        for i in range(7):
            current_date = start_of_week + timedelta(days=i)
            if current_date in attendance_by_date:
                present = attendance_by_date[current_date]['present'] or 0
                absent = total_students - present
                percentage = (present / total_students) * 100 if total_students > 0 else 0
            else:
                present = 0
                absent = total_students
                percentage = 0
            
            days_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day': current_date.strftime('%a'),
                'present': present,
                'absent': absent,
                'percentage': round(percentage, 1)
            })
        
        center_data.append({
            'center': center,
            'total_students': total_students,
            'days': days_data
        })
    
    # Calculate previous and next week offsets
    prev_week_offset = week_offset - 1
    next_week_offset = week_offset + 1
    
    return render_template('attendance/index.html', 
                          form=form, 
                          centers=centers,
                          center_data=center_data,
                          start_date=start_of_week.strftime('%Y-%m-%d'),
                          end_date=end_of_week.strftime('%Y-%m-%d'),
                          prev_week_offset=prev_week_offset,
                          next_week_offset=next_week_offset,
                          week_offset=week_offset)

@attendance_bp.route('/view/<int:center_id>/<date>')
@login_required
@authorized_user
def view_attendance(center_id, date):
    # Convert string date to datetime
    attendance_date = datetime.strptime(date, '%Y-%m-%d').date()
    
    # Get center
    center = Center.query.get_or_404(center_id)
    
    # Get students for this center
    students = Student.query.filter_by(center_id=center_id).all()
    
    # Get attendance for these students on this date
    attendance_records = {}
    for record in Attendance.query.filter_by(date=attendance_date).all():
        attendance_records[record.student_id] = record
    
    # Prepare data for display
    attendance_data = []
    for student in students:
        if student.id in attendance_records:
            record = attendance_records[student.id]
            status = record.status
            remarks = record.remarks
        else:
            status = 'absent'  # Default to absent if no record
            remarks = ''
        
        attendance_data.append({
            'student': student,
            'status': status,
            'remarks': remarks
        })
    
    return render_template('attendance/view.html', 
                          center=center, 
                          date=attendance_date,
                          attendance_data=attendance_data)
