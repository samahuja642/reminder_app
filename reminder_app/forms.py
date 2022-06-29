from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField,TextAreaField,DateField,TimeField,IntegerField
from wtforms.validators import Email,DataRequired,Length,EqualTo,ValidationError
from reminder_app.models import User
import datetime
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user

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
    def validate_email(self,email):
        if User.query.filter_by(email=email.data).first() != None:
            raise ValidationError('Email Already Taken')
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first() != None:
            raise ValidationError('Username Already Taken')
    def validate_phone_number(self,phone_number):
        if User.query.filter_by(phone_number=phone_number.data).first() != None:
            raise ValidationError('Phone Number Already Taken')


class NewReminder(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    message = TextAreaField('Reminder',validators=[DataRequired()])
    date = DateField('Date',validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',validators=[DataRequired()],format='%H:%M')
    submit = SubmitField('Set Reminder')

    def validate_date(self,date):
        if datetime.datetime.now().date() > date.data:
            raise ValidationError("You can't set date back in time")
    def validate_time(self,time):
        if datetime.datetime.now().date() == self.date.data:
            if (datetime.datetime.now() + datetime.timedelta(minutes=30)).time() > time.data:
                raise ValidationError("You can set atleast after 30 min from now")

class EmailVerification(FlaskForm):
    otp = IntegerField('OTP :',validators=[DataRequired()])
    submit = SubmitField('Verify Email')

class AccountUpdationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=2)])
    phone_number = StringField('Phone Number (with country code)',validators=[DataRequired(),Length(min=2)])
    image = FileField('Profile Photo',validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Submit')
    def validate_username(self,username):
        if User.query.filter_by(username=username.data).first():
            if current_user.username != username.data:
                raise ValidationError('Username Already Taken')
    def validate_phone_number(self,phone_number):
        if User.query.filter_by(phone_number=phone_number.data).first() != None:
            if current_user.phone_number != phone_number.data:
                raise ValidationError('Phone Number Already Taken')

class ReminderUpdationForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    message = TextAreaField('Reminder',validators=[DataRequired()])
    date = DateField('Date',validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',validators=[DataRequired()],format='%H:%M')
    submit = SubmitField('Update Reminder')

    def validate_date(self,date):
        if datetime.datetime.now().date() > date.data:
            raise ValidationError("You can't set date back in time")
    def validate_time(self,time):
        if datetime.datetime.now().date() == self.date.data:
            if (datetime.datetime.now() + datetime.timedelta(minutes=30)).time() > time.data:
                raise ValidationError("You can set atleast after 30 min from now")
