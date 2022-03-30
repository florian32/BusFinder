from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime as dt
from twilio.rest import Client


def cookies():
    time.sleep(2)
    cookies_button = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[2]/div/div[6]/button[2]')
    cookies_button.click()
    time.sleep(2)


def find_first_bus():
    global FIRST_BUS
    all_times = driver.find_elements(By.CSS_SELECTOR, '.cn-time-container')
    all_times = [i.text for i in all_times]
    arrival_times = []
    ending_times = []

    for i in range(0, len(all_times), 2):
        arrival_times.append(dt.datetime.strptime(all_times[i], '%H:%M'))

    for i in range(1, len(all_times), 2):
        ending_times.append(dt.datetime.strptime(all_times[i], '%H:%M'))

    counter = 0
    for ending_time in ending_times:
        if (today_hours[0] - ending_time).days == 0 and SAFETY_MARGIN <= (
                today_hours[0] - ending_time).seconds / 60 <= 20:
            break
        counter += 1
    print(f"starting time of the bus is {arrival_times[counter].hour}:{arrival_times[counter].minute}, arrival time "
          f"of the bus is {ending_times[counter].hour}:{ending_times[counter].minute}")

    FIRST_BUS = arrival_times[counter]

    find_second_bus()


def find_second_bus():
    global LAST_BUS
    driver.back()
    input_location(LAST_STOP, FIRST_STOP)
    input_hour(today_hours[1])

    all_times = driver.find_elements(By.CSS_SELECTOR, '.cn-time-container')
    all_times = [i.text for i in all_times]
    starting_times = []
    for i in range(0, len(all_times), 2):
        starting_times.append(dt.datetime.strptime(all_times[i], '%H:%M'))

    for starting_time in starting_times:
        if (starting_time - today_hours[1]).seconds / 60 >= 3.5:
            print(
                f"starting time of the bus is {starting_time.hour}:{starting_time.minute}")
            LAST_BUS = starting_time

            break


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


def input_location(first, last):
    starting_input = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                         '1]/div[2]/form/strong/input')
    starting_input.send_keys(first)
    starting_input.send_keys(Keys.ENTER)
    endpoint_input = driver.find_element(By.XPATH,
                                         '/html/body/div[2]/main/div/ui-view/div/article/div[1]/div/div[1]/div['
                                         '2]/div[2]/form/strong/input')
    endpoint_input.send_keys(last)
    endpoint_input.send_keys(Keys.ENTER)
    time.sleep(1)


# HOW MANY MINUTES EARLIER SHOULD YOU BE AT WORK
SAFETY_MARGIN = 10
# HOW MANY MINUTES DOES IT TAKE TO TRAVEL
TRAVEL_TIME = 40
FIRST_STOP = 'torfowa'
LAST_STOP = 'czarnowiejska'
FIRST_BUS = 0
LAST_BUS = 0

account_sid = 'ACf0b51290381ecfff55ad5b92c0143f96'
auth_token = 'ed6bf392d62d510276ca6a758b844ec2'

working_hours = [("11:15", "12:45"), ("11:30", "16:30"), ("8:00", "11:15"), ("16:45", "20:30")]

today = dt.datetime.today().weekday()
today_hours = []

for x in working_hours[today]:
    hour = dt.datetime.strptime(x, '%H:%M')
    today_hours.append(hour)

bus_starting_hour = today_hours[0] - dt.timedelta(minutes=TRAVEL_TIME)

service = Service("C:\Development\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://jakdojade.pl/krakow/trasa/")

cookies()
input_location(FIRST_STOP, LAST_STOP)
input_hour(bus_starting_hour)
find_first_bus()

# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]/span[1]
# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[2]/div/div[2]/div[2]/div[2]/div[2]/span[1]
# /html/body/div[2]/main/div/ui-view/div/article/div[3]/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/div[1]/div[2]/span


client = Client(account_sid, auth_token)

message = client.messages \
    .create(
    body=f"First bus leaves at {FIRST_BUS.hour}:{FIRST_BUS.minute}. The second bus leaves at {LAST_BUS.hour}:{LAST_BUS.minute}",
    from_='+18596462599',
    to='+48603041099'
)

print(message.status)
