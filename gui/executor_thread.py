from PyQt6.QtCore import pyqtSignal, QThread


class ExecutorThread(QThread):
    sig_finish_one = pyqtSignal()

    def __init__(self, parent) -> None:
        super().__init__(parent)

    def run(self) -> None:
        for i in range(20):
            self.sig_finish_one.emit()
            self.msleep(200)
