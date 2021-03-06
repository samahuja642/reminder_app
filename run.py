from reminder_app import app,db,mail,scheduler
import datetime
import os
from flask_mail import Message
from reminder_app.models import Reminder,User

def mailer():
    with scheduler.app.app_context():
        d = datetime.datetime.now().date()
        t = (datetime.datetime.now() + datetime.timedelta(minutes=30)).time()
        r = Reminder.query.filter(Reminder.date == d , Reminder.time<=t).all()
        for _ in r:
            with mail.connect() as conn:
                user = User.query.filter_by(id = _.user_id).first()
                message = _.message
                subject = _.title
                msg = Message(sender=os.environ.get('email_address'),recipients=[user.email],body=message,subject=subject)
                conn.send(msg)
            if _:
                db.session.delete(_)
                db.session.commit()    
if __name__=='__main__':
    scheduler.add_job(id="mailer",func=mailer,trigger='interval',seconds=60)
    scheduler.start()
    app.run(debug=True)
