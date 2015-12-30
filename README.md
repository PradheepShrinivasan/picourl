# PicoURL
![](https://travis-ci.org/PradheepShrinivasan/picourl.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/PradheepShrinivasan/picourl/badge.svg?branch=master&service=github)](https://coveralls.io/github/PradheepShrinivasan/picourl?branch=master)
[![Code Health](https://landscape.io/github/PradheepShrinivasan/picourl/master/landscape.svg?style=flat)](https://landscape.io/github/PradheepShrinivasan/picourl/master)

A PicoURL is a URL shortener written in python using Flask and pymongo.

I wanted to write a url shortener to improve my understanding of Flask and pymongo.

The code contains unit tests for all modules and also integration tests for all endpoints.


## Configuration
Picourl allows configuration of the following variables in `config.py`
  ```
  PORT              - the port to listen to(default 5000)
  CONNECTION_STRING - the mongodb string to connect(default is mongodb://localhost:27017/)
  SITE_URL          - the site prefix in url shortener (default is localhost)
  ```
  
## Documentation
  The discussion on  design and  configuration are available in blog post [1](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/03/UrlShortener_in_python_Part_1/),[2](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/06/UrlShortener_in_python_Part_2/),[3](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/06/UrlShortener_in_python_Part_3/) 

## Releases

0.1 - Basic working code with storage to backend mongodb and redirect on using shortURL

## LICENCE

The software is provided in BSD licence, see LICENCE file for more details.

