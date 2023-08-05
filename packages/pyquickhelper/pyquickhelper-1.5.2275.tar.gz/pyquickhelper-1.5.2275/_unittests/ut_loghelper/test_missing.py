"""
@brief      test tree node (time=1s)
"""


import sys
import os
import unittest

try:
    import src
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    import src

from src.pyquickhelper.loghelper.flog import fLOG, IsEmptyString
from src.pyquickhelper.loghelper.pqh_exception import PQHException


class TestMissing(unittest.TestCase):

    def test_exception(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        try:
            raise PQHException("error", True)
        except PQHException:
            pass

    def test_is_missing(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        assert IsEmptyString("")
        assert IsEmptyString(None)
        assert not IsEmptyString("-")


if __name__ == "__main__":
    unittest.main()
