import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

from movieforum import app, db
from movieforum.models import User, Post

def drop_nonconfirmed():
    users = User.query.filter_by(confirmed=False).all()
    for user in users:
        if datetime.utcnow() - user.date_created >  timedelta(minutes=60):
            db.session.delete(user)
            db.session.commit()

if __name__ == '__main__':
    # db.session.query(User).delete()
    # db.session.commit()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=drop_nonconfirmed, trigger="interval", seconds=3600)
    scheduler.start()

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
    
    app.run(debug=True)