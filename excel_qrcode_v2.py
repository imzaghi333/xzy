# -*- coding: UTF-8 -*-
# Felix_Qian@Wistron.com
# required modules: qrcode, pandas; python3
# Install: pip install module_name; Linux/Mac use pip3
# Excel至少有两列; col1是QRCode名字, col2是QRCode内容
# 运行方法: python excel_qrcode_v2.py /path/filename.xlsx /path/QRcode_folder; 命令行第一个参数是Excel文件名, 第二个参数是存放QRCode图片的目录; Linux/Mac要用python3
# 只需要把文件和目录拖入command窗口即可,无需把文件名和目录手动输入;拖入后按Enter即可生成QRcode图片到对应目录;

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
    #dest_path = sys.argv[2]+"\\"           #生成的二维码路径
    if os.name == "nt":                
        dest_path = sys.argv[2]+"\\"   # Windows路径
    elif os.name == "posix":
        dest_path = sys.argv[2]+"/"    # ubuntu
    else:                              
        dest_path = sys.argv[2]+"/"    # Mac 路径
    
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