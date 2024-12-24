# Repositories Reasoner

[![CI](https://github.com/dzhovi/repositories-reasoner/actions/workflows/ci.yml/badge.svg)](https://github.com/dzhovi/repositories-reasoner/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/dzhovi/repositories-reasoner/badge.svg?branch=main)](https://coveralls.io/github/dzhovi/repositories-reasoner?branch=main)
[![License](https://img.shields.io/badge/license-MIT-green.svg)]
(https://github.com/dzhovi/repositories-reasoner/blob/main/LICENSE.txt)
[![Known Vulnerabilities](https://snyk.io/test/github/dzhovi/repositories-reasoner/badge.svg)]
(https://snyk.io/test/github/dzhovi/repositories-reasoner)

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
