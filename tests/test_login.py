import unittest

import sys

sys.path.append('..')

from bs4 import BeautifulSoup
from app import app

from app.user import User

class TestLoginAndLogout(unittest.TestCase):
    """ Class to test login and logout of users """

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

    def add_test_user(self, username, password):
        """ adds a user to the database so that we can use it for testing
        """
        user= User(username, password)
        # delete the user if its already in the database
        # just to be sure that its not part of the last
        # unsucessful run
        user.delete_user()
        rv = user.add_user()
        assert rv

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

    def login(self, username, password):
        """ login a user given a usename and password """
        post_data = {'email': username,
                     'password': password,
                     'csrf_token': self.getcsrf_value(),
                     'submit': 'Login'}

        return self.client.post('/login', data=post_data,
                                follow_redirects=True)

    def logout(self):
        """ Logout a logged in user """

        post_data = {'csrf_token': self.getcsrf_value(),
                     'submit': 'Logout'}
        return self.client.post('/logout', data=post_data,
                               follow_redirects=True)

    def test_user_login_logout(self):
        """ create test users and login and logout to make sure
        it works properly
        """

        username = 'user@gmail.com'
        password = 'mypassword'
        self.add_test_user(username, password)

        rv = self.login(username, password)
        assert 'Login successful' in rv.data
        assert 'Hi user@gmail.com!' in rv.data
        assert '/logout' in rv.data

        rv = self.logout()
        assert 'Logout Successful' in rv.data
        assert '/login' in rv.data

        self.delete_test_user(username)

    def test_invalid_login_logout(self):
        """ test loggin in with a wrong username and password """

        username = 'invaliduser@gmail.com'
        password = 'password'

        rv = self.login(username, password)
        assert rv.status_code == 200
        assert 'Invalid e-mail or password' in rv.data
        assert '/login' in rv.data
        assert '/logout' not in rv.data

        rv = self.logout()
        assert rv.status_code == 401

    def test_invalid_login_password(self):
        """  Test loggin in with a valid user name but with invalid password """
        username = 'invaliduser@gmail.com'
        password = 'password'
        password2 = 'password2'
        self.add_test_user(username, password)

        rv = self.login(username, password2)
        assert rv.status_code == 200
        assert 'Invalid e-mail or password' in rv.data
        assert '/login' in rv.data
        assert '/logout' not in rv.data

        rv = self.logout()
        assert rv.status_code == 401

        self.delete_test_user(username)