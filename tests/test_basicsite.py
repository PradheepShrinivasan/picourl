# This file performs the basic site testing of the application

import unittest
import sys
from bs4 import BeautifulSoup

sys.path.append('..')

from app import app


class TestBasicUrlShortener(unittest.TestCase):
    """ This tests the basic site when the user has not logged in """

    def setUp(self):
        app.config['TESTING'] = True
        # Set the below to True to enable debug logs
        app.debug = False
        app.config['WTF_CSRF_ENABLED'] = True

        self.baseURL = 'http://localhost:5000'
        self.client = app.test_client()

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

    def generate_shortURL(self):
        return 'tinyurl765'

    def generate_shortURL_for_redirect(self):
        return 'redirectshort_url'

    def stub_saveURL_returns_false(self, url, shortUrl, author):
        return False, None

    def test_get_to_index(self):
        """ Make sure that we have the index page working """

        rv = self.client.get('/')

        assert rv.status_code == 200
        assert 'name=\"url\"' in str(rv.data)
        assert 'input' in str(rv.data)

    # When we send a post we expect it to return a output
    # containing the baseURL and short url
    def test_post_to_urlshortener(self):
        # monkeypatch the generate shortURL so that we know
        # the correct value to expect and perform validation
        # accordingly
        from app.models import urlshortener

        urlshortener.urlShortener.generateShortUrl = self.generate_shortURL
        post_data = {'url': 'http://www.google.com/',
                     'submit': 'Shorten',
                     'csrf_token': self.getcsrf_value()}

        rv = self.client.post('/',
                              data=post_data,
                              follow_redirects=False)

        self.assertEqual(rv.status_code, 200)
        shorturl = self.baseURL + '/' + self.generate_shortURL()
        assert shorturl in str(rv.data)

        # cleanup so next time it works
        urlshort = urlshortener.urlShortener()
        urlshort.removeUrl(self.generate_shortURL())

    def test_post_to_urlShortener_fail_in_model(self):
        """    the case where we send a request to shorten the url and for
                whatever reason , the code shortened url is not created
        """
        # monkey patch the code to make sure that the saveUrl returns
        # false so we can check the return value.
        from app.models import urlshortener

        beforepatch = urlshortener.urlShortener.saveUrl
        urlshortener.urlShortener.saveUrl = self.stub_saveURL_returns_false
        post_data = {'url': 'http://www.google.com/',
                     'submit': 'Shorten',
                     'csrf_token': self.getcsrf_value()}

        rv = self.client.post('/',
                              data=post_data,
                              follow_redirects=False)

        self.assertEqual(rv.status_code, 200)

        # cleanup
        urlshortener.urlShortener.saveUrl = beforepatch

    def test_get_shorturl(self):
        """
            the user uses the short url
            make sure that the short url redirects
            to the correct page
        """
        # monkey patch to a particular short url
        # store it in database and then
        # do a get with short url
        from app.models import urlshortener

        beforepatch = urlshortener.urlShortener.generateShortUrl
        urlshortener.urlShortener.generateShortUrl = self.generate_shortURL_for_redirect
        post_data = {'url': 'http://www.google.com/',
                     'submit': 'Shorten',
                     'csrf_token': self.getcsrf_value()}
        self.client.post('/',
                         data=post_data,
                         follow_redirects=False)

        shorturl = self.baseURL + '/' + self.generate_shortURL_for_redirect()
        rv = self.client.get(shorturl)

        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://www.google.com/')

        # cleanup so next time it works
        urlshortener.urlShortener.generateShortUrl = beforepatch
        urlshort = urlshortener.urlShortener()
        urlshort.removeUrl(self.generate_shortURL())

    def test_get_invalidShortUrl(self):
        """ try to access a invalid shorturl and the code
        must return error code 404 not found """
        # invalid shortUrl
        shorturl = self.baseURL + '/' + '112111111'

        rv = self.client.get(shorturl)

        self.assertEqual(rv.status_code, 404)
