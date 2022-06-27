from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_session import Session
from flask_apscheduler import APScheduler
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('sec_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('email_address')
app.config['MAIL_PASSWORD'] = os.environ.get('email_password')
# app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'sqlalchemy'
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = "strong"
login_manager.login_message_category = 'info'
login_manager.init_app(app)
db = SQLAlchemy(app)
app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
scheduler = APScheduler()
scheduler.init_app(app)
from reminder_app import routes
