# The MIT License (MIT)
#
# Copyright (c) 2024 Vakhidov Dzhovidon
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

.SHELLFLAGS: -e -o pipefail -c
.ONESHELL:
.PHONY: install test check release
.SILENT:

## The shell to use.
SHELL := bash

# Install required dependencies.
install:
	python3 -m pip install --upgrade pip
	python3 -m pip install pytest pylint
	pip install -r requirements.txt
	pip install twine

# Run pytest.
test:
	export PYTHONPATH=.
	pip install .
	python3 -m pytest tests

cov:
	export PYTHONPATH=.
	pip install .
	python3 -m pytest tests --cov --cov-fail-under=40

check:
	python3 -m pylint '*.py'

# Release package to PyPI.
release:
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/*