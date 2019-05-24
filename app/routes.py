from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, UrlForm, RegistrationForm
from flask_login import login_required, current_user, login_user,logout_user
from app.models import User, Url
from app import db
from flask import request
from werkzeug.urls import url_parse
import pyperclip


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
# @login_required                            #no acsses for anonimous users
def index():
    form = UrlForm()
    if form.validate_on_submit():
        if form.submit.data:
            generate_short_link()
    link = Url.query.filter_by(url_link=form.url_link.data).all()
    if form.validate_on_submit():
        if form.submit2.data:
            pyperclip.copy(str(link[-1]))
    return render_template('index.html', title='Home', form=form, link=link, )


def generate_short_link():
    form = UrlForm()
    username = current_user
    if current_user.is_authenticated:
        us_link = Url(url_link=form.url_link.data, user_id=username.id)
        us_link.create_short_link(form.url_link.data)
        db.session.add(us_link)
        db.session.commit()

    else:
        us_link = Url(url_link=form.url_link.data)
        us_link.create_short_link(form.url_link.data)
        db.session.add(us_link)
        db.session.commit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    urls = Url.query.filter_by(user=current_user).all()
    return render_template('user.html', user=user, urls=urls)


# При переходе по адресу, эта функция проверяет, есть ли такой короткий адрес в БД.
# Если есть - выполняется переход по ссылке.
@app.route('/<short_link>')
def short_link_redirect(short_link):
    try:
        tmp = Url.query.filter_by(short_link=short_link).first()
        tmp.r_count += 1
        db.session.add(tmp)
        db.session.commit()
        return redirect(tmp.url_link)
    except:
        return render_template('index.html')

@app.route('/stat', methods=['GET', 'POST'])
def stat():
    urls = Url.query.all()
    return render_template('statistics.html', urls=urls)