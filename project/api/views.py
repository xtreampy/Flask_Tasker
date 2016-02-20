from functools import wraps
from flask import flash, make_response, redirect, jsonify, session, url_for, Blueprint
from project import db
from project.models import Task

api_blueprint = Blueprint('api', __name__)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

def open_tasks():
    return db.session.query(Task).filter_by(status='1').order_by(Task.due_date.asc())

def closed_tasks():
    return db.session.query(Task).filter_by(status='0').order_by(Task.due_date.asc())

@api_blueprint.route('/api/v1/tasks/')
def api_task():
    results = db.session.query(Task).limit(10).offset(0).all()
    json_result = []
    for result in results:
        data = {
        'task_id':result.task_id,
        'task name':result.name,
        'post date':str(result.posted_date),
        'priority':result.priority,
        'Due date':str(result.due_date),
        'status':result.status,
        'user_id':result.user_id
        }
        json_result.append(data)
    return jsonify(items=json_result)

@api_blueprint.route('/api/v1/tasks/<int:task_id>')
def apiid_task(task_id):
    result =db.session.query(Task).filter_by(task_id=task_id).first()
    if result:
        json_result = {
                    'task_id': result.task_id,
                    'task name': result.name,
                    'due date': str(result.due_date),
                    'priority': result.priority,
                    'posted date': str(result.posted_date),
                    'status': result.status,
                    'user id': result.user_id
                      }
        code = 200
    else:
        json_result = {'error':'element does not exists'}
        code = 404
    return make_response(jsonify(json_result),code)
