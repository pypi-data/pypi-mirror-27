"""
@brief      test log(time=5s)
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

from src.pyquickhelper.ipythonhelper.notebook_helper import remove_execution_number
from src.pyquickhelper.filehelper import change_file_status
from src.pyquickhelper.pycode import get_temp_folder, is_travis_or_appveyor
from src.pyquickhelper.loghelper import fLOG


class TestNotebookNumber(unittest.TestCase):

    def test_notebook_number(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        temp = get_temp_folder(__file__, "temp_notebook_number")
        nbfile = os.path.join(temp, "..", "data", "simple_example.ipynb")
        self.assertTrue(os.path.exists(nbfile))
        outfile = os.path.join(temp, "out_nb.ipynb")
        res = remove_execution_number(nbfile, outfile)
        self.assertTrue(res is not None)
        self.assertTrue(os.path.exists(outfile))
        self.assertTrue('"execution_count": null' in res)
        if is_travis_or_appveyor() == "appveyor":
            change_file_status(outfile)
            change_file_status(temp, strict=True)
        else:
            warnings.warn(
                "linux, unable to test change_file_status: TestNotebookNumber.test_notebook_number")


if __name__ == "__main__":
    unittest.main()
