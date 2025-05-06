
# AaganshikshaPortal Project

A web portal for managing Anganwadi centers, students, teachers, and activities.

## Requirements

- Python 3.11 or higher
- PostgreSQL database (SQLite used in development mode)

## Installation & Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aaganshiksha-portal.git
cd aaganshiksha-portal
```

2. Install required dependencies:
```bash
pip install email-validator flask-login flask-sqlalchemy gunicorn psycopg2-binary flask-wtf reportlab flask-mail werkzeug wtforms pillow
```

Alternatively, install from pyproject.toml:
```bash
pip install -e .
```

3. Initialize the database:
```bash
python reset_db.py
```

4. (Optional) Add sample data:
```bash
python add_dummy_centers.py
python add_dummy_teachers.py
python add_dummy_students.py
python add_dummy_attendance.py
python add_activities.py
python add_nutrition_tips.py
```

Or run the combined script:
```bash
python generate_sample_data.py
```

5. Run the project:
```bash
python main.py
```

The application will be accessible at http://0.0.0.0:5001

## Default Login Credentials

- **Admin**:
  - Username: `admin`
  - Password: `admin123`

- **Teacher**:
  - Username: `teacher`
  - Password: `teacher123`

## Features

- User authentication (Admin, Teacher roles)
- Center management
- Student attendance tracking
- Activity planning
- Inventory management and requests
- Nutrition tips
- Complaint system
- Reports generation

## Project Structure

- `/routes` - Route handlers for different sections
- `/templates` - HTML templates 
- `/static` - Static assets (CSS, JS, images)
- `/models.py` - Database models
- `/forms.py` - Form definitions
- `/app.py` - Main application setup

## API Endpoints

### Admin Routes
- `/admin/dashboard` - Admin dashboard
- `/admin/centers` - Manage centers
- `/admin/users` - Manage users
- `/admin/inventory-requests` - View and manage inventory requests

### Teacher Routes
- `/teacher/dashboard` - Teacher dashboard
- `/teacher/students` - Manage students
- `/teacher/attendance` - Track attendance
- `/teacher/inventory-request` - Request inventory items

### Authentication
- `/auth/login` - Login page
- `/auth/logout` - Logout user
- `/auth/initialize` - Initialize default admin account
