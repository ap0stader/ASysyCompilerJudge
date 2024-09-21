import atexit
import os
import shutil
import tempfile

__tempfiles = []
__tempdirs = []


def request_tempfile(suffix: str | None = None) -> str:
    fd, filename = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    __tempfiles.append(filename)
    return filename


def request_tempdir() -> str:
    dirname = tempfile.mkdtemp()
    __tempdirs.append(dirname)
    return dirname


def __clear_tempfile():
    while len(__tempfiles) > 0:
        os.remove(__tempfiles.pop())
    while len(__tempdirs) > 0:
        shutil.rmtree(__tempdirs.pop())


atexit.register(__clear_tempfile)
