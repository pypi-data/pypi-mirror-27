import sys, math, dwt
import matplotlib.pyplot as plt
import numpy as np
from PySide.QtCore import *
from PySide.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


class Graph(QMainWindow):
    def __init__(self, parent=None):
        MAX_LEVELS = 10

        super(Graph, self).__init__(parent)

        self.mainFrame = QWidget()

        button = QPushButton("Execute DWT", self.mainFrame)
        self.plotter = PlotWidget(self)
        self.plotter.setParent(self.mainFrame)
        self.plotter.staticCanvas.setParent(self.mainFrame)

        lblLevels = QLabel("Levels:", self)
        comboLevels = QComboBox(self)
        comboLevels.addItem("All")
        for i in range(min(int(math.log(len(self.plotter.signal), 2)),
                           MAX_LEVELS)):
            comboLevels.addItem(str(i+1))
        comboLevels.activated[str].connect(self.plotter.onActivatedLevels)

        lblWav = QLabel("Wavelet:", self)
        comboWav = QComboBox(self)
        comboWav.addItem("Haar")
        for i in range(2, 5):
            comboWav.addItem("db"+str(i))
        comboWav.addItem("coif1")
        comboWav.activated[str].connect(self.plotter.onActivatedWavelet)

        lblPadding = QLabel("Padding:", self)
        comboPadding = QComboBox(self)
        comboPadding.addItem("Zero")
        comboPadding.addItem("Periodic")
        comboWav.activated[str].connect(self.plotter.onActivatedPadding)

        waveletBox = QHBoxLayout()
        waveletBox.addWidget(lblWav)
        waveletBox.addWidget(comboWav)

        levelsBox = QHBoxLayout()
        levelsBox.addWidget(lblLevels)
        levelsBox.addWidget(comboLevels)

        paddingBox = QHBoxLayout()
        paddingBox.addWidget(lblPadding)
        paddingBox.addWidget(comboPadding)

        optionsBox = QVBoxLayout()
        optionsBox.addLayout(levelsBox)
        optionsBox.addLayout(waveletBox)
        optionsBox.addLayout(paddingBox)
        optionsBox.addWidget(button)

        hbox = QHBoxLayout()
        hbox.addLayout(optionsBox)
        hbox.addWidget(self.plotter)
        hbox.addWidget(self.plotter.staticCanvas)

        self.mainFrame.setLayout(hbox)
        self.setCentralWidget(self.mainFrame)
        self.setWindowTitle("Stepwise Increments")

        self.connect(button, SIGNAL("clicked()"), self.plotter.change)


class PlotWidget(FigureCanvas):

    def __init__(self, parent=None):
        self.initSignal()

        self.levels = -1
        self.wav = 'haar'
        self.pad = 'zpd'

        self.staticFig = plt.figure()
        self.staticAx = self.staticFig.add_subplot(111)
        self.staticAx.set_title("Original Waveform")
        self.staticAx.plot(self.signal)
        self.staticCanvas = FigureCanvas(self.staticFig)

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        self.draw()

    def initSignal(self):
        f = open("data/p_2_9.dat")
        signal = f.read().replace('\n', '').split(', ')
        self.signal = np.array(map(float, signal))

    def change(self):
        coefs = dwt.dwt(self.signal, levels=self.levels, wav=self.wav)
        self.fig.clf()
        self.fig = dwt.plot(coefs, quiet=True, fig=self.fig)
        self.draw()

    def onActivatedLevels(self, text):
        if text == "All":
            self.levels = -1
        else:
            self.levels = int(text)

    def onActivatedWavelet(self, text):
        self.wav = text

    def onActivatedPadding(self, text):
        if text == "Zero":
            self.pad = 'zpd'
        elif text == "Periodic":
            self.pad = 'ppd'

app = QApplication(sys.argv)
graph = Graph()
graph.show()
app.exec_()
