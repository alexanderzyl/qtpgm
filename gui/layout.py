from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSlider, QHBoxLayout, QComboBox, QLabel, QLineEdit
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from enum import Enum


class NetTypeIndex(Enum):
    MARKOV_NET = 0
    BAYES_NET = 1


class GuiLayout(QMainWindow):
    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        self.markov_layout = QHBoxLayout()
        self.bayes_layout = QHBoxLayout()

        self.net_type = QComboBox()
        self.net_type.addItem("Markov Net")
        self.net_type.addItem("Bayes Net")
        layout.addWidget(self.net_type)

        markov_info_threshold_label = QLabel("Markov Info Threshold")
        self.markov_info_threshold = QSlider(Qt.Horizontal)
        self.markov_info_threshold.setMinimum(0)
        self.markov_info_threshold.setMaximum(100)
        self.markov_layout.addWidget(markov_info_threshold_label)
        self.markov_layout.addWidget(self.markov_info_threshold)

        discretization_bins_label = QLabel("Discretization Bins")
        self.discrete_bins = QLineEdit("10")
        self.bayes_layout.addWidget(discretization_bins_label)
        self.bayes_layout.addWidget(self.discrete_bins)

        scoring_method_label = QLabel("Scoring Method")
        self.scoring_method = QComboBox()
        self.bayes_layout.addWidget(scoring_method_label)
        self.bayes_layout.addWidget(self.scoring_method)

        max_indegree_label = QLabel("Max In-degree")
        self.max_indegree = QLineEdit("3")
        self.bayes_layout.addWidget(max_indegree_label)
        self.bayes_layout.addWidget(self.max_indegree)

        self.markov_widget = QWidget()
        self.markov_widget.setLayout(self.markov_layout)
        layout.addWidget(self.markov_widget)

        self.bayes_widget = QWidget()
        self.bayes_widget.setLayout(self.bayes_layout)
        layout.addWidget(self.bayes_widget)

        layout.addWidget(self.canvas, 1)  # Change here

        self.markov_widget.setVisible(True)
        self.bayes_widget.setVisible(False)

        self.net_type.currentIndexChanged.connect(self.swapLayout)

        widget.setLayout(layout)

    def swapLayout(self, index):
        if index == NetTypeIndex.MARKOV_NET.value:
            self.markov_widget.setVisible(True)
            self.bayes_widget.setVisible(False)
        elif index == NetTypeIndex.BAYES_NET.value:
            self.markov_widget.setVisible(False)
            self.bayes_widget.setVisible(True)

    def get_markov_info_threshold(self):
        return self.markov_info_threshold.value()/100.0

    def get_discrete_bins(self):
        return int(self.discrete_bins.text())

    def get_max_indegree(self):
        return int(self.max_indegree.text())

# show the window
# from PySide6.QtWidgets import QApplication
# import matplotlib
# matplotlib.use('QtAgg')
# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     window = GuiLayout()
#     window.show()
#     sys.exit(app.exec())
