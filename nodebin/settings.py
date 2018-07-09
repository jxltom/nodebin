import os
from os.path import dirname, abspath

import nodebin as project


def _env(env):
    """If ENV exit but with empty value, return empty string."""
    return env if os.getenv(env) else ''


def _getenv(env, default=None):
    """If ENV doesn't exist or None, return default value."""
    # Note that os.getenv('') always returns None
    return os.getenv(_env(env), default)


class Config:
    # Settings for Flask
    SECRET_KEY = _getenv('SECRET_KEY')  # used for session
    TESTING = False

    # Settings for Debug by Flask-DebugToolbar
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # Settings for Database by Flask-SQLAlchemy
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    def __init__(self):
        # Make sure PROJECT_CONFIG is set
        Config._health_check()

    @staticmethod
    def _health_check():
        project_config = '{}_CONFIG'.format(project.__name__.upper())
        if not _getenv(project_config):
            raise Exception(
                'Environment variable {} is not set'.format(project_config)
            )


class DevConfig(Config):
    DEBUG = True

    # Settings for Database
    # If DATABASE_DEV is not available, use DATABASE_URL for Heroku support
    # If DATABASE_URL is not available neither, use local sqlite database
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_DEV',
        default=_getenv(
            'DATABASE_URL',
            default='sqlite:///{}_dev.sqlite3'.format(dirname(abspath(project.__file__)))
        )  # abspath is used for same behaviour of db migrate and run
    )


class TestConfig(Config):
    DEBUG = False

    # Settings for Database
    # If DATABASE_TEST is not available, use DATABASE_URL for Heroku support
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_TEST', default=_getenv('DATABASE_URL')
    )


class ProdConfig(Config):
    DEBUG = False

    # Settings for Database
    # If DATABASE_PROD is not available, use DATABASE_URL for Heroku support
    SQLALCHEMY_DATABASE_URI = _getenv(
        'DATABASE_PROD', default=_getenv('DATABASE_URL')
    )


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
