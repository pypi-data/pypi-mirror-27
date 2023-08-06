from .view import View
from PyQt5.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QRect
from enum import IntEnum


class ProgressBarView(View):
    """View simulating a Progress Bar."""

    _LINE_START_Y = 22.7
    _LINE_START_X = 1
    _MARK_SCALE = 80
    _SCALE = 25
    _PROGRESS_SCALE = 1600

    class Orientation(IntEnum):
        HORIZONTAL = 0
        VERTICAL = 1

    def __init__(self, title="", value=0, unit_text="", color=QColor(Qt.blue),
                 min_value=0, max_value=100, precision=1,
                 orientation=Orientation.HORIZONTAL):
        """
        Initialize the progress bar view
        :param title: title text to display
        :param value: the current value to display
        :param unit_text: unit text to display
        :param color: progress bar fill color
        :param min_value: the minimum value
        :param max_value: the maximum value
        :param precision: precision of the values displayed
        :param orientation: horizontal or vertical
        :return:
        """
        super().__init__()
        self._title = title
        self._unit_text = unit_text
        self._precision = precision
        self._orientation = orientation
        self._color = color
        self._pointText = None
        self._mark_count = 15
        self._bar_value = None
        self._min_value = min_value
        self._max_value = min_value
        self.max_value = max_value
        self.min_value = min_value
        self.value = value

        self._create_text()

    @property
    def value(self):
        """Get 'value' class attribute.

        :return: the value of the 'value' attribute.
        """
        return self._value

    @value.setter
    def value(self, value):
        """Set 'value' class attribute, trigger repaint.

        :param value: float or integer value.
        """
        if value < self._min_value:
            self._bar_value = self._min_value
        elif value > self._max_value:
            self._bar_value = self._max_value
        else:
            self._bar_value = value
        self._value = value
        self.repaint()

    @property
    def max_value(self):
        """Get 'max_value' class attribute.

        :return: the value of the 'max_value' attribute.
        """
        return self._max_value

    @max_value.setter
    def max_value(self, max_value):
        """Set 'max_value' class attribute, trigger repaint.

        :param max_value: float or integer value.
        """
        if max_value <= self.min_value:
            raise ValueError("Max value must be greater than min value")
        self._max_value = max_value

        self._create_text()
        self.repaint()

    @property
    def min_value(self):
        """Get 'min_value' class attribute.

        :return: the value of the 'min_value' attribute.
        """
        return self._min_value

    @min_value.setter
    def min_value(self, min_value):
        """Set 'min_value' class attribute, trigger repaint.

        :param min_value: float or integer value.
        """
        if min_value >= self.max_value:
            raise ValueError("Min value must be smaller than max value")
        self._min_value = min_value

        self._create_text()
        self.repaint()

    @property
    def color(self):
        """Get 'color' class attribute

        :return: the QColor value of the 'color' attribute."""
        return self._color

    @color.setter
    def color(self, to):
        """Set 'color' class attribute, trigger repaint.

        :param to: QColor value
        """
        self._color = to
        self.repaint()

    @property
    def title(self):
        """Get 'value' class attribute.

        :return: the value of the 'value' attribute.
        """
        return self._title

    @title.setter
    def title(self, title):
        """Set 'color' class attribute, trigger repaint.

        :param title: title text to display
        """
        self._title = title
        self.repaint()

    def set_color_rgb(self, r, g, b):
        """Set the progress bar's color by rgb

        :param r: red value.
        :param g: green value.
        :param b: blue value.
        """
        self.color = QColor(r, g, b)

    def paintEvent(self, event):
        """Draw the progress bar graphic onto the widget

        :param event: The paint event.
        """
        paint = QPainter()

        paint.begin(self)

        paint.setRenderHint(QPainter.Antialiasing)

        self._draw_frame(paint)
        self._draw_progress(paint)
        self._draw_markings_and_text(paint)
        self._draw_value_text(paint)

        paint.end()

    def _create_text(self):
        self._pointText = []
        add = (self._max_value - self._min_value) / 5
        value = self._min_value

        for i in range(0, 6):
            self._pointText.append(("%%.%df" % self._precision) % value)
            value += add

    def _draw_frame(self, paint):
        """
        Draw the frame of the progress bar

        :param paint:
        :return:
        """
        scale_x = self.width() / self._MARK_SCALE
        scale_y = self.height() / self._MARK_SCALE

        paint.save()

        paint.setBrush(Qt.darkGray)

        if self._orientation == self.Orientation.VERTICAL:
            paint.drawRect(QRect(12 * scale_x, 11 * scale_y,
                                 30 * scale_x, 65 * scale_y))
        else:
            paint.drawRect(QRect(4 * scale_x, 25 * scale_y,
                                 65 * scale_x, 30 * scale_y))
        paint.restore()

    def _draw_value_text(self, paint):
        """
        Draw the a text displaying the current value

        :param paint:
        :return:
        """
        paint.save()

        scale_x = self.width() / self._SCALE
        scale_y = self.height() / self._SCALE

        font_scale = scale_x if scale_x < scale_y\
            else scale_y
        font_scale *= 2

        font = QFont(self.font())
        font.setPixelSize(font_scale)
        paint.setFont(font)
        paint.setPen(QPen(Qt.black))

        text = ("%%.%df" % self._precision) % self._value

        font_metric = QFontMetrics(font)

        if self._orientation == self.Orientation.VERTICAL:
            # draw the title
            paint.drawText((scale_x * 16 - font_metric.width(text) / 2),
                           scale_y * 4.4, "%s" % self._title)
            # draw the value and unit text
            paint.drawText((scale_x * 16 - font_metric.width(text) / 2),
                           scale_y * 7, "%s %s" % (text, self._unit_text))
        else:
            # draw the title
            paint.drawText(font_metric.width(text) / 2,
                           self.height() / 4, "%s" % self._title)
            # draw the value and unit text
            paint.drawText((scale_x * 6.8 + font_metric.width(text) / 2),
                           self.height() / 4, "%s %s" % (text, self._unit_text))
        paint.restore()

    def _draw_markings_and_text(self, paint):
        """
        Draw the markings and text onto the progress bar

        :param paint:
        :return:
        """
        scale_x = self.width() / self._MARK_SCALE
        scale_y = self.height() / self._MARK_SCALE

        paint.save()

        smallest = self.width() / self._SCALE \
            if self.width() < self.height() \
            else self.height() / self._SCALE

        font = QFont(self.font())
        font.setPixelSize(smallest / 25)
        paint.setFont(font)

        font_metric = QFontMetrics(font)

        if self._orientation == self.Orientation.VERTICAL:
            paint.translate(0, self.height() / 1.5)

            line_x1 = 12 * scale_x
            line_x2 = 15 * scale_x

            for i in range(0, self._mark_count + 1):
                y = self._LINE_START_Y * scale_y - i * scale_y * 4.34
                if not i % 3:
                    text = self._pointText[int(i / 3)]
                    text_offset_x = font_metric.width(text) / 3

                    paint.drawLine(line_x1, y, line_x2 * 1.6, y)
                    paint.drawText(line_x1 - 20 - text_offset_x,
                                   (5.5 - i) * scale_y * 4.3, text)
                else:
                    paint.drawLine(line_x1, y,
                                   line_x2, y)
        else:
            paint.translate(0, self.height() / 3)

            line_y1 = 25.5 * scale_y
            line_y2 = 28 * scale_y
            for i in range(0, self._mark_count + 1):
                x = (self._LINE_START_X + i) * 4.32 * scale_x
                if not i % 3:
                    text = self._pointText[int(i / 3)]
                    text_offset_x = font_metric.width(text) / 2
                    paint.drawLine(x, line_y1 * 0.9, x, line_y2)
                    paint.drawText(x - text_offset_x, 33 * scale_y, text)
                else:
                    paint.drawLine(x, line_y1, x, line_y2)
        paint.restore()

    def _draw_progress(self, paint):
        """
        Draw the colored bar representing the current progress/value
        onto the progress bar

        :param paint:
        """
        scale_x = self.width() / self._PROGRESS_SCALE
        scale_y = self.height() / self._PROGRESS_SCALE

        paint.save()
        paint.translate(-12.5 * scale_x, self.height() / 2)

        paint.setBrush(self._color)

        progress = (self._bar_value - self._min_value) / (self._max_value - self._min_value)

        if self._orientation == self.Orientation.VERTICAL:
            bar_width = scale_x * 600
            bar_height = -(self.height() * 0.815) * progress

            paint.drawRect(QRect(255 * scale_x, 725 * scale_y, bar_width, bar_height))
        else:
            bar_height = scale_y * 600
            bar_width = (self.width() * 0.81) * progress

            paint.drawRect(QRect(96 * scale_x, -300 * scale_y, bar_width, bar_height))

        paint.restore()
