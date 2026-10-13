import sys
try:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import QWidget, QHBoxLayout, QComboBox


class DefaultLabelComboBox(QWidget):
    def __init__(self, parent=None, items=[]):
        super(DefaultLabelComboBox, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.cb = QComboBox()
        self.cb.setEditable(True)
        self.cb.setInsertPolicy(QComboBox.NoInsert)
        self.items = list(items)
        self.cb.addItems(self.items)
        self.cb.lineEdit().setPlaceholderText('product')

        if self.items:
            self.cb.setCurrentIndex(0)
            if hasattr(parent, 'default_label_combo_selection_changed'):
                self.cb.currentIndexChanged.connect(parent.default_label_combo_selection_changed)

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def current_text(self):
        return self.cb.currentText().strip()

    def set_text(self, text):
        text = text or ''
        self.cb.setCurrentText(text)
        if not text and self.items:
            self.cb.setCurrentIndex(0)
