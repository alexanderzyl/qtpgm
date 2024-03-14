from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, \
    QGraphicsDropShadowEffect, QGraphicsItem


class ElasticNode(QGraphicsEllipseItem):
    def __init__(self, x, y, diameter):
        super().__init__(x, y, diameter, diameter)
        self.diameter = diameter
        self.setBrush(QColor(255, 0, 0, 255))
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsGeometryChanges)  # Corrected line

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:  # Corrected line
            for node in nodes:
                if node != self:
                    dx = self.x() - node.x()
                    dy = self.y() - node.y()
                    distance = ((dx ** 2) + (dy ** 2)) ** 0.5
                    if distance < self.diameter and distance != 0:  # Ensure distance is not zero
                        overlap = self.diameter - distance
                        self.setX(self.x() + (overlap * (dx / distance)))
                        self.setY(self.y() + (overlap * (dy / distance)))
        return super().itemChange(change, value)


if __name__ == "__main__":
    app = QApplication([])

    view = QGraphicsView()
    view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    scene = QGraphicsScene()
    view.setScene(scene)

    diameter = 100

    nodes = [ElasticNode(x * diameter, y * diameter, diameter) for x in range(4) for y in range(4)]

    for node in nodes:
        scene.addItem(node)

    view.show()
    app.exec()