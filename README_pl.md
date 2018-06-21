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
pip install pipenv
pipenv install
pipenv install --dev
```

Testy, pokrycie testami, linter i inne skrypty są odpalane z użyciem narzędzia
_Tox_. Uruchom wszystkie testy wpisując po prostu komendę `tox` lub wybierz
interesujący cię skrpyt (poprzez `tox -e NAZWA`):

 * `py36` - uruchom testy jednostkowe i integracyjne, zmierz pokrycie testami,
 * `style` - sprawdź styl kodu i jego dokumentacji oraz złożoność cyklomatyczną,

Analogiczne korzystam z [nvm](https://github.com/creationix/nvm) do zarządzania
wersjami _Node.js_. Oto jak uruchomić testy dla JS:

```bash
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.1/install.sh | bash
NODE_VER=lts/boron
nvm install $NODE_VER
echo $NODE_VER > .nvmrc
nvm use
cd ui/
npm install  # instalacja nvm i Node'a kończy się tutaj
npm test     # zawsze uruchamiaj z katalogu ui/js
```
