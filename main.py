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


def find_bus():
    arrival_times = driver.find_elements(By.CSS_SELECTOR, '.cn-time-container')
    arrival_times = [i.text for i in arrival_times]
    print(arrival_times)


def input_hour(time_object):
    time.sleep(0.25)
    hour_input = driver.find_element(By.XPATH,
                                     '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[2]/div[1]/div['
                                     '2]/timepicker/div/table/tbody/tr/td[2]/input')
    hour_input.click()
    hour_input.send_keys(time_object.hour)

    minutes_input = driver.find_element(By.XPATH,
                                        '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[2]/div[1]/div['
                                        '2]/timepicker/div/table/tbody/tr/td[4]/input')

    minutes_input.send_keys(time_object.minute)
    button = driver.find_element(By.XPATH, '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[2]/div['
                                           '2]/button[2]/div[2]')
    button.click()
    time.sleep(2)
    find_bus()


def input_location():
    starting_input = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                         '1]/div[2]/form/strong/input')
    starting_input.send_keys('torfowa')
    starting_input.send_keys(Keys.ENTER)
    endpoint_input = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                         '2]/div[2]/form/strong/input')
    endpoint_input.send_keys('czarnowiejska')
    endpoint_input.send_keys(Keys.ENTER)
    time.sleep(1)


# HOW MANY MINUTES EARLIER SHOULD YOU BE AT WORK
SAFETY_MARGIN = 10
# HOW MANY MINUTES DOES IT TAKE TO TRAVEL
TRAVEL_TIME = 40

working_hours = [("11:15", "12:45"), ("11:30", "16:30"), ("8:00", "11:15"), ("16:45", "20:30")]

today = dt.datetime.today().weekday()
today_hours = []

for x in working_hours[today]:
    hour = dt.datetime.strptime(x, '%H:%M')
    today_hours.append(hour)

today_hours[0] -= dt.timedelta(minutes=TRAVEL_TIME)

service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://jakdojade.pl/krakow/trasa/")

cookies()
input_location()
input_hour(today_hours[0])

# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/span[1]
# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/span[1]
# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/div[1]/div[2]/span
