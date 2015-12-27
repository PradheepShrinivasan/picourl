import unittest
import pymongo

from user_database import UserDatabase


class TestUser(unittest.TestCase):
    def get_user_collection(self):
        return self.collection

    def setUp(self):
        connection = pymongo.MongoClient('mongodb://localhost:27017/')
        self.database = connection.test
        self.collection = self.database.user
        self.collection.drop()
        self.user = UserDatabase()

        # monkey patch the mongodb handler to use the test database of user
        from MongodbHandler import MongoDatabaseHandler

        MongoDatabaseHandler.get_users_collection = self.get_user_collection

    def test_insert_user(self):
        """save a valid user to the database """
        user = 'testuser@gmail.com'
        password = 'testpassword'

        result = self.user.save_user(user, password)

        self.assertEqual(result, True)
        # read the user from database
        doc = self.collection.find_one({'_id': user})
        self.assertEqual(doc, {'_id': user, 'password': password})

        self.collection.delete_one({'_id': user})

    def test_insert_duplicateuser(self):
        """" save the user twice and that we return a false"""

        user = 'duplicatetestuser'
        password = 'duplicatetestuserpassword'
        password2 = 'duplicatetestuserpassword2'
        _ = self.user.save_user(user, password)

        result = self.user.save_user(user, password2)

        self.assertEqual(result, False)

        self.collection.delete_one({'_id': user})

    def test_remove_user(self):
        user = 'removeuser'
        password = 'removeuserpassword'
        self.user.save_user(user, password)

        result = self.user.delete_user(user)

        self.assertEqual(result, True)
        doc = self.collection.find_one({'_id': user})
        self.assertEqual(doc, None)

    def test_remove_non_existing_user(self):
        user = 'dummyuser'

        result = self.user.delete_user(user)

        self.assertEqual(result, False)

    def test_get_user(self):
        user = 'myuser'
        password = 'mypassword'
        self.user.save_user(user, password)

        result = self.user.get_password(user)

        self.assertEqual(result, password)

        self.collection.delete_one({'_id': user})

    def test_get_user_non_existing(self):
        result = self.user.get_password('nonExistingUser')

        self.assertEqual(result, None)
