#!/bin/bash

# Define a variável de ambiente DATABASE_URL
export DATABASE_URL="sqlite:///test.db"

export PYTHONPATH=$(pwd)

# Executa os testes com pytest
pytest -vv --maxfail=1 --disable-warnings

# Limpa a variável de ambiente após os testes
unset DATABASE_URL
unset PYTHONPATH
