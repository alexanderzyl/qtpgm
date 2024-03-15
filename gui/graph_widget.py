from PySide6.QtCore import Qt, Slot, QRandomGenerator, QRectF
from PySide6.QtGui import QPainter, QLinearGradient
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene

from gui.edge import Edge
from gui.node import Node


class GraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timerId = 0
        scene = QGraphicsScene()
        scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        scene.setSceneRect(-200, -200, 400, 400)
        self.setScene(scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.scale(0.8, 0.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Elastic Nodes")

        self.centerNode = Node(self)
        nodes = [Node(self) for _ in range(5)] + [self.centerNode] + [Node(self) for _ in range(5)]

        nodes[0].setPos(-50, -50)
        nodes[1].setPos(0, -50)
        nodes[2].setPos(50, -50)
        nodes[3].setPos(-50, 0)
        nodes[4].setPos(0, 0)
        nodes[5].setPos(50, 0)
        nodes[6].setPos(-50, 50)
        nodes[7].setPos(0, 50)
        nodes[8].setPos(50, 50)

        for node in nodes:
            scene.addItem(node)

        scene.addItem(Edge(nodes[0], nodes[1]))
        scene.addItem(Edge(nodes[1], nodes[2]))
        scene.addItem(Edge(nodes[1], nodes[4]))
        scene.addItem(Edge(nodes[2], nodes[5]))
        scene.addItem(Edge(nodes[3], nodes[0]))
        scene.addItem(Edge(nodes[3], nodes[4]))
        scene.addItem(Edge(nodes[4], nodes[5]))
        scene.addItem(Edge(nodes[4], nodes[7]))
        scene.addItem(Edge(nodes[5], nodes[8]))
        scene.addItem(Edge(nodes[6], nodes[3]))
        scene.addItem(Edge(nodes[7], nodes[6]))
        scene.addItem(Edge(nodes[8], nodes[7]))


    def itemMoved(self):
        if not self.timerId:
            self.timerId = self.startTimer(1000 // 25)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.centerNode.moveBy(0, -20)
            pass
        elif event.key() == Qt.Key_Down:
            self.centerNode.moveBy(0, 20)
            pass
        elif event.key() == Qt.Key_Left:
            self.centerNode.moveBy(-20, 0)
            pass
        elif event.key() == Qt.Key_Right:
            self.centerNode.moveBy(20, 0)
            pass
        elif event.key() == Qt.Key_Plus:
            self.zoomIn()
            pass
        elif event.key() == Qt.Key_Minus:
            self.zoomOut()
            pass
        elif event.key() == Qt.Key_Space or event.key() == Qt.Key_Enter:
            self.shuffle()
            pass
        else:
            super().keyPressEvent(event)

    def timerEvent(self, _):
        nodes = [item for item in self.scene().items() if isinstance(item, Node)]
        for node in nodes:
            node.calculateForces()

        itemMoved = any([node.advancePosition() for node in nodes])
        if not itemMoved:
            self.killTimer(self.timerId)
            self.timerId = 0

    def wheelEvent(self, event):
        super().wheelEvent(event)

    @Slot()
    def zoomIn(self):
        self.scaleView(1.2)

    @Slot()
    def zoomOut(self):
        self.scaleView(1 / 1.2)

    @Slot()
    def shuffle(self):
        scene = self.scene()
        for item in scene.items():
            if isinstance(item, Node):
                item.setPos(-150 + QRandomGenerator.global_().bounded(300),
                            -150 + QRandomGenerator.global_().bounded(300))

    def drawBackground(self, painter, rect):
        sceneRect = self.sceneRect()
        rightShadow = QRectF(sceneRect.right(), sceneRect.top() + 5, 5, sceneRect.height())
        bottomShadow = QRectF(sceneRect.left() + 5, sceneRect.bottom(), sceneRect.width(), 5)
        if rightShadow.intersects(rect) or rightShadow.contains(rect):
            painter.fillRect(rightShadow, Qt.darkGray)
        if bottomShadow.intersects(rect) or bottomShadow.contains(rect):
            painter.fillRect(bottomShadow, Qt.darkGray)

        gradient = QLinearGradient(sceneRect.topLeft(), sceneRect.bottomRight())
        gradient.setColorAt(0, Qt.white)
        gradient.setColorAt(1, Qt.lightGray)
        painter.fillRect(rect.intersected(sceneRect), gradient)
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(sceneRect)

        textRect = QRectF(sceneRect.left() + 4, sceneRect.top() + 4, sceneRect.width() - 4, sceneRect.height() - 4)
        message = "Click and drag the nodes around, and zoom with the mouse wheel or the '+' and '-' keys"
        font = painter.font()
        font.setBold(True)
        font.setPointSize(14)
        painter.setFont(font)
        painter.setPen(Qt.lightGray)
        painter.drawText(textRect.translated(2, 2), message)
        painter.setPen(Qt.black)
        painter.drawText(textRect, message)

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()
        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
