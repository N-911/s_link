from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_login import LoginManager

# Создаём приложение
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Добавляем в файл конфигурации SECRET_KEY, необходимо для нормальной работы Flask-WTF
app.config['SECRET_KEY'] = 'you-will-never-give-up'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
