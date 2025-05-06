from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm
from app import db
from werkzeug.security import check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        elif current_user.role == 'teacher':
            return redirect(url_for('teacher.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        selected_role = request.form.get('selected_role', 'admin')
        
        # Check if user exists and password is correct
        if user and user.check_password(form.password.data):
            # Check if user has the selected role
            if user.role == selected_role:
                # Log in user
                login_user(user, remember=form.remember.data)
                
                # Store user role in session
                session['user_role'] = user.role
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect(url_for('admin.dashboard'))
                elif user.role == 'teacher':
                    return redirect(url_for('teacher.dashboard'))
            else:
                flash(f'This account does not have {selected_role} privileges. Please select the correct role.', 'warning')
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_role', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home.index'))

@auth_bp.route('/initialize')
def initialize():
    """Route to initialize admin user if no users exist"""
    if User.query.first() is None:
        admin = User(
            username='admin',
            email='admin@aaganshiksha.org',
            role='admin'
        )
        admin.set_password('admin123')
        
        teacher = User(
            username='teacher',
            email='teacher@aaganshiksha.org',
            role='teacher'
        )
        teacher.set_password('teacher123')
        
        db.session.add(admin)
        db.session.add(teacher)
        db.session.commit()
        
        flash('Default admin and teacher accounts have been created.', 'success')
        return redirect(url_for('auth.login'))
    else:
        flash('Users already exist in the database.', 'info')
        return redirect(url_for('home.index'))
