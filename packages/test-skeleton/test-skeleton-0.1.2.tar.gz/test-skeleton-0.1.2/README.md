# test-skeleton

[![Build Status](https://travis-ci.org/jerry-git/test-skeleton.svg?branch=master)](https://travis-ci.org/jerry-git/test-skeleton)
[![Pypi](https://img.shields.io/pypi/v/test-skeleton.svg)](https://pypi.python.org/pypi/test-skeleton)
[![Py vers](https://img.shields.io/pypi/pyversions/test-skeleton.svg)](https://pypi.python.org/pypi/test-skeleton)

A tool for creating a skeleton for Python unit tests based on source code.

Basically, this is a tool for non-TDD development. Use TDD if possible.

A potential use case for this tool could e.g. a legacy project which lacks tests.


## Usage
```bash
python -m test_skeleton path/to/your/source_file.py
```

The result will be printed to std out. If you want to store it into a file, use `--save` flag. The result will be stored into test_<original_filename> in your current working directory. 


## Example

Input:
```python
class Klass(object):
    klass_var = ''

    def __init__(self):
        self.a = ''

    @property
    def property1(self):
        pass

    @classmethod
    def klassmethod1(cls):
        pass

    def method_with_under_scores(self):
        pass


def helper_function1():
    pass

```
Output:
```python
class TestKlass:
    class TestProperty1:
        def test_TODO(self):
            pass

    class TestKlassmethod1:
        def test_TODO(self):
            pass

    class TestMethodWithUnderScores:
        def test_TODO(self):
            pass


class TestHelperFunction1:
    def test_TODO(self):
        pass

```
