# N_A_editor PyQt GUI ver
# Base on: NieR;Automata save game editor by CensoredUsername (https://github.com/CensoredUsername)
# Note: I am not responsible for you fucking your save game up with this.

import os
from os import path
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from N_A_editor import SaveGame
from mainwindow import MainWindow


def main():

    app = QApplication(sys.argv)

    user_folder = os.getenv("USERPROFILE")
    nier_automata_folder = path.join(user_folder, "Documents", "My Games", "NieR_Automata")
    if not path.isdir(nier_automata_folder):
        QMessageBox.warning(None, "Error", "Could not find Nier;Automata's save folder location. Please select the save folder location", QMessageBox.Ok)
        nier_automata_folder = QFileDialog.getExistingDirectory(None, "Open Nier;Automate's save folder")

    gamedata_path = path.join(nier_automata_folder, "GameData.dat")
    if not path.isfile(gamedata_path):
        raise Exception("Could not find NieR_Automata/GameData.dat. Please run Nier;Automata at least once before using this tool.")

    # read the gamedata header.
    with open(gamedata_path, "rb") as f:
        gamedata_header = f.read(12)

    locations = ("SlotData_0.dat", "SlotData_1.dat", "SlotData_2.dat")
    import collections
    saves = collections.OrderedDict()

    for location in locations:
        savedata_path = path.join(nier_automata_folder, location)
        if path.isfile(savedata_path):
            saves[location] = SaveGame(savedata_path)

    w = MainWindow(saves, gamedata_header)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
