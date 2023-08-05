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
from src.pyquickhelper.helpgen.sphinx_main import generate_changes_repo

if sys.version_info[0] == 2:
    from codecs import open


class TestChanges (unittest.TestCase):

    def test_changes(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        path = os.path.abspath(os.path.split(__file__)[0])
        fold = os.path.join(path, "..", "..")
        if sys.version_info[0] == 2:
            fold = os.path.join(fold, "..")
        fold = os.path.normpath(fold)
        if os.path.exists(fold):
            fLOG("exists", fold)
            file = os.path.join(path, "out_table.rst")
            if os.path.exists(file):
                os.remove(file)

            if sys.version_info[0] == 2:
                # encoding, encoding...
                return

            def modifiy_commit(nbch, date, author, comment):
                return nbch, date, author, comment

            generate_changes_repo(file, fold)
            with open(file, "r", encoding="utf8") as f:
                content = f.read()
            self.assertIn(".. plot::", content)
            content = content[
                content.find("List of recent changes:"):]
            self.assertTrue(len(content) > 0)
            self.assertIn(":widths: auto", content)
        else:
            fLOG(
                "sorry, fixing a specific case on another project for accent problem")


if __name__ == "__main__":
    unittest.main()
