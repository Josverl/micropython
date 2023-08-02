# Testing mpremote

## Create and activate a virtual environment

Starting in the project root folder

`python -m venv .venv`

Activate the environment

* Linux/MacOS: `source .venv/bin/activate`
* Windows:  `.venv\Scripts\activate.ps1`

## Install testing dependencies

`pip install ./tools/mpremote[dev,test]`

## Install the mpremote tool in editable mode

`pip install -e ./tools/mpremote`

## Run the test suite

`pytest` using config from pyproject.toml

or explicitly

`pytest tools/tests`
