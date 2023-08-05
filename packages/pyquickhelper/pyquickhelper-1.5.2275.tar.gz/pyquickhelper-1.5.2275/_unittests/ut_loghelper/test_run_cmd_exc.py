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

from src.pyquickhelper.loghelper.flog import fLOG
from src.pyquickhelper.loghelper.run_cmd import run_cmd, parse_exception_message


class TestRunCmdException(unittest.TestCase):

    def test_run_cmd_exc(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")

        cmd = "unexpectedcommand"
        ex = "not affected"
        try:
            out, err = run_cmd(cmd, wait=True, log_error=False, catch_exit=True, communicate=False,
                               tell_if_no_output=120, fLOG=fLOG)
            no_exception = True
            ex = None
        except Exception as e:
            no_exception = False
            out, err = parse_exception_message(e)
            ex = e
        self.assertTrue(not no_exception)
        if sys.platform.startswith("win"):
            if out is None or err is None:
                raise Exception("A\n" + str(ex))
            if len(out) > 0:
                raise Exception("B\n" + str(ex))
            if len(err) == 0:
                raise Exception("C\n" + str(ex))
        else:
            self.assertTrue(out is None)
            self.assertTrue(err is None)
            self.assertTrue(isinstance(ex, Exception))


if __name__ == "__main__":
    unittest.main()
