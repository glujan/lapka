# Łapka

Apka pomagająca przeglądać i adoptować zwierzaki ze schronisk :heart_eyes: 
:dog: :cat:


## Środowisko deweloperskie

Ten projekt wymaga Pythona 3.6. Do zarządzania zainstalowanymi wersjami języka
polecam korzystać z [pyenv](https://github.com/yyuu/pyenv). Po tym jak już
zainstalujesz _pyenv_ należy wykonać poniższe _zaklęcia_:

```bash
ENV_NAME=lapka  # lub dowolna inna nazwa
PY36=3.6.0
pyenv install 3.6.0
pyenv virtualenv $ENV_NAME $PY36       # tworzy virtualenva dla projektu
pyenv local $PY36/env/$ENV_NAME $PY36  # ustawia obie wersje jako lokalne,
                                       # pierwsza dla ciebie, druga dla toxa
pip install -r requirements-dev.txt -r requirements.txt
```

Testy, pokrycie testami i linter są odpalane z użyciem narzędzia _Tox_. Po
prostu wpisz komendę `tox` będąc w katalogu głównym projektu i podziwiaj
wyniki.
