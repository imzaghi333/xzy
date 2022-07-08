# -*- coding: UTF-8 -*-
# python3.9.5 + WN10 64bit
# Felix Qian

# 读取HHQT Device list, 补齐超链接
#Employee site: \\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\員工QR-CODE\+英文名+".jpg"

#Deivices:
#設備QR-CODE: \\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\設備QR-CODE\All\+AssetID(設備識別碼QR-CODE的編號)+".jpg"
#設備照片鏈接: \\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\設備照片\p_+AssetID(設備識別碼QR-CODE的編號)+".jpg"

# 运行方式 python linkToExcel.py excel_file_path/filename /folder_name_to_save_excel

import os,sys,time
import pandas as pd
import numpy as np

def main():
    #超链接路径
    emplpyee_link = r"\\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\員工QR-CODE"+"\\"
    device_qr_code_link = r"\\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\設備QR-CODE\All"+"\\"
    device_pic_link = r"\\10.66.45.34\Handheld\WKS\測試設備及物料\物料管理系統\設備照片"+"\\"

    excel_path = sys.argv[1]        # Excel文件路径
    dest_path = sys.argv[2]+"\\"

    print("====================开始了==============================")
    start = time.time()
    employee_df = pd.read_excel(excel_path, sheet_name="員工QR-CODE")    #員工QR-CODE DataFramme
    device_df = pd.read_excel(excel_path, sheet_name="設備清單all")      #所有设备的DataFrame

    #員工QR-CODE超链接从这里开始
    employee_eng_name = employee_df.iloc[:,5].values    #获取所有人的英文名列表(ndarray)
    emplpyee_link_list = []
    for item in employee_eng_name:
        link = emplpyee_link+item+".jpg"
        emplpyee_link_list.append('=HYPERLINK("{}","{}")'.format(link,link))
    employee_link_df = pd.DataFrame(emplpyee_link_list)
    employee_df["鏈接"] = employee_link_df
    #員工QR-CODE超链接结束

    #設備开始
    column_list = device_df.columns.values    #获取列名表
    device_name = device_df.iloc[:,3].values    #获取所有设备名字, 设备照片名维"p_"+device_name+".jpg"
    device_name_link_list = []    #设备名超链接
    device_pic_link_list = []     #设备照片超链接
    for name in device_name:
        link1 = device_qr_code_link+name+".jpg"
        device_name_link_list.append('=HYPERLINK("{}","{}")'.format(link1,link1))
    for p_name in device_name:
        link2 = device_pic_link+"P_"+p_name+".jpg"
        device_pic_link_list.append('=HYPERLINK("{}","{}")'.format(link2,link2))
    device_name_link_df = pd.DataFrame(device_name_link_list)
    device_pic_link_df = pd.DataFrame(device_pic_link_list)

    device_df["設備QR-CODE"] = device_name_link_df
    device_df["設備照片鏈接"] = device_pic_link_df
    ##設備结束

    with pd.ExcelWriter(dest_path+"HHQT_Device_list_HDC.xlsx") as writer:
        device_df.to_excel(writer, sheet_name="設備清單all",index=None)
        employee_df.to_excel(writer,sheet_name="員工QR-CODE",index=None)

    end = time.time()
    dtime = end-start
    print("任务完成，耗时%.2f秒" %dtime)
    
if __name__ == "__main__":
    main()