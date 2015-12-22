## This file performs the basic site testing of the application

import unittest
import sys
import urllib

sys.path.append('..')

from app import app
from flask import Flask, url_for

# This tests the basic site when the user has not logged in

class TestBasicUrlShortener(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.baseURL = 'http://localhost:5000'

    # this is one of the functions that must be
    # implemented for flask testing.
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.debug = True
        self.baseURL = 'http://localhost:5000'
        return app

    def generate_shortURL(self):
        return 'tinyurl765'

    def generate_shortURL_for_redirect(self):
        return 'redirectshort_url'

    def stub_saveURL_returns_false(self, url, shortUrl):
        return False

    # Make sure that we have the index page working
    def test_get_to_index(self):
        rv = self.client.get('/')

        assert rv.status_code == 200
        assert 'name=\"url\"' in str(rv.data)
        assert 'input' in str(rv.data)

    # when we send a Get , we need to make sure that
    # it redirects to index
    def test_get_to_urlshortener(self):
        rv = self.client.get('urlshorten')

        self.assertEqual(rv.status_code, 302)
        assert 'localhost' in rv.location

    # When we send a post we expect it to return a output
    # containing the baseURL and short url
    def test_post_to_urlshortener(self):
        # monkeypatch the generate shortURL so that we know
        # the correct value to expect and perform validation
        # accordingly
        from app.models import urlshortener
        urlshortener.urlShortener.generateShortUrl = self.generate_shortURL
        post_data = {'url': 'http://www.google.com/'}

        rv = self.client.post('/urlshorten',
                              data=post_data,
                              follow_redirects=False)

        self.assertEqual(rv.status_code, 200)
        shorturl = self.baseURL + '/' + self.generate_shortURL()
        # print rv.data
        assert shorturl in str(rv.data)

        # cleanup so next time it works
        urlshort = urlshortener.urlShortener()
        urlshort.removeUrl(self.generate_shortURL())

    # the case where we send a request to shorten the url and for
    # whatever reason , the code shortened url is not created
    def test_post_to_urlShortener_fail_in_model(self):

        # monkey patch the code to make sure that the saveUrl returns
        # false so we can check the return value.
        from app.models import urlshortener
        beforepatch = urlshortener.urlShortener.saveUrl
        urlshortener.urlShortener.saveUrl = self.stub_saveURL_returns_false
        post_data = {'url': 'http://www.google.com/'}

        rv = self.client.post('/urlshorten',
                              data=post_data,
                              follow_redirects=False)

        self.assertEqual(rv.status_code, 200)

        #cleanup
        urlshortener.urlShortener.saveUrl = beforepatch

    # the user uses the short url
    # make sure that the short url redirects
    # to the correct page
    def test_get_shorturl(self):
        # monkey patch to a particular short url
        # store it in database and then
        # do a get with short url
        from app.models import urlshortener
        urlshortener.urlShortener.generateShortUrl = self.generate_shortURL_for_redirect
        post_data = {'url': 'http://www.google.com/'}
        self.client.post('/urlshorten',
                         data=post_data,
                         follow_redirects=False)

        shorturl = self.baseURL + '/' + self.generate_shortURL_for_redirect()
        rv = self.client.get(shorturl)

        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://www.google.com/')

        # cleanup so next time it works
        urlshort = urlshortener.urlShortener()
        urlshort.removeUrl(self.generate_shortURL())

    # try to access a invalid shorturl and the code
    # must return error code 404 not found
    def test_get_invalidShortUrl(self):
        # invalid shortUrl
        shorturl = self.baseURL + '/' + '112111111'

        rv = self.client.get(shorturl)

        self.assertEqual(rv.status_code, 404)

if __name__ == '__main__':
    unittest.main()
