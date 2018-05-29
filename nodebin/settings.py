import os

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
    SECRET_KEY = b'I\x98\xefQ\xd1\xba\xc6\x99\xc1\xa0\x16L'  # used for session
    TESTING = False

    # Settings for Debug by Flask-DebugToolbar
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False

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


class TestConfig(Config):
    DEBUG = False


class ProdConfig(Config):
    DEBUG = False


config = {
    'dev': DevConfig,
    'test': TestConfig,
    'prod': ProdConfig,
}
