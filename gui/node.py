from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QPainterPath, QLinearGradient, QColor, QPen, QRadialGradient
from PySide6.QtWidgets import QGraphicsItem, QStyle


class Node(QGraphicsItem):
    def __init__(self, graph_widget):
        super().__init__()
        self.graph = graph_widget
        self.newPos = QPointF()
        self.edgeList = []
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(-1)

    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def calculateForces(self):
        if not self.scene() or self.scene().mouseGrabberItem() == self:
            self.newPos = self.pos()
            return

        xvel, yvel = 0.0, 0.0

        for item in self.scene().items():
            if isinstance(item, Node) and item != self:
                vec = self.mapToItem(item, 0, 0)
                dx, dy = vec.x(), vec.y()
                l = dx * dx + dy * dy
                if l > 0:
                    xvel += (dx * 150) / l
                    yvel += (dy * 150) / l

        # Now subtract all forces pulling items together
        weight = (len(self.edgeList) + 1) * 10
        for edge in self.edgeList:
            vec = self.mapToItem(edge.dest, 0, 0) if edge.dest == self else self.mapToItem(edge.source, 0, 0)
            xvel -= vec.x() / weight
            yvel -= vec.y() / weight

    def advancePosition(self):
        if self.newPos == self.pos():
            return False

        self.setPos(self.newPos)
        return True

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, _=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.darkGray)
        painter.drawEllipse(-7, -7, 20, 20)
        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(1, QColor(Qt.yellow).lighter(120))
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.yellow)
            gradient.setColorAt(1, Qt.darkYellow)
        painter.setBrush(gradient)
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edgeList:
                edge.adjust()
            self.graph.itemMoved()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super().mouseReleaseEvent(event)
