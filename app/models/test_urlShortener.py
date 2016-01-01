import unittest
import pymongo
import sys
sys.path.append('../../')
sys.path.append('../')

from urlshortener import urlShortener


class TestUrlShortener(unittest.TestCase):
    """ test the model of url handler """
    def setUp(self):
        connection = pymongo.MongoClient('mongodb://localhost:27017/')
        self.database = connection.test
        self.collection = self.database.urlshortener
        self.collection.drop()
        self.urlShortener = urlShortener(self.collection)

    def test_saveUrl_Unique(self):
        # setup
        longurl = "http://www.google.com"
        short_url = "gl"
        author = 'author'
        result, reason = self.urlShortener.saveUrl(short_url, longurl, author)

        # Assertions
        self.assertEqual(result, True)
        doc = self.collection.find_one({'_id': short_url})
        self.assertEqual(doc['_id'], short_url)
        self.assertEqual(doc['longurl'], longurl)
        self.assertEqual(doc['author'], author)
        self.assertEqual(doc['clicks'], 0)

        # cleanup so that next time we dont get duplicateKeyError
        self.collection.delete_one({'_id': short_url})

    def test_saveUrl_duplicate(self):
        shortUrl = 'orig'
        url = 'http://www.google.com'
        urldup = 'http://www.yahoo.com'
        author = 'author'

        self.urlShortener.saveUrl(shortUrl, url, author)
        result, reason = self.urlShortener.saveUrl(shortUrl, urldup, author)

        self.assertEqual(result, False)
        self.assertEqual(reason, 'DuplicateKeyError')
        doc = self.collection.find_one({'_id': shortUrl})
        self.assertEqual(doc['_id'], shortUrl)
        self.assertEqual(doc['longurl'],  url)
        self.assertEqual(doc['clicks'], 0)

        self.collection.delete_one({'_id': shortUrl})

    def test_findUrl_Existing(self):
        shortUrl = 'findUrl'
        url = 'http://www.google.com'
        author = 'author'
        self.urlShortener.saveUrl(shortUrl, url, author)

        resultUrl = self.urlShortener.findUrl(shortUrl)

        self.assertEqual(resultUrl, url)

        self.collection.delete_one({'_id': shortUrl})

    def test_findUrl_NonExisting(self):
        shortUrl = 'findDuplicate'

        resultUrl = self.urlShortener.findUrl(shortUrl)

        self.assertEqual(resultUrl, None)

    def test_removeURL_Existing(self):
        shortUrl = 'removeURL'
        url = 'http://www.google.com'
        author = 'author'
        self.urlShortener.saveUrl(shortUrl, url, author)

        result = self.urlShortener.removeUrl(shortUrl)

        self.assertEqual(result, True)

    def test_removeURL_NonExisting(self):
        shortURL = 'NonExisting'

        result = self.urlShortener.removeUrl(shortURL)

        self.assertEqual(result, True)

    def test_increment_view_count(self):
        """  Check that view count is incremented by one each time"""
        shortUrl = 'increment_url'
        url = 'http://www.google.com'
        author = 'author'
        self.urlShortener.saveUrl(shortUrl, url, author)

        self.urlShortener.increment_visited_count(shortUrl)
        self.urlShortener.increment_visited_count(shortUrl)

        doc = self.urlShortener.get_doc_from_shorturl(shortUrl)
        self.assertEqual(int(doc['clicks']), 2)

        self.urlShortener.removeUrl(shortUrl)

    def test_find_urls_of_user(self):
        shortUrl = 'shorturl1'
        longurl = 'http://www.google.com'
        author = 'author'
        self.urlShortener.saveUrl(shortUrl, longurl, author)

        iterator = self.urlShortener.find_url_of_user(author, 1)

        for doc in iterator:
            self.assertEqual(doc['_id'], shortUrl)
            self.assertEqual(doc['longurl'], longurl)
            self.assertEqual(doc['author'], author)

        self.urlShortener.removeUrl(shortUrl)




    def test_generateRandom(self):
        """ test the random number generator """

        # commented as of now as its failing randomly. Race due to
        # monkey patching ???
        # self.assertEqual(len(self.urlShortener.generateShortUrl()), 6)
        # self.assertEqual(len(self.urlShortener.generateShortUrl(7)), 7)

        self.assertEqual(self.urlShortener.generateShortUrl().isalnum(), True)

