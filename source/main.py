import sys
import so_class
import data_process
from threads import DP, SHOW

from functools import partial

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDockWidget, QListWidget, QInputDialog, QLineEdit, QDialog, QHeaderView
from PyQt5.QtGui import *

from qt_source.ic_gui import Ui_MainWindow  # 导入创建的GUI类
from qt_source.child_gui import Ui_Dialog


class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.stop = True
        #设置默认的各类阈值
        self.min_threshold.setText('0')
        self.max_threshold.setText('100')
        self.min_bin_threshold.setText('0')
        self.max_bin_threshold.setText('255')
        self.progressBar.setValue(0)

        #设置默认路径
        self.image_path.setText('/home/hewaele/PycharmProjects/ic_analysis_tool/img')
        self.template_path.setText('/home/hewaele/PycharmProjects/ic_analysis_tool/template')
        self.analysis_path.setText('/home/hewaele/PycharmProjects/ic_analysis_tool/analysis_result')

        #打开图片文件夹
        self.chance_image.clicked.connect(self.get_image_path)
        #打开模板文件夹
        self.chance_template.clicked.connect(self.get_template_path)
        self.chance_analysis.clicked.connect(self.get_analysis_path)
        self.start_analysis.clicked.connect(self.data_analysis)

        self.show()

    def get_image_path(self):
        # QMessageBox.information(self, 'Information', '提示消息')
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                     '/home/hewaele/PycharmProjects/ic_analysis_tool/')  # 打开路径为xx，若不指定路径，默认打开当前py文件所在文件夹
        if len(directory) != 0:
            self.image_path.setText(directory)

    def get_template_path(self):
        # QMessageBox.information(self, 'Information', '提示消息')
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选取文件夹",
                                                       '/home/hewaele/PycharmProjects/ic_analysis_tool/')  # 打开路径为xx，若不指定路径，默认打开当前py文件所在文件夹

        if len(directory) != 0:
            self.template_path.setText(directory)

    #当点击分析按钮时弹出进度条 同时进行数据分析

    def get_analysis_path(self):
        directory = QFileDialog.getExistingDirectory(self,
                                                     "选择文件夹",
                                                     '/home/hewaele/PycharmProjects/ic_analysis_tool/')
        if len(directory) != 0:
            self.analysis_path.setText(directory)

    # 进行数据分析
    def data_analysis(self):
        #将按钮锁死
        self.start_analysis.setDisabled(True)
        # 创建一个新的工作进程

        # 获取各类参数
        # self.image = self.image_path.text()
        # self.template = self.template_path.text()
        #
        # self.min_t1 = int(self.min_threshold.toPlainText())
        # self.max_t1 = int(self.max_threshold.toPlainText())
        # self.min_t2 = int(self.min_bin_threshold.toPlainText())
        # self.max_t2 = int(self.max_bin_threshold.toPlainText())

        # 执行分析进程
        self.work_threads = DP(pre_path='../pre_result/creat_test_data.csv',
                               real_path='../pre_result/creat_real_data.csv',
                               save_path='../analysis_result/',
                               merge=False, stop=self.stop)

        self.work_threads.start()
        self.work_threads.sinOut.connect(self.set_processbar)
        # 分析结束开启点击按钮
        self.work_threads.result.connect(self.get_result)
        self.work_threads.finishSignal.connect(self.work_done)


    def get_textedit_values(self, textobj):

        return textobj.toPlainText()
    def get_result(self, list):
        self.result = list

    def work_done(self):

        # QMessageBox.information(self, 'Information', 'analysis done')
        # 创建子窗口显示结果
        self.child_window = childwindow(data = self.result)
        self.start_analysis.setDisabled(False)
        self.progressBar.setValue(0)

    def set_processbar(self, num):
        self.progressBar.setValue(num)


# 定义子窗口
class childwindow(QDialog, Ui_Dialog):
    def __init__(self, data = [], parent=None):
        super(childwindow, self).__init__()
        self.setupUi(self)
        self.data = data
        # 显示该窗口

        self.show_result()
        self.show()

    def show_result(self):
        self.model = QStandardItemModel(len(self.data), 4)
        self.model.setHorizontalHeaderLabels(['roi', 'best_result', 'pre_threshold', 'bin_threshold'])

        # #Todo 优化2 添加数据
        # self.model.appendRow([
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        #     QStandardItem('row %s,column %s' % (11,11)),
        # ])

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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()

    window.show()
    sys.exit(app.exec_())
