"""
@brief      test log(time=8s)
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

from src.pyquickhelper.loghelper.flog import fLOG
from src.pyquickhelper.helpgen.utils_sphinx_config import ie_layout_html, locate_image_documentation, NbImage

from IPython.core.display import Image


class TestHelperHelpGen(unittest.TestCase):

    def test_ie_layout_html(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if sys.version_info[0] == 2:
            return
        ie_layout_html()

    def test_ie_layout_html2(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            return

        try:
            r = locate_image_documentation("completion.png")
            fLOG(r)
        except FileNotFoundError:
            pass

    def test_NbImage(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        r = NbImage("completion.png")
        assert isinstance(r, Image)


if __name__ == "__main__":
    unittest.main()
