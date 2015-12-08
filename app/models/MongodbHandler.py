import pymongo
import os

# TODO: Make this class read from a config file
# Now it reads from the enviornment string
class MongoDatabaseHandler:

    def __init__(self):
        connection_string = os.environ['CONNECTION_STRING']
        self.connection = pymongo.MongoClient(connection_string)
        self.database = self.connection.urlshortener

    def get_ShortURLCollection(self):
        return self.database.shorturls
