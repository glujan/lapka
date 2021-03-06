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
pip install pipenv
pipenv install
pipenv install --dev
```

Tests, coverage, linter and other are run using _Tox_. Run all environments by
typing `tox` or choose a specific one (with `tox -e NAME`):

 * `py36` - run unit and integration tests, measure coverage,
 * `style` - check code and docs style, cyclomatic complexity,

Similary, I'm using [nvm](https://github.com/creationix/nvm) to manage
_Node.js_ versions. This is how to run JS tests:

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
NODE_VER=lts/boron
nvm install $NODE_VER
echo $NODE_VER > .nvmrc
nvm use
cd ui/
npm install  # setup of nvm and Node ends here
npm test     # run this inside ui/js directory
```
