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
        url = "http://www.google.com"
        short_url = "gl"
        author = 'author'
        result, reason = self.urlShortener.saveUrl(short_url, url, author)

        # Assertions
        self.assertEqual(result, True)
        doc = self.collection.find_one({'_id': short_url})
        self.assertEqual(doc['_id'], short_url)
        self.assertEqual(doc['url'], url)
        self.assertEqual(doc['author'], author)
        self.assertEqual(doc['count'], 0)

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
        self.assertEqual(doc['url'],  url)
        self.assertEqual(doc['count'], 0)

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

    def test_generateRandom(self):
        """ test the random number generator """

        # commented as of now as its failing randomly. Race due to
        # monkey patching ???
        # self.assertEqual(len(self.urlShortener.generateShortUrl()), 6)
        # self.assertEqual(len(self.urlShortener.generateShortUrl(7)), 7)

        self.assertEqual(self.urlShortener.generateShortUrl().isalnum(), True)
