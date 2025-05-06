from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, DateField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ComplaintForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Complaint')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('teacher', 'Teacher')])
    aadhar_number = StringField('Aadhar Number', validators=[DataRequired(), Length(min=12, max=12)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    center_id = SelectField('Center (required for teachers)', coerce=int, validators=[Optional()])
    submit = SubmitField('Save User')
    
    def validate_aadhar_number(self, aadhar_number):
        if not aadhar_number.data.isdigit():
            raise ValidationError('Aadhar number must contain only digits')
        if len(aadhar_number.data) != 12:
            raise ValidationError('Aadhar number must be exactly 12 digits')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different one.')

class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('teacher', 'Teacher')])
    aadhar_number = StringField('Aadhar Number', validators=[DataRequired(), Length(min=12, max=12)])
    phone_number = StringField('Phone Number', validators=[Optional(), Length(max=15)])
    address = StringField('Address', validators=[Optional(), Length(max=200)])
    center_id = SelectField('Center (required for teachers)', coerce=int, validators=[Optional()])
    password = PasswordField('New Password (leave blank to keep current)', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[EqualTo('password')])
    submit = SubmitField('Update User')
    
    def validate_aadhar_number(self, aadhar_number):
        if not aadhar_number.data.isdigit():
            raise ValidationError('Aadhar number must contain only digits')
        if len(aadhar_number.data) != 12:
            raise ValidationError('Aadhar number must be exactly 12 digits')
    
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered. Please use a different one.')

class CenterForm(FlaskForm):
    name = StringField('Center Name', validators=[DataRequired(), Length(min=3, max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    contact_number = StringField('Contact Number', validators=[Length(max=15)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField('Save Center')

class StudentForm(FlaskForm):
    name = StringField('Student Name', validators=[DataRequired(), Length(min=2, max=100)])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    parent_name = StringField('Parent Name', validators=[DataRequired(), Length(min=2, max=100)])
    parent_contact = StringField('Parent Contact', validators=[DataRequired(), Length(max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5, max=200)])
    aadhar_number = StringField('Aadhar Number', validators=[DataRequired(), Length(min=12, max=12)])
    center_id = SelectField('Center', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Student')
    
    def validate_aadhar_number(self, aadhar_number):
        if not aadhar_number.data.isdigit():
            raise ValidationError('Aadhar number must contain only digits')
        if len(aadhar_number.data) != 12:
            raise ValidationError('Aadhar number must be exactly 12 digits')

class InventoryForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=100)])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional()])
    center_id = SelectField('Center', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Inventory Item')

class NutritionTipForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    is_active = BooleanField('Active')
    submit = SubmitField('Save Nutrition Tip')

class ActivityForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    is_active = BooleanField('Active')
    submit = SubmitField('Save Activity')

class AttendanceForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Load Students')

class StudentAttendanceForm(FlaskForm):
    student_id = HiddenField('Student ID', validators=[DataRequired()])
    status = SelectField('Status', choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])
    remarks = StringField('Remarks')

class ReportForm(FlaskForm):
    report_type = SelectField('Report Type', choices=[
        ('attendance', 'Attendance Report'),
        ('students', 'Students Report'),
        ('inventory', 'Inventory Report'),
        ('activities', 'Activities Report')
    ], validators=[DataRequired()])
    center_id = SelectField('Center', coerce=int)
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[Optional()])
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Generate Report')

class InventoryRequestForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=2, max=100)])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit = StringField('Unit', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional()])
    center_id = SelectField('Center', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit Request')
