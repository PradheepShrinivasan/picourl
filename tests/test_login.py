import unittest

import sys
sys.path.append('..')

from app import app

class TestLoginAndLogout(unittest.TestCase):
    """ Class to test login and logout of users """

    def setUp(self):
        app.config['TESTING'] = True
        app.debug = True
        # app.config['WTF_CSRF_ENABLED'] = False
        self.baseURL = 'http://localhost:5000'
        self.client = app.test_client()
        # app.config['WTF_CSRF_ENABLED'] = False

    def test_user_login(self):
        pass
