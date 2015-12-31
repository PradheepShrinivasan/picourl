
from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

CsrfProtect(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'my secret key'


from app import views
