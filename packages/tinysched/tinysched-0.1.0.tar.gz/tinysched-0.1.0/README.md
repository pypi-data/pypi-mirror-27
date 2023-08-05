# tinysched

This library provides a simple, dependency-free interface to run a single function in the background, repeatedly, at a specified interval.  The function invocations are serial, and executed in a single thread.

It's really just a little extension for the built-in [sched](https://docs.python.org/3/library/sched.html#sched.scheduler) module.

[![CircleCI](https://circleci.com/gh/dbjohnson/tinysched.svg?style=shield)](https://circleci.com/gh/dbjohnson/tinysched)
[![PyPi](https://img.shields.io/pypi/v/tinysched.svg)](https://pypi.python.org/pypi/tinysched)
[![Maintainability](https://api.codeclimate.com/v1/badges/f23e49426a5af346f634/maintainability)](https://codeclimate.com/github/dbjohnson/tinysched/maintainability)
[![License](https://img.shields.io/github/license/dbjohnson/tinysched.svg)]()

## Installation
```pip install tinysched```

## Usage

```python
from tinysched import scheduler
from datetime import timedelta


def foo():
    print('foo!')


cancel_fn = scheduler.repeat(foo, interval=timedelta(seconds=0.1), max_repeats=10) 

```
