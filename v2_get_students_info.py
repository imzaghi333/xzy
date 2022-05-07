# -*- coding:UTF-8 -*-
# filename:v2_get_students_info.py
# 支持 Windows，Linux, Mac OS; 推荐使用python3.9.x 
# contact me by weichat or imzaghi333@163.com

import os, sys
import pandas as pd
import time

#读取Excel并获取需要的内容
def getData(file_path,num):
    df = pd.read_excel(file_path,sheet_name=(num-1))    #0表示第一张工作表,依次类推
    data = df[["学生姓名","性别","成员1姓名","成员关系1","成员1电话","成员2姓名","成员关系2","成员2电话"]]
    return data.values    #.values返回的生ndarray，类似列表但不是列表

#生新文件需要的DataFrame
def createDataFrame(data):
    length = len(data)
    #标题部分先写好
    record = [["附件2："],["2021年秋季黄冈市中小学（幼儿园）家长（教师）网上培训学习 ——参训家长相关信息汇总表"],
        ["  罗田  县（市、区）                           学校（全称）      学校联系人：                手机号：                  "],
        ["序号","学生姓名","性别","家长姓名","性别","家长单位","职务","手机号码","备注"]]

    for i in range(length):
        # 去掉单元格内容的换行、空格等字符后，再加入到两个作为中间桥梁的列表分别用于记录父母信息，这样就把一行分成了两行
        t1 = str(i+1)+","+str(data[i][0]).strip()+","+str(data[i][1]).strip()+","+str(data[i][2]).strip()+","+"男"+","+","+","+str(data[i][4])[0:11]+","
        t2 = ","+","+","+str(data[i][5]).strip()+","+"女"+","+","+","+str(data[i][7])[0:11]+","
        tmp1 = t1.split(",")    #父亲信息列表
        tmp2 = t2.split(",")    #母亲信息列表
        #[[][]......[]] 父母信息以这种形式保持了
        record.append(tmp1)
        record.append(tmp2)
        print(record)
    return pd.DataFrame(record)    #生成DataFrame

def main():
    excel_path = sys.argv[1]           # Excel文件路径
    if os.name == "nt":                
        dest_path = sys.argv[2]+"\\"   # 生成文件在Windows路径
    else:                              
        dest_path = sys.argv[2]+"/"    # 生成文件在Mac,Linux路径
    
    sheet = int(input("Excel第几张工作表(1,2,3...)："))
    name = input("生成的Excel起个文件名：")
    file_name = name+".xlsx"
    
    print("----------- 任务开始了 -----------")
    start = time.time() 
    data = getData(excel_path,sheet)         # 读取Excel,获取需要的列
    df = createDataFrame(data)               # 生成DataFrame         
    
    #DataFrame写到Excel保存到sys.argv[2]的路径
    with pd.ExcelWriter(os.path.join(dest_path,file_name)) as writer:
        df.to_excel(writer, sheet_name="参训家长",index=None,header=None)

    end = time.time()
    dtime = end-start
    print("任务完成，耗时%.2f秒" %dtime)

if __name__ == "__main__":
    main()