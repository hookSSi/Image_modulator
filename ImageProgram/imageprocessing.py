import sys
from PIL import Image, ImageQt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
import pixel
import random

def set_pixmap_image_in_lbl(lbl, pixmap, img):
    pixmap = QPixmap.fromImage(img)

    lbl.setPixmap(pixmap)
    lbl.setFixedWidth = pixmap.width()
    lbl.setFixedHeight = pixmap.height()

class Frame(QMainWindow):
    widget = None

    origin_pixmap = None # pixmap to show origin image
    origin_qimg = None
    origin_img = None

    result_pixmap = None # pixmap to show result image
    origin_qimg = None
    result_img = None

    lbl_origin_img = None # label to store origin image
    lbl_result_img = None # label to store result image

    hbox = None # Vertical box to store labels

    # check box to check hsv
    ckbox_mode = None
    ckbox_H = None
    ckbox_S = None
    ckbox_V = None

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

        # 체크 박스 초기화
        self.ckbox_mode = QCheckBox('대입 모드')
        self.ckbox_mode.toggle()
        self.ckbox_H = QCheckBox('H')
        self.ckbox_H.toggle()
        self.ckbox_S = QCheckBox('S')
        self.ckbox_V = QCheckBox('V')

        hbox_ckboxlist = QHBoxLayout()
        hbox_ckboxlist.addWidget(self.ckbox_mode)
        hbox_ckboxlist.addWidget(self.ckbox_H)
        hbox_ckboxlist.addWidget(self.ckbox_S)
        hbox_ckboxlist.addWidget(self.ckbox_V)

        # 버튼 초기화
        btn = QPushButton('&이미지 변조')
        btn.setCheckable(False)
        btn.setShortcut('Ctrl+T')
        btn.clicked.connect(self.changeImage)

        # 프로그래스 바 초기화
        pbar = QProgressBar()

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_ckboxlist)
        vbox.addWidget(btn)
        vbox.addWidget(pbar)

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
    def changeImage(self):
        if(self.origin_img):
            self.result_img = Image.new('RGB', self.origin_img.size, (0, 0, 0))
            (width, height) = self.origin_img.size
            pixels_dst = self.result_img.load()
            pixels_ori = self.origin_img.load()

            rand_h, rand_v, rand_s = 0, 0, 0

            if(self.ckbox_H.isChecked()):
                rand_h = random.random() * 2 - 1
            if(self.ckbox_S.isChecked()):
                rand_s = random.random() * 2 - 1
            if(self.ckbox_V.isChecked()):
                rand_v = random.random() * 2 - 1

            print(rand_h)
            print(rand_s)
            print(rand_v)

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
            self.setResultImage(self.result_img)

            if(self.ckbox_mode.isChecked()):
                self.saveImage((rand_h * 100) ,(rand_s * 100), (rand_v * 100), '대입 변조')
            else:
                self.saveImage((rand_h * 100) ,(rand_s * 100), (rand_v * 100), '더하기 변조')
        return True

    def saveImage(self, H, S, V, dec):
        self.result_img.save('색상(%0.2f)채도(%0.2f)명도(%0.2f) %s.png' % (H, S, V, dec))
        return True

def main(argv):
    app = QApplication(argv)
    frame = Frame()
    sys.exit(app.exec_())
    return True
