import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QBoxLayout, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
from PIL.ImageFilter import SHARPEN

app = QApplication([])
main_window = QWidget()
main_window.resize(750,500)
main_window.setWindowTitle("Easy Editor")
ImageText = QLabel("Image")
folderButton = QPushButton("Folder")
leftButton = QPushButton("Left")
rightButton = QPushButton("Right")
mirrorButton = QPushButton("Mirror")
sharpnessButton = QPushButton("Sharpness")
blackwhiteButton = QPushButton("Black/White")

folderLists = QListWidget()

workdir = " "

VerticalBoxLayout1 = QVBoxLayout()
VerticalBoxLayout2 = QVBoxLayout()
HorizontalBoxLayout1 = QHBoxLayout()
HorizontalBoxLayout2 = QHBoxLayout()

VerticalBoxLayout1.addWidget(folderButton)
VerticalBoxLayout1.addWidget(folderLists)
VerticalBoxLayout2.addWidget(ImageText)
HorizontalBoxLayout1.addWidget(leftButton)
HorizontalBoxLayout1.addWidget(rightButton)
HorizontalBoxLayout1.addWidget(mirrorButton)
HorizontalBoxLayout1.addWidget(sharpnessButton)
HorizontalBoxLayout1.addWidget(blackwhiteButton)

VerticalBoxLayout2.addLayout(HorizontalBoxLayout1)
HorizontalBoxLayout2.addLayout(VerticalBoxLayout1, 20)
HorizontalBoxLayout2.addLayout(VerticalBoxLayout2, 80)

main_window.setLayout(HorizontalBoxLayout2)

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extension):
    result = []
    for filename in files:
        for ext in extension:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenameList():
    extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]
    chooseWorkDir()
    filenames = filter(os.listdir(workdir), extensions)
    folderLists.clear()
    for filename in filenames:
        folderLists.addItem(filename)

class ImageProcessor():
    def __init__(self):
        self.Image = None
        self.dir = None
        self.fileName = None
        self.save_dir = "Modified/"
    
    def LoadImage(self,dir,filename):
        self.dir = dir
        self.fileName = filename
        image_path = os.path.join(dir, filename)
        self.Image = Image.open(image_path)
    
    def showImage(self,path):
        ImageText.hide()
        pixmapimage = QPixmap(path)
        w, h = ImageText.width(), ImageText.height()
        pixmapimage = pixmapimage.scaled(w,h, Qt.KeepAspectRatio)
        ImageText.setPixmap(pixmapimage)
        ImageText.show()

    def do_blacknwhite(self):
        self.Image = self.Image.convert("L")
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.fileName)
        self.showImage(image_path)
    
    def do_left(self):
        self.Image = self.Image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.fileName)
        self.showImage(image_path)
    
    def do_right(self):
        self.Image = self.Image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.fileName)
        self.showImage(image_path)

    def do_mirror(self):
        self.Image = self.Image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.fileName)
        self.showImage(image_path)
    
    def do_sharpness(self):
        self.Image = self.Image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir, self.fileName)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        
        image_path = os.path.join(path, self.fileName)
        self.Image.save(image_path)



workImage = ImageProcessor()

def showChosenImage():
    if folderLists.currentRow() >= 0:
        filename = folderLists.currentItem().text()
        workImage.LoadImage(workdir, filename)
        image_path = os.path.join(workImage.dir, workImage.fileName)
        workImage.showImage(image_path)


folderButton.clicked.connect(showFilenameList)
folderLists.currentRowChanged.connect(showChosenImage)
blackwhiteButton.clicked.connect(workImage.do_blacknwhite)
leftButton.clicked.connect(workImage.do_left)
rightButton.clicked.connect(workImage.do_right)
mirrorButton.clicked.connect(workImage.do_mirror)
sharpnessButton.clicked.connect(workImage.do_sharpness)


main_window.show()
app.exec_()