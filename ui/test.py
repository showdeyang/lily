import sys
import random
import PySide2.QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QWidget)
from PySide2.QtCore import (Slot, Qt)

from PyQt5.QtGui import (QIcon, QPixmap)

image = ['/home/jnai01/Pictures/小姐姐.jpg','/home/jnai01/Pictures/54b1e998bfe699b07c16.jpeg','/home/jnai01/Pictures/566ce6b0b4e586b6e59f8ee4b8bb43bc.jpeg']

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]
        self.image = ['/home/jnai01/Pictures/小姐姐.jpg','/home/jnai01/Pictures/54b1e998bfe699b07c16.jpeg','/home/jnai01/Pictures/566ce6b0b4e586b6e59f8ee4b8bb43bc.jpeg']
        self.button = QPushButton("点击看下一张小姐姐　:)")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)
        #self.h1 = QHBoxLayout()
        self.label = QLabel(self)
        self.pixmap = PySide2.QtGui.QPixmap('/home/jnai01/Pictures/小姐姐.jpg')
        pixmap2 = self.pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        self.label.setAlignment(Qt.AlignCenter)
        # Optional, resize window to image size
        #self.resize(pixmap.width(),pixmap.height())
        
        self.layout = QVBoxLayout()
        #self.h1.addLayout(self.layout)
        #self.setLayout(self.layout)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        
#        self.h2 = QHBoxLayout()
#        
#        self.layout2 = QVBoxLayout()
#        
#        self.h2.addLayout(self.layout2)
#        #self.layout.(self.text)
#        self.label = QLabel(self)
#        
#        self.layout2.addWidget(self.label)
#        #self.setLayout(self.layout)
#        
#        self.label.show()

        
        #self.h2 = QHBoxLayout()
        
        
        
        #self.h2.addLabel(self.label)
        
        
        
        
        
        # Connecting the signal
        self.button.clicked.connect(self.magic)
        
        
        
    @Slot()
    def magic(self):
        self.pixmap = PySide2.QtGui.QPixmap(random.choice(self.image))
        #self.pixmap = PySide2.QtGui.QPixmap('/home/jnai01/Pictures/小姐姐.jpg')
        pixmap2 = self.pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap2)
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(300,300)
    widget.show()

    sys.exit(app.exec_())
    