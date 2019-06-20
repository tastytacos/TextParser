import datetime
import pytz


print(time)

utc_time = time.astimezone(tz=pytz.utc)
print(utc_time)