import os
import zope.testrunner
from sparc.testing.fixture import test_suite_mixin
from sparc.sa.testing import SPARC_SA_INTEGRATION_LAYER


class test_suite(test_suite_mixin):
    package = 'sparc.sa.engine'
    module = 'engine'
    layer = SPARC_SA_INTEGRATION_LAYER


if __name__ == '__main__':
    zope.testrunner.run([
                         '--path', os.path.dirname(__file__),
                         '--tests-pattern', os.path.splitext(
                                                os.path.basename(__file__))[0]
                         ])