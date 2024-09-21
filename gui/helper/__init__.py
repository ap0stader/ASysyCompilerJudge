"""
    I do not want to find a fantasy way to arrange my codes. I just want to
    finish it as quickly as possible. So everything is in the 'helper' and
    the observer & executor logic is different from the tui version. It may
    be much easier to re-write everything.
"""

from gui.helper.get_version import get_version
from gui.helper.wrapper import StringWrapper
from gui.helper.observer import FileModifyHandler
import gui.helper.obtain_testcase as Testcase
import gui.helper.get_configure as Configure
import gui.helper.tempfile_handler as TempFile
