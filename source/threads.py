# -*-coding:utf-8 -*-
from PyQt5 import QtCore
from data_process import Data

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget, QInputDialog, QLineEdit, QDialog
from PyQt5.QtGui import *

from qt_source.ic_gui import Ui_MainWindow  # 导入创建的GUI类
from qt_source.child_gui import Ui_Dialog

import time
import ctypes
import os

#继承 QThread 类
class DP(QtCore.QThread):
    #声明一个信号，同时返回一个list，同理什么都能返回啦
    finishSignal = QtCore.pyqtSignal(bool)
    sinOut = pyqtSignal(int)

    #分析完成发送结果回去
    result = pyqtSignal(list)

    #构造函数里增加形参
    def __init__(self, image_path, template_path, analysis_path, parent = None):
        super(DP, self).__init__(parent)
        #创建一个数据分析类

        self.image_path = image_path
        self.template_path = template_path
        self.analysis_path = analysis_path

        self.pre_path = "f:/hewaele/python/mycode/ic_analysis_tool/pre_result/creat_test_data.csv"
        self.real_path = "f:/hewaele/python/mycode/ic_analysis_tool/pre_result/creat_real_data.csv"
        self.save_path = analysis_path
        self.merge = False
        self.analysis_work = Data(self.pre_path, self.real_path, self.save_path, self.merge)

    def recognize(self):
        #读入dll
        os.chdir("F:/hewaele/C语言/my_dll2/")
        self.dll = ctypes.windll.LoadLibrary('F:/hewaele/C语言/my_dll2/Project_stand_version.dll')

        #设置dll函数参数：模板  图片 结果路径 图片数量 识别阈值 二值化阈值
        print(self.template_path)
        p1 = bytes(self.template_path, 'utf8')
        p2 = bytes(self.image_path, 'utf8')
        p3 = bytes(self.analysis_path, 'utf8')
        p4 = ctypes.c_int(len(os.listdir(self.image_path)) - 1)
        p5 = ctypes.c_double(0.1)
        p6 = ctypes.c_int(20)

        self.dll.testoutput(p1, p2, p3, p4, p5, p6)

    #重写 run() 函数，在里面干大事。
    def run(self):
        #执行识别
        # self.recognize()
        print("recognize done")
        #执行分析
        self.analysis_work.draw()

        # for i in range(200):
        #     if i % 100 == 0:
        #         self.sinOut.emit(int(time.time())%100)
        #         time.sleep(2)
        self.result.emit(self.analysis_work.result)

        #大事干完了，发送一个信号告诉主线程窗口
        self.finishSignal.emit(True)


# #定义子窗口
# class childwindow(QDialog, Ui_Dialog):
#     def __init__(self, parent = None):
#         super(childwindow, self).__init__()
#         self.setupUi(self)
#
#         #显示该窗口
#         self.show()
#
#     def show_result(self):
#         pass
#
#
# class SHOW(QtCore.QThread):
#     #声明一个信号，同时返回一个list，同理什么都能返回啦
#     finishSignal = QtCore.pyqtSignal(bool)
#
#     #构造函数里增加形参
#     def __init__(self, parent = None):
#         super(SHOW, self).__init__(parent)
#
#         #创建一个窗口类
#         self.child_window = childwindow()
#
#     #重写 run() 函数，在里面干大事。
#     def run(self):
#         self.child_window.show()
