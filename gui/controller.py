from typing import Any
from main_window import MainWindow


class GuiController:
    def __init__(self, main_window: MainWindow, model: Any):
        self.main_window = main_window
        self.model = model

        self.main_window.slider.valueChanged.connect(self.update_graph)
        self.main_window.slider.setValue(50)

    def update_graph(self, value: int):
        threshold = value / 100.0
        self.model.build_markov_net(threshold=threshold)
        self.main_window.draw_graph(self.model.markov_net)
