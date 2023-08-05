"""
@brief      test log(time=4s)
@author     Xavier Dupre
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

from src.pyquickhelper.loghelper.flog import fLOG
from src.pyquickhelper.pycode import get_temp_folder
from src.pyquickhelper.helpgen import rst2html
from src.pyquickhelper.sphinxext import bigger_role
from docutils.parsers.rst.roles import register_canonical_role

if sys.version_info[0] == 2:
    from codecs import open


class TestBiggerExtension(unittest.TestCase):

    def test_post_parse_sn(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        register_canonical_role("bigger", bigger_role)

    def test_bigger(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            warnings.warn(
                "test_biffer not run on Python 2.7")
            return

        from docutils import nodes as skip_

        content = """
                    test a directive
                    ================

                    before

                    :bigger:`facebook`

                    after

                    this code shoud appear
                    """.replace("                    ", "")
        if sys.version_info[0] >= 3:
            content = content.replace('u"', '"')

        html = rst2html(content,  # fLOG=fLOG,
                        writer="html", keep_warnings=True,
                        directives=None)

        t1 = "this code shoud not appear"
        if t1 in html:
            raise Exception(html)

        t1 = "this code shoud appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "facebook"
        if t1 not in html:
            raise Exception(html)

        t1 = "linkedin"
        if t1 in html:
            raise Exception(html)

        t1 = '{1}'
        if t1 in html:
            raise Exception(html)

        t1 = "visit_sharenet_node"
        if t1 in html:
            raise Exception(html)

        temp = get_temp_folder(__file__, "temp_bigger")
        with open(os.path.join(temp, "out_bigger.html"), "w", encoding="utf8") as f:
            f.write(html)

    def test_bigger_inline(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        if sys.version_info[0] == 2:
            warnings.warn(
                "test_sharenet not run on Python 2.7")
            return

        from docutils import nodes as skip_

        content = """
                    test a directive
                    ================

                    abeforea :bigger:`facebook` aaftera
                    """.replace("                    ", "")
        if sys.version_info[0] >= 3:
            content = content.replace('u"', '"')

        html = rst2html(content,  # fLOG=fLOG,
                        writer="html", keep_warnings=True,
                        directives=None)

        t1 = "abeforea"
        if t1 not in html:
            raise Exception(html)

        t1 = "aftera"
        if t1 not in html:
            raise Exception(html)

        t1 = '{1}'
        if t1 in html:
            raise Exception(html)

        t1 = '<font size="4">facebook</font>'
        if t1 not in html:
            raise Exception(html)

        t1 = "visit_sharenet_node"
        if t1 in html:
            raise Exception(html)

        temp = get_temp_folder(__file__, "temp_bigger_inline")
        with open(os.path.join(temp, "out_bigger.html"), "w", encoding="utf8") as f:
            f.write(html)


if __name__ == "__main__":
    unittest.main()
