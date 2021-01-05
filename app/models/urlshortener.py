import random
import string
import pymongo
import datetime

from app.models.mongodbhandler import MongoDatabaseHandler


class urlShortener(object):
    def __init__(self, collection = None):

        databaseHandler = MongoDatabaseHandler()

        if collection is None:
            self.collection = databaseHandler.get_shortURL_collection()
        else:
            self.collection = collection


    def saveUrl(self, shortUrl, url, author):
        """ Save short Url and url\n"
            The short Url is stored as index as all looks\n"
            find and deletes will be only using short Url\n"
        """

        save_query = dict()
        save_query['_id'] = shortUrl
        save_query['longurl'] = url
        save_query['clicks'] = 0
        save_query['author'] = author
        save_query['date'] = datetime.datetime.utcnow()

        try:
            self.collection.insert_one(save_query)
        except pymongo.errors.DuplicateKeyError:
            return False, 'DuplicateKeyError'
        except:
            return False,'Misc'

        return True, None

    def findUrl(self, shortUrl):
        """ Finds a url from shorUrl that is sent from the user """

        doc = self.collection.find_one({'_id': shortUrl})
        if doc is None:
            return None
        return doc['longurl']

    def get_doc_from_shorturl(self, shortURL):
        """ given an short url it return the corresponding doc"""
        doc = self.collection.find_one({'_id': shortURL})
        return doc

    def removeUrl(self, shortUrl):
        """ remove the short url"""
        try:
            result = self.collection.delete_one({'_id': shortUrl})
        except:
            # we would want to log an error message as of now
            return False
        return True

    def find_url_of_user(self, author, limit_count):
        """ given an author returns the urls of the user """
        iterator = self.collection.find({'author': author}).sort('clicks',pymongo.DESCENDING).limit(limit_count)
        return iterator

    def generateShortUrl(self, length=6):
        """ generates an shorturl needed from so
            http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630"""
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


    def increment_visited_count(self, shorturl):
        """ increment the count of short_url """
        try:
            result = self.collection.update_one({'_id':shorturl}, {'$inc': {'clicks': 1}})
        except:
            pass
