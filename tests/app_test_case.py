import os

from .flask_test_case import FlaskTestCase


class AppTestCase(FlaskTestCase):

    def setUp(self):
        super().setUp()

        # Make sure using dev settings in testing
        self.assertEqual(os.environ.get('NODEBIN_CONFIG'), 'dev')
        self.assertEqual(self.app.config['TESTING'], True)

        # Test project dependent environment variables
        pass
