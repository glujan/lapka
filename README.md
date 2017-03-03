[![Build Status](https://travis-ci.org/glujan/lapka.svg?branch=master)](https://travis-ci.org/glujan/lapka)
[![Coverage](https://codecov.io/gh/glujan/lapka/branch/master/graph/badge.svg)](https://codecov.io/gh/glujan/lapka)
[![Aww cat](https://img.shields.io/badge/aww-cat-brightgreen.svg)](http://i.imgur.com/8dX8Qv2.mp4)
[![Lol cat](https://img.shields.io/badge/lol-cat-brightgreen.svg)](http://i.imgur.com/WM0GVKQ.mp4)
# Łapka

Łapka (pronounce as _ˈwapka_, Polish for _a paw_) is an app to help browse and
adopt animals from shelters :heart_eyes: :dog: :cat:

> Ten plik jest również dostępny [po polsku](README_pl.md).


## Development

This project requires Python 3.6. I recommend using [pyenv](https://github.com/yyuu/pyenv)
to manage Python versions installed on your system. And this is how to set up
your dev environment after installing _pyenv_:

```bash
ENV_NAME=lapka  # or any other name you like
PY36=3.6.0
pyenv install 3.6.0
pyenv virtualenv $ENV_NAME $PY36       # create a virtualenv for development
pyenv local $PY36/env/$ENV_NAME $PY36  # set both versions as your local Python
                                       # 1st for development, 2nd for Tox
pip install -r requirements-dev.txt -r requirements.txt
```

Tests, coverage and linter are run using _Tox_. Just type `tox` from the
project root directory and enjoy results.
