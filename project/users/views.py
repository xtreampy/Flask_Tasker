from project import db,app,bcrypt
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask import flash, render_template, url_for, session, redirect, request,Blueprint
#from flask.ext.sqlalchemy import SQLAlchemy
from project.models import Task,User
from sqlalchemy.exc import IntegrityError


users_blueprint = Blueprint('users', __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('users.login'))
    return wrap

@users_blueprint.route('/logout/')
@login_required
def logout():
    session.pop('logged_in',None)
    session.pop('user_id',None)
    session.pop('role', None)
    session.pop('name',None)
    flash("GoodBye")
    return redirect(url_for('users.login'))

@users_blueprint.route('/', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user =User.query.filter_by(name=request.form['name']).first()
            if user is not None and bcrypt.check_password_hash( user.password, request.form['password']):
                session['logged_in'] = True
                session['user_id'] = user.id
                session['role'] = user.role
                session['name'] = user.name
                flash('Welcome!')
                return redirect(url_for('tasks.tasks'))
            else:
                error = 'Invalid username or password.'
        else:
                error = 'Both fields are required.'
    return render_template('login.html', form=form, error=error)

@users_blueprint.route('/register', methods=['GET','POST'])
def register():
    error = None
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User(form.name.data,form.email.data,bcrypt.generate_password_hash(form.password.data))
            try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Thanks for registering. please do login')
                    return redirect(url_for('users.login'))
            except IntegrityError:
                    error = 'That username and/or email already exists'
                    return render_template('register.html',error=error,form=form)
    return render_template('register.html', form=form, error=error)
