# utils/date_utils.py
#from datetime import datetime
#from config import DATE_FORMAT

#def get_today_string():
    #return datetime.now().strftime(DATE_FORMAT)

# utils/date_utils.py
from datetime import datetime

def get_today():
    return datetime.now()

def get_today_string():
    return get_today().strftime("%Y-%m-%d")

def get_month_prefix():
    # 01, 02, 03 ...
    return get_today().strftime("%m")

