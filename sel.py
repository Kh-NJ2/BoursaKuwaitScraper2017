from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


userEmail = input("Enter Email: ")
userPassword = input("Enter Password: ")

options = Options()
options.add_experimental_option("detach", True)

options.add_argument("--disable-blink-features=AutomationControlled") 

options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
options.add_experimental_option("useAutomationExtension", False) 

driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
 
driver.get("https://data.boursakuwait.com.kw/history/SecEndOfDayData.aspx")

email = driver.find_element(By.ID, "MainContent_txtLoginEmail")
password = driver.find_element(By.ID, 'MainContent_txtLoginPassword')
loginBtn = driver.find_element(By.ID, 'MainContent_btnLogon')

email.send_keys(userEmail)
password.send_keys(userPassword)
loginBtn.click()

securityDataBtn = driver.find_element(By.LINK_TEXT, 'Security Data')
securityDataBtn.click()

Data = []
daysList = []
keyList = ["Bank", "Date",	"Security",	"Open",	"Close", "High", "Low",	"Volume", "Total Trades", "Value", "52 Week High", "52 Week Low", "Special Trades Volume", "Special Trades Trade", "Special Trades Value"]
finish_row = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '']

days = 0
while days < 1:
    for month in range(1, 13):
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12 :
            for i in range(1, 32):
                daysList.append(str(i) + "/" + str(month) + "/2017")
                days+= 1

        elif month == 4 or month == 6 or month == 9 or month == 11:
            for i in range(1, 31):
                daysList.append(str(i) + "/" + str(month) + "/2017")
                days+= 1
                
        elif month == 2:
            for i in range(1, 29):
                daysList.append(str(i) + "/" + str(month) + "/2017")
                days+= 1
     
s = 5
for i in range(0, 52):
    daysList.pop(s)
    daysList.pop(s)
    s+= 5

for i in range(1, 152):
    for j in range(0, 262):
        securityOptions = Select(driver.find_element(By.ID, 'MainContent_SectList'))
        dateField = driver.find_element(By.ID, "MainContent_txtFrom")
        dateField.clear()

        securityOptions.select_by_index(i)
        dateField.send_keys(daysList[j])

        showBtn = driver.find_element(By.ID, 'MainContent_showDataBtn')
        showBtn.click()

        values = driver.find_elements(By.XPATH ,'//table[@id="MainContent_BKDataGV"]//tr[1]//td')
        valuesList = ["{}".format(i)]
        for value in values:
            valuesList.append(value.text)

        Data.append(dict(zip(keyList, valuesList)))
    Data.append(dict(zip(keyList, finish_row)))

df = pd.DataFrame(Data)
df.to_csv("boursaKuwait_2017.csv")