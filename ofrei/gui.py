from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from steam import *
from sys import exit
from tvn import *
import httpx
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt5.QtGui import QPalette, QColor
import sys

global version
version = '0.1.3-SNAPSHOT'


class Ui_MainWindow(object):
    def setupUi(self, app, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(608, 180)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(608, 180))
        MainWindow.setMaximumSize(QtCore.QSize(608, 180))
        MainWindow.setAcceptDrops(False)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAnimated(True)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 131, 141))
        self.label.setText("")
        if getattr(sys, "frozen", False):
            # PyInstaller executable
            toasty = str(Path(sys._MEIPASS).resolve().joinpath("toast.png"))
        else:
            # Raw .py file
            toasty = "toast.png"
        self.label.setPixmap(QtGui.QPixmap(toasty))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(toasty), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.browse = QtWidgets.QPushButton(self.centralwidget)
        self.browse.setGeometry(QtCore.QRect(160, 20, 121, 28))
        self.browse.setObjectName("browse")
        self.browse.clicked.connect(self.clickBrowse)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(290, 20, 291, 28))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 60, 121, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(290, 60, 291, 28))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(160, 100, 421, 16))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(380, 130, 90, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.clickUpdate)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 130, 90, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.clickCancel)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 133, 211, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OFToast " + version))
        self.browse.setText(_translate("MainWindow", "Browse"))
        self.lineEdit.setText(_translate("MainWindow", "GAMEDIR"))
        self.label_2.setText(_translate("MainWindow", "Download URL"))
        self.lineEdit_2.setText(_translate("MainWindow", "https://toast.openfortress.fun/toast/"))
        self.pushButton.setText(_translate("MainWindow", "Update"))
        self.pushButton_2.setText(_translate("MainWindow", "Cancel"))
        self.label_3.setText(_translate("MainWindow", "Installed Revision: None"))

    def clickBrowse(self):
        temp = self.lineEdit.text()
        gamepath = QFileDialog.getExistingDirectory(MainWindow, "Game path", "")
        if gamepath == '':
            self.lineEdit.setText(temp)
        else:
            self.lineEdit.setText(gamepath)
        revision = get_installed_revision(Path(self.lineEdit.text()))
        if revision >= 0:
            self.label_3.setText("Installed Revision: " + str(revision))
        else:
            self.label_3.setText("Installed Revision: None")

    def clickUpdate(self):
        global version
        try:
            self.pushButton.setText('Updating')
            self.browse.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.pushButton_2.setDisabled(True)
            game_path = Path(self.lineEdit.text())
            url = self.lineEdit_2.text()
            if 'open_fortress' not in str(game_path):
                try:
                    Path.mkdir(game_path / Path('open_fortress'))
                except FileExistsError:
                    pass
            installed_revision = get_installed_revision(game_path)
            try:
                num_threads = get_threads(url)
            except:
                error_message = traceback.format_exc()
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Error!")
                errorMsg.setText("We failed to obtain the thread file from the server!" + error_message)
                errorMsg.exec_()
                exit(1)
            try:
                latest_ver = get_latest_ver(url)
            except:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Error!")
                errorMsg.setText("We failed to obtain the latest version file from the server!")
                errorMsg.exec_()
                exit(1)
            try:
                latest_revision = fetch_latest_revision(url)
            except:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Error!")
                errorMsg.setText("We failed to obtain the latest revision file from the server!")
                errorMsg.exec_()
                exit(1)
            print(version)
            if latest_ver != version:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Out-of-date Launcher!")
                errorMsg.setText(
                    "This isn't the latest version! you need to download the latest version from the website.\nlatest "
                    "version: " + latest_ver)
                errorMsg.exec_()
            try:
                revisions = fetch_revisions(url, installed_revision, latest_revision)
            except:
                error_message = traceback.format_exc()
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Error!")
                errorMsg.setText("We failed to obtain the revision file from the server!" + error_message)
                errorMsg.exec_()
                exit(1)
            changes = replay_changes(revisions)
            writes = list(filter(lambda x: x["type"] == TYPE_WRITE, changes))
            limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)
            client = httpx.Client(headers={'user-agent': 'Mozilla/5.0', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0'}, timeout=None, limits=limits)
            todl = [[url + "objects/" + x["object"], game_path / x["path"], client] for x in writes]
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
            self.pushButton.setText('Downloading')
            pbar_sg(todl, self, app, num_threads)
            self.pushButton.setText('Checking')
            done = False
            missing = False
            while not done:
                for x in writes:
                    if not (game_path / x["path"]).exists():
                        missing = True
                        while not (game_path / x["path"]).exists():
                            work([url + "objects/" + x["object"], game_path / x["path"], client])
                    else:
                        app.processEvents()
                if missing == False:
                    done = True
            (game_path / ".revision").touch(0o777)
            (game_path / ".revision").write_text(str(latest_revision))
            exitMsg = QMessageBox()
            exitMsg.setWindowTitle("OFToast")
            exitMsg.setText("Done!")
            exitMsg.exec_()
            exit(1)
        except TimeoutError or httpx.RequestError or ConnectionResetError or httpx.ReadTimeout:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText("We have lost connection to the server. Please try again later. Error Code 1")
            errorMsg.exec_()
        except TimeoutError or httpx.RequestError or ConnectionResetError:
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("Error!")
            errorMsg.setText("We have lost connection to the server. Please try again later. Error Code 2")
            errorMsg.exec_()
        except Exception as e:
            error_message = traceback.format_exc()
            if 'timeout' or 'reset' in error_message:
                errorMsg = QMessageBox()
                errorMsg.setWindowTitle("Error!")
                errorMsg.setText("We have lost connection to the server. Please try again later. Error Code 3")
                errorMsg.exec_()
            errorMsg = QMessageBox()
            errorMsg.setWindowTitle("rei?")
            errorMsg.setText(
                "Something's gone wrong! Post the following error in the troubleshooting channel: " + error_message)
            errorMsg.exec_()
            exit(1)

    def clickCancel(self):
        exit(1)


def get_threads(url):
    r = httpx.get(url + "/reithreads", timeout=None)
    return int(r.text)


def get_latest_ver(url):
    r = httpx.get(url + "/reiversion", timeout=None)
    return r.text.strip()


def work(arr):
    exists = False
    while exists == False:
        resp = arr[2].get(arr[0])
        file = open(arr[1], "wb+")
        file.write(resp.content)
        file.close()
        if arr[1].exists():
            exists = True
        else:
            print("file hasn't downloaded...")


def pbar_sg(iter, self, app, num_cpus=16):
    length = len(iter)
    z = 0
    executor = ThreadPoolExecutor(num_cpus)
    futures = {executor.submit(work, x): x for x in iter}
    for _ in as_completed(futures):
        z = z + 1
        self.progressBar.setValue(z)
        self.progressBar.setMaximum(length)
        app.processEvents()


def get_revision(url: str, revision: int):
    limits = httpx.Limits(max_keepalive_connections=None, max_connections=None)
    r = httpx.get(url + "/" + str(revision), timeout=None, limits=limits)
    return json.loads(r.text)


def existing_game_check(ui, MainWindow):
    ofpath = getpath()
    if ofpath != -1:
        sdk_download(ofpath.parents[1])
        revision = get_installed_revision(ofpath)
        if revision >= 0:
            path = os.path.join(ofpath, '.revision')
            os.remove(path)
            ui.label_3.setText("Repairing Game")
        ui.lineEdit.setText(str(ofpath))


def set_theme(app, MainWindow):
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
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    set_theme(app, MainWindow)
    ui.setupUi(app, MainWindow)
    existing_game_check(ui, MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
