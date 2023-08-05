"""
@brief      test log(time=2s)
"""

import sys
import os
import unittest

if "temp_" in os.path.abspath(__file__):
    raise ImportError(
        "this file should not be imported in that location: " +
        os.path.abspath(__file__))

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
from src.pyquickhelper.filehelper import FileTreeNode
from src.pyquickhelper.helpgen.utils_sphinx_doc import filecontent_to_rst, replace_relative_import


class TestFileNodeTree(unittest.TestCase):

    def test_file_tree_node(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        this = os.path.abspath(os.path.dirname(__file__))
        folder = os.path.normpath(os.path.join(this, "..", "..", "src"))

        def filter(root, path, f, d):
            return "__pycache__" not in path and "__pycache__" not in f

        ftn = FileTreeNode(folder, fLOG=fLOG, log=True, log1=True,
                           filter=filter)
        if len(ftn) == 2:
            raise Exception("%d" % len(ftn))
        nb = 0
        nrst = 0
        for f in ftn:
            if f.isfile():
                hash = f.hash_md5_readfile()
                s = str(f)
                assert len(s) > 0
                assert len(hash) > 0
                nb += 1
                if nb > 15:
                    break

                if "__init__" not in f.name and ".py" in f.name and ".pyc" not in f.name:
                    content = f.get_content()
                    rst = filecontent_to_rst(f.fullname, content)
                    contr, doc = rst
                    nrst += 1
                    assert "no documentation" not in doc
                    assert ".. _f-" in contr

                    cont2 = replace_relative_import(f.fullname)
                    lines = cont2.split("\n")
                    condition = "# replace # from ." in cont2
                    if not condition:
                        for line in lines:
                            if "from ." in line and "import" in line:
                                if sys.version_info[0] == 2:
                                    if "from __future__ " not in cont2:
                                        raise Exception(cont2)
                                else:
                                    raise Exception(
                                        "{0}\nLINE:\n{1}\nCONT:\n{2}".format(f.fullname, line, cont2))

        assert nb > 0
        assert nrst > 0


if __name__ == "__main__":
    unittest.main()
