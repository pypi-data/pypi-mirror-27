#!/bin/bash

mypy cli_pipeline/__init__.py

pip install --ignore-installed --no-cache -e .

pipeline version
