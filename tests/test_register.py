import unittest

import sys

sys.path.append('..')

from bs4 import BeautifulSoup
from app import app

from app.user import User

class TestRegister(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.debug = False
        app.config['WTF_CSRF_ENABLED'] = True

        self.baseURL = 'http://localhost:5000'
        self.client = app.test_client()

    def delete_test_user(self, username):
        """  deletes the user from database """
        user = User(username, 'dummy')
        user.delete_user()

    def getcsrf_value(self):
        """ returns the csrf token by sending a dummy request """

        # I spent a good amount of time making the csr_token invalidation with the
        #    configuration work, but seems i end up trouble making it work.so the easier
        #    way is to parse the code and get the csr value. This was due to bug
        #    https://github.com/lepture/flask-wtf/issues/208

        rv = self.client.get('/')

        soup = BeautifulSoup(rv.data, 'html.parser')
        tag = soup.body.find('input', attrs={'name': 'csrf_token'})
        return tag['value']

    def test_basic_register_get(self):

        rv = self.client.get('/register', data={'csrf_token': self.getcsrf_value()})

        assert rv.status_code == 200
       # print rv.data

    def test_basic_register_post(self):
        """  register a user and check if user is logged in
        """
        user = 'test@gmail.com'
        # delete the user just for failed earlier runs
        self.delete_test_user(user)
        post_data = {
                'email': user,
                'password':'password',
                'confirm_password':'password',
                'csrf_token': self.getcsrf_value(),
                'submit': 'Register'
        }

        rv = self.client.post('/register', data=post_data,
                              follow_redirects=True)

        #print rv.data
        assert rv.status_code == 200
        assert 'Thanks for registering' in rv.data
        # The user must be logged in so check that logout
        # and Hi username is present.
        assert 'Hi '+user in rv.data
        assert '/logout' in rv.data

        #clean up
        self.delete_test_user(user)


    def test_register_twice(self):
        """  trying to register the same user again must result in failure """

        user = 'twiceregister@gmail.com'

        # delete the user just for failed earlier runs
        self.delete_test_user(user)
        post_data = {
            'email': user,
            'password':'password',
            'confirm_password':'password',
            'csrf_token': self.getcsrf_value(),
            'submit' : 'Register'
        }
        _ = self.client.post('/register', data=post_data,
                          follow_redirects=True)

        # send the registration request again
        rv = self.client.post('/register', data=post_data,
                          follow_redirects=True)

        # print rv.data
        assert rv.status_code == 200
        assert 'User already registered.Try login' in rv.data
