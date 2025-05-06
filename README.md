
# AaganshikshaPortal Project

A web portal for managing Anganwadi centers, students, teachers, and activities.

## Requirements

- Python 3.11 or higher
- PostgreSQL database

## Dependencies

```bash
email-validator==2.2.0
flask==3.1.0
flask-login==0.6.3
flask-mail==0.10.0
flask-sqlalchemy==3.1.1
flask-wtf==1.2.2
gunicorn==23.0.0
psycopg2-binary==2.9.10
reportlab==4.4.0
sqlalchemy==2.0.40
werkzeug==3.1.3
wtforms==3.2.1
pillow==11.2.1
```

## Setup Instructions

1. Install required dependencies:
```bash
pip install email-validator flask-login flask-sqlalchemy gunicorn psycopg2-binary flask-wtf reportlab flask-mail werkzeug wtforms pillow
```

2. Initialize the database (Optional - adds sample data):
```bash
python reset_db.py
python add_dummy_centers.py
python add_dummy_teachers.py
python add_dummy_students.py
python add_dummy_attendance.py
python add_activities.py
python add_nutrition_tips.py
```

3. Run the project:

Development mode:
```bash
python main.py
```

Production mode:
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Features

- User authentication (Admin, Teacher roles)
- Center management
- Student attendance tracking
- Activity planning
- Inventory management
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

## Access

The application will be accessible at http://0.0.0.0:5000

Default login:
- Admin: Create using the database initialization scripts
- Teachers: Added through admin interface
