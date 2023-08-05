"""
@brief      test tree node (time=5s)
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
from src.pyquickhelper.pycode import clean_readme


class TestCleanReadme(unittest.TestCase):

    def test_write_script(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        fold = os.path.abspath(os.path.dirname(__file__))
        data = os.path.join(fold, "data", "aREADME.rst")
        with open(data, "r", encoding="utf-8") as f:
            content = f.read()
        clean = clean_readme(content)
        exp = """
                README
                ======


                .. image:: https://travis-ci.org/sdpython/mlstatpy.svg?branch=master
                    :target: https://travis-ci.org/sdpython/mlstatpy
                    :alt: Build status

                .. image:: https://ci.appveyor.com/api/projects/status/5env33qptorgshaq?svg=true
                    :target: https://ci.appveyor.com/project/sdpython/mlstatpy
                    :alt: Build Status Windows

                .. image:: http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/_images/nbcov.png
                    :target: http://www.xavierdupre.fr/app/mlstatpy/helpsphinx/all_notebooks_coverage.html
                    :alt: Notebook Coverage

                **Links:**

                * `GitHub/mlstatpy <https://github.com/sdpython/mlstatpy/>`_
                """.replace("                ", "").strip("\n ")
        self.assertEqual(clean.strip("\n "), exp)


if __name__ == "__main__":
    unittest.main()
