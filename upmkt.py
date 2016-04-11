import mkt
import time
todaydate = time.strftime('%Y%m%d')
#mkt.mktequd('20151221')
#mkt.mktequd(todaydate)

def upmktall():
	mkt.mktequd(todaydate)
	mkt.mktfutd(todaydate)
	mkt.mktidxd(todaydate)
	mkt.mktblockd(todaydate)
	mkt.mktrepod(todaydate)
	mkt.mktbondd(todaydate)
	#mkt.mkthkequd(todaydate)
	mkt.mktfundd(todaydate)
	mkt.mktoptd(todaydate)
	mkt.mktall(todaydate)

	mkt.mktindex(todaydate)
#mkt.mktequd(todaydate)
mkt.mktbondd('20160406')