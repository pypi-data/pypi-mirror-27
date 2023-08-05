cookietransfer [![Build Status](https://travis-ci.org/terry-lim/cookietransfer.svg?branch=master)](https://travis-ci.org/terry-lim/cookietransfer) [![codecov](https://codecov.io/gh/terry-lim/cookietransfer/branch/master/graph/badge.svg)](https://codecov.io/gh/terry-lim/cookietransfer) [![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat-square)](LICENSE.txt)
=
The purpose of this package is to help transfer cookie data between Selenium webdriver and request session vice versa. This comes in handy when you need to use a browser to login but then don't really need the browser after that.

----------
Usage
=

*Transfer from request session to webdriver*
```python
import requests
from selenium import webdriver
from cookietransfer import cookietransfer


driver = webdriver.Chrome()
s = requests.Session()
url = 'http://testing-ground.scraping.pro/login?mode=login'
s.post(url, data={'usr': 'admin', 'pwd': '12345'})
cookietransfer(s, driver, url)
# logged in!
driver.get('http://testing-ground.scraping.pro/login?mode=welcome')
```
*Transfer from webdriver to request session*
```python
import requests
from selenium import webdriver
from cookietransfer import cookietransfer


s = requests.Session()
driver = webdriver.Chrome()
url = 'https://httpbin.org/cookies/set?name=stransfer&value=42'
s.get(url)
cookietransfer(s, driver, url)
driver.get('https://httpbin.org/cookies')
# cookie transfered
```

Installation
=
```python
pip install cookietransfer
```

Todo
=
* support Firefox