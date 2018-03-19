# all the imports
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from mongoengine import *
from models import Entry
from .flaskr import app

connect('test_db')

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict('test_db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    mongoengine.connect(db_name='test_db',
        host = '127.0.0.1',
        port = 27017,
        username = None,
        password = None
    )

#def init_db():
 #   db = get_db()
  #  with app.open_resource('test_db', mode='r') as f:
   #     db.cursor().executescript(f.read())
    #db.commit()

#@app.cli.command('initdb')
#def initdb_command():
 #   """Initializes the database."""
  #  init_db()
   # print('Initialized the database.')

#def get_db():
 #   """Opens a new database connection if there is none yet for the
  #  current application context.
   # """
    #if not hasattr(g, 'sqlite_db'):
     #   g.sqlite_db = connect_db()
    #return g.sqlite_db

#@app.teardown_appcontext
#def close_db(error):
 #   """Closes the database again at the end of the request."""
  #  if hasattr(g, 'sqlite_db'):
   #     g.sqlite_db.close()

@app.route('/')
def show_entries():
    entries = [dict(title=entry.title, text=entry.text) \
            for entry in Entry.objects]
    return render_template('show_entries.html', entries=entries)
    

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
        entry = Entry(
            title = request.form['title'],
            text = request.form['text']
        )
    entry.save()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    connect_db()
    app.run()



