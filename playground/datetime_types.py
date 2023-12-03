import datetime

current_date = datetime.date.today()
current_time = datetime.datetime.now().time()
current_datetime = datetime.datetime.now()
duration = datetime.timedelta(days=5, hours=3)

print(type(current_date))
print(type(current_time))
print(type(current_datetime))
print(type(duration))
