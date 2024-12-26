# Repositories Reasoner

[![CI](https://github.com/dzhovi/repositories-reasoner/actions/workflows/ci.yml/badge.svg)](https://github.com/dzhovi/repositories-reasoner/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/repo-reasoner.svg)](https://pypi.org/project/repo-reasoner/)
[![Coverage Status](https://coveralls.io/repos/github/dzhovi/repositories-reasoner/badge.svg)](https://coveralls.io/github/dzhovi/repositories-reasoner)[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/dzhovi/repositories-reasoner/blob/main/LICENSE.txt)
[![Known Vulnerabilities](https://snyk.io/test/github/dzhovi/repositories-reasoner/badge.svg)](https://snyk.io/test/github/dzhovi/repositories-reasoner)

Repositories Reasoner is a command-line application that facilitates llm
capabilities to reason about different aspects
of repository.
Primary task that can be solved using repositories reasoner is to determine
whether repository maintained or not.

**Motivation**. During the work on [CaM](https://github.com/yegor256/cam)
project,
where we're building datasets with open source Java programs,
we [discovered](https://github.com/yegor256/cam/issues/297)
the need for filtering out repositories that not maintained. This repository
is portable command-line tool that filters those repositories.

## How to use

First, install it from [PyPI](https://pypi.org/project/repo-reasoner/0.0.6/) like that:

```bash
pip install repo-reasoner
```

then, execute:

```bash
repo-reasoner is-maintained --repository=author/repository_name --key=your_gigachat_api_key
```

For `--repository` you should provide a name of **existing** Github reposioty,
in a format `author/repository_name`. The result would be printed into stdout.
If `repo-reasoner` thinks that a given repository is maintained, it will answer `yes`,
and `no` otherwise.
If you feel missed, try `--help` and tool will explain to you what you should do.

## Limitations
In current implementation, you have no other options but gigachat as a llm.
