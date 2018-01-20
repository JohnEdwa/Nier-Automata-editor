from PyQt5.QtWidgets import QComboBox, QSpinBox, QItemDelegate
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel


class SpinDelegate(QItemDelegate):
    def __init__(self, parent):
        super(SpinDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        return QSpinBox(parent)

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setValue(int(index.model().data(index, QtCore.Qt.DisplayRole)))
        self.set_maximum(editor, index)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        if model.data(index, QtCore.Qt.DisplayRole) != editor.value():
            model.setData(index=index, value=int(editor.value()))

    def set_maximum(self, editor, index): pass


class ComboDelegate(QItemDelegate):
    def __init__(self, parent):
        super(ComboDelegate, self).__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        self.setcombolist(combo, index)
        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(editor.findText(
            index.model().data(index, QtCore.Qt.DisplayRole)))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        if model.data(index, QtCore.Qt.DisplayRole) != editor.currentText():
            model.setData(index, editor.currentText())

    def setcombolist(self, editor, index): pass


class NAthingsModel(QAbstractTableModel):
    def __init__(self):
        QAbstractTableModel.__init__(self)
        self.row = 0
        self._header = []
        self._editable = []
        self.things = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.row

    def columnCount(self, index=QtCore.QModelIndex()):
        return len(self._header)

    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < self.row):
            return QtCore.QVariant()
        if role == QtCore.Qt.DisplayRole:
            thing = self.things[index.row()]
            return self.setthing(index, thing)
        return QtCore.QVariant()

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            return self._header[section]
        if orientation == QtCore.Qt.Vertical:
            return section

    def setthing(self, index, thing):
        return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        return False

    def flags(self, index):
        if index.column() in self._editable:
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled
