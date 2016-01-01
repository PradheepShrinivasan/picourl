# import things
from flask_table import Table, Col

# Declare your table
class UserURLCollection(Table):
    classes = ['table']
    serialNo = Col('#')
    shortURL = Col('Short URL')
    LongURL = Col('Long URL')
    clicks = Col('Clicks')


# Get some objects
class urlcollection(object):
    def __init__(self, sno, short_url, url, clicks):
        self.serialNo = sno
        self.shortURL = short_url
        self.LongURL = url
        self.clicks = clicks

    @classmethod
    def create_collection(cls, iterator):
        url_list = []
        count = 1
        for document in iterator:
            url_list.append(urlcollection(count, document['_id'], document['longurl'], document['clicks']))
            count += 1

        return UserURLCollection(url_list)


# urlcollection = [urlcollection('1', 'Name1', 'Description1', 1),
#          urlcollection('2', 'Name2', 'Description2', 2),
#          urlcollection('3', 'Name3', 'Description3', 3),
#          urlcollection('4', 'Name1', 'Description1', 1),
#          urlcollection('5', 'Name2', 'Description2', 2),
#          urlcollection('6', 'Name3', 'Description3', 3)]
#
#
# # Or, more likely, load items from your database with something like
# # items = ItemModel.query.all()
#
# # Populate the table
# table = UserURLCollection(urlcollection)
#
# # Print the html
# # print(table.__html__())
