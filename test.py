import datetime
import pytz

for i in range(5):
    try:

        print i
        if i == 3:
            raise Exception
            pass
    except Exception:
        print "exception"
        continue
