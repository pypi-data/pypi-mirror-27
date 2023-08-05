"""
@brief      test log(time=3s)
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

from src.pyquickhelper.ipythonhelper.notebook_helper import install_python_kernel_for_unittest
from src.pyquickhelper.ipythonhelper import run_notebook
from src.pyquickhelper.pycode import get_temp_folder
from src.pyquickhelper.loghelper import fLOG
from src.pyquickhelper.pycode import is_travis_or_appveyor


class TestNotebookRunnerEmpty (unittest.TestCase):

    def test_notebook_runner_empty(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if sys.version_info[0] == 2:
            # written in Python 3
            return
        temp = get_temp_folder(__file__, "temp_notebook_empty")
        nbfile = os.path.join(
            temp,
            "..",
            "data",
            "td2a_cenonce_session_4B.ipynb")
        assert os.path.exists(nbfile)
        addpath = os.path.normpath(os.path.join(temp, "..", "..", "..", "src"))
        assert os.path.exists(addpath)

        kernel_name = None if is_travis_or_appveyor() is not None else install_python_kernel_for_unittest(
            "pyquickhelper")

        outfile = os.path.join(temp, "out_notebook.ipynb")
        assert not os.path.exists(outfile)
        out = run_notebook(nbfile, working_dir=temp, outfilename=outfile,
                           additional_path=[addpath], fLOG=fLOG,
                           kernel_name=kernel_name)
        fLOG(out)
        assert os.path.exists(outfile)
        assert "No module named 'pyquickhelper'" not in out


if __name__ == "__main__":
    unittest.main()
