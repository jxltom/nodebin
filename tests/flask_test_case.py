from unittest import TestCase

from nodebin.wsgi import create_app


class FlaskTestCase(TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

        self.app_context = self.app.test_request_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()
