# -*-coding:utf-8 -*-
import ctypes
import os
import time
import numpy as np
os.chdir("F:/hewaele/C语言/my_dll2/")
pDll = ctypes.windll.LoadLibrary("F:/hewaele/C语言/my_dll2/Project_stand_version.dll")


#char* inputModelPath,
#  char* intputpath,
# char* intputoutputpath,
# int picnumber,
# double recogThred,
# int binchar* inputModelPath,
#  char* intputpath,
# char* intputoutputpath,
#  int picnumber,
#  double recogThred,
# int bin

#testoutput("C:\\Users\\lenovo\\Desktop\\江门Model",
    # "C:\\Users\\lenovo\\Desktop\\江门卡",
    # "C:\\Users\\lenovo\\Desktop\\江门卡\\测试",
    # 5, 0.1, 20);

# pDll.add.restype = ctypes.POINTER(r)
# path = bytes("F:/hewaele/python/mycode/ic_analysis_tool/source/img.jpg", "utf8")
# path2 = bytes("F:/hewaele/python/mycode/ic_analysis_tool/source/erweima.png", "utf8")
# pDll.add(path)
# pDll.test(path2)

p1 = bytes('F:\\hewaele\\python\\mycode\\ic_analysis_tool\\image\\JMModel', "utf8")
p2 = bytes('F:\\hewaele\\python\\mycode\\ic_analysis_tool\\image\\JM', "utf8")
p3 = bytes('F:\\hewaele\\python\\mycode\\ic_analysis_tool\\image\\result', "utf8")
p4 = ctypes.c_int(4)
p5 = ctypes.c_double(0.1)
p6 = ctypes.c_int(20)

print(time.ctime())
pDll.testoutput(p1, p2, p3, 4, p5, p6)
# pDll.show(p1)
print(time.ctime())


