# -*- coding:UTF-8 -*-
# 先定一个小目标，比如中个500万。运行下面的代码，你将有机会获得500万.

import random

def blueBall():
    blueList = []
    loop = 0
    while True:
        num = random.randint(1,33)
        if num not in blueList:
            blueList.append(num)
            blueList.sort()
        loop += 1
        if len(blueList) == 6:
            break
    return blueList

def redBall():
    return str(random.randint(1,16))

def listToString(aList):
    result = []
    for tmp in aList:
        result.append(str(tmp))
    return ' '.join(result)

def main():
    print("你一夜暴富的机会来了~~~")
    print("咱们先定一个小目标,比如我先中他个500万")
    circle = input("您打算买几组彩票:) ：")
    print("\n")
    print("蓝色球                            红色球")
    for i in range(int(circle)):
        blue = blueBall()
        red = redBall()
        print("第"+str(i+1)+"组数字："+listToString(blue).rjust(5)+red.rjust(10))

if __name__ == "__main__":
    main()


"""
# -*- coding: UTF-8 -*-
# python3.9.5 + WN10
# Felix Qian

import os, sys, time
import pandas as pd
import qrcode

#读取Excel并获取两列,一列作为二维码图片名，一列作为二维码内容
def readExcel(file_path):
    sheetname = int(input("读取第几张工作表(用数字表示): "))    #从左往右1,2,3,4........
    qr_name = int(input("图片名列(用数字表示): "))             #第几列
    qr_content = int(input("二维码内容列(用数字表示): "))
    df = pd.read_excel(file_path,sheet_name=(sheetname-1))   #下标从0开始
    df = df.iloc[:,[qr_name-1,qr_content-1]]                 #获取名字列，内容列的所有内容
    return df

#制作二维码
def makeQRCode(data,path):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(path)

# -------------------- main function --------------------
def main():
    source_file = sys.argv[1]              #源excel路径
    dest_path = sys.argv[2]+"\\"           #生成的二维码路径
    
    excel = readExcel(source_file)         #读取excel
    content = excel.values                 #excel文件已经过滤，只有两列
    length = len(content)
    print("--------------二维码制作开始,请稍等------------------")
    start = time.time()
    for record in content:
        print("{}=======>{}".format(record[0],record[1]))
        img_path = dest_path+record[0]+".jpg"
        qr_text = record[1]
        makeQRCode(qr_text,img_path)
    end = time.time()
    dtime = end-start
    print("\n{}张二维码制作完成,耗时{}秒".format(length,dtime))

if __name__ == "__main__":
    main()
"""

"""
import numpy as np
from PIL import Image
from matplotlib import cm as mplcm

#第一张图

r = np.tile(np.linspace(192,255, 300, dtype=np.uint8), (600,1)).T
g = np.tile(np.linspace(192,255, 600, dtype=np.uint8), (300,1))
b = np.ones((300,600), dtype=np.uint8)*224

im = np.dstack((r,g,b))
x = np.arange(600)
y = np.sin(np.linspace(0, 2*np.pi, 600))
y = np.int32((y+1)*0.9*300/2 + 0.05*300)
for i in range(0, 150, 6):
    im[y[:-i],(x+i)[:-i]] = np.array([255,0,255])
im = Image.fromarray(im, mode='RGB')
im.show()
"""

#第二张图
"""
cm1 = mplcm.get_cmap('jet')       # jet是专属定制类的ColorMap
cm2 = mplcm.get_cmap('Paired')    # Paired是分段阶梯类的ColorMap
w, h = 9, 7

i = np.repeat(np.arange(h), w).reshape(h, w)
j = np.tile(np.arange(w), (h,1))

i = i - h//2
j = j - w//2
d = np.hypot(i, j)

def draw_picture(w, h, cm1='jet', cm2='Paired'):
    cm1, cm2 = mplcm.get_cmap(cm1), mplcm.get_cmap(cm2)
    colormap1, colormap2 = np.array([cm1(k) for k in range(cm1.N)]), np.array([cm2(k) for k in range(cm2.N)])
    i, j = np.repeat(np.arange(h),w).reshape(h,w)-h//2, np.tile(np.arange(w), (h,1))-w//2
    d = np.hypot(i, j)
    e = d[(j*j/10)<i]
    d = np.int32((cm1.N-1)*(d-d.min())/(d.max()-d.min()))
    d = np.uint8(255*colormap1[d])
    e = np.int32((cm2.N-1)*(e-e.min())/(e.max()-e.min()))
    d[(j*j/10)<i] = np.uint8(255*colormap2[e])
    Image.fromarray(d).show()

draw_picture(1200, 900, cm1='jet', cm2='Paired')
"""

# 微信公众号上的原文
"""
NumPy也可以画图吗？当然！NumPy不仅可以画，还可以画得更好、画得更快！比如下面这幅画，只需要10行代码就可以画出来。若能整明白这10行代码，就意味着叩开了NumPy的大门。请打开你的Python IDLE，跟随我的脚步，一起来体验一下交互式编程的乐趣吧，看看如何用NumPy画图，以及用NumPy可以画出什么样的图画来。
图片

1. 导入模块

仅导入NumPy就可以完成绘画过程，PIL的Image模块只是用来显示或者保存绘画结果。若能邀请Matplotlib的ColorMap来帮忙的话，处理颜色就会轻松很多，色彩也会更丰富，但这并不意味着ColorMap是必需的。

import numpy as np
from PIL import Image
from matplotlib import cm as mplcm
2. 基本绘画流程
借助于Image.fromarray()函数，可以将NumPy生成的数组转为PIL对象。PIL对象的show()方法可以直接显示图像，save()方法则可以将图像保存为文件。这一系列的操作过程中，有一个非常关键的知识点：NumPy数组的类型必须是单字节无符号整型，即np.uint8或np.ubyte类型。下面的代码使用NumPy的随机子模块random生成了100行300列的二维数组，转换为宽300像素高100像素的随机灰度图并直接显示出来。
im = np.random.randint(0, 255, (300,600), dtype=np.uint8)
im = Image.fromarray(im)
im.show() # 或者im.save(r'gray_300_600.jpg')保存为文件
图片
3. 生成随机彩色图像

上面的代码中，如果random生成的数组包含3个通道，就会得到一幅彩色的随机图像。

im = np.random.randint(0, 255, (300,600,3), dtype=np.uint8)
Image.fromarray(im, mode='RGB').show()
图片
图片

4. 生成渐变色图像

np.linspace()函数类似于Python的range()函数，返回的是浮点数的等差序列，经过np.tile()重复之后，分别生成RGB通道的二维数组，再用np.dstack()合并成三维数组，最终输出一幅渐变色图像。

r = np.tile(np.linspace(192,255, 300, dtype=np.uint8), (600,1)).T
g = np.tile(np.linspace(192,255, 600, dtype=np.uint8), (300,1))
b = np.ones((300,600), dtype=np.uint8)*224
im = np.dstack((r,g,b))
Image.fromarray(im, mode='RGB').show()

图片

5. 在渐变色背景上画曲线

对图像数组中的特定行列定位之后，再修改其颜色，就可以得到期望的结果。

r = np.tile(np.linspace(192,255, 300, dtype=np.uint8), (600,1)).T
g = np.tile(np.linspace(192,255, 600, dtype=np.uint8), (300,1))
b = np.ones((300,600), dtype=np.uint8)*224
im = np.dstack((r,g,b))
x = np.arange(600)
y = np.sin(np.linspace(0, 2*np.pi, 600))
y = np.int32((y+1)*0.9*300/2 + 0.05*300)
for i in range(0, 150, 6):
  im[y[:-i],(x+i)[:-i]] = np.array([255,0,255])
  
Image.fromarray(im, mode='RGB').show()
图片
6.使用颜色映射（ColorMap）
颜色映射（ColorMap）是数据可视化必不可少的概念，枯燥无趣的数据正是经过颜色映射之后才变得五颜六色、赏心悦目的。Matplotlib的cm子模块提供了7大类共计82种颜色映射表，每种映射表名字之后附加“_r” ，可以获得该映射表的反转版本。

图片

下面是专属定制类中jet颜色映射表和分段阶梯类中Paired颜色映射表的色带图。

图片
Matplotlib的cm子模块使用起来也非常简单。下面的代码有助于理解颜色映射（ColorMap）的机制、熟悉cm对象的使用方法。

cm1 = mplcm.get_cmap('jet') # jet是专属定制类的ColorMap
cm1.N # jet有256种颜色
256
cm1(0) # 返回序号为0的颜色
(0.0, 0.0, 0.5, 1.0)
cm1(128) # 返回序号为128的颜色
(0.4901960784313725, 1.0, 0.4775458570524984, 1.0)
cm1(255) # 返回序号为255的颜色
(0.5, 0.0, 0.0, 1.0)
cm2 = mplcm.get_cmap('Paired') # Paired是分段阶梯类的ColorMap
cm2.N # Paired有12种颜色
12
cm2(0) # 返回序号为0的颜色
(0.6509803921568628, 0.807843137254902, 0.8901960784313725, 1.0)
cm2(11) # 返回序号为11的颜色
(0.6941176470588235, 0.34901960784313724, 0.1568627450980392, 1.0)
展示NumPy的魅力

对于一幅图像（假如图像有9个像素宽7个像素高），可以很容易地得到由每个像素的行号组成的二维数组（以i表示），以及由每个像素的列号组成的二维数组（以j表示）。

w, h = 9, 7
i = np.repeat(np.arange(h), w).reshape(h, w)
j = np.tile(np.arange(w), (h,1))
i
array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 1, 1, 1, 1, 1, 1, 1],
       [2, 2, 2, 2, 2, 2, 2, 2, 2],
       [3, 3, 3, 3, 3, 3, 3, 3, 3],
       [4, 4, 4, 4, 4, 4, 4, 4, 4],
       [5, 5, 5, 5, 5, 5, 5, 5, 5],
       [6, 6, 6, 6, 6, 6, 6, 6, 6]])
j
array([[0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8],
       [0, 1, 2, 3, 4, 5, 6, 7, 8]])

稍加变换，就得到各个像素在以图像中心点为原点的平面直角坐标系里的坐标。
i = i - h//2
j = j - w//2
i
array([[-3, -3, -3, -3, -3, -3, -3, -3, -3],
       [-2, -2, -2, -2, -2, -2, -2, -2, -2],
       [-1, -1, -1, -1, -1, -1, -1, -1, -1],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 1,  1,  1,  1,  1,  1,  1,  1,  1],
       [ 2,  2,  2,  2,  2,  2,  2,  2,  2],
       [ 3,  3,  3,  3,  3,  3,  3,  3,  3]])
j
array([[-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4],
       [-4, -3, -2, -1,  0,  1,  2,  3,  4]])
自然，也很容易计算出每个像素距离图像中心的距离数组（以d表示）。下面的代码使用np.hypot()函数完成距离计算，如果先求平方和再开平方，也没有问题，只是不够酷而已。
d = np.hypot(i, j)
d
array([[5.        , 4.24264069, 3.60555128, 3.16227766, 3.        ,
        3.16227766, 3.60555128, 4.24264069, 5.        ],
       [4.47213595, 3.60555128, 2.82842712, 2.23606798, 2.        ,
        2.23606798, 2.82842712, 3.60555128, 4.47213595],
       [4.12310563, 3.16227766, 2.23606798, 1.41421356, 1.        ,
        1.41421356, 2.23606798, 3.16227766, 4.12310563],
       [4.        , 3.        , 2.        , 1.        , 0.        ,
        1.        , 2.        , 3.        , 4.        ],
       [4.12310563, 3.16227766, 2.23606798, 1.41421356, 1.        ,
        1.41421356, 2.23606798, 3.16227766, 4.12310563],
       [4.47213595, 3.60555128, 2.82842712, 2.23606798, 2.        ,
        2.23606798, 2.82842712, 3.60555128, 4.47213595],
       [5.        , 4.24264069, 3.60555128, 3.16227766, 3.        ,
        3.16227766, 3.60555128, 4.24264069, 5.       ]])
设想一下，如果想将不同的距离使用jet颜色映射表映射为不同的颜色，图像是什么样子呢？如果再选取图像中的某个特定区域，比如列号的平方小于10倍行号的全部像素，将选中区域各个点的距离使用Paired颜色映射表映射为不同的颜色，图像又会变成什么样子呢？下面用10行代码实现了这一切。
def draw_picture(w, h, cm1='jet', cm2='Paired'):
    cm1, cm2 = mplcm.get_cmap(cm1), mplcm.get_cmap(cm2)
    colormap1, colormap2 = np.array([cm1(k) for k in range(cm1.N)]), np.array([cm2(k) for k in range(cm2.N)])
    i, j = np.repeat(np.arange(h),w).reshape(h,w)-h//2, np.tile(np.arange(w), (h,1))-w//2
    d = np.hypot(i, j)
    e = d[(j*j/10)<i]
    d = np.int32((cm1.N-1)*(d-d.min())/(d.max()-d.min()))
    d = np.uint8(255*colormap1[d])
    e = np.int32((cm2.N-1)*(e-e.min())/(e.max()-e.min()))
    d[(j*j/10)<i] = np.uint8(255*colormap2[e])
    Image.fromarray(d).show()
 
 
draw_picture(1200, 900, cm1='jet', cm2='Paired')


"""