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
        'SELECT p.id, title, body, created, author_id, username, likes_count, dislikes_count'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    print('printing post data...')
    for row in posts:
        print(row['likes_count'], row['dislikes_count'])
        print('\n')

    print('I just printed some post data...')

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
                'INSERT INTO post (title, body, author_id, likes_count, dislikes_count)'
                ' VALUES (?, ?, ?, ?, ?)',
                (title, body, g.user['id'], 0, 0)
            )
                        
            db.commit()

            # Update likers table
            post = get_db().execute(
                'SELECT id FROM post',                
            ).fetchone()

            db.execute(
                'INSERT INTO likers (user_id_, post_id, like_status)'
                'VALUES (?, ?, ?)',
                (g.user['id'], g.post['id'], 'none')
            )

            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')    

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, likes_count, dislikes_count'
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
        'SELECT p.id, title, body, created, author_id, username, likes_count, dislikes_count'
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

    liker = db.execute(
        'SELECT user_id_, post_id, like_status'
        'FROM likers'
    )

    print(liker)

    db.execute(
            'UPDATE post SET ' + likeOrDislike + 's_count' + ' = ' + likeOrDislike + 's_count' + ' + 1'
            ' WHERE id = ?',
            (id,)
        )

    db.execute(
        'UPDATE likers SET like_status = ' + likeOrDislike
    )

    db.commit()

    '''
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username, likes_count, dislikes_count'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    '''

    return redirect(url_for('blog.view_post', id=id))

 