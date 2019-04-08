# -*-coding:utf-8 -*-
import sys
import os
sys.path.append('f:\hewaele\python\mycode\ic_analysis_tool')
import so_class
import data_process
from threads import DP

from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget, QInputDialog, QLineEdit, QDialog, QHeaderView
from PyQt5.QtGui import *

from qt_source.ic_gui import Ui_MainWindow  # 导入创建的GUI类
from qt_source.child_gui import Ui_Dialog
from qt_source.image_gui import Ui_Dialog2

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
##############################初始化设置
        #设置默认路径
        self.image_path.setText('f:/hewaele/python/mycode/ic_analysis_tool/image/JM')
        self.template_path.setText('f:/hewaele/python/mycode/ic_analysis_tool/image/JMModel')
        self.analysis_path.setText('f:/hewaele/python/mycode/ic_analysis_tool/analysis_result')

        #设置默认的各类阈值
        self.set_roi_mune()
        self.threshold_dic = {}
        self.threshold_init()

        self.status.setText('已保存')
        self.status.setReadOnly(True)
        #进度条初始化
        self.progressBar.setValue(0)

        ######################################按钮触事件
        #打开图片文件夹
        self.chance_image.clicked.connect(self.get_image_path)
        #打开模板文件夹
        self.chance_template.clicked.connect(self.get_template_path)
        self.chance_analysis.clicked.connect(self.get_analysis_path)
        self.start_analysis.clicked.connect(self.data_analysis)

        #下拉菜单改变时更新各类参数
        self.roi_menu.currentIndexChanged.connect(self.show_threshold)
        self.save_threshold.clicked.connect(self.update_threshold)

        #判断文本是否发生改变
        self.min_threshold.textChanged.connect(self.threshold_status)
        self.max_threshold.textChanged.connect(self.threshold_status)
        self.min_bin_threshold.textChanged.connect(self.threshold_status)
        self.max_bin_threshold.textChanged.connect(self.threshold_status)

        self.show()

    def threshold_status(self):
        self.status.setText('已修改')

    def get_image_path(self):
        # QMessageBox.information(self, 'Information', '提示消息')
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                     '')  # 打开路径为xx，若不指定路径，默认打开当前py文件所在文件夹
        if len(directory) != 0:
            self.image_path.setText(directory)

    def get_template_path(self):

        # QMessageBox.information(self, 'Information', '提示消息')
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                       '')  # 打开路径为xx，若不指定路径，默认打开当前py文件所在文件夹

        if len(directory) != 0:
            self.template_path.setText(directory)
            #更新roi
            self.set_roi_mune()
            self.threshold_dic = {}
            self.threshold_init()

    def set_roi_mune(self):
        # 将之前数据删除
        self.roi_menu.clear()
        # 设置自下拉roi下拉菜单  根据模板多少
        for i in range(len(os.listdir(self.template_path.text())) - 1):
            self.roi_menu.insertItem(i, 'roi:' + str(i))

    def get_analysis_path(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选择文件夹",
                                                     '')
        if len(directory) != 0:
            self.analysis_path.setText(directory)

    # 进行数据分析
    def data_analysis(self):
        #将分析按钮锁死
        self.start_analysis.setDisabled(True)
        self.set_processbar(99)
        # 创建一个新的工作进程
        # 执行分析进程
        self.work_threads = DP(image_path=self.image_path.text(),
                               template_path=self.template_path.text(),
                               analysis_path=self.analysis_path.text(),
                               )

        self.work_threads.start()
        # self.work_threads.sinOut.connect(self.set_processbar)
        # 分析结束开启点击按钮
        self.work_threads.result.connect(self.get_result)
        self.work_threads.finishSignal.connect(self.work_done)

    def get_result(self, list):
        self.result = list

    def work_done(self):
        # 创建子窗口显示结果
        self.child_window = childwindow(data = self.result,
                                        image_path=self.analysis_path.text()
                                        )
        self.start_analysis.setDisabled(False)
        self.progressBar.setValue(0)

    def threshold_init(self):
        #获取roi个数
        roi_num = len(os.listdir(self.template_path.text()))-1
        for i in range(roi_num):
            self.threshold_dic['roi'+str(i)] = {}

        #
        for i in range(roi_num):
            self.threshold_dic['roi'+str(i)]['min_t1'] = 0
            self.threshold_dic['roi'+str(i)]['max_t1'] = 100
            self.threshold_dic['roi'+str(i)]['min_t2'] = 0
            self.threshold_dic['roi'+str(i)]['max_t2'] = 255
        self.show_threshold()

    def show_threshold(self):
        try:
            roi = self.roi_menu.currentIndex()
            #根据roi显示当前字典信息
            #创建一个阈值字典
            threshold = self.threshold_dic['roi'+str(roi)]
            self.min_threshold.setText(str(threshold['min_t1']))
            self.max_threshold.setText(str(threshold['max_t1']))
            self.min_bin_threshold.setText(str(threshold['min_t2']))
            self.max_bin_threshold.setText(str(threshold['max_t2']))
        except:
            pass
        self.status.setText('已保存')


    def update_threshold(self):
        roi = self.roi_menu.currentIndex()
        #将当前edittxt数值设置为阈值
        self.threshold_dic['roi' + str(roi)]['min_t1'] = self.min_threshold.text()
        self.threshold_dic['roi' + str(roi)]['max_t1'] = self.max_threshold.text()
        self.threshold_dic['roi' + str(roi)]['min_t2'] = self.min_bin_threshold.text()
        self.threshold_dic['roi' + str(roi)]['max_t2'] = self.max_bin_threshold.text()

        self.status.setText('已保存')
    def set_processbar(self, num):
        self.progressBar.setValue(num)

# 定义数据表子窗口
class childwindow(QDialog, Ui_Dialog):
    def __init__(self, image_path, data = []):
        super(childwindow, self).__init__()
        self.setupUi(self)
        self.data = data
        # 显示该窗口
        self.image_path = image_path
        self.show_result()
        self.show()
        self.set_roi_menu()
        self.image_window = imagewindow()
        self.show_img.clicked.connect(self.result_vis)
    #根据表单行数，设置roi
    def set_roi_menu(self):

        for i in range(len(self.data)):
            self.roi_menu.insertItem(i, 'roi:'+str(i))

    def result_vis(self):
        #获取当前roi值
        roi = self.roi_menu.currentIndex()
        self.image_window.show_image(self.image_path, roi)

    def show_result(self):
        self.model = QStandardItemModel(len(self.data), 4)
        self.model.setHorizontalHeaderLabels(['roi', 'best_result', 'pre_threshold', 'bin_threshold'])

        for i, row in enumerate(self.data):
            for j, value in enumerate(row):
                item = QStandardItem(str(value))
                # 设置每个位置的文本值
                self.model.setItem(i, j, item)

        #todo 优化1 表格填满窗口
        #水平方向标签拓展剩下的窗口部分，填满表格
        self.tableView.horizontalHeader().setStretchLastSection(True)
        #水平方向，表格大小拓展到适当的尺寸
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 实例化表格视图，设置模型为自定义的模型
        # self.tableView = QTableView()
        self.tableView.setModel(self.model)
        self.tableView.show()

# 定义显示图片窗口
class imagewindow(QDialog, Ui_Dialog2):
    def __init__(self):
        super(imagewindow, self).__init__()
        self.setupUi(self)

    def show_image(self, path, roi):
        jpg = QtGui.QPixmap(os.path.join(path, 'roi_'+str(roi)+'_vis.png'))
        jpg = jpg.scaled(self.image_label.width(), self.image_label.height())
        self.image_label.setPixmap(jpg)
        self.image_label.show()
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())
