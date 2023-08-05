# tinysched

This library provides a simple, dependency-free interface to run a single function in the background, repeatedly, at a specified interval.  The function invocations are serial, and executed in a single thread.

It's really just a little extension for the built-in [sched](https://docs.python.org/3/library/sched.html#sched.scheduler) module.

[![License](https://img.shields.io/github/license/dbjohnson/tinysched.svg)]()
[![PyPi](https://img.shields.io/pypi/v/tinysched.svg)](https://pypi.python.org/pypi/tinysched)
[![Code Climate](https://codeclimate.com/github/dbjohnson/tinysched/badges/gpa.svg)](https://codeclimate.com/github/dbjohnson/tinysched)

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
