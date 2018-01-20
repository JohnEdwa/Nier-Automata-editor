from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from ui_thingeditorui import Ui_ThingsManager
import NAAbstractClass as Na
import items

empty_str = '(Empty)'


class ItemCountSpinDelegate(Na.SpinDelegate):
    def __init__(self, parent):
        Na.SpinDelegate.__init__(self, parent)

    def set_maximum(self, editor, index):
        item = index.model().items[index.row()]
        if item != items.ItemsRecord.EMPTY_RECORD:
            if item.uq == 1:
                editor.setMaximum(1)
            else:
                editor.setMaximum(99)
        else:
            editor.setMaximum(0)


class ItemComboDelegate(Na.ComboDelegate):
    def __init__(self, parent):
        Na.ComboDelegate.__init__(self, parent)
        self.available_items = (empty_str,) + items.ItemsRecord.AVAILABLE_ITEMS

    def setcombolist(self, editor, index):
        editor.addItems(self.available_items)
        _items = index.model().items[:]
        for i in range(_items.count(-1)):  # remove empty items
            _items.remove(-1)
        for item in _items:
            editor.model().findItems(item.name)[0].setEnabled(False)


class ItemsModel(Na.NAthingsModel):
    def __init__(self, items_manager):
        Na.NAthingsModel.__init__(self)
        self._items_manager = items_manager
        self._header = ['name', 'count', 'id']
        self._editable = [0, 1]
        self.available_items = (empty_str,) + items.ItemsRecord.AVAILABLE_ITEMS
        self.items = self.things
        self.init()

    def init(self):
        self.row = self._items_manager.SAVE_DATA_ITEMS_COUNT
        for row in range(self.row):
            current = self._items_manager.get_item_at(row)
            self.items.append(current)

    def setthing(self, index, item):
        if item != items.ItemsRecord.EMPTY_RECORD:
            ret = {
                0: lambda x: x.name,
                1: lambda x: x.item_count,
                2: lambda x: '0x%04X' % x.item_id,
            }[index.column()](item)
            return ret
        else:
            ret = {
                0: lambda x: empty_str,
                1: lambda x: 0,
                2: lambda x: QtCore.QVariant(),
            }[index.column()](item)
            return ret

    def _set_name(self, row, value) -> items.ItemsRecord:
        record = items.ItemsRecord.EMPTY_RECORD
        if empty_str != value:
            record = items.ItemsRecord.from_name(value)
        return record

    def _set_count(self, row, value) -> items.ItemsRecord:
        record = items.ItemsRecord.EMPTY_RECORD
        name = self.items[row].name
        if empty_str != name:
            record = items.ItemsRecord.from_name(name)
            record.item_count = int(value)
        return record

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)
        if index.isValid() & role == QtCore.Qt.DisplayRole:
            row = index.row()
            record = {
                0: self._set_name,
                1: self._set_count,
            }[index.column()](row, value)
            self.items[row] = record
            self._items_manager.set_item_at(int(row), record)
            self.dataChanged.emit(index, index)
            return True
        return False


class ItemsManagerUI(QDialog):
    def __init__(self, savedata, parent=None):
        super(ItemsManagerUI, self).__init__(parent)
        self.ui = Ui_ThingsManager()
        self.ui.setupUi(self)
        # savedata:bytes  self._save_data:bytearray
        self._save_data = bytearray(savedata)
        self._items_manager = items.ItemsRecordManager(self._save_data)
        self._model = ItemsModel(self._items_manager)
        self.widget_init()

    def widget_init(self):
        self.setWindowTitle("NieR;Automata Items Editor")
        self.ui.saveButton.clicked.connect(self.on_save_clicked)
        self.ui.closeButton.clicked.connect(self.on_close_clicked)
        self.ui.table.setItemDelegateForColumn(0, ItemComboDelegate(self))
        self.ui.table.setItemDelegateForColumn(
            1, ItemCountSpinDelegate(self))
        self.ui.table.setModel(self._model)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            3)  # self adjust horizontalheader size
        self.ui.table.show()

    def on_save_clicked(self):
        self._save_data[items.ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET:
                        items.ItemsRecordManager.SAVE_DATA_ITEMS_OFFSET_END] = self._items_manager.blocks
        self.accept()

    def on_close_clicked(self):
        self.close()

    def get_save_data(self) -> bytes:
        """
        :rtype: bytes
        """
        return bytes(self._save_data)
