import os

from app import app
from flask import render_template
from flask import request, redirect, abort
from models.urlshortener import urlShortener


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/UrlShorten', methods=['POST', 'GET'])
def shortenUrl():
    if request.method == 'POST':
        url = request.form['url']
        url_shortener_handler = urlShortener()

        #TODO have a mechanism for handling duplicate key error
        short_url = url_shortener_handler.generateShortUrl()

        if url_shortener_handler.saveUrl(short_url, url):
            # TODO move the site_prefix to a config file
            site_url = os.environ['SITE_URL']
            return render_template('index.html', shortURL=site_url+short_url)
        else:
            #TODO change this to temporary error message
            return render_template('index.html', shortURL=None)
    else:
        return redirect('/')


@app.route('/<shorturl>')
def getURL(shorturl):

    url_shortener_handler = urlShortener()
    url = url_shortener_handler.findUrl(shorturl)

    app.logger.debug("value of url is %s", url)

    if url is not None:
        return redirect(url, code=302)
    else:
        return abort(404)


#@app.errorhandler(404)
#def page_not_found(error):
#    return render_template('page_not_found.html'), 404
