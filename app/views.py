from os import urandom

from app import app, login_manager
from app.login_form import LoginForm
from app.register_form import RegisterForm

from flask import render_template, request, redirect, abort, flash, url_for, session
from flask_login import login_user, logout_user, current_user, login_required

from models.urlshortener import urlShortener
from user import User
from config import SITE_URL



@app.route('/')
@app.route('/index')
def index():
    return redirect('/urlshorten')


@app.route('/urlshorten', methods=['POST', 'GET'])
def shortenUrl():

    login_form = LoginForm()
    if request.method == 'POST':
        url = request.form['url']

        url_shortener_handler = urlShortener()

        app.logger.debug('in post method to shorten Url(%s)', url)
        # TODO have a mechanism for handling duplicate key error
        short_url = url_shortener_handler.generateShortUrl()

        if url_shortener_handler.saveUrl(short_url, url):
            app.logger.debug('value of short url(%s) for url is (%s)', short_url, url)
            return render_template('index.html', login_form = login_form, shortURL=SITE_URL + '/' + short_url )
        else:
            app.logger.critical('Error in saving short url(%s) for url is (%s)', short_url, url)
            flash('Internal error try again')
            return render_template('index.html', login_form = login_form, shortURL = None)
    else:
        return render_template('index.html', login_form = login_form, shortURL = None)


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

    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        login_user(User.getuser(login_form.email.data))
        nexturl = request.args.get('next')
        return redirect(nexturl or url_for('index'))

    return redirect(url_for('index'))


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    """ Logout user when he is done """

    if request.method == 'POST':
        session.pop('email', None)
        user = current_user
        user.authenticated = False
        logout_user()

    redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """ handles user registration """

    app.logger.debug('registering user')

    form = RegisterForm(request.form)
    if request.method == 'POST':
        app.logger.debug('The user name(%s) and password(%s) ', form.email.data, form.password.data)
        user = User(form.email.data, form.password.data)
        if user.add_user():
            flash('Thanks for registering')
        else:
            flash('User already registered.Try login')

        return redirect(url_for('index'))

    return render_template('register.html', form=form)



@login_manager.user_loader
def user_loader(user_id):
    app.logger.debug("Loading user")
    return User.getuser(user_id)


"""
@login_manager.request_loader
def load_user(request):
    token = request.headers.get('Authorization')
    if token is None:
        token = request.args.get('token')

    if token is not None:
        username,password = token.split(":") # naive token
        user_entry = User.getuser(username)
        if (user_entry is not None) and user_entry.checkpassword(password):
                return user_entry
    return None
"""


#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('page_not_found.html'), 404
