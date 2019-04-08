# -*-coding:utf-8 -*-
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
from pyecharts import HeatMap
# import seaborn as sns
# import random

class Data():
    def __init__(self, pre_path = 'creat_test_data.txt', real_path = 'creat_real_data.txt', save_path = '', merge=True):
        self.pre_path = pre_path
        self.real_path = real_path
        self.save_path = save_path
        self.merge = merge
        #
        self.result = []


    def get_img_num(self):
        self.img_num_list = self.real_data['img_name'].unique()

    def get_roi_num(self):
        self.roi_num_list = self.real_data['roi'].unique()

    #将预测结果和实际结果结合
    def merge_data(self):
        if self.merge is True:
            tmp = self.pre_data.copy()
            result = pd.merge(tmp, self.real_data, on = ['img_name', 'roi'], how='left')
            self.pre_data = result
            self.pre_data['result_x'].astype(str)
            self.pre_data['result_y'].astype(str)
            self.pre_data['true'] = (self.pre_data['result_x'] == self.pre_data['result_y']).astype(int)
            self.pre_data['pre_len'] = self.pre_data['result_x'].apply(lambda s: len(str(s)))
            self.pre_data['real_len'] = self.pre_data['result_y'].apply(lambda s: len(str(s)))
            self.pre_data['miss'] = (self.pre_data['pre_len'] < self.pre_data['real_len']).astype(int)
            self.pre_data['extra'] = (self.pre_data['pre_len'] > self.pre_data['real_len']).astype(int)
            self.pre_data.to_csv(os.path.join(self.save_path, 'merge_test.csv'))
        else:
            self.pre_data = pd.read_csv(os.path.join(self.save_path, 'merge_test.csv'))
        #绘图

    #根据roi绘制图片
    def draw(self):
        self.real_data = pd.read_csv(self.real_path)
        self.pre_data = pd.read_csv(self.pre_path)

        # 获得图片的总数
        self.get_img_num()
        # 获得roi区域个数
        self.get_roi_num()
        self.merge_data()
        for r in self.roi_num_list[:]:
            self.draw_by_roi(r)

        #
    def draw_by_roi(self, roi):
        #判断是否有二值化，如果有二值化，则进行三维画图
        if self.is_gray(roi):
            data = self.pre_data[self.pre_data['roi'] == roi]
            #获取识别阈值
            t1_list = sorted(data['t1'].unique())
            #获取二值化阈值
            t2_list = sorted(data['t2'].unique())
            vis_data = []

            for t1i in t1_list[:]:
                t1_t2_total = data[data.t1 == t1i].groupby('t2')['true'].agg('count').values
                t1_t2_ac = data[data.t1 == t1i].groupby('t2')['true'].agg('sum').values

                t1_t2_er = t1_t2_total - t1_t2_ac
                ac = t1_t2_ac/t1_t2_total*100
                er = t1_t2_er/t1_t2_total*100

                t1_t2_miss = data[data.t1 == t1i].groupby('t2')['miss'].agg('sum').values
                t1_t2_extra = data[data.t1 == t1i].groupby('t2')['extra'].agg('sum').values
                vis_data.append(ac)

            # 获取最优结果
            tmp_roi = roi
            tmp_result = 0
            tmp_t1 = []
            tmp_t2 = []
            for i, low in enumerate(vis_data):
                for j, v in enumerate(low):
                    #更新最优结果
                    if v == tmp_result:
                        tmp_result = v
                        tmp_t1.append(i)
                        tmp_t2.append(j)
                    if v > tmp_result:
                        #清空当前
                        tmp_result = v
                        tmp_t1 = [i]
                        tmp_t2 = [j]

            self.result.append([tmp_roi, tmp_result, tmp_t1, tmp_t2])

            #获取热力图显示格式
            test_hot = []
            for i, l in enumerate(vis_data):
                for j, v in enumerate(l):
                    test_hot.append([j, i, v])

            heatmap = HeatMap(width=2000, height=1000, )
            # print(test_hot)

            heatmap.add(
                "gray"+':roi'+str(roi),

                t2_list,
                t1_list,
                test_hot,
                is_visualmap=True,
                visual_text_color="#000",
                visual_orient="horizontal",
                # yaxis_interval=4,
                is_label_emphasis=True,
                # is_label_show=True,
                yaxis_type = 'category',
                xaxis_type = 'category',

                is_datazoom_show=True,
                datazoom_type="slider",
                datazoom_range=[10, 25],
                # 新增额外的 dataZoom 控制条，纵向
                is_datazoom_extra_show=True,
                datazoom_extra_type="slider",
                datazoom_extra_range=[10, 25],
                is_toolbox_show=False,
            )
            heatmap.render(os.path.join(self.save_path,"roi_"+str(roi)+'_vis.html'))
            # sns.heatmap(test_hot, cmap='Reds', vmin = 0, vmax=100)
            # plt.show()

        else:
            #获取该区域的数据
            data = self.pre_data[self.pre_data['roi'] == roi]
            #获取阈值列表
            threshold_list = sorted(data['t1'].unique())
            #将该区域按阈值进行分组
            #获得各个区域的总数
            total = data.groupby(['t1'])['true'].agg('count').values

            #计算准确率
            ac = data.groupby(['t1'])['true'].agg('sum').values
            ac = ac/total*100
            #计算错误率
            er = 100 - ac
            #计算漏检
            miss = data.groupby(['t1'])['miss'].agg('sum').values
            miss = miss/total*100
            #计算多检率
            extra = data.groupby(['t1'])['extra'].agg('sum').values
            extra = extra/total*100


            #获取最优结果
            tmp_roi = roi
            tmp_result = 0
            tmp_t1 = []
            tmp_t2 = 'none'
            for index, v in enumerate(ac):
                if v == tmp_result:
                    tmp_result = v
                    tmp_t1.append(threshold_list[index])
                if v > tmp_result:
                    tmp_result = v
                    tmp_t1 = [threshold_list[index]]

            self.result.append([tmp_roi, tmp_result, tmp_t1, tmp_t2])

            #绘图
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)

            # ac error miss extra
            ax.plot(threshold_list, ac, 'go-', label = 'accuracy')
            ax.plot(threshold_list, er, 'r*-', label = 'error')
            ax.plot(threshold_list, miss, 'b+-', label = 'miss')
            ax.plot(threshold_list, extra, 'y^-', label = 'extra')
            ax.set_xlabel('threshold')
            ax.set_ylabel('score')
            ax.set_title('roi'+str(roi))
            ax.set_xticks(range(threshold_list[0],len(threshold_list)+5, 5))
            ax.set_xticklabels(threshold_list[::5], rotation=90, fontsize='small')

            ax.set_yticks(range(0, 110, 10))
            ax.set_yticklabels(range(0, 110, 10), rotation=90, fontsize='small')
            ax.grid(True)
            plt.legend(loc = 'center right', fontsize='large')
            plt.savefig(os.path.join(self.save_path, 'roi_'+str(roi)+'_vis.png'), dpi= 300)
            # plt.show()


    def is_gray(self, roi):
        tmp = self.pre_data[self.pre_data.roi == roi]
        if tmp['gray'].values[0] == 1:
            return True
        else:
            return False


if __name__ == "__main__":
    t = Data(pre_path = '../pre_result/creat_test_data.txt',
             real_path = '../pre_result/creat_real_data.txt',
             save_path = '../analysis_result/',
             merge=True)
    t.draw()