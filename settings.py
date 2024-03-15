import json
from tkinter import *
import tkinter as tk
import platform
import datetime
import os
import sys
import re
# window = tk.Tk()
# window.title("settings.py")
# window.geometry('380x400')
# window.resizable(False, False)
# menu = tk.Menu(window)
# window.config(menu=menu)
# menu.add_command(label="File")
# menu.add_command(label='Browser')
# menu.add_command(label="Preference")
CONST_CHROME_DRIVER_WEBSITE = 'https://chromedriver.chromium.org/'
CONST_EDGE_DRIVER_WEBSITE = 'https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/#downloads'
def main():
    data={
        "SYSTEM":"",
        'BROWSER':"",
        'BROWSER_PATH':'',
        'WEB_PAGE':"https://www.uniair.com.tw/rwd/B2C/booking/ubk_search.aspx",
        'rsd_adult_num':'',
        'adult_num':'',
        "numOfPassenger" : 0 ,
        "date": "",
    }
    while True:
        if platform.system() == 'Darwin':
            print("Choose your browser: \n1: Brave\n2: Chrome\n3: Edge\n4: Safari")
            data['SYSTEM']="Darwin"
            opt=input()
            if opt=='1':
                data['BROWSER']="Brave"
                brave_path='/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
                data['BROWSER_PATH']=brave_path
            elif opt=='2':
                data['BROWSER']="Chrome"
            elif opt=='3':
                data['BROWSER']="Edge"
            elif opt=='4':
                data['BROWSER']="Safari"
                safari_path='/usr/bin/safaridriver'
                data['BROWSER_PATH']=safari_path
            else:
                print("Input should be between 1-4")
                continue
            break
                
        elif platform.system() == 'Windows':
            print("Choose your browser: \n1: Brave\n2: Chrome\n3: Edge")
            data['SYSTEM']="Windows"
            opt=input()
            if opt=='1':
                data['BROWSER']="Brave"
                brave_path = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                data['BROWSER_PATH']=brave_path
                if not os.path.exists(brave_path):
                    brave_path = os.path.expanduser('~') + "\\AppData\\Local\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                if not os.path.exists(brave_path):
                    brave_path = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                if not os.path.exists(brave_path):
                    brave_path = "D:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
            elif opt=='2':
                data['BROWSER']="Chrome"
                # chrome_path=""
                # data['BROWSER_PATH']=chrome_path
            elif opt=='3':
                data['BROWSER']="Edge"
                # edge_path=''
                # data['BROWSER_PATH']=edge_path
            else:
                print("Input should be between 1-3")
                continue
            break
    while True:
        print("Enter the departure date (yyyy/mm/dd) : ")
        date=input()
        date_format = "%Y/%m/%d"
        try:
            dateObject = datetime.datetime.strptime(date, date_format)
            print(dateObject)
            break
        except ValueError:
                print("Incorrect date format, plese input as yyyy/mm/dd")
    
    data['date']=date
    data['numOfPassenger']=int(input("Enter the number of total passenger: "))
    while True:
        rsd_adult_num=input("Enter the number of adult passenger (local residents): ")
        adult_num=input("Enter the number of adult passenger (not local residents): ")
        if int(rsd_adult_num)+int(adult_num)!=data['numOfPassenger']:
            print("Number of Passenger does not match, try again!")
        else:
            break
    data['adult_num']=adult_num
    data['rsd_adult_num']=rsd_adult_num
    # Serializing json
    json_object = json.dumps(data,indent=4)
    #Writing to settings.json
    with open('./settings.json','w') as f:
        f.write(json_object)
        f.close()
    
    # window.mainloop()
    while not input("Press 'q' to quit ")=='q':
        pass
    print("exit setting")
    
if __name__=='__main__':
    main()
    