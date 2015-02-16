__author__ = 'Shane DiNozzo'  # Created by Shane DiNozzo @ 2015.02.14

import json
import sys
# noinspection PyProtectedMember
from pip._vendor import requests

# Try to import PyQt5 module. If it is not fount, then the app exits.
try:
    # noinspection PyUnresolvedReferences
    import PyQt5
except ImportError:
    print('PyQt5 module not found! Please install it!')
    exit(0)

# noinspection PyUnresolvedReferences
from PyQt5 import QtWidgets, uic, QtGui, QtCore
# noinspection PyUnresolvedReferences
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from PyQt5.QtGui import *
# noinspection PyUnresolvedReferences
from PyQt5.QtWidgets import QApplication, QStyleFactory

# Load Qt Designer .ui file as GUI for the app
form_class = uic.loadUiType('sd_currency.ui')[0]

    
class MainWindowClass(QtWidgets.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        # Set window style
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        # Set icon
        self.iconres = QtGui.QPixmap(':/Icon/emblem_money.ico')
        self.icon = QtGui.QIcon(self.iconres)

        # Set progressbar initial values
        self.progressBar.setRange(0, 1)

        # Try to set values of comboboxes
        try:
            json_data = open('countries.json', encoding='utf8')
            data = json.load(json_data)
            for item in data['results'].values():
                self.from_cBox.addItems([item['currencyId'] + ', ' + item['currencyName'] + ', ' + item['name']])
                self.to_cBox.addItems([item['currencyId'] + ', ' + item['currencyName'] + ', ' + item['name']])
            json_data.close()
        except FileNotFoundError:
            print('Can\'t find countries.json file!')
            exit(0)

        # Set button click events
        self.arfolyam_button.clicked.connect(
            lambda: self.get_arfolyam(self.from_cBox.currentText(), self.to_cBox.currentText()))
        self.valto_button.clicked.connect(
            lambda: self.get_valtas(self.from_cBox.currentText(), self.to_cBox.currentText(),
                                    self.type_in_lineEdit.text()))

    @staticmethod
    def get_arfolyam(from_val, to_val):
        myWindow.vegeredmeny_label.setText('')
        from_selected = from_val[0] + from_val[1] + from_val[2]
        to_selected = to_val[0] + to_val[1] + to_val[2]
        # noinspection PyUnresolvedReferences
        try:
            json_rate = requests.get('http://jsonrates.com/get/?from=' + from_selected + '&to=' + to_selected)
            json_c = json_rate.json()
            rate = float(json_c['rate'])
            myWindow.vegeredmeny_label.setText('1 ' + from_selected + ' = ' + str(rate) + ' ' + to_selected)

            myWindow.vegeredmeny_label.setStyleSheet('QLabel#vegeredmeny_label {color: black}')
        except requests.exceptions.ConnectionError:
            myWindow.vegeredmeny_label.setText(
                'Nem sikerült kapcsolódni a kiszolgálóhoz!\nEllenőrizd az internetkapcsolatot')
            myWindow.vegeredmeny_label.setStyleSheet('QLabel#vegeredmeny_label {color: red}')

    @staticmethod
    def get_valtas(from_val, to_val, user_amount):
        myWindow.vegeredmeny_label.setText('')
        try:
            int(user_amount)
        except ValueError:
            myWindow.vegeredmeny_label.setText('HIBA: Csak számot adhatsz meg összegként!')
            myWindow.vegeredmeny_label.setStyleSheet('QLabel#vegeredmeny_label {color: red}')
            return None
        from_selected = from_val[0] + from_val[1] + from_val[2]
        to_selected = to_val[0] + to_val[1] + to_val[2]
        # noinspection PyUnresolvedReferences
        try:
            response = requests.get(
                'http://jsonrates.com/convert/?from=' + from_selected + '&to=' + to_selected + '&amount=' + user_amount)
            json_c = response.json()
            amount = float(json_c['amount'])
            myWindow.vegeredmeny_label.setText(
                user_amount + ' ' + from_selected + ' = ' + str('{:,}'.format(amount)) + ' ' + to_selected)

            myWindow.vegeredmeny_label.setStyleSheet('QLabel#vegeredmeny_label {color: black}')
        except requests.exceptions.ConnectionError:
            myWindow.vegeredmeny_label.setText(
                'Nem sikerült kapcsolódni a kiszolgálóhoz!\nEllenőrizd az internetkapcsolatot')
            myWindow.vegeredmeny_label.setStyleSheet('QLabel#vegeredmeny_label {color: red}')


app = QtWidgets.QApplication(sys.argv)
myWindow = MainWindowClass(None)
myWindow.show()
app.exec()
