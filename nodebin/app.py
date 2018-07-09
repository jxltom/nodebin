import os
from os.path import dirname, join, abspath
import sys

from flask import Flask
from flask.json import JSONEncoder
from flask_compress import Compress
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from raven.contrib.flask import Sentry
from whitenoise import WhiteNoise
import click

import nodebin as project
from nodebin.settings import config


PROJECT_NAME = project.__name__
ENV_CONFIG = os.getenv('{}_CONFIG'.format(PROJECT_NAME.upper()), 'dev')

sentry = Sentry()
compress = Compress()
db = SQLAlchemy()
migrate = Migrate()


class CustomJSONEncoder(JSONEncoder):
    """Custom JSON output."""
    item_separator = ','
    key_separator = ':'

    def __init__(self, **kwargs):
        kwargs['ensure_ascii'] = False
        super(CustomJSONEncoder, self).__init__(**kwargs)


def create_app():
    # Initialize Flask instance and enable static file serving
    app = Flask(__name__)
    app.config.from_object(config[ENV_CONFIG]())  # instance is for __init__
    app.wsgi_app = WhiteNoise(app.wsgi_app, root='static/')

    # Initialize Sentry for error tracking
    sentry.init_app(app)

    # Custom Json
    app.json_encoder = CustomJSONEncoder
    compress.init_app(app)

    # Initialize DebugToolbar
    if app.config['DEBUG']:
        from flask_debugtoolbar import DebugToolbarExtension
        toolbar = DebugToolbarExtension()
        toolbar.init_app(app)

    # Initialize Database and Migration by Flask-Sqlalchey and Flask-Migrate
    db.init_app(app)
    migrate.init_app(
        app, db,
        directory=join(abspath(dirname(project.__file__)), 'migrations')
    )  # set directory for compatible with Heroku

    # Initialize app blueprint
    from .blueprints.app import app as app_blueprint
    app.register_blueprint(app_blueprint, url_prefix='/')

    # Initialize api10 blueprint
    from .blueprints.api10 import api10 as api10_blueprint
    app.register_blueprint(api10_blueprint, url_prefix='/v1')

    # Initialize CLI shell command
    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db)

    # Initialize CLI command for pytest-cov
    @app.cli.command(name='py.test')
    @click.option('--cov')
    @click.option('--cov-report')
    def pytest_cov(cov, cov_report):
        """Run pytest with pytest-cov plugin."""
        import pytest

        sys.argv = ['py.test', '-s']
        sys.argv += ['--cov={}'.format(cov)] if cov else []
        sys.argv += ['--cov-report={}'.format(cov_report)] if cov_report else []

        sys.exit(pytest.main())

    return app


application = create_app()
