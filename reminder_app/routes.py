from reminder_app import app,bcrypt,db,mail
from reminder_app.forms import LoginForm,RegistrationForm,NewReminder,EmailVerification
from flask import render_template,redirect,url_for,abort,flash,request,session
from flask_login import login_user,login_required,current_user,logout_user
from reminder_app.models import User,Reminder
from datetime import datetime
import random
from flask_mail import Message
import os,time

@app.route('/home',methods=['POST','GET'])
@login_required
def home():
    reminders = Reminder.query.filter_by(user_id=current_user.id)
    return render_template('home.html',reminders=reminders)

@app.route('/<string:username>/new_reminder',methods=['POST','GET'])
@login_required
def new_reminder(username):
    if username!=current_user.username:
        return abort(403)
    form = NewReminder()
    if form.validate_on_submit():
        reminder = Reminder(title=form.title.data,message=form.message.data,time=form.time.data,date=form.date.data,author=current_user)
        db.session.add(reminder)
        db.session.commit()
        return redirect(url_for('home',username=current_user.username))
    return render_template('new_reminder.html',form=form)
        
@app.route('/login',methods=['POST','GET'])
def login():
    if current_user.is_authenticated==True:
        return redirect(url_for('home',username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password,form.password.data):
                login_user(user,remember=form.remember_me.data)
                flash('You Have Logged In Successfully','success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('home',username=user.username))
            else:
                flash('Incorrect Password or Username','danger')
        else:
            flash('Incorrect Username','danger')
    return render_template('login.html',form=form)                           

@app.route('/register',methods=['POST','GET'])
def register():
    if current_user.is_authenticated==True:
        return redirect(url_for('home',username=current_user.username))
    form = RegistrationForm()
    form2 = EmailVerification()
    if form.validate_on_submit():
        session['otp'] = random.randrange(1000,9999)
        with mail.connect() as conn:
            message = f'OTP for creating an account with email id {form.email.data}is {session["otp"]}.'
            subject = 'Email Verification'
            msg = Message(sender=os.environ.get('email_address'),recipients=[form.email.data],body=message,subject=subject)
            conn.send(msg)
        session['email'] = form.email.data
        session['username'] = form.username.data
        session['password'] = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        session['phone_number'] = form.phone_number.data
    if form2.validate_on_submit() and session['otp']==form2.otp.data:
        user = User(email=session['email'],username=session['username'],password=session['password'],phone_number=session['phone_number'])
        db.session.add(user)
        db.session.commit()
        session.pop('otp')
        return redirect(url_for('login'))
    elif form2.validate_on_submit():
        flash('Otp is not Correct','warning')
    return render_template('register.html',form=form,form2=form2)

@app.route('/logout')
def logout():
    if current_user.is_authenticated== True:
        logout_user()
        return redirect(url_for('login'))
    
