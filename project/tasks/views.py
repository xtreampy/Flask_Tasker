from project import db,app
from functools import wraps
from forms import AddTaskForm, RegisterForm, LoginForm
from flask import flash, render_template, url_for, session, redirect, request,Blueprint
#from flask.ext.sqlalchemy import SQLAlchemy
from project.models import Task,User
from sqlalchemy.exc import IntegrityError


tasks_blueprint = Blueprint('tasks', __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('users.login'))
    return wrap

def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

@tasks_blueprint.route('/tasks/')
@login_required
def tasks():
    #open_tasks = db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())
    #closed_tasks = db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())
    return render_template('tasks.html',form=AddTaskForm(request.form),open_tasks=open_tasks(),closed_tasks=closed_tasks(),username=session['name'])

@tasks_blueprint.route('/add', methods=['POST'])
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
            return redirect(url_for('tasks.tasks'))
        else:
            return render_template('tasks.html',form=form,error=error)
    return render_template('tasks.html',form=form,error=error,open_tasks=open_tasks(),closed_tasks=closed_tasks())

@tasks_blueprint.route('/complete/<int:task_id>/')
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
        return redirect(url_for('tasks.tasks'))
    else:
        flash('you can only upate your own tasks')
        return redirect(url_for('tasks.tasks'))

@tasks_blueprint.route('/delete/<int:task_id>')
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
        return redirect(url_for('tasks.tasks'))
    else:
        flash("You can only delete your own task")
        return redirect(url_for('tasks.tasks'))

