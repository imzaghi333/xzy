# -*- coding: UTF-8 -*-
# Required modules: qrcode, pandas

import os,time
from datetime import datetime
import qrcode
import pandas as pd

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

root = Tk()
root.geometry("650x400+400+300")
root.title("WGT QRCode")

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
current_day = str(datetime.now().year)+"-"+str(datetime.now().month)+"-"+str(datetime.now().day)
save_path = desktop+"/"+current_day

# 制作二维码方法
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

# 生成一个二维码图片
def make_one_qrcode():
    txt = entry1.get()

    # Mac桌面创建一个当天日期命名的目录保存图片
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    img_path = save_path+"/"+txt+".jpg"
    makeQRCode(txt,img_path)
    messagebox.showinfo(title="@", message="Done!~~~")

# 读取Excel批量生成二维码图片
def make_mass_qrcode():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("All Files", "*.*")])
    
    # Mac桌面创建一个当天日期命名的目录保存图片
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    start = time.time()
    df = pd.read_excel(file_path,sheet_name=0)
    df = df.iloc[:,[0,1]]
    content = df.values 
    length = len(content)
    for record in content:
        #print("{}=======>{}".format(record[0],record[1]))
        img_path = save_path+"/"+str(record[0])+".jpg"
        qr_text = record[1]
        makeQRCode(qr_text,img_path)
    end = time.time()
    dtime = end-start
    messagebox.showinfo(title="@", message="{}个用时{:.2f}秒".format(length,dtime))

# ------- Title ------
label0 = Label(root,text="Making QR Code",font=("Helvetica",18),fg="#04a06d")
label0.grid(row=0,column=0,columnspan=3)
blank0 = Label(root,text="",font=("Helvetica",16),fg="#ffffff")
blank0.grid(row=1,column=0)

# ------- Make one qrcode -------
label1 = Label(root,text="输入你的二维码内容: ",font=("Helvetica",16),fg="#23466c")
label1.grid(row=2,column=0)

entry1 = Entry(root,font=("Helvetica",16),fg="#23466c",width=30)
entry1.grid(row=2,column=1)

btn1 = Button(root,text="Start",fg='#e94b1b',font=("Helvetica",16),command=make_one_qrcode)
btn1.grid(row=2,column=2)
# ------- End -------

blank1 = Label(root,text="",font=("Helvetica",16),fg="#ffffff")
blank1.grid(row=3,column=0)

# ------- Make mass qrcode -------
label2 = Label(root,text="读取Excel批量生成: ",font=("Helvetica",16),fg="#23466c")
label2.grid(row=4,column=0)
btn2 = Button(root,text="Pick an Excel...",fg='#e94b1b',font=("Helvetica",16),width=20,command=make_mass_qrcode)
btn2.grid(row=4,column=1)

cc = Label(root,text="★ Excel必须有两列,第一列为二维码图片名，第二列为二维码内容;第一行为标题行",font=("Helvetica",14),fg="#cc2229")
cc.grid(row=5,column=0,columnspan=3)
# ------- End -------

# ---- Description ----
blank2 = Label(root,text="",font=("Helvetica",16),fg="#ffffff")
blank2.grid(row=6,column=0)
description = Text(root, width=65, height=5, undo=True, autoseparators=False,font=("Helvetica",14),fg="#00698f")
description.grid(row=7,column=0,columnspan=3)
description.insert(INSERT,"Readme\n\n1. 可以生成单个QR Code\n2. 仅支持Excel批量生成\n3. Excel第一行为标题行;必须有两列,第一列为二维码图片名，第二列为二维码内容")
# ------- End -------

root.mainloop()