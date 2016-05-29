import json
import random
from special.models import Company

def unpack_json_data(datafile):
	try:
		with open(datafile) as data_file:
			myData=json.load(data_file)
		return myData
	except Exception, e:
		print str(e)


def create_company(stock_name,ticker_symbol):
	try:
		a = Company(name=stock_name,ticker_symbol=ticker_symbol)
		a.save()
	except Exception, e:
		print str(e)



	
