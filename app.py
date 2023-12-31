import sqlite3
import os
from flask import Flask, render_template, request, g, url_for, flash, abort
from FDataBase import FDataBase

# configuration
DATABASE ='Flask.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'Flask.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Helper function for creating database tables"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Connecting to the database if it is not already established"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.route('/')
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnonce())


@app.route('/add_post', methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbase = FDataBase(db)

    if request.method == "POST":
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'])
            if not res:
                flash('Error adding article', category = 'error')
            else:
                flash('Article added successfully', category ='success')
        else:
            flash('Error adding article', category = 'error')
    return render_template('add_post.html', menu = dbase.getMenu(), title='Adding an article')


@app.teardown_appcontext
def close_db(error):
    """Close the connection to the database if it was established"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/post/<int:id_post>')
def showPost(id_post):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=dbase.getMenu(), title=title, post=post)


if __name__ == "__main__":
    app.run(
        debug=True,
        use_reloader=False,
        )