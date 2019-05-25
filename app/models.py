from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import random
import string


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    urls = db.relationship('Url', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_link = db.Column(db.String(140))
    short_link = db.Column(db.String(40), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    r_count = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'https://s-link.herokuapp.com/{}'.format(self.short_link)

    # функция генерации short_link
    def create_short_link(self, url_link):
        while True:
            short_link = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits)
                                 for _ in range(random.randrange(5, 8)))
            if Url.query.filter_by(short_link=short_link).first() is None:
                self.short_link = short_link
                break
