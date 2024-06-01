import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Ensure the password is URL-encoded if it contains special characters
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Raffin%40786@localhost:3306/todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_description = db.Column(db.String(100), nullable=False)
    task_deadline = db.Column(db.Date, nullable  = False)
    task_completed = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Tasks.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task(): 
    task_name = request.form.get("name")
    task_description = request.form.get("description")
    task_deadline = datetime.strptime(request.form.get('deadline'), '%Y-%m-%d')
    task = Tasks(task_name=task_name, task_description=task_description, task_deadline=task_deadline)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    task = Tasks.query.get(task_id)
    task.task_name = request.form.get('name')
    task.task_description = request.form.get('description')
    task.task_deadline = datetime.strptime(request.form.get('deadline'), '%Y-%m-%d')
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    task = Tasks.query.get(task_id)
    task.task_completed = not task.task_completed
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
