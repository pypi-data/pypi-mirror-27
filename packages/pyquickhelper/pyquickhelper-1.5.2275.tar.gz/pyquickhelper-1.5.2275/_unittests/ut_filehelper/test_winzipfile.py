"""
@brief      test log(time=2s)
@author     Xavier Dupre
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
from src.pyquickhelper.filehelper.winzipfile import WinZipFile


class TestWinZipFile(unittest.TestCase):

    def test_winzipfile(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        this = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(this, "data", "loghelper.zip")
        nb = 0
        with WinZipFile(data, "r") as f:
            names = f.infolist()
            for name in names:
                self.assertIn("/", name.filename)
                c = f.read(name.filename)
                if len(c) == 0 and not name.filename.endswith("/") and "__init__" not in name.filename:
                    raise Exception("empty file '{0}'".format(name.filename))
                nb += 1
        self.assertTrue(nb > 0)


if __name__ == "__main__":
    unittest.main()
