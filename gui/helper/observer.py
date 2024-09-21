from pathlib import Path

from watchdog.events import FileSystemEvent, FileSystemEventHandler

from PyQt6.QtCore import QObject, pyqtSignal


class FileModifyHandler(QObject, FileSystemEventHandler):
    sig_modified = pyqtSignal()

    def __init__(self, parent, target_path: str) -> None:
        super(QObject, self).__init__(parent)
        super(FileSystemEventHandler, self).__init__()
        self.target_path = Path(target_path)

    def on_created(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return
        if Path(event.src_path).resolve() == self.target_path.resolve():
            self.sig_modified.emit()
