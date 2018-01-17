from PyQt5.QtWidgets import QWidget
from saveslotui import SaveSlotUi
from ui_mainwindow import Ui_mainwindow
import binascii


class MainWindow(QWidget):
    def __init__(self, saves, gamedata_header, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_mainwindow()
        self.ui.setupUi(self)
        self.saves = saves
        self.gamedata_header = gamedata_header
        self.save_slot = []
        self.widget_init()

    def widget_init(self):
        self.ui.gameDataHeaderLabel.setText(binascii.hexlify(self.gamedata_header).decode())
        for i, (name, data) in enumerate(self.saves.items()):
            self.save_slot.append(
                SaveSlotUi(parent=self, index=i, name=name, savedata=data, gamedata_header=self.gamedata_header))
            self.ui.gamesaveslotLayout.addWidget(self.save_slot[i], 1)
            self.save_slot[i].show()

