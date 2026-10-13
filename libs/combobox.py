import sys
try:
    from PyQt5.QtCore import Qt, QTimer, pyqtSignal
    from PyQt5.QtGui import QStandardItem, QStandardItemModel
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox, QLineEdit
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtCore import Qt, QTimer, pyqtSignal
    from PyQt4.QtGui import (QWidget, QHBoxLayout, QComboBox, QLineEdit,
                             QStandardItem, QStandardItemModel)


class ComboBox(QWidget):
    selectionChanged = pyqtSignal(object)

    def __init__(self, parent=None, items=None):
        super(ComboBox, self).__init__(parent)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.cb = QComboBox()
        self.cb.setEditable(False)
        self.cb.currentIndexChanged.connect(self._on_selection_changed)
        self.items = []
        self.update_items(items or [])

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def _on_selection_changed(self, _index):
        self.selectionChanged.emit(self.selected_labels())

    def update_items(self, items):
        self.items = list(items)
        self.cb.blockSignals(True)
        self.cb.clear()
        self.cb.addItem('All labels')
        for text in self.items:
            self.cb.addItem(text)
        self.cb.blockSignals(False)
        self.update_summary()

    def selected_labels(self):
        current_text = self.cb.currentText()
        if current_text == 'All labels' or not current_text:
            return set()
        return {current_text}

    def toggle_item(self, index):
        if index >= 0:
            self.cb.setCurrentIndex(index)

    def update_summary(self):
        current_text = self.cb.currentText()
        if not current_text or current_text == 'All labels':
            self.cb.setCurrentIndex(0)
            self.cb.setToolTip('All labels')
        else:
            self.cb.setToolTip(current_text)
