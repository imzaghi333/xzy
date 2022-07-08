# -*- coding:UTF-8 -*-
# 先订一个小目标, 比如先中个500万

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
    print("你的暴富机会来了~~~")
    print("先定一个小目标,比如中个500万")
    circle = input("您打算买几组彩票:) ：")
    print("\n")
    print("蓝色球\t红色球")
    for i in range(int(circle)):
        blue = blueBall()
        red = redBall()
        print("第"+str(i+1)+"组数字："+listToString(blue).rjust(5)+red.rjust(10))

if __name__ == "__main__":
    main()