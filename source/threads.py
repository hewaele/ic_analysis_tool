from PyQt5 import QtCore
from data_process import Data

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget, QInputDialog, QLineEdit, QDialog
from PyQt5.QtGui import *

from qt_source.ic_gui import Ui_MainWindow  # 导入创建的GUI类
from qt_source.child_gui import Ui_Dialog

import time
#继承 QThread 类
class DP(QtCore.QThread):
    #声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(bool)
    sinOut = pyqtSignal(int)

    #分析完成发送结果回去
    result = pyqtSignal(list)

    #构造函数里增加形参
    def __init__(self, pre_path, real_path, save_path, merge, parent = None, stop = False):
        super(DP, self).__init__(parent)
        #创建一个数据分析类

        self.pre_path = pre_path
        self.real_path = real_path
        self.save_path = save_path
        self.merge = merge
        self.stop = stop
        self.analysis_work = Data(self.pre_path, self.real_path, self.save_path, self.merge)

    #重写 run() 函数，在里面干大事。
    def run(self):
        #执行识别
        pass

        #执行分析
        self.analysis_work.draw()

        for i in range(200):
            if i % 100 == 0:
                self.sinOut.emit(int(time.time())%100)
                time.sleep(2)
        # print(self.analysis_work.result)
        self.result.emit(self.analysis_work.result)

        #大事干完了，发送一个信号告诉主线程窗口
        self.finishSignal.emit(True)


#定义子窗口
class childwindow(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        super(childwindow, self).__init__()
        self.setupUi(self)

        #显示该窗口
        self.show()

    def show_result(self):
        pass


class SHOW(QtCore.QThread):
    #声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(bool)

    #构造函数里增加形参
    def __init__(self, parent = None):
        super(SHOW, self).__init__(parent)

        #创建一个窗口类
        self.child_window = childwindow()

    #重写 run() 函数，在里面干大事。
    def run(self):
        self.child_window.show()
