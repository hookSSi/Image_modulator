import sys
from PIL import Image, ImageQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import *
import pixel
import random
import hashlib

'''
To do list
1. 클래스화 하여 좀 모듈화좀 할 것
2. 사용하기 이~~~지 하게 좀
'''

def set_pixmap_image_in_lbl(lbl, pixmap, img):
    pixmap = QPixmap.fromImage(img)

    lbl.setPixmap(pixmap)
    lbl.setFixedWidth = pixmap.width()
    lbl.setFixedHeight = pixmap.height()

class ProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setRange(0, 1)
        self.setAlignment(Qt.AlignCenter)

    def Progressing(self):
        self.repaint()

    def Start(self):
        self.setRange(0, 0)
        return True

    def End(self):
        self.setRange(0, 1)
        return True

class FactorSlider(QWidget):
    slider = None
    lcd = None

    init_value = 5

    def __init__(self):
        super().__init__()
        self.__initUI__()

    def __initUI__(self):
        self.slider = QSlider(Qt.Horizontal, self)
        self.lcd = QLCDNumber(3, self)

        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(self.init_value)
        self.slider.setTickInterval(1)

        self.lcd.display(self.init_value)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)
        vbox.addWidget(self.slider)
        self.setLayout(vbox)

        self.slider.valueChanged.connect(self.lcd.display)

    def value(self):
        return (self.slider.value() / 100.0)

class ComboBox(QWidget):
    cb = None

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.cb = QComboBox(self)
        self.cb.addItem('갯수', userData = 0)
        self.cb.addItem('1', userData = 1)
        self.cb.addItem('5', userData = 5)
        self.cb.addItem('10', userData = 10)
        self.cb.addItem('20', userData = 20)
        self.cb.addItem('50', userData = 50)
        self.cb.addItem('100', userData = 100)

        vbox = QVBoxLayout()
        vbox.addWidget(self.cb)
        self.setLayout(vbox)

    def value(self):
        return self.cb.currentData()

# 나중에 이걸로 모듈화할거임
class Pixmap(QLabel):
    qpixmap = None
    qimg = None
    img = None

    def __init__(self):
        super().__init__()

class Frame(QMainWindow):
    widget = None

    origin_pixmap = None # pixmap to show origin image
    origin_qimg = None
    origin_img = None

    result_pixmap = None # pixmap to show result image
    result_qimg = None
    result_img = None

    lbl_origin_img = None # label to store origin image
    lbl_result_img = None # label to store result image

    hbox = None # Vertical box to store labels

    # slider to controll image modulation factor
    slider = None

    # check box to check hsv
    ckbox_mode = None
    ckbox_H = None
    ckbox_S = None
    ckbox_V = None

    # combo box to controll how many create pictures
    cb = None

    pbar = None # progress bar can toggle
    

    def __init__(self):
        super().__init__()

        self.initUI()

    # Initiate app
    def initUI(self):

        # 메뉴바에서 이미지 파일 여는 것
        openAction = QAction('Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('이미지 파일 열기')
        openAction.triggered.connect(self.chooseImage)

        # 메뉴바에서 프로그램 종료하는 것
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('프로그램 종료')
        exitAction.triggered.connect(qApp.quit)

        # 메뉴바 초기화
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)

        self.widget = QWidget(self)
        self.setCentralWidget(self.widget)

        # 이미지 표시할 라벨들 초기화
        self.origin_pixmap = QPixmap()
        self.result_pixmap = QPixmap()

        self.lbl_origin_img = QLabel()
        self.lbl_origin_img.setPixmap(self.origin_pixmap)
        self.lbl_result_img = QLabel()
        self.lbl_result_img.setPixmap(self.result_pixmap)

        # 이미지 변조 펙터를 조절할 슬라이더
        self.slider = FactorSlider()

        # 체크 박스 초기화
        self.ckbox_mode = QCheckBox('대입 모드')
        self.ckbox_H = QCheckBox('색상')
        self.ckbox_H.toggle()
        self.ckbox_S = QCheckBox('채도')
        self.ckbox_V = QCheckBox('명도')
        
        # 콤보 박스 초기화
        self.cb = ComboBox()

        hbox_ckboxlist = QHBoxLayout()
        hbox_ckboxlist.addWidget(self.ckbox_mode)
        hbox_ckboxlist.addWidget(self.ckbox_H)
        hbox_ckboxlist.addWidget(self.ckbox_S)
        hbox_ckboxlist.addWidget(self.ckbox_V)
        hbox_ckboxlist.addWidget(self.cb)

        # 버튼 초기화
        btn = QPushButton('&이미지 변조')
        btn.setCheckable(False)
        btn.setShortcut('Ctrl+T')
        btn.clicked.connect(self.ImageModulation)
        

        # 프로그래스 바 초기화
        self.pbar = ProgressBar()

        vbox = QVBoxLayout()
        vbox.addWidget(self.slider)
        vbox.addLayout(hbox_ckboxlist)
        vbox.addWidget(btn)
        vbox.addWidget(self.pbar)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl_origin_img)
        self.hbox.addLayout(vbox)
        self.hbox.addWidget(self.lbl_result_img)

        self.widget.setLayout(self.hbox)

        self.statusBar()

        self.setWindowTitle('이미지 변조기')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    # Show file dialog to open files
    def chooseImage(self):

        fname = QFileDialog.getOpenFileName(self, caption = '이미지 파일을 입력하세요.',
                                           filter = "Images (*.png *.tif *.jpg);;All files (*.*)")
        print(fname[0])

        try:
            self.origin_img = Image.open(fname[0])
            self.reuslt_img = self.origin_img

            self.setOriginImage(self.origin_img)
            self.setResultImage(self.reuslt_img)
            print("이미지 불러오기 완료")
        except Exception as e:
            print("이미지 불러오기 실패\n", e)
            pass

        return True

    # 원본 이미지를 pixmap에 로드
    def setOriginImage(self, img):
        self.origin_qimg = ImageQt.ImageQt(img)

        set_pixmap_image_in_lbl(self.lbl_origin_img, self.origin_pixmap, self.origin_qimg)
        return True
    # 변활될 이미지를 pixmap에 로드
    def setResultImage(self, img):
        self.result_qimg = ImageQt.ImageQt(img)

        set_pixmap_image_in_lbl(self.lbl_result_img, self.result_pixmap, self.result_qimg)
        return True

    # 이미지 변조
    def ImageModulation(self):
        num = self.cb.value()

        for i in range(0, num):
            self.changeImage()

        return True

    def changeImage(self):
        self.pbar.Start()

        if(self.origin_img):
            self.result_img = Image.new('RGB', self.origin_img.size, (0, 0, 0))
            (width, height) = self.origin_img.size
            pixels_dst = self.result_img.load()
            pixels_ori = self.origin_img.load()

            rand_h, rand_v, rand_s = 0, 0, 0

            if(self.ckbox_H.isChecked()):
                rand_h = (random.random() * pixel.PI2 * 2 - pixel.PI2) * self.slider.value()
            if(self.ckbox_S.isChecked()):
                rand_s = (random.random() * 2 - 1) * self.slider.value()
            if(self.ckbox_V.isChecked()):
                rand_v = (random.random() * 2 - 1) * self.slider.value()

            for y in range(0, height):
                for x in range(0, width):
                    color = pixels_ori[x, y]
                    hsv = pixel.rgb_to_hsv(color)

                    # 체크박스 모드에 따라 변조 방식을 자유롭게 설정하도록 할 것
                    # 메뉴바에서 선택하는 것도 나쁘지 않을 듯
                    if(self.ckbox_mode.isChecked()):
                        hsv = pixel.modulate_hsv_assign(hsv, h = rand_h, s = rand_s, v = rand_v)
                    else:
                        hsv = pixel.modulate_hsv_plus(hsv, h = rand_h, s = rand_s, v = rand_v)

                    color = pixel.hsv_to_rgb(hsv)
                    pixels_dst[x, y] = tuple(color)
                self.pbar.Progressing()

            self.setResultImage(self.result_img)
            if(self.ckbox_mode.isChecked()):
                self.saveImage((rand_h * pixel.PI / 180) ,(rand_s * 100), (rand_v * 100), 'W') # 대입
            else:
                self.saveImage((rand_h * pixel.PI / 180) ,(rand_s * 100), (rand_v * 100), 'A') # 더하기

        return self.pbar.End()

    def saveImage(self, H, S, V, dec):
        temp = random.random()
        h = hashlib.md5(str(temp).encode('utf8')).hexdigest()

        self.result_img.save('H(%0.4f)S(%0.4f)V(%0.4f)%s-%s.png' % (H, S, V, dec, h[:5]))
        return True

def main(argv):
    app = QApplication(argv)
    frame = Frame()
    sys.exit(app.exec_())
    return True
