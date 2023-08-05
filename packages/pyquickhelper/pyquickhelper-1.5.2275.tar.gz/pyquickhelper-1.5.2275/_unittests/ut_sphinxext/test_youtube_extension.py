"""
@brief      test log(time=4s)
@author     Xavier Dupre
"""

import sys
import os
import unittest
import logging
from docutils.parsers.rst import directives
from sphinx.util.logging import getLogger

if sys.version_info[0] == 2:
    from StringIO import StringIO
else:
    from io import StringIO


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
from src.pyquickhelper.sphinxext import YoutubeDirective
from src.pyquickhelper.sphinxext.sphinx_youtube_extension import youtube_node, visit_youtube_node, depart_youtube_node


if sys.version_info[0] == 2:
    from codecs import open


class TestYoutubeExtension(unittest.TestCase):

    def test_post_parse_sn_youtube(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        directives.register_directive("youtube", YoutubeDirective)

    def test_youtube(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from docutils import nodes as skip_

        content = """
                    test a directive
                    ================

                    before

                    .. youtube:: https://www.youtube.com/watch?v=vSchPGmtikI

                    this code shoud appear___

                    after
                    """.replace("                    ", "")
        if sys.version_info[0] >= 3:
            content = content.replace('u"', '"')

        tives = [("youtube", YoutubeDirective, youtube_node,
                  visit_youtube_node, depart_youtube_node)]

        html = rst2html(content, writer="custom",
                        keep_warnings=True, directives=tives)

        temp = get_temp_folder(__file__, "temp_youtube")
        with open(os.path.join(temp, "out_todoext.html"), "w", encoding="utf8") as f:
            f.write(html)

        t1 = "this code shoud appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "embed/https:"
        if t1 in html:
            raise Exception(html)

        t1 = "https://www.youtube.com/embed/vSchPGmtikI"
        if t1 not in html:
            raise Exception(html)

    def test_youtube_size(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from docutils import nodes as skip_

        content = """
                    test a directive
                    ================

                    before

                    .. youtube:: https://www.youtube.com/watch?v=vSchPGmtikI
                        :width: 300

                    this code shoud appear___

                    after
                    """.replace("                    ", "")
        if sys.version_info[0] >= 3:
            content = content.replace('u"', '"')

        tives = [("youtube", YoutubeDirective, youtube_node,
                  visit_youtube_node, depart_youtube_node)]

        html = rst2html(content, writer="custom",
                        keep_warnings=True, directives=tives)

        temp = get_temp_folder(__file__, "temp_youtube_size")
        with open(os.path.join(temp, "out_todoext.html"), "w", encoding="utf8") as f:
            f.write(html)

        t1 = "this code shoud appear"
        if t1 not in html:
            raise Exception(html)

        t1 = "after"
        if t1 not in html:
            raise Exception(html)

        t1 = "embed/https:"
        if t1 in html:
            raise Exception(html)

        t1 = "https://www.youtube.com/embed/vSchPGmtikI"
        if t1 not in html:
            raise Exception(html)

    def test_youtube_size_warning(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        from docutils import nodes as skip_

        content = """
                    test a directive
                    ================

                    before

                    .. youtube:: https://www.youtube.com/watch?g=vSchPGmtikI
                        :width: 300

                    this code shoud appear___

                    after
                    """.replace("                    ", "")
        if sys.version_info[0] >= 3:
            content = content.replace('u"', '"')

        tives = [("youtube", YoutubeDirective, youtube_node,
                  visit_youtube_node, depart_youtube_node)]

        logger = getLogger("youtube")
        log_capture_string = StringIO()
        ch = logging.StreamHandler(log_capture_string)
        ch.setLevel(logging.DEBUG)
        logger.logger.addHandler(ch)

        rst2html(content, writer="custom",
                 keep_warnings=True, directives=tives)

        lines = log_capture_string.getvalue()
        t1 = "[youtube] unable to extract video id from"
        if t1 not in lines:
            raise Exception(lines)


if __name__ == "__main__":
    unittest.main()
