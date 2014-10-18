from flask import Flask, flash, redirect, render_template, request, session, url_for, g
from functools import wraps
import sqlite3

from forms import ProposeNewHangout


app = Flask(__name__)
app.config.from_object('config')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('login'))
	return wrap

@app.route('/logout/')
def logout():
	session.pop('logged_in', None)
	flash('You are logged out. Bye. :(')
	return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
		    error = 'Invalid Credentials. Please try again.'
		    return render_template('login.html', error=error)
		else:
			session['logged_in'] = True
			return redirect(url_for('tasks'))
	if request.method == 'GET':
		return render_template('login.html')

@app.route('/tasks/')
@login_required
def tasks():
	g.db = connect_db()
	cur = g.db.execute(
		'select title, hangout_date, level, language, description from hangout where status=1')
	upcoming_hangouts = [dict(title=row[0], hangout_date=row[1],
		level=row[2], language=row[3], description=row[4]) for row in cur.fetchall()]
	
	cur = g.db.execute(
		'select title, hangout_date, level, language, description from hangout where status=0')
	previous_hangouts = [dict(title=row[0], hangout_date=row[1],
		level=row[2], language=row[3], description=row[4]) for row in cur.fetchall()]
	
	g.db.close()
	return render_template(
		'tasks.html',
		form = ProposeNewHangout(request.form),
		open_tasks=upcoming_hangouts,
		closed_tasks=previous_hangouts
	)

@app.route('/add/', methods = ['POST'])
@login_required
def new_task():
	g.db = connect_db()
	name = request.form['name']
	date = request.form['due_date']
	priority = request.form['priority']
	if not name or not date or not priority:
		flash("All fields are required. Please try again.")
		return redirect(url_for('tasks'))
	else:
		g.db.execute('INSERT into tasks (name, due_date, priority, status) values (?, ?, ?, 1)', [request.form['name'], request.form['due_date'],request.form['priority']])
		g.db.commit()
		g.db.close()
		flash('New entry was successfully posted. Thanks.')
		return redirect(url_for('tasks'))

#Mark tasks as complete
@app.route('/complete/<int:task_id>/',)
@login_required
def complete(task_id):
	g.db = connect_db()
	g.db.execute(
		'UPDATE tasks set status = 0 where task_id='+str(task_id)
	)
	g.db.commit()
	g.db.close()
	flash('The task was marked as complete.')
	return redirect(url_for('tasks'))

@app.route('/delete/<int:task_id>/',)
@login_required
def delete_entry(task_id):
	g.db = connect_db()
	g.db.execute('delete from tasks where task_id='+ str(task_id))
	g.db.commit()
	g.db.close()
	flash('The task was deleted.')
	return redirect(url_for('tasks'))


