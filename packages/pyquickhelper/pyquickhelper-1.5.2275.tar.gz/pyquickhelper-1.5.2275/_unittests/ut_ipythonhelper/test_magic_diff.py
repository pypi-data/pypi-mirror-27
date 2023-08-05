"""
@brief      test log(time=1s)
"""


import sys
import os
import unittest
import warnings


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
from src.pyquickhelper.ipythonhelper.magic_class_diff import MagicDiff


class TestMagicDiff(unittest.TestCase):

    def test_textdiff(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            warnings.warn("disable on python 2.7")
            return

        from IPython.core.display import Javascript
        mg = MagicDiff()
        mg.add_context(
            {"f1": "STRING1\nSTRING2", "f2": "STRING1\nSTRING3"})
        cmd = "f1 f2"
        res = mg.textdiff(cmd)
        assert isinstance(res, Javascript)


if __name__ == "__main__":
    unittest.main()
