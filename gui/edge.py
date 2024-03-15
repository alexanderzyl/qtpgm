import numpy as np
from PySide6.QtCore import QPointF, Qt, QLineF, QRectF, QSizeF, qFuzzyCompare
from PySide6.QtGui import QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsItem


class Edge(QGraphicsItem):
    def __init__(self, source_node, dest_node):
        super().__init__()
        self.source = source_node
        self.dest = dest_node
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()
        self.arrowSize = 10
        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source.addEdge(self)
        self.dest.addEdge(self)

    def sourceNode(self):
        return self.source

    def destNode(self):
        return self.dest

    def adjust(self):
        if not self.source or not self.dest:
            return
        line = QLineF(self.mapFromItem(self.source, 0, 0), self.mapFromItem(self.dest, 0, 0))
        length = line.length()
        self.prepareGeometryChange()
        if length > 20:
            edge_offset = QPointF((line.dx() * 10) / length, (line.dy() * 10) / length)
            self.sourcePoint = line.p1() + edge_offset
            self.destPoint = line.p2() - edge_offset
        else:
            self.sourcePoint = self.destPoint = line.p1()

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()
        penWidth = 1
        extra = (penWidth + self.arrowSize) / 2.0
        return (QRectF(self.sourcePoint,
                       QSizeF(
                           self.destPoint.x() - self.sourcePoint.x(),
                           self.destPoint.y() - self.sourcePoint.y()))
                .normalized().adjusted(-extra, -extra, extra, extra))

    def paint(self, painter, option, widget=None):
        if not self.source or not self.dest:
            return
        line = QLineF(self.sourcePoint, self.destPoint)
        if qFuzzyCompare(line.length(), 0.0):
            return

        # draw the line itself
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.drawLine(line)

        # draw the arrows
        angle = np.arctan2(-line.dy(), line.dx())
        source_arrow_p1 = self.sourcePoint + QPointF(np.sin(angle + np.pi / 3) * self.arrowSize,
                                                     np.cos(angle + np.pi / 3) * self.arrowSize)
        source_arrow_p2 = self.sourcePoint + QPointF(np.sin(angle + np.pi - np.pi / 3) * self.arrowSize,
                                                     np.cos(angle + np.pi - np.pi / 3) * self.arrowSize)
        dest_arrow_p1 = self.destPoint + QPointF(np.sin(angle - np.pi / 3) * self.arrowSize,
                                                 np.cos(angle - np.pi / 3) * self.arrowSize)
        dest_arrow_p2 = self.destPoint + QPointF(np.sin(angle - np.pi + np.pi / 3) * self.arrowSize,
                                                 np.cos(angle - np.pi + np.pi / 3) * self.arrowSize)

        painter.setBrush(Qt.black)
        painter.drawPolygon(QPolygonF([line.p1(), source_arrow_p1, source_arrow_p2]))
        painter.drawPolygon(QPolygonF([line.p2(), dest_arrow_p1, dest_arrow_p2]))
