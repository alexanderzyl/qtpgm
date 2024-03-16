import sys

# we need to set backend before importing pyplot
import matplotlib

from gui.controller import GuiController
from gui.main_window import MainWindow
from models.life_exp import LifeExpModel

matplotlib.use('QtAgg')

from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    model = LifeExpModel(data_file='/Users/aliaksandrzyl/Desktop/projects/qtpgm/data/life expectancy.csv')
    controller = GuiController(window, model)

    window.show()

    sys.exit(app.exec())
