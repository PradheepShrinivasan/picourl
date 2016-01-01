import random
import string
import pymongo

from mongodbhandler import MongoDatabaseHandler


class urlShortener(object):
    def __init__(self, collection = None):

        databaseHandler = MongoDatabaseHandler()

        if collection is None:
            self.collection = databaseHandler.get_shortURL_collection()
        else:
            self.collection = collection

    #  Save short Url and url
    # The short Url is stored as index as all looks
    # find and deletes will be only using short Url
    def saveUrl(self, shortUrl, url):

        saveQuery = {'_id': shortUrl, 'url': url}
        try:

            self.collection.insert_one(saveQuery)

        except pymongo.errors.DuplicateKeyError:
            return False, 'DuplicateKeyError'
        except:
            return False,'Misc'

        return True, None

    # Finds a url from shorUrl that is sent from the user
    def findUrl(self, shortUrl):

        doc = self.collection.find_one({'_id': shortUrl})
        if doc is None:
            return None

        return doc['url']

    def removeUrl(self, shortUrl):

        try:
            result = self.collection.delete_one({'_id': shortUrl})
        except:
            # we would want to log an error message as of now
            return False
        return True

    # generates an shorturl needed from so
    #  http://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python/23728630#23728630
    def generateShortUrl(self, length=6):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))
