# -*-coding:utf-8 -*-
import ctypes
import sys
import os

#返回值结构体类
class SO():

    def __init__(self, so_path = '../so_file/test.so'):
        self.so_path = so_path

    # 构建一个结构体
    class STU(ctypes.Structure):
        _fields_ = [('a', ctypes.c_int),
                    ('path', ctypes.c_char_p)]


    def run(self):
        #读取so文件
        dll = ctypes.cdll.LoadLibrary(self.so_path)

        # 创建一个结构体测试传送结构体参数
        test = ctypes.pointer(self.STU())
        test.a = ctypes.c_int(2)
        print('test.a:' + str(test.a))
        test.path = bytes("hello", "utf8")
        dll.cshow(test)
        print(test.a)


        # 结构返回结构体参数
        dll.cre_test.restype = ctypes.POINTER(self.STU)
        self.result = dll.cre_test()
        re = str(self.result.contents.path)
        print(re)

if __name__ == "__main__":
    t = SO()
    t.run()
