
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)

CSRFProtect(app)
Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.secret_key = 'my secret key'


from app import views
