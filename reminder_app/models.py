from flask_login import UserMixin
from reminder_app import db,login_manager,app
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable=False)
    username = db.Column(db.String(50),unique=True,nullable=False)
    image_file = db.Column(db.String(1000),nullable=False,default="default.jpg")
    password = db.Column(db.String(50),nullable=False)
    reminders = db.relationship('Reminder',backref='author',lazy=True)
    phone_number = db.Column(db.String(15),unique=True,nullable=False)
    # def get_reset_token(self,expire_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'],expire_sec)
    #     return s.dumps({'user_id':self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serailzer(app.config['SECRET_KEY'].decode('utf-8')
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)
    # def __repr__(self):
    #     return f'Username {self.username} ID {self.id}'

class Reminder(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    message = db.Column(db.Text,nullable=False)
    date = db.Column(db.Date,nullable=False)
    time = db.Column(db.Time,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f'ID {self.user_id} Title {self.title}'


class ActiveReminder(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(150),nullable=False)
    message = db.Column(db.Text,nullable=False)
    time = db.Column(db.DateTime,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f'ID {self.user_id} Title {self.title}'    
