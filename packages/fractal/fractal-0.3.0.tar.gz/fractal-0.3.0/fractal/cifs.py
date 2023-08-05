"""
    Complex Iterated Function System.
    复迭代函数系统
"""

import pygame
from .base import Base
from .colors import *
from threading import Thread

class CIFS(Base):

    def __init__(self, size, title=""):
        Base.__init__(self, size, self.__run, title)
        self.setRadius(10)
        self.width = size[0]
        self.height = size[1]
        self.setRange(10, 10)
        self.setCentre(0 + 0j)
        self.ifunc = None

    def setFunction(self, ifunc):
        # 设置迭代函数
        self.ifunc = ifunc

    def setRadius(self, R):
        # 设置逃逸半径
        self.R = R

    def color(self, n, r=2):
        if n < len(reds):
            return reds[n]
        else:
            if r < self.R:
                return blues[int((len(blues) - 1) * r / self.R)]
            else:
                return purples[int((len(purples) - 1) * self.R / r)]

    def setColor(self, call):
        self.color = call

    def setCentre(self, z0):
        # 设置中心点
        self.z0 = z0

    def setRange(self, xmax, ymax):
        # 设置坐标范围，范围越小图放大倍数越高
        self.xmax = xmax
        self.ymax = ymax

    def __getXY(self, i, j):
        # 通过像素坐标获取映射后的坐标
        return complex((i / self.width - 0.5) * self.xmax + self.z0.real, (j / self.height - 0.5) * self.ymax + self.z0.imag)

    def scala(self, i, j, rate):
        # 将(i, j)像素点置于中心位置，放大rete倍
        self.setCentre(self.__getXY(i, j))
        self.xmax /= rate
        self.ymax /= rate

    def __calc(self, start, w, h):
        # 绘制以start为起点，宽w,高h的子区域
        for i in range(w):
            for j in range(h):
                ct = 0
                z = self.__getXY(start[0] + i, start[1] + j)
                for k in range(self.N):
                    ct = k
                    if abs(z) > self.R:  # 大于逃逸半径，则返回
                        break
                    z = self.ifunc(z)
                self.screen.set_at(
                    [start[0] + i, start[1] + j], self.color(ct, abs(z)))

    def __run(self):
        print("x range ：[-%.2e,%.2e]\ny range ：[-%.2e,%.2e]" % (
            self.xmax, self.xmax, self.ymax, self.ymax))
        tn = 5  # 25 个子线程绘图
        ci = self.width // tn
        cj = self.height // tn
        ts = []
        for i in range(tn):
            for j in range(tn):
                t = Thread(target=self.__calc, args=(
                    [i * ci, j * cj], self.width // tn, self.height // tn))
                t.start()
                ts.append(t)
        for t in ts:
            t.join()
        del ts

    def doCifs(self, N):
        # 进入迭代
        # N: 单点最大迭代次数
        self.N = N
