from PyQt5.QtCore import QObject, pyqtSignal

class WorkerSignals(QObject):
    """线程信号类"""

    result = pyqtSignal(str)
    progress = pyqtSignal(int)
    complete = pyqtSignal()
    error = pyqtSignal(str)
