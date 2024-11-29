# ModalHandler.py

from PySide6.QtCore import QObject, Slot, QMetaObject, Qt, QUrl
from PySide6.QtQuick import QQuickView
import login

class ModalHandler(QObject):
    def __init__(self, engine, base_path, pyinterface):
        super().__init__()
        self.engine = engine
        self.base_path = base_path
        self.is_modal_visible = False
        self.modal_view = None
        self.stack_view = None
        self.pyinterface = pyinterface

    @Slot()
    def show_modal(self):
        self.pyinterface.stopScript()  # 실행 중인 스크립트 중지

        if not self.is_modal_visible:
            self.is_modal_visible = True
            self.modal_view = QQuickView()
            self.modal_view.rootContext().setContextProperty("modalHandler", self)
            self.modal_view.setSource(QUrl.fromLocalFile(str(self.base_path / 'warningPage.qml')))
            self.modal_view.setFlags(Qt.FramelessWindowHint | Qt.Window)
            self.modal_view.setResizeMode(QQuickView.SizeRootObjectToView)
            self.modal_view.showFullScreen()

        if login.webView is not None and login.webView.isVisible():
            login.webView.close()

        if self.stack_view:
            QMetaObject.invokeMethod(self.stack_view, "popToInitial", Qt.DirectConnection)

    @Slot()
    def close_modal(self):
        if self.modal_view:
            self.modal_view.close()
            self.modal_view.deleteLater()
            self.modal_view = None
        self.is_modal_visible = False

    @Slot(QObject)
    def setStackView(self, stack_view):
        self.stack_view = stack_view
