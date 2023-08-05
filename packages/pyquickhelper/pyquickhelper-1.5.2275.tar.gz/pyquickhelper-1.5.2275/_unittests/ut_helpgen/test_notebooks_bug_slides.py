"""
@brief      test log(time=30s)
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
from src.pyquickhelper.helpgen import process_notebooks
from src.pyquickhelper.helpgen.sphinx_main import setup_environment_for_help
from src.pyquickhelper.pycode import is_travis_or_appveyor, get_temp_folder


if sys.version_info[0] == 2:
    from codecs import open


class TestNoteBooksBugSlides(unittest.TestCase):

    def test_notebook_slides(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        if sys.version_info[0] == 2:
            # does not work on Python 2
            return
        path = os.path.abspath(os.path.split(__file__)[0])
        fold = os.path.normpath(os.path.join(path, "notebooks_slides"))
        nbs = [os.path.join(fold, _)
               for _ in os.listdir(fold) if ".ipynb" in _]
        formats = ["slides"]

        if is_travis_or_appveyor() in ('travis', 'appveyor'):
            return

        temp = get_temp_folder(__file__, "temp_nb_bug_slides")
        setup_environment_for_help()

        res = process_notebooks(nbs, temp, temp, formats=formats)
        fLOG("*****", len(res))
        for _ in res:
            fLOG(_)
            assert os.path.exists(_[0])

        with open(os.path.join(temp, "js_bokeh.slides.html"), "r", encoding="utf8") as f:
            content = f.read()
        exp = "is one if the most mature and complete library using javascript."
        if exp not in content:
            raise Exception(content)


if __name__ == "__main__":
    unittest.main()
