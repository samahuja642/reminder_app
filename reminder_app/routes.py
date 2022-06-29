from reminder_app import app,bcrypt,db,mail
from reminder_app.forms import LoginForm,RegistrationForm,NewReminder,EmailVerification,AccountUpdationForm,ReminderUpdationForm
from flask import render_template,redirect,url_for,abort,flash,request,session
from flask_login import login_user,login_required,current_user,logout_user
from reminder_app.models import User,Reminder
from datetime import datetime
import random
from flask_mail import Message
import os,time,secrets
from PIL import Image

def image_saver(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics/',picture_fn)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/home',methods=['POST','GET'])
@login_required
def home():
    reminders = Reminder.query.filter_by(user_id=current_user.id)
    return render_template('home.html',reminders=reminders)

@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/settings',methods=['POST','GET'])
@login_required
def settings():
    form = AccountUpdationForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.phone_number = form.phone_number.data
        if form.image.data:
            print("samarth")
            current_user.image_file = image_saver(form.image.data)
        db.session.commit()
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.phone_number.data = current_user.phone_number
    return render_template('settings.html',form=form)
    

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

@app.route('/reminder/<string:id>')
@login_required
def show_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if current_user != reminder.author:
        return abort(403)
    return render_template("reminder.html",reminder=reminder)
    
@app.route('/update/<string:id>',methods=['POST','GET'])
@login_required
def update_reminder(id):
    form = ReminderUpdationForm()
    reminder = Reminder.query.get_or_404(id)
    if current_user != reminder.author:
        return abort(403)
    if form.validate_on_submit():
        reminder.title = form.title.data
        reminder.message = form.message.data
        reminder.date = form.date.data
        reminder.time = form.time.data
        db.session.commit()
        flash('Your Reminder has been Updated','success')
        return redirect(url_for('update_reminder',id=id))
    elif request.method == 'GET':
        form.title.data = reminder.title
        form.message.data = reminder.message
        form.date.data = reminder.date
        form.time.data = reminder.time
    return render_template('update_reminder.html',form=form)


@app.route('/delete/<string:id>',methods=['POST'])
@login_required
def delete_reminder(id):
    reminder = Reminder.query.get_or_404(id)
    if current_user != reminder.author:
        abort(403)
    db.session.delete(reminder)
    db.session.commit()
    flash('Your Reminder Has Been Delete!','success')
    return redirect(url_for('home'))
