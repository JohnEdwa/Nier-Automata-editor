from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIntValidator
from ui_saveslotui import Ui_saveedit
from itemsui import ItemsManagerUI
import binascii


class SaveSlotUi(QWidget):
    def __init__(self, index, name, savedata, gamedata_header, parent=None):
        super(SaveSlotUi, self).__init__(parent)
        self.ui = Ui_saveedit()
        self.ui.setupUi(self)

        self._index = index
        self._name = name
        self._savedata = savedata
        self._gamedata_header = gamedata_header
        self.items_widget = None
        self.chips_widget = None
        self.widget_init()

    def widget_init(self):
        self.ui.saveSlotIndexLable.setText("Save slot {}:".format(self._index))
        self.ui.saveFileNameLable.setText(self._name)
        self.ui.gameDataHeaderLabel.setText(
            binascii.hexlify(self._savedata.gamedata_header).decode())
        self.ui.characterNameEdit.setText(self._savedata.name)
        self.ui.expEdit.setText(format(self._savedata.experience))
        self.ui.moneyEdit.setText(format(self._savedata.money))

        self.ui.expEdit.setValidator(QIntValidator())
        self.ui.moneyEdit.setValidator(QIntValidator())

        self.ui.importheaderButton.clicked.connect(self.importgamedataheader)
        self.ui.setCharacterNameButton.clicked.connect(self.setcharactername)
        self.ui.setExpButton.clicked.connect(self.setexp)
        self.ui.setMoneyButton.clicked.connect(self.setmoney)
        self.ui.chipButton.clicked.connect(self.on_chip_clicked)
        self.ui.itemButton.clicked.connect(self.on_item_clicked)
        self.ui.saveButton.clicked.connect(self.on_savedata_clicked)

    def importgamedataheader(self):
        self._savedata.gamedata_header = self._gamedata_header
        self.gameDataHeaderLabel.setText(
            binascii.hexlify(self._savedata.gamedata_header))
        self.ui.saveButton.setEnabled(True)

    def setcharactername(self):
        self._savedata.name = self.characterNameEdit.text()
        self.ui.saveButton.setEnabled(True)

    def setexp(self):
        self._savedata.experience = int(self.expEdit.text())
        self.ui.saveButton.setEnabled(True)

    def setmoney(self):
        self._savedata.money = int(self.moneyEdit.text())
        self.ui.saveButton.setEnabled(True)

    def on_savedata_clicked(self):
        self._savedata.save()
        self.ui.saveButton.setEnabled(False)

    def on_chip_clicked(self): 
        pass

    def on_item_clicked(self):
        items_widget = ItemsManagerUI(
            parent=self, savedata=self._savedata.original)
        if items_widget.exec_() == 1:
            self._savedata.original = items_widget.get_save_data()
            self.ui.saveButton.setEnabled(True)
        items_widget.destroy()

