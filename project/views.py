#import sqlite3
from project import db,app
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask import flash, render_template, url_for, session, redirect, request, g
#from flask.ext.sqlalchemy import SQLAlchemy
from project.models import Task,User
from sqlalchemy.exc import IntegrityError



#configurations and initializing flask app to an object="app" app.config is what finds CAPs  and __name__ tells the app its same as name of app
#app = Flask(__name__)
#app.config.from_object('_config')
#db = SQLAlchemy(app)

#helper function which connects to db using 'g'
#def connect_db():
	#return sqlite3.connect(app.config['DATABASE_PATH'])

# decorator function to check if user logged in or not
def open_tasks():
	return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
def closed_tasks():
	return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash("You need to login first")
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in',None)
	session.pop('user_id',None)
	session.pop('role', None)
	flash("GoodBye")
	return redirect(url_for('login'))
@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			user =User.query.filter_by(name=request.form['name']).first()
			if user is not None and user.password == request.form['password']:
				session['logged_in'] = True
				session['user_id'] = user.id
				session['role'] = user.role
				flash('Welcome!')
				return redirect(url_for('tasks'))
			else:
				error = 'Invalid username or password.'
		else:
				error = 'Both fields are required.'
	return render_template('login.html', form=form, error=error)
@app.route('/tasks/')
@login_required
def tasks():
	#open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
	#closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
	return render_template('tasks.html',form=AddTaskForm(request.form),open_tasks=open_tasks(),closed_tasks=closed_tasks())

@app.route('/add', methods=['POST'])
@login_required
def add():
	"""g.db = connect_db()
	name = request.form['name']
	due_date = request.form['due_date']
	priority = request.form['priority']
	if not name or not due_date or not priority:
		flash("Please fill all the fields")
		return redirect(url_for('tasks'))
	else:
		#g.db.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES(?, ?, ?, 1)",[request.form['name'],request.form['due_date'],request.form['priority']])
		#g.db.commit()
		#g.db.close()
		flash("Your entry was successfully admitted")
		return redirect(url_for('tasks'))"""
	form = AddTaskForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_task = Task(form.name.data,form.due_date.data,form.priority.data,'1',session['user_id'])
			db.session.add(new_task)
			db.session.commit()
			flash('New entry was successfully posted. Thanks.')
			return redirect(url_for('tasks'))
		else:
			return render_template('tasks.html',form=form,error=error)
	return render_template('tasks.html',form=form,error=error,open_tasks=open_tasks(),closed_tasks=closed_tasks())

@app.route('/complete/<int:task_id>/')
@login_required
def complete(task_id):
	"""g.db = connect_db()
	g.db.execute("UPDATE tasks SET status=0 WHERE task_id ="+str(task_id))
	g.db.commit()
	g.db.close()
	flash("The tasks was marked as complete")
	return redirect(url_for('tasks'))"""
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id:
		task.update({"status":"0"})
		db.session.commit()
		flash('The task is complete. Nice.')
		return redirect(url_for('tasks'))
	else:
		flash('you can only upate your own tasks')
		return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>')
@login_required
def delete(task_id):
	"""g.db = connect_db()
	g.db.execute("DELETE from tasks where task_id="+str(task_id))
	g.db.commit()
	g.db.close()
	flash("Task successfully deleted")""
	return redirect(url_for('tasks'))"""
	new_id = task_id
	task = db.session.query(Task).filter_by(task_id=new_id)
	if session['user_id'] == task.first().user_id:
		task.delete()
		db.session.commit()
		flash('Task deleted successfully')
		return redirect(url_for('tasks'))
	else:
		flash("You can only delete your own task")
		return redirect(url_for('tasks'))

@app.route('/register', methods=['GET','POST'])
def register():
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(form.name.data,form.email.data,form.password.data)
			try:
					db.session.add(new_user)
					db.session.commit()
					flash('Thanks for registering. please do login')
					return redirect(url_for('login'))
			except IntegrityError:
					error = 'That username and/or email already exists'
					return render_template('register.html',error=error,form=form)
	return render_template('register.html', form=form, error=error)
def flash_error():
	for field,errors in form.errors.items():
		for error in errors:
			flash(u"error in the %s field - %s" %(getattr(form,field).label.text,error),'error')

















