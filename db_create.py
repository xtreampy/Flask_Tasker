from project import db,bcrypt
from project.models import Task
from datetime import date
#from project._config import SQLALCHEMY_DATABASE_URI
#from flask_sqlalchemy import SQLAlchemy
#from _config import DATABASE_PATH

"""with sqlite3.connect(DATABASE_PATH) as connection:
	cursor = connection.cursor()
	cursor.execute("DROP TABLE IF EXISTS tasks")
	cursor.execute("CREATE TABLE tasks(task_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, due_date TEXT NOT NULL, priority INTEGER NOT NULL,status INTEGER NOT NULL)")
	cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Finish this tutorial','15/02/2016',10,1)")
	cursor.execute("INSERT INTO tasks(name, due_date, priority, status) VALUES('Real python tutorial finish','15/03/2016',10,1)")"""
db.create_all()
#db.session.add(Task("Finish this tutorial", date(2015, 3, 13), 10,1))
#db.session.add(Task("Finish Real Python", date(2015, 3, 13), 10, 1))
db.session.commit()
