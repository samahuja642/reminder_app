from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,DateField,TimeField,IntegerField
from wtforms.validators import Email,DataRequired,Length,EqualTo,ValidationError
from reminder_app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
        
class RegistrationForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired(),Length(min=2)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=2,max=20)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),Length(min=2,max=20),EqualTo('password',"Data should match with password's data")])
    phone_number = StringField('Phone Number (with country code)',validators=[DataRequired(),Length(min=2)])
    submit = SubmitField('Sign Up')
    def validate_email(FlaskForm,email):
        if User.query.filter_by(email=email.data).first() != None:
            raise ValidationError('Email Already Taken')
    def validate_username(FlaskForm,username):
        if User.query.filter_by(username=username.data).first() != None:
            raise ValidationError('Username Already Taken')
    def validate_phone_number(FlaskForm,phone_number):
        if User.query.filter_by(phone_number=phone_number.data).first() != None:
            raise ValidationError('Phone Number Already Taken')


class NewReminder(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    message = TextAreaField('Reminder',validators=[DataRequired()])
    date = DateField('Date',validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',validators=[DataRequired()],format='%H:%M')
    submit = SubmitField('Set Reminder')

class EmailVerification(FlaskForm):
    otp = IntegerField('OTP :',validators=[DataRequired()])
    submit = SubmitField('Verify Email')
