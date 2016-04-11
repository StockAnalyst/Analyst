import fund
import time
todaydate = time.strftime('%Y%m%d')
import datetime
now_time = datetime.datetime.now()
yes_time = now_time + datetime.timedelta(days=-1)
yes_time_nyr = yes_time.strftime('%Y%m%d')
def upfundall():
	fund.fund()
	fund.fundnav(yes_time_nyr)
	fund.funddivm(yes_time_nyr)
	fund.fundassets()
	fund.fundholdings()
