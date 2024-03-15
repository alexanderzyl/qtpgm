import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from gui.graph_widget import GraphWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    widget = GraphWidget(main_window)
    main_window.setCentralWidget(widget)
    main_window.show()
    sys.exit(app.exec())
