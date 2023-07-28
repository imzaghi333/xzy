# -*- coding:UTF-8 -*-
# 运行方式: python3 convert_powerlog_v3.py ~/PowerLog路径, 比如python3 v3_convert_powerlog.py ~/Desktop/PowerLogs
# changes: 1. Get required time; 2. Calculte charge time from 10%~100%~stop

import sqlite3
import datetime
import sys,os, time

# PLSQL获取的数据写到 powerlog 文件
def createResultFile(root,sn, data):
    defaultFilename = sn + ".powerlog"
    with open(os.path.join(root,defaultFilename),'w') as fobj:
        fobj.write(data)

# 获取PLSQL数据
def fetchRowsFromBatteryTable(sqliteFile):
	ID_pos = 0
	timestamp_pos = 1
	level_pos = 2
	rawLevel_pos = 3
	atCriticalLevel_pos = 4
	voltage_pos = 5
	appleRawBatteryVoltage_pos = 6
	adapterVoltage_pos = 7
	instantAmperage_pos = 8
	fullAvailableCapacity_pos = 9
	currentCapacity_pos = 10
	appleRawCurrentCapacity_pos = 11
	maxCapacity_pos = 12
	appleRawMaxCapacity_pos = 13
	designCapacity_pos = 14
	cycleCount_pos = 15
	chargeStatus_pos = 16
	isCharging_pos = 17
	fullyCharged_pos = 18
	amperage_pos = 19
	temperature_pos = 20
	adapterInfo_pos = 21
	externalConnected_pos = 22
	chemID_pos = 23

	connection = sqlite3.connect(sqliteFile)

	c = connection.cursor()

	data = ""
	try: 
		for row in c.execute("SELECT * FROM PLBatteryAgent_EventBackward_Battery"):
			# Timestamp
			data += datetime.datetime.fromtimestamp(int(row[timestamp_pos])).strftime('%m/%d/%y %H:%M:%S')
			data += " "
			# Battery line tag
			data += "[Battery]"
			data += " "
			# Level
			data += "level="
			data += "%.2f" % row[level_pos]
			data += "%;"
			data += " "
			# Raw Level
			data += "raw_level="
			data += "%.2f" % row[rawLevel_pos]
			data += "%;"
			data += " "	
			# Voltage
			data += "voltage="
			data += str(row[voltage_pos])
			data += " mV;"
			data += " "	
			# Charge Current
			data += "current="
			data += str(row[instantAmperage_pos])
			data += " mA;"
			data += " "	
			# Current Capacit
			data += "current_capacity="
			data += str(row[currentCapacity_pos])
			data += " mAh;"
			data += " "
			# Raw Max Capacity
			data += "raw_max_capacity="
			data += str(row[maxCapacity_pos])
			data += " mAh;"
			data += " "
			# Is Charging
			data += "charging_state="
			data += str(row[isCharging_pos])
			data += ";"
			data += " "
			# Fully Charged
			data += "fully_charged="
			data += str(row[fullyCharged_pos])
			data += ";"
			data += " "
			# Charger Current
			data += "charger_current="
			data += str(row[amperage_pos])
			data += " mA;"
			data += " "	
			# Battery Temperature
			data += "battery_temp="
			data += str(row[temperature_pos])
			data += " C;"
			data += " "	
			# Adapter Info
			data += "adapter_info="
			data += str(row[adapterInfo_pos])
			data += ";"
			data += " "
			# Charger connected
			data += "charger_connected="
			data += str(row[externalConnected_pos])
			data += ";"
			data += " "
			# ChemID
			data += "chem_id="
			data += str(row[chemID_pos])
			data += ";"
			data += " "
			# Cycle Count
			data += "cycle_count="
			data += str(row[cycleCount_pos])
			data += ";"
			data += " "
		
			data += "\n"
	except sqlite3.DatabaseError as e:
		print(sqliteFile + " " + str(e))
	connection.close()
	return data

# 从powerlog获取放电充电时间，并计算每个10%的充电时间
def getStandardTime(contents):
    drain_start = ""       #放电开始
    drain_trap = ""        #放电结束
    charge_start = ""      #开始充电,charging_state=1
    charge_ten = ""        #充电到10%
    charge_twenty = ""
    charge_thirty = ""
    charge_fourty = ""
    charge_fifty = ""
    charge_sixty = ""
    charge_seventy = ""
    charge_eighty = ""
    charge_ninty = ""
    charge_full = ""       #充电到100%
    charge_stop = ""       #停止充电

    temp_list = contents.split("\n")
    flag_trap = 0          #放电标记位
    flag_charge = 0        #充电标记位
    
    ten_percent = ""       #充电到10%时间
    twenty_percent = ""    #充电到20%时间
    thirty_pencent = ""    #充电到30%时间
    fourty_percent = ""    #充电到40%时间
    fifty_percent = ""     #充电到50%时间
    sixty_percent = ""     #充电到60%时间
    seventy_percent = ""   #充电到70%时间
    eighty_percent = ""    #充电到80%时间
    ninty_percent = ""     #充电到90%时间
    full_time = ""         #充电到100%时间
    stop_time = ""         #充电停止
    
    for index, row in enumerate(temp_list):
        #index, row --->3006  11/05/22 13:20:14 [Battery] level=100.00%; raw_level=99.28%; voltage=4429 mV; current=-224 mA; current_capacity=100 mAh; raw_max_capacity=100 mAh; charging_state=0; fully_charged=1; charger_current=3000 mA; battery_temp=25.69 C; adapter_info=-536854518; charger_connected=1; chem_id=1012902627; cycle_count=37; 
        row_array = row.split("; ")
        #['11/05/22 13:20:13 [Battery] level=100.00%', 'raw_level=99.28%', 'voltage=4429 mV', 'current=-383 mA', 'current_capacity=100 mAh', 'raw_max_capacity=100 mAh', 'charging_state=0', 'fully_charged=1', 'charger_current=1500 mA', 'battery_temp=25.69 C', 'adapter_info=-536854523', 'charger_connected=1', 'chem_id=1012902627', 'cycle_count=37', '']
        #['11/05/22 13:20:14 [Battery] level=100.00%', 'raw_level=99.28%', 'voltage=4429 mV', 'current=-224 mA', 'current_capacity=100 mAh', 'raw_max_capacity=100 mAh', 'charging_state=0', 'fully_charged=1', 'charger_current=3000 mA', 'battery_temp=25.69 C', 'adapter_info=-536854518', 'charger_connected=1', 'chem_id=1012902627', 'cycle_count=37', '']
        if index < len(temp_list)-1:
            row_array_next = temp_list[index+1].split("; ")
            # ======== Power Drain ======
            try:
                if "[Battery] level=100.00%" in row_array[0] and "[Battery] level=99.00%" in row_array_next[0]:
                    drain_start = convertDatetime(row_array[0][0:17])
            except:
                drain_start = ""
            try:
                if "[Battery] level=1.00%" in row_array[0] and "[Battery] level=0.00%" in row_array_next[0]:
                    drain_trap = convertDatetime(row_array_next[0][0:17])
                    flag_trap = index
            except:
                drain_trap = ""
                flag_trap = index
                
            # ======== Battery Charge start ======
            if "[Battery] level=0.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            elif "[Battery] level=1.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            elif "[Battery] level=2.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            elif "[Battery] level=3.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 10% ======
            try:
                if "[Battery] level=9.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=10.00%" in row_array_next[0]:
                    charge_ten = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_ten = ""
                flag_charge = index
            # ======== Battery Charge 20% ======
            try:
                if "[Battery] level=19.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=20.00%" in row_array_next[0]:
                    charge_twenty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 30% ======
            try:
                if "[Battery] level=29.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=30.00%" in row_array_next[0]:
                    charge_thirty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 40% ======
            try:
                if "[Battery] level=39.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=40.00%" in row_array_next[0]:
                    charge_fourty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 50% ======
            try:
                if "[Battery] level=49.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=50.00%" in row_array_next[0]:
                    charge_fifty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 60% ======
            try:
                if "[Battery] level=59.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=60.00%" in row_array_next[0]:
                    charge_sixty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 70% ======
            try:
                if "[Battery] level=69.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=70.00%" in row_array_next[0]:
                    charge_seventy = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 80% ======
            try:
                if "[Battery] level=79.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=80.00%" in row_array_next[0]:
                    charge_eighty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 90% ======
            try:
                if "[Battery] level=89.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=90.00%" in row_array_next[0]:
                    charge_ninty = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge 100% ======
            try:
                if index > flag_charge and "[Battery] level=99.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=100.00%" in row_array_next[0]:
                    charge_full = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
            # ======== Battery Charge stop ======
            try:
                if index >= (flag_charge+1) and row_array[7] == "fully_charged=0" and row_array_next[7] == "fully_charged=1":
                    charge_stop = convertDatetime(row_array_next[0][0:17])
                    flag_charge = index
            except:
                charge_twenty = ""
                flag_charge = index
    
    #计算充电到10%的时间
    try:
        if charge_ten:
            ten_percent = calChargeTime(charge_start,charge_ten)
    except:
        ten_percent = ""
    #计算充电到20%的时间
    try:
        if charge_twenty:
            twenty_percent = calChargeTime(charge_start,charge_twenty)
    except:
        twenty_percent = ""
    #计算充电到30%的时间
    try:
        if charge_thirty:
            thirty_pencent = calChargeTime(charge_start,charge_thirty)
    except:
        thirty_pencent = ""
    #计算充电到40%的时间
    try:
        if charge_fourty:
            fourty_percent = calChargeTime(charge_start,charge_fourty)
    except:
        fourty_percent = ""
    #计算充电到50%的时间
    try:
        if charge_fifty:
            fifty_percent = calChargeTime(charge_start,charge_fifty)
    except:
        fifty_percent = ""
    #计算充电到60%的时间
    try:
        if charge_sixty:
            sixty_percent = calChargeTime(charge_start,charge_sixty)
    except:
        sixty_percent = ""
    #计算充电到70%的时间
    try:
        if charge_seventy:
            seventy_percent = calChargeTime(charge_start,charge_seventy)
    except:
        eighty_percent = ""
    #计算充电到80%的时间
    try:
        if charge_eighty:
            eighty_percent = calChargeTime(charge_start,charge_eighty)
    except:
        eighty_percent = ""
    #计算充电到90%的时间
    try:
        if charge_ninty:
            ninty_percent = calChargeTime(charge_start,charge_ninty)
    except:
        ninty_percent = ""
    #计算充电到100%的时间
    try:
        if charge_full:
            full_time = calChargeTime(charge_start,charge_full)
    except:
        full_time = ""
    #计算充电停止的时间
    try:
        if charge_stop:
            stop_time = calChargeTime(charge_start,charge_stop)
    except:
        stop_time =""
    
    return [drain_start,drain_trap,charge_start,charge_ten,charge_twenty,charge_thirty,charge_fourty,charge_fifty,charge_sixty,
            charge_seventy,charge_eighty,charge_ninty,charge_full,charge_stop,ten_percent,twenty_percent,thirty_pencent,
            fourty_percent,fifty_percent,sixty_percent,seventy_percent,eighty_percent,ninty_percent,full_time,stop_time]

# log的月/日/年 时:分:秒 格式,---> 年/月/日 时:分:秒 格式               
def convertDatetime(timedt):
    convert_time = timedt[6:8] + "/" + timedt[0:2] + "/" + timedt[3:5] + " " +timedt[9:17]     #年/月/日 时:分:秒 格式
    return convert_time

#计算充电时间
def calChargeTime(start,end):
    t0 = datetime.datetime.strptime(start,"%y/%m/%d %H:%M:%S")
    t1 = datetime.datetime.strptime(end,"%y/%m/%d %H:%M:%S")
    return to_hrs_mins_secs((t1-t0).seconds)

# 秒数转成x小时y分z秒形式
def to_hrs_mins_secs(seconds):
    if seconds >= 3600:
        hours = seconds//3600
        tmp = seconds%3600
        mins = tmp//60
        secs = tmp%60
        return str(hours)+"小时"+str(mins)+"分"+str(secs)+"秒"
    
    elif seconds > 60:
        mins = seconds//60
        secs = seconds%60
        return str(mins)+"分"+str(secs)+"秒"
    
    else:
        return str(seconds)+"秒"

# 放电时间,充电时间写到csv,x小时y分z秒格式
def getDrainAndChargeTime(result,sn,data):
    result += sn
    result += ","
    result += getStandardTime(data)[0]      #Start to drain
    result += ","
    result += getStandardTime(data)[1]      #Drain to trap
    result += ","
    result += getStandardTime(data)[2]      #charge start
    result += ","
    result += getStandardTime(data)[3]      #charge to 10%
    result += ","
    result += getStandardTime(data)[4]      #charge to 20%
    result += ","
    result += getStandardTime(data)[5]      #charge to 30%
    result += ","
    result += getStandardTime(data)[6]      #charge to 40%
    result += ","
    result += getStandardTime(data)[7]      #charge to 50%
    result += ","
    result += getStandardTime(data)[8]      #charge to 60%
    result += ","
    result += getStandardTime(data)[9]      #charge to 70%
    result += ","
    result += getStandardTime(data)[10]     #charge to 80%
    result += ","
    result += getStandardTime(data)[11]     #charge to 90%
    result += ","
    result += getStandardTime(data)[12]     #charge to 100%
    result += ","
    result += getStandardTime(data)[13]     #charge stop
    result += ","
    result += getStandardTime(data)[14]     #charge to 10% time
    result += ","
    result += getStandardTime(data)[15]     #charge to 20% time
    result += ","
    result += getStandardTime(data)[16]     #charge to 30% time
    result += ","
    result += getStandardTime(data)[17]     #charge to 40% time
    result += ","
    result += getStandardTime(data)[18]     #charge to 50% time
    result += ","
    result += getStandardTime(data)[19]     #charge to 60% time
    result += ","
    result += getStandardTime(data)[20]     #charge to 70% time
    result += ","
    result += getStandardTime(data)[21]     #charge to 80% time
    result += ","
    result += getStandardTime(data)[22]     #charge to 90% time
    result += ","
    result += getStandardTime(data)[23]     #charge to 100% time
    result += ","
    result += getStandardTime(data)[24]     #charge stop time
    result += "\n"
    return result

# 获取一个日期
def getFullDate():
    t = datetime.datetime.today()
    return str(t.year)+"-"+str(t.month)+"-"+str(t.day)

# 数据写到结果CSV文件中
def createTimeTableFile(inputDictory,data):
    fileName = "Charge_Time_"+getFullDate()+".csv"
    with open(os.path.join(inputDictory,fileName), "w") as fobj:
        fobj.write(data)

def main():
    inputDirectory = sys.argv[1]
    filePathList = [] #文件路径列表
    tailList = []     #文件名列表
    print("{} 为您捞出所需要的充电时间并计算".format(sys.argv[0]))
    csv_result = "Serial_NO,Start_Drain,Drain_Over,Charge_Start,Charge_TO_10%,Charge_TO_20%,Charge_TO_30%,Charge_TO_40%,Charge_TO_50%,Charge_TO_60%,Charge_TO_70%,Charge_TO_80%,Charge_TO_90%,Charge_TO_100%,Charge_Over,Charge_10%_Time,Charge_20%_Time,Charge_30%_Time,Charge_40%_Time,Charge_50%_Time,Charge_60%_Time,Charge_70%_Time,Charge_80%_Time,Charge_90%_Time,Charge_100%_Time,Charge_Stop_Time\n"
    
    start = time.time()
    for folderName,subfolders,filenames in os.walk(inputDirectory):
        for filename in filenames:
            filePath = os.path.join(folderName, filename)
            if not filename.startswith("Corrupt") and filePath.endswith(".PLSQL"):
                fileDir = os.path.dirname(filePath)
                head, tail = os.path.split(fileDir)
                if not tail in tailList:
                    tailList.append(tail)
                filePathList.append(filePath)

    for sn in tailList:
        data = ""
        for file_path in filePathList:
            fileDir = os.path.dirname(file_path)
            head, tail = os.path.split(fileDir)
            if tail == sn:
                print("Getting data from PLSQL file: {0} for {1}".format(file_path,sn))
                data += fetchRowsFromBatteryTable(file_path)
                folder_name = fileDir
        createResultFile(folder_name,sn,data)    #PLSQL转成powerlog
        #tt = getStandardTime(data)
        csv_result = getDrainAndChargeTime(csv_result,sn,data)
        
    createTimeTableFile(inputDirectory,csv_result)
    end = time.time()
    dtime = end-start
    print("\n任务完成,耗时{:.3f}秒".format(dtime))

if __name__ == "__main__":
	main()


"""

                   _ooOoo_
                  o8888888o
                  88" . "88
                  (| -_- |)
                  O\  =  /O
               ____/`---'\____
             .'  \\|     |//  `.
            /  \\|||  :  |||//  \
           /  _||||| -:- |||||-  \
           |   | \\\  -  /// |   |
           | \_|  ''\---/''  |   |
           \  .-\__  `-`  ___/-. /
         ___`. .'  /--.--\  `. . __
      ."" '<  `.___\_<|>_/___.'  >'"".
     | | :  `- \`.;`\ _ /`;.`/ - ` : | |
     \  \ `-.   \_ __\ /__ _/   .-` /  /
======`-.____`-.___\_____/___.-`____.-'======
                   `=---='
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
               佛祖请赐我一个小目标
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

"""