"""
@brief      test log(time=4s)
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
from src.pyquickhelper.pycode import get_temp_folder
from src.pyquickhelper.filehelper import check, read_url, gzip_files, zip_files, zip7_files, download
from src.pyquickhelper.pycode import is_travis_or_appveyor


class TestDownload (unittest.TestCase):

    def test_download_zip(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        fold = get_temp_folder(__file__, "temp_download")
        url = "https://docs.python.org/3/library/ftplib.html"
        f = download(url, fold)
        fLOG(f)
        self.assertTrue(os.path.exists(f))
        if not f.endswith("ftplib.html"):
            raise Exception(f)

        out1 = os.path.join(fold, "try.html.gz")
        gzip_files(out1, [f], fLOG=fLOG)
        self.assertTrue(os.path.exists(out1))

        out2 = os.path.join(fold, "try.zip")
        zip_files(out2, [f], fLOG=fLOG)
        self.assertTrue(os.path.exists(out2))

        if is_travis_or_appveyor() in ("circleci", None):
            out7 = os.path.join(fold, "try.7z")
            zip7_files(out7, [out1, out2], fLOG=fLOG, temp_folder=fold)
            if not os.path.exists(out7):
                raise FileNotFoundError(out7)
        else:
            fLOG("skip 7z")

    def test_check(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        check()

    def test_read_url(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        url = "https://raw.githubusercontent.com/sdpython/pyquickhelper/master/src/pyquickhelper/ipythonhelper/magic_parser.py"
        content = read_url(url, encoding="utf8")
        self.assertTrue("MagicCommandParser" in content)
        self.assertTrue(isinstance(content, str  # unicode#
                                   ))


if __name__ == "__main__":
    unittest.main()
