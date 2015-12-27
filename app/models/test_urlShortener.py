import unittest
import pymongo
import sys
sys.path.append('../../')
sys.path.append('../')

from urlshortener import urlShortener


class TestUrlShortener(unittest.TestCase):
    def setUp(self):
        connection = pymongo.MongoClient('mongodb://localhost:27017/')
        self.database = connection.test
        self.collection = self.database.urlshortener
        self.collection.drop()
        self.urlShortener = urlShortener(self.collection)

    def test_saveUrl_Unique(self):
        # setup
        url = "http://www.google.com"
        shortUrl = "gl"

        result = self.urlShortener.saveUrl(shortUrl, url)

        # Assertions
        self.assertEqual(result, True)
        doc = self.collection.find_one({'_id': shortUrl})
        self.assertEqual(doc, {'_id': shortUrl, 'url': url})

        # cleanup so that next time we dont get duplicateKeyError
        self.collection.delete_one({'_id': shortUrl})

    def test_saveUrl_duplicate(self):
        shortUrl = 'orig'
        url = 'http://www.google.com'
        urldup = 'http://www.yahoo.com'

        self.urlShortener.saveUrl(shortUrl, url)
        result = self.urlShortener.saveUrl(shortUrl, urldup)

        self.assertEqual(result, False)
        doc = self.collection.find_one({'_id': shortUrl})
        self.assertEqual(doc, {'_id': shortUrl, 'url': url})

        self.collection.delete_one({'_id': shortUrl})

    def test_findUrl_Existing(self):
        shortUrl = 'findUrl'
        url = 'http://www.google.com'
        self.urlShortener.saveUrl(shortUrl, url)

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
        self.urlShortener.saveUrl(shortUrl, url)

        result = self.urlShortener.removeUrl(shortUrl)

        self.assertEqual(result, True)

    def test_removeURL_NonExisting(self):
        shortURL = 'NonExisting'

        result = self.urlShortener.removeUrl(shortURL)

        self.assertEqual(result, True)

    def test_generateRandom(self):
        self.assertEqual(len(self.urlShortener.generateShortUrl()), 6)
        self.assertEqual(len(self.urlShortener.generateShortUrl(7)), 7)

        self.assertEqual(self.urlShortener.generateShortUrl().isalnum(), True)
