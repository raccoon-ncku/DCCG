import datetime

# Get the current date and time
now = datetime.datetime.now()
print(now)

# Get the current date
today = datetime.date.today()
print(today)

# format the datetime
print(now.strftime("%Y/%m/%d %H:%M:%S"))