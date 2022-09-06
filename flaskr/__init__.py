# __init__.py contains the application factory, 
# and it tells Python that the flaskr directory 
# should be treated as a package.

import os
from flask import Flask
from . import db, auth, blog

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    
    UPLOAD_FOLDER = app.root_path

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    if test_config is None:
        # Load instance config, if exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # A simple page saying hello
    @app.route('/hello/')
    def hello():
        return 'Hello man!'

    db.init_app(app)

    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app