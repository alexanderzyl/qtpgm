from typing import Any
from PySide6.QtCore import Slot

from gui.layout import NetTypeIndex
from main_window import MainWindow


class GuiController:
    def __init__(self, main_window: MainWindow, model: Any):
        self.main_window = main_window
        self.model = model

        self.main_window.markov_info_threshold.valueChanged.connect(self.markov_info_threshold_changed)
        self.main_window.markov_info_threshold.setValue(50)

        self.main_window.net_type.currentIndexChanged.connect(self.net_type_changed)
        self.main_window.discrete_bins.textChanged.connect(self.discrete_bins_changed)

        self.main_window.scoring_method.addItems(["bicscore", "k2score", "bdeuscore", "bdsscore", "aicscore"])

        self.main_window.scoring_method.currentIndexChanged.connect(self.scoring_method_changed)

        self.main_window.max_indegree.textChanged.connect(self.max_indegree_changed)

    def redraw(self):
        if self.main_window.net_type.currentIndex() == NetTypeIndex.MARKOV_NET.value:
            self.main_window.draw_graph(self.model.gauss_markov_net(
                threshold=self.main_window.get_markov_info_threshold()),
                NetTypeIndex.MARKOV_NET)
        elif self.main_window.net_type.currentIndex() == NetTypeIndex.BAYES_NET.value:
            self.main_window.draw_graph(self.model.bayes_net(
                discret_bins=self.main_window.get_discrete_bins(),
                scoring_method=self.main_window.get_scoring_method(),
                max_indegree=self.main_window.get_max_indegree(),),
                NetTypeIndex.BAYES_NET)
        else:
            raise ValueError(f'Unknown index: {self.main_window.net_type.currentIndex()}')

    @Slot(int)
    def markov_info_threshold_changed(self, value: int):
        self.redraw()

    @Slot(int)
    def net_type_changed(self, index: int):
        self.redraw()

    @Slot(str)
    def discrete_bins_changed(self, text: str):
        self.redraw()

    @Slot(int)
    def scoring_method_changed(self, index: int):
        self.redraw()

    @Slot(str)
    def max_indegree_changed(self, text: str):
        self.redraw()
