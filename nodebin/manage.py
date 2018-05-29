#!/usr/bin/env python

import os
import sys

from flask.cli import main

import nodebin as project


if __name__ == '__main__':
    app = '{}/wsgi.py'.format(os.path.dirname(project.__file__))
    os.environ.setdefault('FLASK_APP', app)
    if os.getenv('FLASK_BOILERPLATE_CONFIG') == 'dev':
        os.environ.setdefault('FLASK_DEBUG', '1')

    sys.argv = ['flask'] + sys.argv[1:] if len(sys.argv) > 1 \
        else ['flask'] + input('flask@{} > '.format(project.__name__)).split()
    main(as_module=True)
