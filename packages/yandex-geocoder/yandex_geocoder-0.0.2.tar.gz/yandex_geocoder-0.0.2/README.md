Yandex Geocoder
===
Get address coordinates via Yandex geocoder

[![Build Status](https://travis-ci.org/cryptomaniac512/yandex-geocoder.svg?branch=master)](https://travis-ci.org/cryptomaniac512/yandex-geocoder)
[![Coverage Status](https://coveralls.io/repos/github/cryptomaniac512/yandex-geocoder/badge.svg?branch=master)](https://coveralls.io/github/cryptomaniac512/yandex-geocoder?branch=master)
![Python versions](https://img.shields.io/badge/python-3.5,%203.6-blue.svg)
[![PyPi](https://img.shields.io/badge/PyPi-0.0.2-yellow.svg)](https://pypi.python.org/pypi/yandex-geocoder)

Installation
---
Install it via `pip` tool:

``` shell
pip install yandex-geocoder
```

Usage example
---

``` python
from yandex_geocoder import Client
Client.coordinates('Хабаровск 60 октября 150')  # ('135.114326', '48.47839')
```

Credits
---
- [f213](https://github.com/f213)
