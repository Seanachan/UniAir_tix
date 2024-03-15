from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import ddddocr
import time
import sys
import requests
def getAuthCode(driver)->int:
    driver.find_element(By.CSS_SELECTOR,"#btn_ViewPolicy").click()
    #get authentication code's image
    imgCode = driver.find_element(By.CSS_SELECTOR,"#c_b2c_booking_ubk_search_cph_body_logincaptcha_CaptchaImage")
    time.sleep(1)
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
    auth_code=getAuthCode(driver)
    print("auth_code",auth_code)
    
    driver.find_element(By.CSS_SELECTOR,"#CPH_Body_txt_CaptchaCode").send_keys(auth_code)
    time.sleep(0.8)
    #click search-btn
    search_btn=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_SelectFlight")
    time.sleep(0.8)
    search_btn.click()
def but_ticket(driver):
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#CPH_Body_uc_SelectFlight_rpt_Flight_btn_SelectFlight_2")))
    flight_selector = "#CPH_Body_uc_SelectFlight_rpt_Flight_btn_SelectFlight_"
    for flight_num in range(4,-1,-1):
        try:
            flight = driver.find_element(By.CSS_SELECTOR,flight_selector+str(flight_num))
            flight.click()
        except Exception as e:
            print(e)
            continue
        
        adult_num=1
        rsd_adult_num=2
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
    checkbox=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_cb_CheckTrem")
    checkbox.click()
    
    next_step=driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_NextStep")
    next_step.click()
def main():
    #Open Brave Browser
    brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    web_page = "https://www.uniair.com.tw/rwd/B2C/booking/ubk_search.aspx"
    
    date=sys.argv[1]
    numOfPassenger=sys.argv[2]
    print("data: "+str(date))
    print("numOfPassenger: "+numOfPassenger)
    driver_path = "./driver/chromedriver"
    
    try:
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path
        driver = webdriver.Chrome(service=Service(driver_path),options=option)
        driver.get(web_page)
        print("Loading {}..".format(web_page))
    except Exception as e:
        print(e)
    driver.set_window_size(900,1080)
    # load_page = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CSS_SELECTOR, "#ddl_DEP"),"Element Not found")
    # driver.maximize_window()
    search_seat(driver=driver,date=str(date),numOfPassenger=numOfPassenger)
    
    but_ticket(driver=driver)
    
    confirm_schedule(driver=driver)
    while input("Press 'q' to quit ")!='q':
        time.sleep(1)
    
if __name__=='__main__':
    main()
