"""
@brief      test tree node (time=50s)
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

from src.pyquickhelper.loghelper import fLOG
from src.pyquickhelper.pycode import is_travis_or_appveyor
from src.pyquickhelper.pycode.venv_helper import run_base_script, is_virtual_environment


class TestVenvBase(unittest.TestCase):

    def test_run_base_script(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if is_travis_or_appveyor() == "travis":
            # no end on travis
            return

        this = os.path.abspath(__file__)
        this = os.path.join(os.path.dirname(
            this), "example_venv_base_simple.py")
        if is_virtual_environment():
            fLOG("virtual_environment")
            out = run_base_script(this, file=True, fLOG=fLOG)
        else:
            fLOG("no virtual_environment")
            out = run_base_script(this, file=True, fLOG=fLOG)
        if sys.version_info[0] == 2:
            if "(u'example_venv_base_simple.py', u'execution')" not in out:
                raise Exception(out)
        else:
            if "example_venv_base_simple.py execution" not in out:
                raise Exception(out)


if __name__ == "__main__":
    unittest.main()
