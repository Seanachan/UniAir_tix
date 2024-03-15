from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import sys
import os
import json
import requests
try:
    import ddddocr
except:
    print("No module named 'ddddocr")
    pass

#Opening JSON object file
f=open('settings.json')
#returns JSON object as a dict
data = json.load(f)

SYSTEM=data['SYSTEM']
BROWSER_PATH = data['BROWSER_PATH']
BROWSER=data['BROWSER']
WEB_PAGE = data["WEB_PAGE"]
print(data)
def getAuthCode(driver)->int:
    driver.find_element(By.CSS_SELECTOR,"#btn_ViewPolicy").click()
    #get authentication code's image
    imgCode = driver.find_element(By.CSS_SELECTOR,"#c_b2c_booking_ubk_search_cph_body_logincaptcha_CaptchaImage")
    
    #將驗證碼截圖, save as code.png
    imgCode.screenshot('code.png')
    driver.implicitly_wait(5)
    ocr = ddddocr.DdddOcr(beta=True)
    with open("code.png","rb") as fp:
        image = fp.read()
    
    return ocr.classification(image)

def search_seat(driver,date:str,numOfPassenger:int):
    
    dept = Select(driver.find_element(By.CSS_SELECTOR,"#ddl_DEP"))
    dept.select_by_visible_text("松山(TSA)")
    
    dest = Select(driver.find_element(By.CSS_SELECTOR,"#ddl_ARR"))
    dest.select_by_visible_text("金門(KNH)")
    
    #send value into the hidden date input element
    script_date="return document.getElementById('CPH_Body_hi_TRIP_DATE').value='{}'".format(date)
    driver.execute_script(script_date)
    
    #click passenger select
    driver.find_element(By.CSS_SELECTOR,"#CPH_Body_tb_PaxNum").click()
    #click plus passegner
    for i in range(int(numOfPassenger)-1):
        driver.find_element(By.CSS_SELECTOR,"#CPH_Body_div_PaxNum > div > div:nth-child(1) > div > div.col-6.col-lg-5 > div > div:nth-child(3) > button").click()
    
    #wait the button the be ready
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#CPH_Body_div_PaxNum > div > button")))
    
    #get authentication code
    try:
        auth_code=getAuthCode(driver)
        print("auth_code",auth_code)

        driver.find_element(By.CSS_SELECTOR,"#CPH_Body_txt_CaptchaCode").send_keys(auth_code)
    except:
        print("No need auth_code")
    time.sleep(0.8)
    #click search-btn
    search_btn=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_SelectFlight")
    time.sleep(0.8)
    search_btn.click()
def but_ticket(driver,adult_num,rsd_adult_num):
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#CPH_Body_uc_SelectFlight_rpt_Flight_btn_SelectFlight_2")))
    flight_selector = "#CPH_Body_uc_SelectFlight_rpt_Flight_btn_SelectFlight_"
    for flight_num in range(4,-1,-1):
        try:
            flight = driver.find_element(By.CSS_SELECTOR,flight_selector+str(flight_num))
            flight.click()
        except Exception as e:
            print(e)
            continue
        
        WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0")))
        
        adult=Select(driver.find_element(By.CSS_SELECTOR,"#CPH_Body_rpt_FareType_rpt_FareInfo_0_ddl_Num_0"))
        time.sleep(1)
        adult.select_by_value(str(adult_num))
        
        rsd_adult=Select(driver.find_element(By.CSS_SELECTOR,"#CPH_Body_rpt_FareType_rpt_FareInfo_1_ddl_Num_0"))
        time.sleep(1)
        rsd_adult.select_by_value(str(rsd_adult_num))
        
        confirm=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_NextStep")
        confirm.click()
        break
def confirm_schedule(driver):
    WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,"#CPH_Body_cb_CheckTrem")))
    
    checkbox=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_cb_CheckTrem")
    checkbox.click()
    
    next_step=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_NextStep")
    next_step.click()
def add_options(option):
    option.add_argument("--disable-animations")
    option.add_argument("--disable-blink-features=AutomationControlled")
    option.add_argument("--disable-infobars")
    option.add_argument("--disable-notifications")
    option.add_argument("--disable-popup-blocking")
    option.add_argument("--disable-print-preview")
    option.add_argument("--disable-setuid-sandbox")
    option.add_argument("--disable-site-isolation-trials")
    option.add_argument("--disable-smooth-scrolling")
    option.add_argument("--disable-sync")
    option.add_argument("--no-sandbox");
    option.add_argument('--disable-features=TranslateUI')
    option.add_argument('--disable-translate')
    option.add_argument('--disable-web-security')
    option.add_argument('--lang=zh-TW')

    # for navigator.webdriver
    option.add_experimental_option("excludeSwitches", ['enable-automation'])
    # Deprecated chrome option is ignored: useAutomationExtension
    #option.add_experimental_option('useAutomationExtension', False)
    option.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False, "translate":{"enabled": False}})
    option.page_load_strategy = 'eager'
    #options.page_load_strategy = 'none'
    option.unhandled_prompt_behavior = "accept"
    return option
def main():
    #Open Brave Browser
    
    date=data['date']
    numOfPassenger=numOfPassenger=data["numOfPassenger"]
    # print("data: "+str(date))
    # print("numOfPassenger: ",numOfPassenger)
    
    driver_path = "./driver"#driver is store in ./driver directory
    if BROWSER=="Brave":
        driver_path = os.path.join(driver_path,"chromedriver")
        option = webdriver.ChromeOptions()
        option=add_options(option=option)
        option.binary_location = BROWSER_PATH
        driver = webdriver.Chrome(service=Service(driver_path),options=option)
    
    elif BROWSER=='Edge':
        driver_path = os.path.join(driver_path,"msedgedriver")
        option=webdriver.EdgeOptions()
        option=add_options(option=option)
        driver=webdriver.Edge(service=Service(driver_path),options=option)
    # elif BROWSER=='Safari':
    #     driver_path = os.path.join(driver_path,"msedgedriver")
    #     option=webdriver.SafariOptions()
    #     driver=webdriver.Safari(service=Service(driver_path),options=option)
    
    else:#Chrome
        driver_path = os.path.join(driver_path,"chromedriver")
        option = webdriver.ChromeOptions()
        option=add_options(option=option)
        driver = webdriver.Chrome(service=Service(),options=option)
    
    
    
    #load to the web page
    try:
        driver.get(WEB_PAGE)
        print("Loading {}..".format(WEB_PAGE))
    except Exception as e:
        print(e)
        return
        
    # load_page = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CSS_SELECTOR, "#ddl_DEP"),"Element Not found")
    driver.set_window_size(900,1080)
    search_seat(driver=driver,date=str(date),numOfPassenger=numOfPassenger)
    but_ticket(driver=driver,adult_num=data['adult_num'],rsd_adult_num=data['rsd_adult_num'])
    
    
    confirm_schedule(driver=driver)
    while input("Press 'q' to quit ")!='q':
        time.sleep(1)
    
if __name__=='__main__':
    main()
    f.close()
