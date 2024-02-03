import os
import sys

import requests
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [850, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.zoom = 5
        self.address = [44.269772, 46.307847]
        self.get_image()
        self.initUI()

    def get_image(self):
        map_params = {
            "ll": ','.join(list(map(str, self.address))),
            "z": self.zoom,
            "l": "map",
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageUp:
            self.zoom += 1 if self.zoom < 17 else 0
        elif event.key() == QtCore.Qt.Key_PageDown:
            self.zoom -= 1 if self.zoom > 1 else 0
        elif event.key() == QtCore.Qt.Key_Left:
            self.address[0] -= (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Up:
            self.address[1] += (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Right:
            self.address[0] += (0.0025 * 2 ** (17 - self.zoom)) / 2
        elif event.key() == QtCore.Qt.Key_Down:
            self.address[1] -= (0.0025 * 2 ** (17 - self.zoom)) / 2
        if self.address[0] > 180:
            self.address[0] = -360 + self.address[0]
        elif self.address[0] < -180:
            self.address[0] = 360 + self.address[0]
        if self.address[1] > 85:
            self.address[1] = -170 + self.address[1]
        elif self.address[1] < -85:
            self.address[1] = 170 + self.address[1]
        self.get_image()
        self.image.setPixmap(QPixmap(self.map_file))

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.image = QLabel(self)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap(self.map_file))

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
