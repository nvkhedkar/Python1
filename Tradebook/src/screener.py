import time, urllib2

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

import re
import urllib2
import json
import time
import datetime

class Render(QWebPage):
	def __init__(self, url):
		self.app = QApplication(sys.argv)
		QWebPage.__init__(self)
		self.loadFinished.connect(self._loadFinished)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def _loadFinished(self, result):
		self.frame = self.mainFrame()
		self.app.quit()


class GoogleFinanceAPI:
	def __init__(self):
		self.interval = '300'
		self.prefix = "https://www.google.com/finance?q="
		self.prefix1 = "http://www.google.com/finance/getprices?q=NVK_STOCK_CODE&x=NVK_INDEX&i="+\
		               self.interval+"&p=.04d&f=d,o,c,v"
		self.prefix2 = "http://www.google.com/finance/getprices?q=NVK_STOCK_CODE&x=NVK_INDEX&i=300&p=.04d&f=d,o,h,l,c,v"

	def get(self, symbol, exchange):
		url = self.prefix +exchange+":"+symbol
		print url
		u = urllib2.urlopen(url)
		content = u.read()

		obj = json.loads(content)
		print obj
		return obj[0]

	def parse_content(self,content):
		carr = content.split('\n')
		unix_time = 0
		for i in range(len(carr)):
			cc = carr[i]
			if re.search('^a[\d]+,',cc):
				unix_time = int(cc[1:11])
				print datetime.datetime.fromtimestamp(unix_time
					).strftime('%Y-%m-%d %H:%M:%S')
			if re.search('^[\d]+,',cc):
				tint = re.search('^([\d]+),',cc).group(1)
				ctime = unix_time+int(tint)*int(self.interval)
				dtime = datetime.datetime.fromtimestamp(ctime
					).strftime('%Y-%m-%d %H:%M:%S')
				print dtime,cc

	def get_quote(self, symbol, exchange):
		url = re.sub('NVK_STOCK_CODE',symbol,self.prefix1)
		url = re.sub('NVK_INDEX', exchange, url)
		print url
		u = urllib2.urlopen(url)
		content = u.read()
		# print "\n==========\n"
		# print content
		# print "\n==========\n", len(content.split('\n'))
		self.parse_content(content)
		# obj = json.loads(content)
		# print obj

		return

c = GoogleFinanceAPI()

# while 1:
quote = c.get_quote("AKSHARCHEM",'NSE')
print quote
time.sleep(60)
sys.exit()

url = 'https://www.screener.in/company/TATAGLOBAL/consolidated/'
r = Render(url)
html = r.frame.toHtml()
print html
print 'New html'

def gethtml(url):
	try:
		req = urllib2.Request(url)
		return urllib2.urlopen(req).read()
	except Exception, e:
		time.sleep(2)
		return ''
# print gethtml(url)


