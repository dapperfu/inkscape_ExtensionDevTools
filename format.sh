#!/usr/bin/env bash

black --target-version py38 *.py
reorder-python-imports --py38-plus *.py
