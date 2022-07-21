from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from steam import *
from sys import exit
from tvn import *
import httpx
import traceback
import hashlib
import pygame
from time import time,sleep
from subprocess import Popen, PIPE,call
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QEvent, Qt
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
from PyQt5.QtGui import QPalette, QColor, QFont, QFontDatabase,QMovie
import sys

global version
version = '0.3.2'
user_agent = 'toast_ua'
default_url = 'https://toast.openfortress.fun/toast/'


def clickable(widget):  # make this function global
    class Filter(QObject):
        clicked = pyqtSignal()

        def eventFilter(self, obj, event):
            if obj == widget and event.type() == QEvent.MouseButtonRelease and obj.rect().contains(event.pos()):
                self.clicked.emit()
                return True
            else:
                return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked
def ResolvePath(obj):
    if getattr(sys, "frozen", False):
        # PyInstaller executable
        return str(Path(sys._MEIPASS).resolve().joinpath(Path(obj)))
    else:
        # Raw .py file
        return obj



class Ui_MainWindow(object):
    wasWarned = False
    verWarned = False
    muted = True
    downloading = False
    def play(self,path,chan):
        if not self.muted:
            pygame.mixer.Channel(chan).play(pygame.mixer.Sound(path))
    def stop(self,chan):
        pygame.mixer.Channel(chan).stop()
    def setupUi(self, app, MainWindow, advWindow):
        pygame.init()
        pygame.mixer.set_num_channels(10)
        font_db = QFontDatabase()
        font_db.addApplicationFont(ResolvePath("Staatliches-Regular.ttf"))
        font_db.addApplicationFont(ResolvePath("Roboto-Regular.ttf"))
        # families = font_db.applicationFontFamilies(font_id)
        font = QFont("Staatliches")
        QApplication.setFont(font)
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(653, 450)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(653, 450))
        MainWindow.setMaximumSize(QtCore.QSize(653, 450))
        MainWindow.setAcceptDrops(False)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)

        advWindow.setObjectName("advWindow")
        advWindow.setWindowTitle("Advanced Settings")
        advWindow.setEnabled(False)
        advWindow.resize(597, 254)
        advWindow.setSizePolicy(sizePolicy)
        advWindow.setMinimumSize(QtCore.QSize(597, 254))
        advWindow.setMaximumSize(QtCore.QSize(597, 254))
        advWindow.setAcceptDrops(False)
        advWindow.setWindowOpacity(1.0)

        self.centralwidget2 = QtWidgets.QWidget(advWindow)
        self.centralwidget2.setObjectName("centralwidget2")

        self.downloadurl = QtWidgets.QLabel(self.centralwidget2)
        self.downloadurl.setObjectName("downloadurl")
        self.downloadurl.setGeometry(QtCore.QRect(30, 40, 193, 35))
        self.downloadurl.setMinimumSize(QtCore.QSize(193, 35))
        self.downloadurl.setMaximumSize(QtCore.QSize(193, 35))
        self.font5 = QFont()
        self.font5.setFamily("Staatliches")
        self.font5.setPointSize(20)
        self.font5.setBold(False)
        self.font5.setItalic(False)
        self.font5.setWeight(50)
        self.downloadurl.setFont(self.font5)
        self.downloadurl.setStyleSheet("color: rgb(238, 225, 207);")
        self.downloadurl.setTextFormat(Qt.PlainText)
        self.downloadurl.setScaledContents(False)
        self.downloadurl.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.gamedir = QtWidgets.QLabel(self.centralwidget2)
        self.gamedir.setObjectName("gamedir")
        self.gamedir.setGeometry(QtCore.QRect(30, 100, 193, 35))
        self.gamedir.setMinimumSize(QtCore.QSize(193, 35))
        self.gamedir.setMaximumSize(QtCore.QSize(193, 35))
        self.gamedir.setFont(self.font5);
        self.gamedir.setStyleSheet("color: rgb(238, 225, 207);")
        self.gamedir.setTextFormat(Qt.PlainText)
        self.gamedir.setScaledContents(False)
        self.gamedir.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.launchoptions = QtWidgets.QLabel(self.centralwidget2)
        self.launchoptions.setObjectName("launchoptions")
        self.launchoptions.setGeometry(QtCore.QRect(30, 160, 193, 35))
        self.launchoptions.setMinimumSize(QtCore.QSize(193, 35))
        self.launchoptions.setMaximumSize(QtCore.QSize(193, 35))
        self.launchoptions.setFont(self.font5)
        self.launchoptions.setStyleSheet("color: rgb(238, 225, 207);")
        self.launchoptions.setTextFormat(Qt.PlainText)
        self.launchoptions.setScaledContents(False)
        self.launchoptions.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget2)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QtCore.QRect(200, 220, 193, 28))
        self.buttonBox.setMinimumSize(QtCore.QSize(193, 28))
        self.buttonBox.setMaximumSize(QtCore.QSize(193, 28))
        self.font6 = QFont()
        self.font6.setFamily("Staatliches")
        self.font6.setPointSize(12)
        self.font7 = QFont()
        self.font7.setFamily("Roboto")
        self.font7.setPointSize(12)
        self.buttonBox.setFont(self.font7)
        self.buttonBox.setStyleSheet("color: rgb(238, 225, 207);")
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.downloadurlbox = QtWidgets.QLineEdit(self.centralwidget2)
        self.downloadurlbox.setFont(self.font7)
        self.downloadurlbox.setObjectName("downloadurlbox")
        self.downloadurlbox.setGeometry(QtCore.QRect(250, 44, 311, 31))
        self.downloadurlbox.setMinimumSize(QtCore.QSize(311, 31))
        self.downloadurlbox.setMaximumSize(QtCore.QSize(311, 31))
        self.gamedirbox = QtWidgets.QLineEdit(self.centralwidget2)
        self.gamedirbox.setFont(self.font7)
        self.gamedirbox.setObjectName("gamedirbox")
        self.gamedirbox.setGeometry(QtCore.QRect(250, 100, 311, 31))
        self.gamedirbox.setMinimumSize(QtCore.QSize(311, 31))
        self.gamedirbox.setMaximumSize(QtCore.QSize(311, 31))
        self.launchoptionsbox = QtWidgets.QLineEdit(self.centralwidget2)
        self.launchoptionsbox.setFont(self.font7)
        self.launchoptionsbox.setObjectName("launchoptionsbox")
        self.launchoptionsbox.setGeometry(QtCore.QRect(250, 160, 311, 31))
        self.launchoptionsbox.setMinimumSize(QtCore.QSize(311, 31))
        self.launchoptionsbox.setMaximumSize(QtCore.QSize(311, 31))

        self.gamedirbox.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
        self.gamedirbox.setEnabled(False)
        # clickable(self.gamedirbox).connect(self.downloadWarning)
        clickable(self.downloadurlbox).connect(self.downloadWarning)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 60, 150, 150))
        self.label.setText("")
        self.label.setScaledContents(True)
        self.label.setPixmap(QtGui.QPixmap(ResolvePath("toast.png")))

        self.secret = QtWidgets.QLabel(self.centralwidget)
        self.secret.setGeometry(QtCore.QRect(50, 50, 161, 171))
        self.secret.setMinimumSize(QtCore.QSize(161, 171))
        self.secret.setMaximumSize(QtCore.QSize(161, 171))
        self.secret.setText("")
        self.secret.setScaledContents(True)
        self.secret.setPixmap(QtGui.QPixmap(ResolvePath("how.png")))
        self.secret.setVisible(False)

        self.mute = QtWidgets.QPushButton(self.centralwidget)
        self.mute.setObjectName("mute")
        self.mute.setText("")
        self.mute.setGeometry(QtCore.QRect(20, 20, 31, 28))
        self.muteico = QtGui.QIcon()
        self.muteico.addPixmap(QtGui.QPixmap(ResolvePath("muted.png")))
        self.upico = QtGui.QIcon()
        self.upico.addPixmap(QtGui.QPixmap(ResolvePath("up.png")))       
        self.mute.setIcon(self.muteico)
        clickable(self.mute).connect(self.clickMute)

        #self.movie = QMovie(ResolvePath("toast.gif"))

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(ResolvePath("toast.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        advWindow.setWindowIcon(icon)
        self.launcher = QtWidgets.QLabel(self.centralwidget)
        self.launcher.setObjectName("launcher")
        self.launcher.setGeometry(QtCore.QRect(260, 160, 361, 50))
        self.launcher.setAlignment(Qt.AlignRight)
        self.font1 = QFont()
        self.font1.setFamily("Staatliches")
        self.font1.setPointSize(28)
        self.font1.setBold(False)
        self.font1.setItalic(False)
        self.font1.setWeight(50)
        self.launcher.setFont(self.font1)
        self.launcher.setStyleSheet("color: rgb(238, 225, 207)")
        # launcher.setTextFormat(Qt.PlainText)
        self.launcher.setScaledContents(False)
        self.oftoast = QtWidgets.QLabel(self.centralwidget)
        self.oftoast.setObjectName("oftoast")
        if platform.startswith('win32'):
            self.oftoast.setGeometry(QtCore.QRect(350, 70, 361, 100))
        else:
            self.oftoast.setGeometry(QtCore.QRect(270, 70, 361, 100))
        self.font2 = QFont()
        self.font2.setFamily("Staatliches")
        self.font2.setPointSize(72)
        self.font2.setBold(False)
        self.font2.setItalic(False)
        self.font2.setWeight(50)
        self.oftoast.setFont(self.font2)
        self.oftoast.setStyleSheet("color: rgb(238, 225, 207)")
        self.oftoast.setTextFormat(Qt.PlainText)
        self.oftoast.setScaledContents(True)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setStyleSheet("color: rgb(238, 225, 207);")
        self.line.setGeometry(QtCore.QRect(20, 260, 611, 16))
        self.line.setMaximumSize(QtCore.QSize(621, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        p = QPalette()
        p.setColor(QPalette.Highlight, QColor(144, 106, 172))
        self.progressBar.setPalette(p)
        self.progressBar.setGeometry(QtCore.QRect(150, 340, 471, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setVisible(False)

        self.progressBarText = QtWidgets.QLabel(self.centralwidget)
        self.progressBarText.setGeometry(QtCore.QRect(150, 300, 168, 41))
        self.progressBarText.setObjectName("progressBarText")
        self.progressBarText.setMinimumSize(QtCore.QSize(168, 41))
        self.progressBarText.setMaximumSize(QtCore.QSize(168, 41))
        self.progressBarText.setFont(self.font1)
        self.progressBarText.setStyleSheet("color: rgb(238, 225, 207);")
        self.progressBarText.setScaledContents(False)
        self.progressBarText.setVisible(False)

        self.font4 = QFont()
        self.font4.setFamily("Roboto")
        self.font4.setPointSize(10)

        self.progressBarTextUnder = QtWidgets.QLabel(self.centralwidget)
        self.progressBarTextUnder.setGeometry(QtCore.QRect(152, 370, 451, 45))
        self.progressBarTextUnder.setObjectName("progressBarText")
        self.progressBarTextUnder.setFont(self.font4)
        self.progressBarTextUnder.setStyleSheet("color: rgb(238, 225, 207);")
        self.progressBarTextUnder.setVisible(False)
        self.progressBarTextUnder.setAlignment(Qt.AlignLeft)
        self.progressBarTextUnder.setVisible(False)

        MainWindow.setCentralWidget(self.centralwidget)

        self.launch = QtWidgets.QPushButton(self.centralwidget)
        self.launch.setObjectName("launch")
        self.launch.setGeometry(QtCore.QRect(20, 290, 93, 28))
        self.font3 = QFont()
        self.font3.setFamily("Staatliches")
        self.font3.setPointSize(12)
        self.launch.setFont(self.font3)
        self.launch.setStyleSheet("color: rgb(238, 225, 207)")

        self.verify = QtWidgets.QPushButton(self.centralwidget)
        self.verify.setObjectName("verify")
        self.verify.setGeometry(QtCore.QRect(20, 330, 93, 28))
        self.verify.setFont(self.font3)
        self.verify.setStyleSheet("color: rgb(238, 225, 207)")
        clickable(self.verify).connect(self.clickVerify)

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setGeometry(QtCore.QRect(20, 360, 91, 20))
        self.line_2.setStyleSheet("color: rgb(238, 225, 207);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.advanced = QtWidgets.QPushButton(self.centralwidget)
        self.advanced.setObjectName("advanced")
        self.advanced.setGeometry(QtCore.QRect(20, 380, 93, 28))
        self.advanced.setFont(self.font3)
        self.advanced.setStyleSheet("color: rgb(238, 225, 207)")
        clickable(self.advanced).connect(self.clickAdvanced)


        self.secretText = QtWidgets.QLabel(self.centralwidget)
        self.secretText.setObjectName("secretText")
        self.secretText.setGeometry(QtCore.QRect(400, 220, 168, 41))
        self.secretText.setFont(self.font1)
        self.secretText.setVisible(False)

        self.installed = QtWidgets.QLabel(self.centralwidget)
        self.installed.setObjectName("installed")
        self.installed.setGeometry(QtCore.QRect(140, 290, 480, 50))
        self.installed.setFont(self.font1)
        self.installed.setStyleSheet("color: rgb(238, 225, 207)")
        self.installed.setAlignment(Qt.AlignRight)
        
        self.latest = QtWidgets.QLabel(self.centralwidget)
        self.latest.setObjectName("latest")
        self.latest.setGeometry(QtCore.QRect(140, 350, 480, 50))
        self.latest.setFont(self.font1)
        self.latest.setStyleSheet("color: rgb(238, 225, 207)")
        self.latest.setAlignment(Qt.AlignRight)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OFToast " + version))
        self.launcher.setText(_translate("MainWindow", "Launcher"))
        self.oftoast.setText(_translate("MainWindow", "OFToast"))
        self.launch.setText(_translate("MainWindow", "Launch"))
        self.verify.setText(_translate("MainWindow", "Verify"))
        self.secretText.setText(_translate("MainWindow", "HOW?"))
        self.advanced.setText(_translate("MainWindow", "Advanced"))
        self.installed.setText(_translate("MainWindow", "Current Game Version:"))
        self.latest.setText(_translate("MainWindow", "Latest Game Version:"))
        self.progressBarText.setText(_translate("MainWindow", "Installing..."))
        self.progressBarTextUnder.setText(_translate("MainWindow", ""))
        self.downloadurl.setText(_translate("MainWindow", "Download URL:"))
        self.gamedir.setText(_translate("MainWindow", "Game Directory:"))
        self.launchoptions.setText(_translate("MainWindow", "Launch Options:"))
        self.downloadurlbox.setText(_translate("MainWindow", "https://toast.openfortress.fun/toast/"))
        self.gamedirbox.setText(_translate("MainWindow", "GAMEDIR"))
        self.launchoptionsbox.setText(_translate("MainWindow", "-console"))

        # self.lineEdit.setText(_translate("MainWindow", "GAMEDIR"))
        # self.label_2.setText(_translate("MainWindow", "Download URL:"))
        # self.label_4.setText(_translate("MainWindow", "Install Folder:"))
        # self.label_status.setText(_translate("MainWindow", "Waiting to Download"))
        # self.lineEdit_2.setText(_translate("MainWindow", "https://toast.openfortress.fun/toast"))
        #self.pushButton.setText(_translate("MainWindow", "Install"))
        #self.pushButton_2.setText(_translate("MainWindow", "Advanced"))
        #self.pushButton_3.setText(_translate("MainWindow", "Verify"))
        #self.pushButton_5.setText(_translate("MainWindow", "Unmute"))
        #self.label_3.setText(_translate("MainWindow", "Installed Revision: None"))
        #self.pushButton_4.setText(_translate("MainWindow", "Launch"))

    #def clickBrowse(self):
    #    temp = self.lineEdit.text()
    #    gamepath = QFileDialog.getExistingDirectory(MainWindow, "Game path", "")
    #    if gamepath == '':
    #        self.lineEdit.setText(temp)
    #    else:
    #        self.lineEdit.setText(gamepath)
    #    revision = get_installed_revision(Path(self.lineEdit.text()))
    #    if revision >= 0:
    #        self.label_3.setText("Installed Revision: " + str(revision))
    #    else:
    #        self.label_3.setText("Installed Revision: None")

    def clickUpdate(self):
        self.play(ResolvePath("toast.wav"),0)
        self.play(ResolvePath("start.wav"),1)
        global version
        try:
            # self.pushButton.setText('Updating...')
            self.progressBarText.setFont(self.font5)
            self.progressBarText.setText('Downloading...')
            self.progressBarTextUnder.setVisible(True)
            self.progressBar.setVisible(True)
            self.progressBarText.setVisible(True)
            self.installed.setVisible(False)
            self.latest.setVisible(False)
            self.verify.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.verify.setEnabled(False)
            self.launch.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.launch.setEnabled(False)
            self.advanced.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.advanced.setEnabled(False)
            app.processEvents()
            game_path = Path(self.gamedirbox.text())
            url = self.downloadurlbox.text()
            response = httpx.get(url, headers={'user-agent': user_agent}, follow_redirects=True)
            resUrl = response.url
            url = "https://" + resUrl.host + "/toast/"
            print("Server Selected: " + url)
            if 'open_fortress' not in str(game_path):
                try:
                    Path.mkdir(game_path / Path('open_fortress'))
                except FileExistsError:
                    pass
            installed_revision = get_installed_revision(game_path)
            try:
                num_threads = get_threads(url)
                latest_ver = get_latest_ver(url)
                latest_revision = fetch_latest_revision(url)
            except:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("OFToast")
                errorMsg.setText("Invalid URL!")
                errorMsg.exec_()
                error_message = traceback.format_exc()
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("rei?")
                errorMsg.setText(
                    "Something's gone wrong! Post the following error in the troubleshooting channel: " + error_message)
                errorMsg.exec_()
                existing_game_check(self, MainWindow)
                return
            print(version)
            if latest_ver != version and self.verWarned == False:
                self.verWarned = True
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Launcher Out Of Date!")
                errorMsg.setText(
                    "This isn't the latest version of the launcher! Please ensure you update here: https://toast.openfortress.fun/toast/ \nlatest "
                    "version: " + latest_ver)
                errorMsg.exec_()
            revisions = fetch_revisions(url, installed_revision, latest_revision)
            changes = replay_changes(revisions)
            writes = list(filter(lambda x: x["type"] == TYPE_WRITE, changes))
            todl = [[url + "objects/" + x["object"], game_path / x["path"], x["hash"]] for x in writes]
            try:
                os.remove(game_path / ".revision")
            except FileNotFoundError:
                pass

            for x in list(filter(lambda x: x["type"] == TYPE_DELETE, changes)):
                try:
                    os.remove(game_path / x["path"])
                except FileNotFoundError:
                    pass

            for x in list(filter(lambda x: x["type"] == TYPE_MKDIR, changes)):
                try:
                    os.mkdir(game_path / x["path"], 0o777)
                except FileExistsError:
                    pass
            # self.pushButton.setText('Downloading...')
            errs = ariabar(todl, self, app, num_threads)
            (game_path / ".revision").touch(0o777)
            (game_path / ".revision").write_text(str(latest_revision))
            if errs != []:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Toast Meditation")
                error_message = '\n'.join(errs)
                if "errorCode=29" or "errorCode=1" in error_message:
                    errorMsg.setText("The server appears to have overheated. Try again later.")
                else:
                    errorMsg.setText(
                    "Something's gone wrong with the downloading! Post the following error(s) in the troubleshooting "
                    "channel: " + error_message)
                errorMsg.exec_()
                exit(1)
            # now verify just in case
            self.clickVerify()
            self.progressBarTextUnder.setVisible(False)
            existing_game_check(self, MainWindow)
            return
        except TimeoutError or httpx.RequestError or ConnectionResetError or httpx.ReadTimeout:
            errorMsg = QMessageBox()

            errorMsg.setWindowTitle("hmm... raspberry.")
            errorMsg.setText("The server you've connected to is down! Try again later.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
        except TimeoutError or httpx.RequestError or ConnectionResetError:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("hmm... raspberry.")

            errorMsg.setText("The server you've connected to is down! Try again later.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
        except Exception as e:
            error_message = traceback.format_exc()
            if 'timeout' or 'reset' in error_message:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("I actually prefer marmalade.")
                errorMsg.setText("The server you've connected to is down! Try again later.")
                errorMsg.exec_()
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("Uh oh.")
            errorMsg.setText(
                "Something's gone catastrophically wrong! Post the following error in the troubleshooting channel: " + error_message)
            errorMsg.exec_()
            existing_game_check(self, MainWindow)

    def clickAdvanced(self):
        p = os.path.join(os.path.expanduser('~'), ".oftoast")
        if os.path.exists("{}/launchoptions.txt".format(p)):
            f = open("{}/launchoptions.txt".format(p), 'r')
            self.launchoptionsbox.setText(f.read())
            f.close()
            advWindow.setVisible(True)
            advWindow.setEnabled(True)
        else:
            if not os.path.exists(p):
                os.makedirs(p)
            f = open("{}/launchoptions.txt".format(p), 'w')
            f.write(self.launchoptionsbox.text())
            f.close()
            advWindow.setVisible(True)
            advWindow.setEnabled(True)
        #if os.path.exists("{}/gamedir.txt".format(p)):
        #    f = open("{}/gamedir.txt".format(p), 'r')
        #    self.gamedirbox.setText(f.read())
        #    f.close()
        #    advWindow.setVisible(True)
        #    advWindow.setEnabled(True)
        #else:
        #    if not os.path.exists(p):
        #        os.makedirs(p)
        #    f = open("{}/gamedir.txt".format(p), 'w')
        #    f.write(self.gamedirbox.text())
        #    f.close()
        #    advWindow.setVisible(True)
        #    advWindow.setEnabled(True)
        self.buttonBox.clicked.connect(self.advClose)
    
    def advClose(self):
        p = os.path.join(os.path.expanduser('~'), ".oftoast")
        f = open("{}/launchoptions.txt".format(p), 'w')
        f.write(str(self.launchoptionsbox.text()))
        f.close()
        #g = open("{}/launchoptions.txt".format(p), 'w')
        #g.write(str(self.gamedirbox.text()))
        #g.close()
        self.launchoptionsbox.setText(str(self.launchoptionsbox.text()))
        self.gamedirbox.setText(str(self.gamedirbox.text()))
        self.downloadurl.setText(str(self.downloadurl.text()))
        advWindow.setEnabled(False)
        advWindow.hide()


    def clickMute(self):
        if not self.muted:
            self.muted = True
            self.mute.setIcon(self.muteico)
            if pygame.mixer.Channel(0).get_busy():
                self.stop(0)
        else:
            self.muted = False
            self.mute.setIcon(self.upico)
            if not pygame.mixer.Channel(0).get_busy() and (self.downloading == True):
                self.play(ResolvePath("toast.wav"), 0)


    def clickVerify(self):
        #self.label.setMovie(self.movie)
        #self.movie.start()
        self.play(ResolvePath("start.wav"),1)
        global version
        try:
            self.progressBarText.setText('Verifying...')
            self.progressBarTextUnder.setVisible(False)
            self.progressBar.setVisible(True)
            self.progressBarText.setVisible(True)
            self.installed.setVisible(False)
            self.latest.setVisible(False)
            self.verify.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.verify.setEnabled(False)
            self.launch.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.launch.setEnabled(False)
            self.advanced.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            self.advanced.setEnabled(False)
            app.processEvents()
            game_path = Path(self.gamedirbox.text())
            url = self.downloadurlbox.text()
            response = httpx.get(url, headers={'user-agent': user_agent}, follow_redirects=True)
            resUrl = response.url
            url = "https://" + resUrl.host + "/toast/"
            print("Server Selected: " + url)
            if 'open_fortress' not in str(game_path):
                try:
                    Path.mkdir(game_path / Path('open_fortress'))
                except FileExistsError:
                    pass
            installed_revision = -1  # = get_installed_revision(game_path)
            try:
                num_threads = get_threads(url)
                latest_ver = get_latest_ver(url)
                latest_revision = fetch_latest_revision(url)
            except:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("OFToast")
                errorMsg.setText("Invalid URL!")
                errorMsg.exec_()
                #exit(1)
                existing_game_check(self, MainWindow)
                return
            print(version)
            if latest_ver != version and self.verWarned == False:
                self.verWarned = True
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("out of date!")
                errorMsg.setText(
                    "This isn't the latest version of the launcher! Please ensure you update here: https://toast.openfortress.fun/toast/ \nlatest "
                    "version: " + latest_ver)
                errorMsg.exec_()
            app.processEvents()
            revisions = fetch_revisions(url, installed_revision, latest_revision)
            changes = replay_changes(revisions)
            writes = list(filter(lambda x: x["type"] == TYPE_WRITE, changes))
            todl = [[url + "objects/" + x["object"], game_path / x["path"], x["hash"]] for x in writes]
            try:
                os.remove(game_path / ".revision")
            except FileNotFoundError:
                pass

            for x in list(filter(lambda x: x["type"] == TYPE_DELETE, changes)):
                try:
                    os.remove(game_path / x["path"])
                except FileNotFoundError:
                    pass

            for x in list(filter(lambda x: x["type"] == TYPE_MKDIR, changes)):
                try:
                    os.mkdir(game_path / x["path"], 0o777)
                except FileExistsError:
                    pass
            # self.pushButton_3.setText('Verifying...')
            self.play(ResolvePath("toast.wav"),0)
            self.downloading = True
            pbar_qt_verif(todl, self, app, num_threads)
            (game_path / ".revision").touch(0o777)
            (game_path / ".revision").write_text(str(latest_revision))
            self.stop(0)
            #self.movie.stop()
            exitMsg = QMessageBox()
            exitMsg.setWindowTitle("OFToast")
            exitMsg.setText("Done!")
            self.play(ResolvePath("done.wav"),1)
            self.downloading = False
            exitMsg.exec_()
            #exit(1)
            existing_game_check(self, MainWindow)
            self.progressBar.setValue(0)
            return
        except TimeoutError or httpx.RequestError or ConnectionResetError or httpx.ReadTimeout:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText("The server you've connected to is down! Try again later.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
        except TimeoutError or httpx.RequestError or ConnectionResetError:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText("The server you've connected to is down! Try again later.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
        except Exception as e:
            error_message = traceback.format_exc()
            if 'timeout' or 'reset' in error_message:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("rei?")
                errorMsg.setText("The server you've connected to is down! Try again later.")
                errorMsg.exec_()
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText(
                "Something's gone wrong! Post the following error in the troubleshooting channel: " + error_message)
            errorMsg.exec_()
            #exit(1)
            existing_game_check(self, MainWindow)
            return

    def clickLaunch(self):
        #self.label_status.setText('Launching...')
        args = self.launchoptionsbox.text()
        game_path = Path(self.gamedirbox.text())
        installed = os.path.isfile((game_path/Path('.revision')))
        if not installed:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText("You dont seem to have Open Fortress installed! Click the 'Install' button to install.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
            return

        if game_path != -1:
            library_folders = vdf.load(open(game_path.parents[1] / Path('libraryfolders.vdf')))['libraryfolders']
            sdkExists = False
            tf2Exists = False
            for x in library_folders:
                if ('243750' in library_folders[x]['apps'].keys()):
                    #print(library_folders[x]['path'])
                    sdkPath = (library_folders[x]['path'] / Path('steamapps') / Path('common') / Path('Source SDK Base 2013 Multiplayer'))
                    if os.path.isdir((sdkPath / Path('bin'))):
                        sdkExists = True
            for x in library_folders:
                if ('440' in library_folders[x]['apps'].keys()):
                    #print(library_folders[x]['path'])
                    tf2Path = (library_folders[x]['path'] / Path('steamapps') / Path('common') / Path('Team Fortress 2'))
                    if os.path.isdir((tf2Path / Path('bin'))):
                        tf2Exists = True


            if sdkExists == False and tf2Exists == False:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("rei?")
                errorMsg.setText("You dont seem to have the Source Sdk 2013 Base Multiplayer or Team Fortress 2 installed!" +
                "They are a requirement to play Open Fortress.\nHowever, you may continue if you think you've definitely have both installed.")
                errorMsg.exec_()
                existing_game_check(self, MainWindow)

            if sdkExists == False:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("rei?")
                errorMsg.setText("You dont seem to have the Source Sdk 2013 Base Multiplayer installed! It is a requirement to play Open Fortress.\nHowever, you may continue if you think you've definitely have it installed.")
                errorMsg.exec_()
                existing_game_check(self, MainWindow)

            if tf2Exists == False:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("rei?")
                errorMsg.setText("You dont seem to have Team Fortress 2 installed! It is a requirement to play Open Fortress.\nHowever, you may continue if you think you've definitely have it installed.")
                errorMsg.exec_()
                existing_game_check(self, MainWindow)


        else:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText("You dont seem to have Open Fortress installed! Click the 'Install' button to install.")
            errorMsg.exec_()
            existing_game_check(self, MainWindow)
            return
        app.processEvents()
        sdk = str(sdkPath)
        game = str(game_path)
        if platform.startswith('win32'):
            run("start /d \"{}\" hl2.exe -game \"{}\" -secure -steam {}".format(sdk,game,args), shell=True)
        else:
            # Needed to run under the Steam Runtime
            os.environ["SteamEnv"] = "1"
            #hl2 = "{sdk}\hl2_linux".format(sdk = sdkPath)
            #run([hl2, "-game", ofpath])
            Popen("\"{}/hl2.sh\" -game {} -secure -steam {}".format(sdk,game,args), shell=True)
        existing_game_check(self, MainWindow)

    def downloadWarning(self):
        if self.wasWarned == False:
            self.wasWarned = True
            warnMsg = QMessageBox()
            warnMsg.setWindowTitle("Warning")
            warnMsg.setText("Changing any of these input boxes is not advised. Only change it if you know what you're doing.")
            warnMsg.exec_()



def get_threads(url):
    r = httpx.get(url + "/reithreads", headers={'user-agent': user_agent}, follow_redirects=True)
    return int(r.text)


def get_latest_ver(url):
    r = httpx.get(url + "/reiversion", headers={'user-agent': user_agent}, follow_redirects=True)
    return r.text.strip()

def work(arr,verif = False):
    certs = ResolvePath("ca-certificates.crt")
    if sys.platform.startswith('win32'):
        ariapath = ResolvePath("aria2c.exe")
        drive = str(arr[1])[:2]
        cmd = '{} {} -o \"{}\" --checksum=md5={} --ca-certificate={} -d {} -j 100 --disable-ipv6 -m 10 -V -U {}/{}'.format(ariapath,arr[0],str(arr[1])[3:],arr[2],certs,drive,user_agent,version)

    else:
        ariapath = ResolvePath("./aria2c")
        cmd = '{} {} -o \"{}\" --checksum=md5={} --ca-certificate={} -d / -j 100 --disable-ipv6 -m 10 -V -U {}/{}'.format(ariapath,arr[0],arr[1],arr[2],certs,user_agent,version)
    done = False
    if (verif):
        cmd = cmd + " --auto-file-renaming=false --allow-overwrite=true"
    while not done:
        fp = Popen(cmd, shell=True, stdout=PIPE)
        fp.wait()
        content = [x.decode(encoding="utf-8", errors="ignore") for x in fp.stdout]
        if 'OK' in content[-1]:
            done = True
        else:
            print(content)


def work_verif(arr):
    try:
        if arr[1].exists():
            f = open(arr[1], "rb")
            fcontents = f.read()
            f.close()
            hasher = hashlib.md5()
            hasher.update(fcontents)
            hodl = hasher.hexdigest()
            if hodl == arr[2]:
                # good :)
                pass
            else:
                print(arr[1], "failed verification, redownloading...")
                work(arr,True)
        else:
            print(arr[1], "not found, redownloading...")
            work(arr)
    except:
        work_verif(arr)


def ariabar(arr, self, app, num_cpus=16):
    print(num_cpus)
    todl = ResolvePath("todl.txt")
    certs = ResolvePath("ca-certificates.crt")
    x = open(todl, 'w')
    totalfileCount = 0
    for a in arr:
        if sys.platform.startswith('win32'):
            x.write('{}\n out={}\n checksum=md5={}\n'.format(a[0],str(a[1])[3:], a[2]))
        else:
            x.write('{}\n out={}\n checksum=md5={}\n'.format(a[0],a[1], a[2]))
        totalfileCount = totalfileCount + 1
    x.close()
    length = len(arr)
    z = 0
    if sys.platform.startswith('win32'):
        ariapath = ResolvePath("aria2c.exe")
        drive = str(arr[0][1])[:2]
        fp = Popen('{} --ca-certificate={} -i {} -d {} -x {} -j 100 -m 10 -V --disable-ipv6 -U {}/{}'.format(ariapath,certs,todl,drive,num_cpus,user_agent,version), shell=True,
                   stdin=PIPE, stdout=PIPE, universal_newlines=True)
    else:
        ariapath = ResolvePath("./aria2c")
        fp = Popen('{} --ca-certificate={} -i {} -d / -x {} -j 100 -m 10 -V --disable-ipv6 -U {}/{}'.format(ariapath,certs,todl,num_cpus,user_agent,version), shell=True,stdin=PIPE, stdout=PIPE, universal_newlines=True)
    done = False
    errs = []
    while not done:
        for l in fp.stdout:
            print(l)
            app.processEvents()
            if 'Verification finished successfully.' in l:
                z = z + 1
                self.progressBar.setValue(z)
                self.progressBar.setMaximum(length)
                fileName = l.split("open_fortress")[1]
                self.progressBarTextUnder.setText("open_fortress{} {}/{}".format(fileName,z,totalfileCount))
                if not self.muted:
                    if not pygame.mixer.Channel(0).get_busy():
                        self.play(ResolvePath("toast.wav"), 0)
                app.processEvents()
            if "(OK):download completed" or '(ERR):error occurred' in l:
                done = True
            if "Exception" in l:
                  errs.append(l)
            if "503" in l:
                done = True
    return errs

def pbar_qt_verif(iter, self, app, num_cpus=16):
    length = len(iter)
    z = 0
    executor = ThreadPoolExecutor(num_cpus)
    futures = {executor.submit(work_verif, x): x for x in iter}
    for _ in as_completed(futures):
        z = z + 1
        self.progressBar.setValue(z)
        self.progressBar.setMaximum(length)
        app.processEvents()


def get_revision(url: str, revision: int):
    r = httpx.get(url + "/" + str(revision), headers={'user-agent': user_agent}, follow_redirects=True)
    return json.loads(r.text)


def fetch_latest_revision(url):
    # r = urllib.request.urlopen()
    r = httpx.get(url + "revisions/latest", headers={'user-agent': user_agent}, follow_redirects=True)
    return int(r.text)


def fetch_revisions(url, first, last):
    revisions = []
    for x in range(first + 1, last + 1):
        if not (x < 0):
            # r = urllib.request.urlopen(url + "revisions/" + str(x))
            r = httpx.get(url + "revisions/" + str(x), headers={'user-agent': user_agent}, follow_redirects=True)
            revisions.append(json.loads(r.text))
    return revisions


def existing_game_check(ui, MainWindow):
    ofpath = getpath()
    ui.launch.setEnabled(True)
    ui.launch.setStyleSheet("color: rgb(238, 225, 207);")
    ui.verify.setEnabled(True)
    ui.verify.setStyleSheet("color: rgb(238, 225, 207);")
    ui.advanced.setEnabled(True)
    ui.advanced.setStyleSheet("color: rgb(238, 225, 207);")
    ui.progressBar.setVisible(False)
    ui.progressBarText.setVisible(False)
    ui.progressBarTextUnder.setVisible(False)
    ui.latest.setVisible(True)
    ui.installed.setGeometry(QtCore.QRect(140, 290, 480, 50))
    ui.installed.setVisible(True)
    if ofpath != -1:
        sdk_download(ofpath.parents[1])
        revision = get_installed_revision(ofpath)
        latest = fetch_latest_revision(default_url)
        if revision > 0:
            ui.installed.setText("Current Game Version: " + str(revision))
            ui.latest.setText("Latest Game Version: " + str(latest))
            if revision < latest:
                ui.launch.setText("Update")
                clickable(ui.launch).connect(ui.clickUpdate)
                ui.verify.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
                ui.verify.setEnabled(False)
            else:
                ui.launch.setText("Launch")
                clickable(ui.launch).connect(ui.clickLaunch)
                ui.verify.setStyleSheet("color: rgb(238, 225, 207);")
                ui.verify.setEnabled(True)
        else:
            ui.installed.setGeometry(QtCore.QRect(140, 290, 480, 50))
            ui.installed.setText("Click Install now!")
            ui.latest.setVisible(False)
            ui.verify.setStyleSheet("color: rgb(84, 82, 82);background-color: rgb(37, 27, 45);") # grey
            ui.verify.setEnabled(False)
            ui.launch.setText("Install")
            clickable(ui.launch).connect(ui.clickUpdate)

    ui.gamedirbox.setText(str(ofpath))


def set_theme(app, MainWindow, advWindow):
    QApplication.setStyle("fusion")
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor('#584169'))
    palette.setColor(QPalette.WindowText, QColor('#C8C1C7'))
    palette.setColor(QPalette.Base, QColor('#F7EAD6'))
    palette.setColor(QPalette.AlternateBase, QColor("#27234d"))
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    palette.setColor(QPalette.Text, QColor('#433157'))
    palette.setColor(QPalette.Button, QColor("#2C1642"))
    palette.setColor(QPalette.ButtonText, QColor('#C8C1C7'))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor("#584169"))
    palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))
    app.setPalette(palette)


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    advWindow = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    set_theme(app, MainWindow,advWindow)
    ui.setupUi(app, MainWindow, advWindow)
    existing_game_check(ui, MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())