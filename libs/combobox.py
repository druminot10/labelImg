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
        self.model = QStandardItemModel(self.cb)
        self.cb.setModel(self.model)
        self.cb.setEditable(True)
        self.cb.lineEdit().setReadOnly(True)
        self.cb.activated.connect(self.toggle_item)
        self.items = []
        self.update_items(items or [])

        layout.addWidget(self.cb)
        self.setLayout(layout)

    def update_items(self, items):
        selected = self.selected_labels()
        self.items = list(items)
        self.model.clear()
        for text in self.items:
            item = QStandardItem(text)
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                          Qt.ItemIsUserCheckable)
            item.setData(Qt.Checked if text in selected else Qt.Unchecked,
                         Qt.CheckStateRole)
            self.model.appendRow(item)
        self.update_summary()

    def selected_labels(self):
        return {self.model.item(index).text()
                for index in range(self.model.rowCount())
                if self.model.item(index).checkState() == Qt.Checked}

    def toggle_item(self, index):
        item = self.model.item(index)
        if item is None:
            return
        state = Qt.Unchecked if item.checkState() == Qt.Checked else Qt.Checked
        item.setCheckState(state)
        selected = self.selected_labels()
        self.update_summary()
        self.selectionChanged.emit(selected)
        QTimer.singleShot(0, self.cb.showPopup)

    def update_summary(self):
        selected = self.selected_labels()
        if not selected:
            summary = 'All labels'
        else:
            summary = '%d labels selected' % len(selected)
        self.cb.lineEdit().setText(summary)
