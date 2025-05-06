from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import NutritionTip, Activity, Complaint
from app import db
from datetime import datetime
from forms import ComplaintForm

# Create the blueprint
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Get limited nutrition tips and activities for home page
    nutrition_tips = NutritionTip.query.order_by(NutritionTip.created_at.desc()).all()
    activities = Activity.query.order_by(Activity.created_at.desc()).all()

    # Get total counts for "show more" button logic
    total_nutrition_tips = NutritionTip.query.count()
    total_activities = Activity.query.count()

    return render_template('home/index.html', 
                          nutrition_tips=nutrition_tips, 
                          activities=activities, 
                          total_nutrition_tips=total_nutrition_tips,
                          total_activities=total_activities,
                          page=1, 
                          has_more=True)

@home_bp.route('/about')
def about():
    return render_template('home/about.html')

@home_bp.route('/api/nutrition-tips/<int:id>')
def get_nutrition_tip(id):
    tip = NutritionTip.query.get_or_404(id)
    return jsonify({
        'id': tip.id,
        'title': tip.title,
        'content': tip.content,
        'date': tip.created_at.strftime('%d %b, %Y'),
        'author': tip.user_id
    })

@home_bp.route('/api/activities/<int:id>')
def get_activity(id):
    activity = Activity.query.get_or_404(id)
    return jsonify({
        'id': activity.id,
        'title': activity.title,
        'description': activity.description,
        'date': activity.date.strftime('%d %b, %Y')
    })

@home_bp.route('/nutrition-tips/<int:page>')
def load_more_nutrition_tips(page):
    per_page = 3
    offset = (page - 1) * per_page + 6  # Skip the first 6 items that are shown initially

    nutrition_tips = NutritionTip.query.order_by(NutritionTip.created_at.desc()).offset(offset).limit(per_page).all()

    # Check if there are more items to load
    total_count = NutritionTip.query.count()
    has_more = (offset + per_page) < total_count

    return render_template('home/_nutrition_tips_partial.html', nutrition_tips=nutrition_tips, page=page+1, has_more=has_more)

@home_bp.route('/activities/<int:page>')
def load_more_activities(page):
    per_page = 3
    offset = (page - 1) * per_page + 6  # Skip the first 6 items that are shown initially

    activities = Activity.query.order_by(Activity.created_at.desc()).offset(offset).limit(per_page).all()

    # Check if there are more items to load
    total_count = Activity.query.count()
    has_more = (offset + per_page) < total_count

    return render_template('home/_activities_partial.html', activities=activities, page=page+1, has_more=has_more)

@home_bp.route('/nutrition-tip/<int:id>')
def nutrition_tip_detail(id):
    tip = NutritionTip.query.get_or_404(id)
    return render_template('home/nutrition_tip_detail.html', tip=tip)

@home_bp.route('/activity/<int:id>')
def activity_detail(id):
    activity = Activity.query.get_or_404(id)
    return render_template('home/activity_detail.html', activity=activity)

@home_bp.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not all([name, email, subject, message]):
        flash('All fields are required', 'danger')
        return redirect(url_for('home.index'))

    # Send an email using Flask-Mail
    try:
        from app import mail
        from flask_mail import Message
        
        # Create email message
        msg = Message(
            subject=f"Aaganshiksha Complaint/Feedback: {subject}",
            recipients=["vibhorkashyap1907@gmail.com"],
            body=f"""
            New contact form submission:

            Name: {name}
            Email: {email}
            Subject: {subject}
            Message: 
            {message}

            Submitted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """,
            sender=("Aaganshiksha Portal", email)
        )
        
        # Send email
        mail.send(msg)
        flash('Your message has been sent successfully!', 'success')
    except Exception as e:
        flash(f'There was an error sending your message. Please try again later.', 'danger')
        print(f"Email error: {str(e)}")  # Log the error

    return redirect(url_for('home.index'))