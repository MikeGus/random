#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5 import QtWidgets
import random
from scipy import stats

def count_elements(lst):
    s = set(lst)
    c = []
    for el in s:
        c.append(lst.count(el))

    return c


def is_mean(lst, order):

    chi_2_level = 0.05
    chi_2_order = 1 - chi_2_level
    chi_2_order_low = (1 - chi_2_order) / 2
    chi_2_order_high = 1 - chi_2_order_low

    expected_probability = 1.0 / order
    n = len(lst)
    expected_number = expected_probability * n

    element_counts = count_elements(lst)

    chi_2 = 0
    for count in element_counts:
        chi_2 += (count - expected_number)**2 / expected_number

    chi_2 += expected_number * (order - len(element_counts))
    quant_low = stats.distributions.chi2.ppf(chi_2_order_low, order - 1)
    quant_high = stats.distributions.chi2.ppf(chi_2_order_high, order - 1)

    if quant_low < chi_2 < quant_high:
        return 'Случайная'
    return 'Неслучайная'


# def is_mean(lst, order):
#     mean = 1 / float(order)
#     cnt = count_elements(lst)
#     n  = len(lst)
#
#     diff = 0
#     for el in cnt:
#         diff = max(diff, abs(el / float(n) - mean))
#
#     stat = (6 * n * diff + 1) / (6 * math.sqrt(n))
#     stats = [1.224, 1.358, 1.628]
#
#     if stat <= stats[2]:
#         return 'Случайная'
#
#     return 'Неслучайная'


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.functional = [[],[],[]]
        self.file = [[],[],[]]

        random.seed()
        self.displayNumber = 11
        self.fullNumber = 1000

        self.resize(800, 600)
        self.btnGenerate = QtWidgets.QPushButton(self)
        self.btnGenerate.setText('Обновить')
        self.btnGenerate.clicked.connect(self.generate_btn_press)

        self.tableFunctionalLabel = QtWidgets.QLabel(self)
        self.tableFunctionalLabel.setText('Сгенерированные')
        self.tableFunctional = QtWidgets.QTableWidget(self)
        self.tableFunctional.setColumnCount(3)
        self.tableFunctional.setRowCount(self.displayNumber)
        self.tableFunctional.setHorizontalHeaderItem(0,
                                                     QtWidgets.QTableWidgetItem('1р'))

        self.tableFunctional.setHorizontalHeaderItem(1,
                                                     QtWidgets.QTableWidgetItem('2р'))

        self.tableFunctional.setHorizontalHeaderItem(2,
                                                     QtWidgets.QTableWidgetItem('3р'))
        header = self.tableFunctional.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.tableFileLabel = QtWidgets.QLabel(self)
        self.tableFileLabel.setText('Из файла')
        self.tableFile = QtWidgets.QTableWidget(self)
        self.tableFile.setColumnCount(3)
        self.tableFile.setRowCount(self.displayNumber)
        self.tableFile.setHorizontalHeaderItem(0,
                                                     QtWidgets.QTableWidgetItem('1р'))

        self.tableFile.setHorizontalHeaderItem(1,
                                                     QtWidgets.QTableWidgetItem('2р'))

        self.tableFile.setHorizontalHeaderItem(2,
                                                     QtWidgets.QTableWidgetItem('3р'))
        header = self.tableFile.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        self.inputLabel = QtWidgets.QLabel(self)
        self.inputLabel.setText('Проверка:')
        self.input = QtWidgets.QTextEdit(self)

        self.lblRand = QtWidgets.QLabel(self)

        self.btnCheck = QtWidgets.QPushButton(self)
        self.btnCheck.setText('Проверить')
        self.btnCheck.clicked.connect(self.check_btn_press)

        self.layoutGrid = QtWidgets.QGridLayout(self)
        self.layoutGrid.addWidget(self.tableFunctionalLabel, 0, 0)
        self.layoutGrid.addWidget(self.tableFileLabel, 0, 1)
        self.layoutGrid.addWidget(self.tableFunctional, 1, 0)
        self.layoutGrid.addWidget(self.tableFile, 1, 1)
        self.layoutGrid.addWidget(self.inputLabel, 2, 0)
        self.layoutGrid.addWidget(self.btnGenerate, 2, 1)
        self.layoutGrid.addWidget(self.input, 3, 0, 1, 2)
        self.layoutGrid.addWidget(self.lblRand, 4, 0)
        self.layoutGrid.addWidget(self.btnCheck, 4, 1)

        self.generate_btn_press()

    def generate_new(self):
        self.functional[0].clear()
        self.functional[1].clear()
        self.functional[2].clear()

        for i in range(self.fullNumber):
            self.functional[0].append(random.randint(0, 9))
            self.functional[1].append(random.randint(10, 99))
            self.functional[2].append(random.randint(100, 999))

        self.tableFunctional.setItem(0, 0, QtWidgets.QTableWidgetItem())
        self.tableFunctional.item(0, 0).setText(str(is_mean(self.functional[0], 10)))

        self.tableFunctional.setItem(0, 1, QtWidgets.QTableWidgetItem())
        self.tableFunctional.item(0, 1).setText(str(is_mean(self.functional[1], 100)))

        self.tableFunctional.setItem(0, 2, QtWidgets.QTableWidgetItem())
        self.tableFunctional.item(0, 2).setText(str(is_mean(self.functional[2], 1000)))

        for i in range(1, self.displayNumber):
            self.tableFunctional.setItem(i, 0, QtWidgets.QTableWidgetItem())
            self.tableFunctional.item(i, 0).setText(str(self.functional[0][i]))

            self.tableFunctional.setItem(i, 1, QtWidgets.QTableWidgetItem())
            self.tableFunctional.item(i, 1).setText(str(self.functional[1][i]))

            self.tableFunctional.setItem(i, 2, QtWidgets.QTableWidgetItem())
            self.tableFunctional.item(i, 2).setText(str(self.functional[2][i]))

    def find_file_new(self):
        self.file[0].clear()
        self.file[1].clear()
        self.file[2].clear()

        file = open('digits.txt')
        for line in file:
            numbers = list(map(int, line.split()))[1:]
            if len(self.file[0]) < self.fullNumber:
                self.file[0] += [n % 10 for n in numbers]
            elif len(self.file[1]) < self.fullNumber:
                self.file[1] += [n % 100 for n in numbers]
            elif len(self.file[2]) < self.fullNumber:
                self.file[2] += [n % 1000 for n in numbers]
            else:
                break

        file.close()

        self.tableFile.setItem(0, 0, QtWidgets.QTableWidgetItem())
        self.tableFile.item(0, 0).setText(str(is_mean(self.file[0], 10)))

        self.tableFile.setItem(0, 1, QtWidgets.QTableWidgetItem())
        self.tableFile.item(0, 1).setText(str(is_mean(self.file[1], 100)))

        self.tableFile.setItem(0, 2, QtWidgets.QTableWidgetItem())
        self.tableFile.item(0, 2).setText(str(is_mean(self.file[2], 1000)))

        for i in range(1, self.displayNumber):
            self.tableFile.setItem(i, 0, QtWidgets.QTableWidgetItem())
            self.tableFile.item(i, 0).setText(str(self.file[0][i]))

            self.tableFile.setItem(i, 1, QtWidgets.QTableWidgetItem())
            self.tableFile.item(i, 1).setText(str(self.file[1][i]))

            self.tableFile.setItem(i, 2, QtWidgets.QTableWidgetItem())
            self.tableFile.item(i, 2).setText(str(self.file[2][i]))

    def generate_btn_press(self):
        self.generate_new()
        self.find_file_new()

    def check_btn_press(self):
        lst = self.input.toPlainText().split()
        lst = list(map(int, lst))

        if len(lst) == 0:
            self.lblRand.setText('Случайная')
            return

        mx = max(lst)
        order = 1

        while mx > 0:
            mx = int(mx / 10)
            order *= 10

        self.lblRand.setText(is_mean(lst, order))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName('Псевдослучайные числа')

    main = MyWindow()
    main.show()

    sys.exit(app.exec_())
