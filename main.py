#!/usr/bin/env python
# -*- coding:utf-8 -*-

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from math import exp
from math import factorial

from PyQt5 import QtCore
from PyQt5 import QtWidgets


class MatplotlibWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)

        self.axis = self.figure.add_subplot(111)

        self.layoutVertical = QtWidgets.QVBoxLayout(self)  # QVBoxLayout
        self.layoutVertical.addWidget(self.canvas)


class DistributionDataGetter(QtCore.QObject):
    emitter = QtCore.pyqtSignal(list)

    def erlangDens(self, l, k, x):
        if x < 0:
            return 0
        return ((l ** k) * (x ** (k - 1)) * exp(-l * x)) / factorial(k - 1)

    def erlangDist(self, l, k, x):
        if x < 0:
            return 0
        sum = 0
        for i in range(0, int(k - 1)):
            sum += (exp(-l * x) * ((l * x) ** i)) / factorial(i)
        return 1 - sum

    def erlangSecondBound(self, firstParam, secondParam):
        secondBound = 0
        while self.erlangDist(firstParam, secondParam, secondBound) < 0.999:
            secondBound += 1

        return secondBound + 1

    def evenDist(self, firstParam, secondParam, x):
        return 0 + (x - firstParam) / float(secondParam - firstParam)

    def run(self, firstParam, secondParam, isEven=True):
        x = []
        dataDist = []
        dataDens = []
        if isEven:
            step = 0.001
            val = firstParam
            while val <= secondParam:
                x.append(val)
                val += step

            dataDens = [1 / (secondParam - firstParam)] * len(x)
            dataDist = [self.evenDist(firstParam, secondParam, val) for val in x]

        else:
            step = 0.001
            val = -1
            secondBound = self.erlangSecondBound(firstParam, secondParam)
            while val <= secondBound:
                x.append(val)
                val += step

            dataDens = [self.erlangDens(firstParam, secondParam, val) for val in x]
            dataDist = [self.erlangDist(firstParam, secondParam, val) for val in x]

        self.emitter.emit([x, dataDens, dataDist])


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.radioGroup = QtWidgets.QButtonGroup(self)

        self.radioEven = QtWidgets.QRadioButton(self)
        self.radioEven.setText('Равномерное распределение')
        self.radioEven.setChecked(True)
        self.radioEven.clicked.connect(self.on_radioEven_clicked)
        self.radioGroup.addButton(self.radioEven)

        self.radioErlang = QtWidgets.QRadioButton(self)
        self.radioErlang.setText('Распределение Эрланга')
        self.radioErlang.clicked.connect(self.on_radioErlang_clicked)
        self.radioGroup.addButton(self.radioErlang)

        self.firstParamLabel = QtWidgets.QLabel(self)
        self.firstParamLabel.setText('a = ')
        self.secondParamLabel = QtWidgets.QLabel(self)
        self.secondParamLabel.setText('b = ')

        self.firstParam = QtWidgets.QDoubleSpinBox(self)
        self.firstParam.setMinimum(-1000)
        self.firstParam.setMaximum(1000)

        self.secondParam = QtWidgets.QDoubleSpinBox(self)
        self.secondParam.setMinimum(-1000)
        self.secondParam.setMaximum(1000)

        self.pushButtonPlot = QtWidgets.QPushButton(self)
        self.pushButtonPlot.setText("Построить график")
        self.pushButtonPlot.clicked.connect(self.on_pushButtonPlot_clicked)

        self.densityWidget = MatplotlibWidget(self)
        self.densityWidget.figure.set_label('Плотность распределения')
        self.distrubutionWidget = MatplotlibWidget(self)
        self.distrubutionWidget.figure.set_label('Функция распределения')

        self.layoutGrid = QtWidgets.QGridLayout(self)
        self.layoutGrid.addWidget(self.radioEven, 0, 0)
        self.layoutGrid.addWidget(self.radioErlang, 1, 0)
        self.layoutGrid.addWidget(self.firstParamLabel, 2, 0)
        self.layoutGrid.addWidget(self.firstParam, 2, 1)

        self.layoutGrid.addWidget(self.secondParamLabel, 3, 0)
        self.layoutGrid.addWidget(self.secondParam, 3, 1)

        self.layoutGrid.addWidget(self.pushButtonPlot, 4, 0)

        self.layoutGrid.addWidget(self.densityWidget, 5, 0)
        self.layoutGrid.addWidget(self.distrubutionWidget, 5, 1)

        self.distributionDataGetter = DistributionDataGetter()
        self.distributionDataGetter.emitter.connect(self.showData)

    @QtCore.pyqtSlot()
    def on_pushButtonPlot_clicked(self):
        if self.radioEven.isChecked() and self.firstParam.value() >= self.secondParam.value():
            msg = QtWidgets.QMessageBox(self)
            msg.setText('B должна быть больше, чем A!')
            msg.show()
            return
        self.distrubutionWidget.axis.clear()
        self.densityWidget.axis.clear()
        self.distributionDataGetter.run(self.firstParam.value(),
                                        self.secondParam.value(),
                                        self.radioEven.isChecked())

    @QtCore.pyqtSlot()
    def on_radioEven_clicked(self):
        self.firstParamLabel.setText('a = ')
        self.secondParam.setMinimum(-1000)
        self.secondParamLabel.setText('b = ')
        self.secondParam.setMinimum(-1000)
        self.secondParam.setDecimals(2)

    @QtCore.pyqtSlot()
    def on_radioErlang_clicked(self):
        self.firstParamLabel.setText('λ = ')
        self.firstParam.setMinimum(0.01)
        self.firstParam.setValue(1)

        self.secondParamLabel.setText('k = ')
        self.secondParam.setValue(1)
        self.secondParam.setMinimum(1)
        self.secondParam.setDecimals(0)

    @QtCore.pyqtSlot(list)
    def showData(self, data):
        self.densityWidget.axis.plot(data[0], data[1])
        self.densityWidget.axis.set_xlabel('x')
        self.densityWidget.axis.set_ylabel('f(x)')

        self.densityWidget.canvas.draw()

        self.distrubutionWidget.axis.plot(data[0], data[2])
        self.distrubutionWidget.axis.set_xlabel('x')
        self.distrubutionWidget.axis.set_ylabel('F(x)')

        self.distrubutionWidget.canvas.draw()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Построение графиков распределений')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
