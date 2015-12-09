#!flask/bin/python
import os

from app import app
from config import PORT

app.run(host='0.0.0.0', port=int(PORT),debug=True)
