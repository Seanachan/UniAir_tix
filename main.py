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
    
    #click search-btn
    driver.find_element(By.CSS_SELECTOR,"#CPH_Body_btn_SelectFlight").click()
def main():
    #Open Brave Browser
    brave_path = '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'
    web_page = "https://www.uniair.com.tw/rwd/B2C/booking/ubk_search.aspx"
    
    date=sys.argv[1]
    numOfPassenger=sys.argv[2]
    print("data: "+str(date))
    print("numOfPassenger: "+numOfPassenger)
    driver_path = "/Users/seanachan/code/chromedriver"
    
    try:
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path
        driver = webdriver.Chrome(service=Service(driver_path),options=option)
        driver.get(web_page)
        print("Loading {}..".format(web_page))
    except Exception as e:
        print(e)
    
    # load_page = WebDriverWait(driver,10).until(EC.presence_of_element_located(By.CSS_SELECTOR, "#ddl_DEP"),"Element Not found")
    driver.maximize_window()
    search_seat(driver=driver,date=str(date),numOfPassenger=numOfPassenger)
    
    while input("Press 'q' to quit ")!='q':
        time.sleep(1)
    
if __name__=='__main__':
    main()
