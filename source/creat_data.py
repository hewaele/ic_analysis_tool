import pandas as pd
import random
import numpy as np
import os

data = [ 'G130626200607191221', '2015/12/01', '2025/09/01', 'TEST00711',
         'G130626200811170014', '2015/12/01', '2025/09/01', 'TEST00274',
         'G130626200711070032', '2015/12/01', '2025/09/01', 'TEST00462',
         'G130626200910250036', '2015/12/01', '2025/09/01', 'TEST00310',
         'G130626200808180019', '2015/12/01', '2025/09/01', 'TEST00186',
         'G130626200805301217', '2015/12/01', '2025/09/01', 'TEST00122',
         'G130626200906160046', '2015/12/01', '2025/09/01', 'TEST00308',
         'G130626200807110019', '2015/12/01', '2025/09/01', 'TEST00153',
         'L130626200709060150', '2015/12/01', '2025/09/01', 'TEST00498',
         'L130626200810200066', '2015/12/01', '2025/09/01', 'TEST00240',
         'L130626200712170035', '2015/12/01', '2025/09/01', 'TEST00006',
         'G130626200708130049', '2015/12/01', '2025/09/01', 'TEST00559',
         'G130626200710181697', '2015/12/01', '2025/09/01', 'TEST00478',
         'G130626200710172635', '2015/12/01', '2025/09/01', 'TEST00018',
         'G130626200711137663', '2015/12/01', '2025/09/01', 'TEST00028',
         'G130626200706261213', '2015/12/01', '2025/09/01', 'TEST00598',
         'G130626200803010010', '2015/12/01', '2025/09/01', 'TEST00382',
         'G130626200802250012', '2015/12/01', '2025/09/01', 'TEST00082',
         'G130626200710244918', '2015/12/01', '2025/09/01', 'TEST00022',
         'G130626200712250879', '2015/12/01', '2025/09/01', 'TEST00045',
         'G130626200701305838', '2015/12/01', '2025/09/01', 'TEST00670',
         'G130626200805252865', '2015/12/01', '2025/09/01', 'TEST00118',
         'G130626200703020043', '2015/12/01', '2025/09/01', 'TEST00664',
         'G130626200709125831', '2015/12/01', '2025/09/01', 'TEST00507',
         'G130626200801010017', '2015/12/01', '2025/09/01', 'TEST00047',
         'G130626200801184906', '2015/12/01', '2025/09/01', 'TEST00059',
         'G130626200809092619', '2015/12/01', '2025/09/01', 'TEST00207',
         'G130626200709260013', '2015/12/01', '2025/09/01', 'TEST00518',
         'G130626200707051218', '2015/12/01', '2025/09/01', 'TEST00482']


def creat_pre_data(save_path = ''):
    l = len(data)
    img_name = []
    t1 = []
    t2 = []
    roi = []
    gray = []
    result = []

    for i in range(100000):
        tmp = random.randint(0, 3)
        #判断是否进行二值化，  在01则进行二值化
        if tmp == 1:
            #连续生成255个结果
            n = random.randint(0, 28)
            th1 = random.randint(0, 95)
            for j in range(135):
                img_name.append(n)
                t1.append(th1)
                t2.append(j)
                gray.append(1)
                roi.append(tmp)
                result.append(data[random.randint(0, l - 1)])
        #随机生成图片id
        else:
            img_name.append(random.randint(0,28))
            t1.append(random.randint(0,95))
            t2.append(random.randint(0, 135))
            gray.append(0)
            roi.append(tmp)
            result.append(data[random.randint(0,l-1)])

    df = pd.DataFrame({'img_name':img_name,
                       't1':t1,
                       't2':t2,
                       'gray':gray,
                       'roi':roi,
                       'result':result})
    df.to_csv(os.path.join(save_path,'creat_test_data.csv'), index=False)

def creat_real_result(save_path = ''):
    img_name = []
    roi = []
    result = []

    np_data = np.array(data)
    b = np.reshape(np_data, [int(len(np_data) / 4), 4])
    for index, low in enumerate(b):
        for j, v in enumerate(low):
            img_name.append(index)
            roi.append(j)
            result.append(v)

    df = pd.DataFrame({'img_name':img_name,
                       'roi':roi,
                       'result':result})
    df.to_csv(os.path.join(save_path, 'creat_real_data.csv'), index = False)

if __name__ == '__main__':
    # real_data = pd.read_csv('../pre_result/real_result.txt')['id'].values
    path = '../pre_result'
    creat_pre_data(path)
    creat_real_result(path)

