from flask import Flask, render_template, request, flash, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from config import Config
from datetime import datetime


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)
loginManager = LoginManager(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
    volume = db.Column(db.Integer)

    histories = db.relationship('History', backref='user')

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return password == self.password

    def __repr__(self):
        return '<User {}>'.format(self.username)


class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, index=True, default=datetime.now())
    weight = db.Column(db.Integer)
    set = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weights = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<History {}>'.format(self.id)

import core

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    age = PasswordField('Age', validators=[DataRequired()])
    weight = PasswordField('Weight', validators=[DataRequired()])
    height = PasswordField('Height', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/personal.png')
def main_plot():
    """The view for rendering the scatter chart"""
    img = core.get_image()
    return send_file(img, mimetype='image/png', cache_timeout=0)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user', username=current_user.username))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, age=form.age.data, weight=form.weight.data,
                    height=form.height.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@loginManager.user_loader
def load_user(id):
    return User.query.get(int(id))


@loginManager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')


if __name__ == '__main__':
    app.run()
