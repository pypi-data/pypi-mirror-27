from hmpy.views.view import View
from PyQt5.QtWidgets import QDial


class DialView(View):

    def __init__(self, value=None, min_value=0, max_value=100,
                 notches_visible=True):
        """Initialize the DialView QWidget

        :param value: value of the dial.
        :param min_value: The minimum value.
        :param max_value: The maximum value.
        :param notches_visible: show/hide notches"""
        super().__init__()

        self.dial = QDial(self)
        self.min_value = min_value
        self.max_value = max_value

        if value is None:
            value = min_value

        self.dial.setValue(value)
        self.dial.setNotchTarget(self.width() / 130.0)
        self.dial.setNotchesVisible(notches_visible)

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.dial.size():
            self.dial.resize(size)

    def on_value_changed(self, callback):
        if callable(callback):
            self.dial.valueChanged.connect(callback)
        else:
            raise TypeError("Callback must be a callable function")

    @property
    def value(self):
        return self.dial.value()

    @value.setter
    def value(self, value):
        self.dial.setValue(value)

    @property
    def min_value(self):
        return self.dial.minimum()

    @min_value.setter
    def min_value(self, value):
        if value > self.max_value:
            raise ValueError
        self.dial.setMinimum(value)

    @property
    def max_value(self):
        return self.dial.maximum()

    @max_value.setter
    def max_value(self, value):
        if value < self.min_value:
            raise ValueError
        self.dial.setMaximum(value)
