# PicoURL
![](https://travis-ci.org/PradheepShrinivasan/picourl.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/PradheepShrinivasan/picourl/badge.svg?branch=master&service=github)](https://coveralls.io/github/PradheepShrinivasan/picourl?branch=master)
[![Code Health](https://landscape.io/github/PradheepShrinivasan/picourl/master/landscape.svg?style=flat)](https://landscape.io/github/PradheepShrinivasan/picourl/master)

A PicoURL is a URL shortener written in python using Flask and pymongo.

I wanted to write a url shortener to improve my understanding of Flask and pymongo.

The code contains unit tests for all modules and also integration tests for all endpoints.

## Installation

1. To install the application clone the application using 

    ```
        git clone https://github.com/PradheepShrinivasan/picourl.git
    ```
2. Install the required python dependencies using

    ```
        pip install requirements.txt
    ```
3. Install mongodb using the following commands as mentioned in [mongodb  documentation](https://docs.mongodb.org/manual/installation/)


## Configuration
Picourl allows configuration of the following variables in `config.py`
  ```
  PORT              - the port to listen to(default 5000)
  CONNECTION_STRING - the mongodb string to connect(default is mongodb://localhost:27017/)
  SITE_URL          - the site prefix in url shortener (default is localhost)
  ```
  
## Starting application

To run the application go to the cloned folder and run it using

    ```
        python run.py
    ```
    
if you have used the default configuration the system must be listening in port `5000` and you can access it by using
    `http://localhost:5000`
    
The application screen should something like below 

![image](https://raw.githubusercontent.com/PradheepShrinivasan/picourl/images/picourl.jpg)

And logged in page looks like below 

![image](https://raw.githubusercontent.com/PradheepShrinivasan/picourl/images/picourl_logged_in.png)

one can look at the site hosted at heroku [http://picourl.herokuapp.com/](http://picourl.herokuapp.com/)
## Documentation
  The discussion on  design and  configuration are available in blog post [1](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/03/UrlShortener_in_python_Part_1/),[2](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/06/UrlShortener_in_python_Part_2/),[3](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/06/UrlShortener_in_python_Part_3/) [4](http://pradheepshrinivasan.github.io/mongodb/python/flask/pymongo/2015/12/17/UrlShortener_in_python_Part_4/)

## Releases

0.1 - Basic working code with storage to backend mongodb and redirect on using shortURL

0.2 - Added UI and form validation using csrf tokens. 

0.3 - Added support to show the users clicked 7 urls.

## LICENCE

The software is provided in BSD licence, see LICENCE file for more details.

