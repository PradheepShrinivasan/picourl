import pymongo
import datetime
from app.models.mongodbhandler import MongoDatabaseHandler


class UserDatabase(object):
    def __init__(self):
        """ save the username and password """
        databaseHandler = MongoDatabaseHandler()
        self.collection = databaseHandler.get_users_collection()

    def get_password(self, username):
        """ get password from a given username """
        doc = self.collection.find_one({'_id': username}, {'_id': 0, 'password': 1})
        if doc is None:
            return None
        return doc['password']

    def save_user(self, username, password):
        """save the username and password to the database
            return false if trying to add the same user again
        """
        try:
            self.collection.insert_one({'_id': username, 'password': password, 'date':datetime.datetime.now()})
        except pymongo.errors.DuplicateKeyError:
            return False

        return True

    def delete_user(self, username):
        """  delete the user given an username  """

        result = self.collection.delete_one({'_id': username})
        if result.deleted_count:
            return True
        else:
            return False



