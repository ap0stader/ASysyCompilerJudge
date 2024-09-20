import sys
import traceback


def exception_hook(exception_type, value, trace_back):
    try:
        from PyQt6.QtWidgets import QMessageBox

        fn_critical = lambda title, content: QMessageBox.critical(
            None, title, "<pre>" + content.replace(">", "&gt;").replace("<", "&lt;") + "</pre>",
            QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Abort
        )
        val_ignore = QMessageBox.StandardButton.Ignore
    except ImportError:
        from tkinter import messagebox

        fn_critical = messagebox.showerror
        val_ignore = ()

    s = "\n".join(traceback.format_exception(exception_type, value, trace_back))
    if val_ignore != fn_critical("Uncaught Exception", s):
        sys.exit(1)


sys.excepthook = exception_hook


from PyQt6.QtWidgets import QApplication

from gui.main_widget import MainWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWidget()
    widget.show()

    sys.exit(app.exec())
