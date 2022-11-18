# -*- coding:UTF-8 -*-

import sqlite3
import datetime
import sys,os

def createResultFile(root,sn, data):
    defaultFilename = sn + ".powerlog"
    with open(os.path.join(root,defaultFilename),'w') as fobj:
        fobj.write(data)

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
    flag_trap = 0
    flag_charge = len(temp_list)
    
    for index, row in enumerate(temp_list):
        #index, row --->3006  11/05/22 13:20:14 [Battery] level=100.00%; raw_level=99.28%; voltage=4429 mV; current=-224 mA; current_capacity=100 mAh; raw_max_capacity=100 mAh; charging_state=0; fully_charged=1; charger_current=3000 mA; battery_temp=25.69 C; adapter_info=-536854518; charger_connected=1; chem_id=1012902627; cycle_count=37; 
        row_array = row.split("; ")
        """
        row_array
        ['11/05/22 13:20:13 [Battery] level=100.00%', 'raw_level=99.28%', 'voltage=4429 mV', 'current=-383 mA', 'current_capacity=100 mAh', 'raw_max_capacity=100 mAh', 'charging_state=0', 'fully_charged=1', 'charger_current=1500 mA', 'battery_temp=25.69 C', 'adapter_info=-536854523', 'charger_connected=1', 'chem_id=1012902627', 'cycle_count=37', '']
        ['11/05/22 13:20:14 [Battery] level=100.00%', 'raw_level=99.28%', 'voltage=4429 mV', 'current=-224 mA', 'current_capacity=100 mAh', 'raw_max_capacity=100 mAh', 'charging_state=0', 'fully_charged=1', 'charger_current=3000 mA', 'battery_temp=25.69 C', 'adapter_info=-536854518', 'charger_connected=1', 'chem_id=1012902627', 'cycle_count=37', '']
        """
        if index < len(temp_list)-1:
            row_array_next = temp_list[index+1].split("; ")
            # ======== Power Drain ======
            if "[Battery] level=100.00%" in row_array[0] and "[Battery] level=99.00%" in row_array_next[0]:
                drain_start = convertDatetime(row_array[0][0:17])
            elif "[Battery] level=1.00%" in row_array[0] and "[Battery] level=0.00%" in row_array_next[0]:
                drain_trap = convertDatetime(row_array_next[0][0:17])
                flag_trap = index
            elif "[Battery] level=2.00%" in row_array[0] and "[Battery] level=1.00%" in row_array_next[0]:
                drain_trap = convertDatetime(row_array_next[0][0:17])
                flag_trap = index
            elif "[Battery] level=3.00%" in row_array[0] and "[Battery] level=2.00%" in row_array_next[0]:
                drain_trap = convertDatetime(row_array_next[0][0:17])
                flag_trap = index
                
            # ======== Battery Charge start ======
            elif "[Battery] level=0.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            elif "[Battery] level=1.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            elif "[Battery] level=2.00%" in row_array[0] and row_array[6] == "charging_state=0" and row_array_next[6] == "charging_state=1":
                charge_start = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 10% ======
            elif "[Battery] level=9.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=10.00%" in row_array_next[0]:
                charge_ten = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 20% ======
            elif "[Battery] level=19.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=20.00%" in row_array_next[0]:
                charge_twenty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 30% ======
            elif "[Battery] level=29.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=30.00%" in row_array_next[0]:
                charge_thirty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 40% ======
            elif "[Battery] level=39.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=40.00%" in row_array_next[0]:
                charge_fourty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 50% ======
            elif "[Battery] level=49.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=50.00%" in row_array_next[0]:
                charge_fifty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 60% ======
            elif "[Battery] level=59.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=60.00%" in row_array_next[0]:
                charge_sixty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 70% ======
            elif "[Battery] level=69.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=70.00%" in row_array_next[0]:
                charge_seventy = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 80% ======
            elif "[Battery] level=79.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=80.00%" in row_array_next[0]:
                charge_eighty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 90% ======
            elif "[Battery] level=89.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=90.00%" in row_array_next[0]:
                charge_ninty = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge 100% ======
            elif index > flag_charge and "[Battery] level=99.00%" in row_array[0] and row_array[6] == "charging_state=1" and "[Battery] level=100.00%" in row_array_next[0]:
                charge_full = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            # ======== Battery Charge stop ======
            elif index >= (flag_charge+1) and row_array[7] == "fully_charged=0" and row_array_next[7] == "fully_charged=1":
                charge_stop = convertDatetime(row_array_next[0][0:17])
                flag_charge = index
            
    return [drain_start,drain_trap,charge_start,charge_ten,charge_twenty,charge_thirty,charge_fourty,charge_fifty,charge_sixty,
            charge_seventy,charge_eighty,charge_ninty,charge_full,charge_stop]
                
def convertDatetime(timedt):
    convert_time = timedt[6:8] + "/" + timedt[0:2] + "/" + timedt[3:5] + " " +timedt[9:17]     #年/月/日 时:分:秒 格式
    return convert_time

def getDrainAndChargeTime(result,sn,data):
    result += sn
    result += ","
    result += getStandardTime(data)[0]
    result += ","
    result += getStandardTime(data)[1]
    result += ","
    result += getStandardTime(data)[2]
    result += ","
    result += getStandardTime(data)[3]
    result += ","
    result += getStandardTime(data)[4]
    result += ","
    result += getStandardTime(data)[5]
    result += ","
    result += getStandardTime(data)[6]
    result += ","
    result += getStandardTime(data)[7]
    result += ","
    result += getStandardTime(data)[8]
    result += ","
    result += getStandardTime(data)[9]
    result += ","
    result += getStandardTime(data)[10]     #charge to 80%
    result += ","
    result += getStandardTime(data)[11]     #charge to 90%
    result += ","
    result += getStandardTime(data)[12]     #charge to 100%
    result += ","
    result += getStandardTime(data)[13]     #charge stop
    result += "\n"
    return result

def createTimeTableFile(inputDictory,data):
    fileName = "Charge_Time.csv"
    with open(os.path.join(inputDictory,fileName), "w") as fobj:
        fobj.write(data)

# ====================================================
def main():
    inputDirectory = sys.argv[1]
    filePathList = [] #文件名列表
    tailList = []     #文件路径列表
    csv_result = "Serial_NO,Start_Drain,Drain_Over,Charge_Start,Charge_TO_10%,Charge_TO_20%,Charge_TO_30%,Charge_TO_40%,Charge_TO_50%,Charge_TO_60%,Charge_TO_70%,Charge_TO_80%,Charge_TO_90%,Charge_TO_100%,Charge_Over\n"

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
        #print(tt)
        #print(len(tt))
        csv_result = getDrainAndChargeTime(csv_result,sn,data)
        
    createTimeTableFile(inputDirectory,csv_result)
    ss = """
    ____________________________
    欢迎来到牛厂当牛做马 嘿嘿嘿
    ----------------------------
         \   ^__^
          \  (oo)\ |_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
    """
    print(ss)

if __name__ == "__main__":
	main()

"""
 * Felix Qian 嘿嘿嘿
 *  .--,       .--,
 * ( (  \.---./  ) )
 *  '.__/o   o\__.'
 *     {=  ^  =}
 *      >  -  <
 *     /       \
 *    //       \\
 *   //|   .   |\\
 *   "'\       /'"_.-~^`'-.
 *      \  _  /--'         `
 *    ___)( )(___
 *   (((__) (__)))    
 * 高山仰止,景行行止.虽不能至,心向往之。
"""