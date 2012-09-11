#!/usr/bin/env python
import sys
from tests.shared import unittest

if __name__ == '__main__':
    failfast = False
    if '--xml' in sys.argv:
        import xmlrunner
        runner = xmlrunner.XMLTestRunner(output='test-results')
        sys.argv.remove('--xml')
    else:
        if '--ff' in sys.argv:
            failfast=True
            sys.argv.remove('--ff')
        runner = unittest.TextTestRunner(failfast=failfast)
    loader = unittest.TestLoader()
    runner.run(loader.discover('tests/', top_level_dir='.'))
