from PyQt5.QtGui import QColor


class Color:

    def __init__(self, r, g, b):
        self._color = QColor(r, g, b)

    @classmethod
    def from_qcolor(cls, color):
        return cls(color.red, color.green, color.blue)

    @property
    def red(self):
        return Color.from_qcolor(QColor.red)
