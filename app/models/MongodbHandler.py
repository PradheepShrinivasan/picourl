import pymongo
import os

from config import CONNECTION_URI

# TODO: Make this class read from a config file
# Now it reads from the enviornment string
class MongoDatabaseHandler(object):

    def __init__(self):
        self.connection = pymongo.MongoClient(CONNECTION_URI)
        self.database = self.connection.urlshortener

    def get_ShortURLCollection(self):
        return self.database.shorturls
