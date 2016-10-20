import pkgutil
import unittest2


def all_names():
    for _, modname, _ in pkgutil.iter_modules(__path__):
        if modname.startswith('test_'):
            yield 'rbcz.test.' + modname


def all():
    return unittest2.defaultTestLoader.loadTestsFromNames(all_names())
