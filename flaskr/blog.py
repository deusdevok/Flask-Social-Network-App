from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    print('Creating post...')
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )                        

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')    

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post    

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)    

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))    

# View each blog post individually in its own route
@bp.route('/<int:id>', methods = ('GET',))
def view_post(id):

    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, likers, dislikers'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    return render_template('blog/blog_view.html', post=post)

# Like post
@bp.route('/<int:id>/<likeOrDislike>/', methods = ('GET',))
@login_required
def like_post(id, likeOrDislike):

    db = get_db()
    
    post = db.execute(
        'SELECT p.id, title, body, created, author_id, username, likers, dislikers'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    likers, dislikers = post['likers'], post['dislikers']

    # likers (and dislikers) is a string with user id's separated by commas
    # Convert each one to a Python list
    try:
        likers = [int(n) for n in likers.split(',')]
    except:
        likers = []

    try:    
        dislikers = [int(n) for n in dislikers.split(',')]
    except:
        dislikers = []

    if likeOrDislike == 'like': # Like
        if g.user['id'] not in likers:
            likers.append(g.user['id'])
        else:            
            likers.pop(likers.index(g.user['id']))
        if g.user['id'] in dislikers:
            dislikers.pop(dislikers.index(g.user['id']))
    else: # Dislike
        if g.user['id'] not in dislikers:
            dislikers.append(g.user['id'])
        else:
            dislikers.pop(dislikers.index(g.user['id']))
        if g.user['id'] in likers:
            likers.pop(likers.index(g.user['id']))

    likers = ','.join(str(n) for n in likers)
    dislikers = ','.join(str(n) for n in dislikers)
    
    db.execute(
            'UPDATE post SET '            
            'likers = ?,'
            'dislikers = ?'
            ' WHERE id = ?',
            (likers, dislikers, id,)
        )

    db.commit()

    return redirect(url_for('blog.view_post', id=id))

 