import math
import wx
import matplotlib
matplotlib.use('agg')

from matplotlib.backends.backend_agg import FigureCanvasAgg

class FigureCanvas(wx.StaticBitmap):
    def __init__(self, parent, figure, id=-1):
        bounds = figure.bbox.bounds
        width = int(math.ceil(bounds[2]))
        height = int(math.ceil(bounds[3]))
        super(FigureCanvas, self).__init__(parent, id, size=(width, height))
        self.SetMinSize((1, 1))
        self._canvas = FigureCanvasAgg(figure)
        self._draw_size = (0, 0)
        self.Bind(wx.EVT_SIZE, self._on_size)

    def _on_size(self, evt):
        if self.GetSize() != self._draw_size:
            self.draw()

    def draw(self):
        self._draw_size = self.GetSize()
        width, height = self._draw_size
        figure = self._canvas.figure
        figure.set_size_inches(width / figure.dpi, height / figure.dpi)
        self._canvas.resize(width, height)
        self._canvas.draw()
        bounds = figure.bbox.bounds
        width = int(math.ceil(bounds[2]))
        height = int(math.ceil(bounds[3]))
        buf = self._canvas.tostring_rgb()
        bitmap = wx.BitmapFromBuffer(width, height, buf)
        self.SetBitmap(bitmap)
