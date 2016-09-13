import datetime as dt
import pandas as pd
import numpy as np
import sys
import os
from bokeh.plotting import *

def GetData():
	df = pd.read_csv("../data/nifty_pe_mov_avg.csv")
	print "done"
	print df
	ndf = df.loc[:,['Date','PE']]
	ndf.to_csv("../data/pe.csv")

class NiftyPE:
	def __init__(self):
		self.pe_data = pd.DataFrame()
		self.mov_avg = pd.DataFrame()
		self.curr_pe = 0
		self.p = figure(plot_width=1200, plot_height=400, x_axis_type="datetime")

	def setBokLineY(self,x,y,w=2,col="navy"):
		self.p.line(x,y,line_width=w,line_alpha=0.7,line_color=col)

	def getData(self,csv):
		self.pe_data = pd.read_csv(csv,index_col=False)
		self.pe_data['Date'] = pd.to_datetime(self.pe_data['Date'])
		self.curr_pe = self.pe_data.loc[len(self.pe_data.index)-1,'PE']
		self.pe_data.sort_values('Date',ascending=False,inplace=True)
		self.setBokLineY(self.pe_data['Date'],self.pe_data['PE'],1.5,rgbToHex(25,65,175))
#		print self.pe_data

	def movAvg(self,days,col):
		avgs = []
		nn = len(self.pe_data.index)
		pecol = self.pe_data.columns.get_loc('PE')
		print pecol
		for ii in range(0,nn):
			if ii < nn - days:
				df = self.pe_data.iloc[ii:ii+days,pecol]
				avgs.append(np.average(df))
			else:
				avgs.append(0)

		self.mov_avg[str(days)] = avgs
		self.setBokLineY(self.pe_data['Date'],\
		                 self.mov_avg.loc[0:nn-days-1,[str(days)]],\
		                 1,col)
		print self.mov_avg

	def getBokehHist(self,titl,data,bin,w,h):
		hist, edges = np.histogram(data, density=False, bins=bin)
		chist = []
		chist.append(0)
		for ii in range(1,len(hist)):
			chist.append(hist[ii]+ chist[ii-1])
		p = figure(plot_width=w, plot_height=h,title=titl, background_fill="#E8DDCB",tools="save")
		p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],\
			fill_color="#036564", line_color="#033649", alpha=0.6)
		# p.line(edges,chist,line_width=2,line_alpha=0.7,line_color="#033649")
		print edges
		print hist
		# print titl
		# print len(data),np.mean(data)
		# print hist
		return p

	def getBokehCumHist(self,titl,data,bin,w,h,curPE):
		hist, edges = np.histogram(data, density=False, bins=bin)
		chist = []
		for ii in range(1,len(hist)):
			hist[ii] = hist[ii]+hist[ii-1]
		for ii in range(len(hist)):
			chist.append(100*(float(hist[ii])/float(hist[len(hist)-1])))
		cloc = 0
		for ii in range(len(edges)):
			if curPE <= edges[ii]:
				cloc = ii
				break

		p = figure(plot_width=w, plot_height=h,title=titl, background_fill="#E8DDCB",tools="save")
		p.quad(top=chist, bottom=0, left=edges[:-1], right=edges[1:],\
			fill_color="#036564", line_color="#033649", alpha=0.6)
		p.circle(edges[cloc],chist[cloc-1],size=15, color="orange", alpha=0.8)
		# print titl
		# print len(data),np.mean(data)
		# print hist
		return p

	def setPETable(self,fdata,days,div):
		data = fdata.iloc[0:days,]
		avg = np.mean(data)
		stdev = np.std(data)
		pmin = np.min(data)
		pmax = np.max(data)
		updivs = int((pmax - avg)/(div*stdev))
		downdivs = int((avg - pmin)/(div*stdev))
		upList=[avg+j*stdev for j in range(updivs+1)]
		downList=[avg-i*stdev for i in range(downdivs,0,-1)]
		rangeList = downList+upList

		print "UPLIST",pmax,updivs,avg,stdev
		print upList
		print "DOWNLIST",pmin,downdivs,avg
		print rangeList
		hist, edges = np.histogram(data, density=False, bins=rangeList)
		print "Freqs"
		print hist
		print edges
		print data



	def bplot(self):
		output_file("niftype.html", title="Nifty P/E")
		expr = self.pe_data['PE']
		h0 = self.getBokehHist("Nifty P/E",expr,40,600,400)
		h1 = self.getBokehCumHist("Nifty P/E: Cuml Freq",expr,30,600,400,self.curr_pe)
		print self.curr_pe
		hh = hplot(h0,h1)
		f = vplot(self.p,hh)
		show(f)



def qcutEx():
	df = pd.DataFrame(
			{'A' : range(1,14),
			 'B' : range(11,24) })
	print df.loc[:,['A']]
	df['A Bucs'] = pd.qcut(df['A'],5,[1,2,3,4,5])
	print df
	return
	df['A Bucs'] = bs
	print df
	return

def rgbToHex(r,g,b):
	return '#%02x%02x%02x' % (r, g, b)
def main(args):
	# qcutEx()
	# return
	npe = NiftyPE()
	npe.getData("../data/nifty_pe.csv")

	# npe.movAvg(200,rgbToHex(100,100,250))
	# npe.movAvg(400,rgbToHex(70,250,70))
	npe.movAvg(1500,rgbToHex(30,30,250))
	npe.movAvg(750,rgbToHex(30,250,30))
	npe.movAvg(250,rgbToHex(250,30,30))
	npe.setPETable(npe.pe_data['PE'],7,0.5)
	npe.bplot()
	return


if __name__ == "__main__":
	main(sys.argv)

os._exit(0)
