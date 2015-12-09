# Contains all the configuration
import os

CONNECTION_URI = os.getenv('CONNECTION_STRING','mongodb://localhost:27017/')
SITE_URL = os.getenv('SITE_URL', 'http://localhost:5000')
PORT = os.getenv('PORT', 5000)