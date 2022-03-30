from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime as dt


def cookies():
    time.sleep(2)
    cookies_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/div/div[6]/button[2]')
    cookies_button.click()
    time.sleep(2)


# HOW MANY MINUTES EARLIER SHOULD YOU BE AT WORK
SAFETY_MARGIN = 10

working_hours = [("11:15", "12:45"), ("11:30", "16:30"), ("8:00", "11:15"), ("16:45", "20:30")]

today = dt.datetime.today().weekday()

# for time in working_hours[today]:
#     hour = time.split(":")
#     print(hour)

service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://jakdojade.pl/krakow/trasa/")

cookies()

starting_input = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                               '1]/div[2]/form/strong/input')

starting_input.send_keys('torfowa')
starting_input.send_keys(Keys.ENTER)
endpoint_input = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                               '2]/div[2]/form/strong/input')
endpoint_input.send_keys('czarnowiejska')
endpoint_input.send_keys(Keys.ENTER)