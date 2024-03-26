# 🍔 moku.blog
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Django](https://img.shields.io/badge/django-5.0-green?logo=django)](https://docs.djangoproject.com/en/5.0/)
[![Python version: >= 3.10](https://img.shields.io/badge/python-%3E%3D%203.12-blue)](https://docs.python.org/3.12/)
[![License](https://img.shields.io/github/license/m5ka/moku.blog)](LICENSE)
[![GitHub workflow status](https://img.shields.io/github/actions/workflow/status/m5ka/moku.blog/test.yaml?label=tests&logo=github)](https://github.com/m5ka/moku.blog/actions)

**moku.blog** is a small-web community for food enthusiasts.

## 🥐 behind the name
**moku** is the [toki pona](https://tokipona.org/) word for "food", "drink", "eat" or, really, anything to do with consuming. it comes from the japanese onomatopoeia [もぐもぐ](https://en.wiktionary.org/wiki/%E3%82%82%E3%81%90%E3%82%82%E3%81%90#Japanese) (_mogu-mogu_) which represents the sound of chewing.

## 🍕 contributing
it's great that you want to help out! a good place to start is checking in [issues](https://github.com/m5ka/moku.blog/issues) to see if what you're thinking about has already been discussed.

### pre-requisites
* python 3.12 and [poetry](https://python-poetry.org/)
* postgresql

### setting up the environment
the environment is all managed by poetry so it's pretty easy to get started once you have poetry set up.
```sh
poetry install --with dev,test
```

if you get an error about `psycopg2`, make sure you have the system package `libpq-dev` installed on your system.

### code-style
all our code is linted and formatted by [ruff](https://docs.astral.sh/ruff/) so it's important to make sure any changes you make are compliant.

```sh
poetry run ruff check .
poetry run ruff format --check .
```

if you want ruff to auto-format your code, you can use `poetry run ruff format .`

## 🧁 license
moku.blog's code is licensed under the [bsd 2-clause license](LICENSE), which more or less means you're free to do whatever you want with it so long as any copies or modifications you make are under the same license.