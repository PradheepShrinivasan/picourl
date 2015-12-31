
from app import app, login_manager
from app.login_form import LoginForm
from app.register_form import RegisterForm
from app.logout_form import LogoutForm
from app.shorturl_form import ShortURLForm

from flask import render_template, request, redirect, abort, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required

from models.urlshortener import urlShortener
from user import User
from config import SITE_URL


@app.route('/', methods=['post', 'get'])
@app.route('/index', methods=['post', 'get'])
def index():

    login_form = LoginForm()
    logout_form = LogoutForm()
    short_url_form = ShortURLForm()
    register_form = RegisterForm()
    short_url = None

    if request.method == 'POST' and short_url_form.validate():
        url = short_url_form.url.data
        url_shortener_handler = urlShortener()

        app.logger.debug('in post method to shorten Url(%s)', url)

        # TODO have a mechanism for handling duplicate key error
        short_url = url_shortener_handler.generateShortUrl()

        if url_shortener_handler.saveUrl(short_url, url):
            app.logger.debug('value of short url(%s) for url is (%s)', short_url, url)
            short_url=SITE_URL + '/' + short_url
        else:
            app.logger.critical('Error in saving short url(%s) for url is (%s)', short_url, url)
            flash('Internal error try again')

    return render_template('index.html',
                           login_form=login_form,
                           logout_form=logout_form,
                           shorturl_form=short_url_form,
                           register_form=register_form,
                           shortURL=short_url)


@app.route('/<shorturl>')
def getURL(shorturl):
    """  Given a short url, the code looks up the short url in database
         and if found redirects to the long url path.
         if not found sends a 404 page not found.
    """
    url_shortener_handler = urlShortener()
    url = url_shortener_handler.findUrl(shorturl)

    app.logger.debug('value of url is %s', url)

    if url is not None:
        return redirect(url, code=302)
    else:
        return abort(404)


@app.route('/login', methods=['POST', 'GET'])
def login():
    """" handles all user login handling """

    app.logger.debug('Inside Login form')

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        app.logger.debug('Post menthod recieved and form validated')

        login_user(User.getuser(login_form.email.data))
        nexturl = request.args.get('next')
        return redirect(nexturl or url_for('index'))

    return redirect(url_for('index'))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """ Logout user when he is done """
    app.logger.debug("Inside logout with request method(%s)", request.method)

    if request.method == 'POST':
        user = current_user
        user.authenticated = False
        app.logger.debug("Logged out user %s", user.email)
        flash('Logout Successful')
        logout_user()
    else:
        flash('User is not logged in. Login again')

    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    """ handles user registration """

    app.logger.debug('registering user')

    form = RegisterForm(request.form)
    if form.validate():
        app.logger.debug('The user name(%s) and password(%s) ', form.email.data, form.password.data)
        user = User(form.email.data, form.password.data)
        if user.add_user():
            login_user(user)
            flash('Thanks for registering')
        else:
            flash('User already registered.Try login')

    return redirect(url_for('index'))




@login_manager.user_loader
def user_loader(user_id):
    """  Loads ther user when needed for Login """
    app.logger.debug("Loading user")
    return User.getuser(user_id)

# @app.errorhandler(404)
# def page_not_found(error):
#    return render_template('page_not_found.html'), 404
