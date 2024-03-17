import sys

# we need to set backend before importing pyplot
import matplotlib

from gui.controller import GuiController
from gui.main_window import MainWindow
from models.csv import CsvDataModel

matplotlib.use('QtAgg')

from PySide6.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    data_file = sys.argv[1]

    window = MainWindow()
    model = CsvDataModel(csv_file_path=data_file)
    controller = GuiController(window, model)

    window.show()

    sys.exit(app.exec())
