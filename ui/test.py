import sys
import random
import PySide2.QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QHBoxLayout, QWidget, QInputDialog, QLineEdit)
from PySide2.QtCore import (Slot, Qt)

from PyQt5.QtGui import (QIcon, QPixmap)

image = ['/home/show/Pictures/Wallpapers/2bf1faac5c1e26d5cb94128cf762517a-petra.jpg','/home/show/Pictures/Wallpapers/maxresdefault.jpg']

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]
        self.image = ['/home/show/Pictures/Wallpapers/2bf1faac5c1e26d5cb94128cf762517a-petra.jpg','/home/show/Pictures/Wallpapers/maxresdefault.jpg']
        self.button = QPushButton("点击看下一张　:)5")  #
        #self.button.resize(400,600)
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)
        #self.h1 = QHBoxLayout()
        self.label = QLabel(self)
        self.pixmap = PySide2.QtGui.QPixmap('/home/show/Pictures/Wallpapers/2bf1faac5c1e26d5cb94128cf762517a-petra.jpg')
        self.pixmap2 = self.pixmap.scaled(800, 800, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap2)
        self.label.setAlignment(Qt.AlignCenter)
        
        self.labelInput = QLabel(self)
        # Optional, resize window to image size
        #self.resize(pixmap.width(),pixmap.height())
        
        self.layout = QVBoxLayout()
        
        #self.layoutButton = QHBoxLayout()
        #self.h1.addLayout(self.layout)
        #self.setLayout(self.layout)
#        self.layoutButton.addStretch(1)
#        self.layoutButton.addWidget(self.button)
#        self.layoutButton.addStretch(1)
        
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.labelInput)
        
        self.text1, self.okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if self.okPressed and self.text1 != '':
            self.text2 = QLabel(self.text1)
        self.layout.addWidget(self.labelInput)
        self.layout.addWidget(self.text2)
        
        #self.layout.addWidget(self.layoutButton)
        
        self.layout.addWidget(self.button)
        #self.layout.addWidget(self.layoutButton)
        
        self.setLayout(self.layout)
        #self.setLayout(self.layoutButton)
        
        
        # Connecting the signal
        self.button.clicked.connect(self.magic)
        

    def initUI(self):
        
        self.getInteger()
        self.getText()
        self.getDouble()
        self.getChoice()
        self.getText()
        self.show()
        
    def getInteger(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 28, 0, 100, 1)
        if okPressed:
            print(i)

    def getDouble(self):
        d, okPressed = QInputDialog.getDouble(self, "Get double","Value:", 10.50, 0, 100, 10)
        if okPressed:
            print( d)
        
    def getChoice(self):
        items = ("Red","Blue","Green")
        item, okPressed = QInputDialog.getItem(self, "Get item","Color:", items, 0, False)
        if okPressed and item:
            print(item)

    def getText(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Your name:", QLineEdit.Normal, "")
        if okPressed and text != '':
            print(text)    
        
    @Slot()
    def magic(self):
        self.pixmap = PySide2.QtGui.QPixmap(random.choice(self.image))
        #self.pixmap = PySide2.QtGui.QPixmap('/home/jnai01/Pictures/小姐姐.jpg')
        self.pixmap2 = self.pixmap.scaled(800, 800, QtCore.Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap2)
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(1000,700)
    widget.show()

    sys.exit(app.exec_())
    