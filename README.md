# BusFinder
A project that uses Selenium webdriver to get the data about the bus you need to take in order to get to work and return.

## How does it work?
The program takes information about your working hours and how much time earlier should the bus at the location.

```python
# HOW MANY MINUTES EARLIER SHOULD YOU BE AT WORK
SAFETY_MARGIN = 7
# HOW MANY MINUTES DOES IT TAKE TO TRAVEL
TRAVEL_TIME = 40
FIRST_STOP = 'torfowa'
LAST_STOP = 'czarnowiejska'

account_sid = ''
auth_token = ''

working_hours = [("11:15", "12:45"), ("11:30", "16:30"), ("8:00", "11:15"), ("16:45", "20:30"), ("16:45", "20:30")]

```

Then it opens the site https://jakdojade.pl/krakow/trasa/ and uses it to get informations about the proper bus. Finaly the program uses the twillio API to send the SMS with the data.
