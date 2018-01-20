from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog

import chips
import NAAbstractClass as Na
from ui_thingeditorui import Ui_ThingsManager

empty_str = '(Empty)'


class ChipSizeComboDelegate(Na.ComboDelegate):
    def __init__(self, parent):
        Na.ComboDelegate.__init__(self, parent)
        self.available_sizes = [str(i) for i in range(31)]

    def setcombolist(self, editor, index):
        editor.addItems(self.available_sizes)


class ChipComboDelegate(Na.ComboDelegate):
    def __init__(self, parent):
        Na.ComboDelegate.__init__(self, parent)
        self.available_chips = (empty_str,) + chips.ChipsRecord.AVAILABLE_CHIPS

    def setcombolist(self, editor, index):
        editor.addItems(self.available_chips)


class ChipsModel(Na.NAthingsModel):
    def __init__(self, chips_manager: chips.ChipsRecordManager):
        Na.NAthingsModel.__init__(self)
        self._chips_manager = chips_manager
        self._header = ['name', 'size']
        self._editable = [0, 1]
        self.chips = self.things
        self.init()

    def init(self):
        self.row = 300  # self._chips_manager.SAVE_DATA_CHIPS_SIZE
        for row in range(self.row):
            current = self._chips_manager.get_chip_at(row)
            self.chips.append(current)

    def setthing(self, index, chip: chips.ChipsRecord):
        if chip != chips.ChipsRecord.EMPTY_RECORD:
            ret = {
                0: lambda x: chip.name,
                1: lambda x: str(chip.size),
                2: lambda x: 0
            }[index.column()](chip)
            return ret
        else:
            ret = {
                0: lambda x: empty_str,
                1: lambda x: str(0),
                2: lambda x: QtCore.QVariant()
            }[index.column()](chip)
            return ret

    def _set_name(self, row, value) -> chips.ChipsRecord:
        record = chips.ChipsRecord.EMPTY_RECORD
        if empty_str != value:
            record = chips.ChipsRecord.from_name(value)
        return record

    def _set_size(self, row, value) -> chips.ChipsRecord:
        record = chips.ChipsRecord.EMPTY_RECORD
        name = self.chips[row].name
        if empty_str != value:
            record = chips.ChipsRecord.from_name(name)
            record.size = int(value)
        return record

    def setData(self, index, value, role=QtCore.Qt.DisplayRole):
        print("setData", index.row(), index.column(), value)
        if index.isValid() & role == QtCore.Qt.DisplayRole:
            row = index.row()
            record = {
                0: self._set_name,
                1: self._set_size,
            }[index.column()](row, value)
            self.chips[row] = record
            self._chips_manager.set_chip_at(int(row), record)
            self.dataChanged.emit(index, index)
            return True
        return False

    def flags(self, index):
        if index.column() in self._editable:
            current = self.chips[index.row()]
            if current != chips.ChipsRecord.EMPTY_RECORD:
                if current.offset_a != -1 or current.offset_b != -1 or current.offset_c != -1:
                    return QtCore.Qt.NoItemFlags
            return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemIsEnabled


class ChipsManagerUI(QDialog):
    def __init__(self, savedata, parent=None):
        super(ChipsManagerUI, self).__init__(parent)
        self.ui = Ui_ThingsManager()
        self.ui.setupUi(self)
        self.resize(400, self.size().height())
        # savedata:bytes  self._save_data:bytearray
        self._save_data = bytearray(savedata)
        self._chips_manager = chips.ChipsRecordManager(self._save_data)
        self._model = ChipsModel(self._chips_manager)
        self.widget_init()

    def widget_init(self):
        self.setWindowTitle("NieR;Automata Chips Editor")
        self.ui.label.setText(
            'Equipped chips are not editable, un-equip them first')
        self.ui.saveButton.clicked.connect(self.on_save_clicked)
        self.ui.closeButton.clicked.connect(self.on_close_clicked)
        self.ui.table.setItemDelegateForColumn(0, ChipComboDelegate(self))
        self.ui.table.setItemDelegateForColumn(
            1, ChipSizeComboDelegate(self))
        self.ui.table.setModel(self._model)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            3)  # self adjust horizontalheader size
        self.ui.table.show()

    def on_save_clicked(self):
        self._save_data[chips.ChipsRecordManager.SAVE_DATA_CHIPS_OFFSET:
                        chips.ChipsRecordManager.SAVE_DATA_CHIPS_OFFSET_END] = self._chips_manager.blocks
        self.accept()

    def on_close_clicked(self):
        self.close()

    def get_save_data(self) -> bytes:
        """
        :rtype: bytes
        """
        return bytes(self._save_data)
