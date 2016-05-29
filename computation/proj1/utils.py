import json
import random
from special.models import Company
import datetime


def unpack_json_data(datafile):
    try:
        with open(datafile) as data_file:
            myData = json.load(data_file)
        return myData
    except Exception, e:
        print str(e)


def create_company(stock_name, ticker_symbol):
    try:
        a = Company(name=stock_name, ticker_symbol=ticker_symbol)
        a.save()
    except Exception, e:
        print str(e)

#needs to be tested
#this unpacks all company information from the json files provided.
def company_info_to_dict():
    nyse = 'nyse.json'
    nasdaq = 'nasdaq.json'
    amex = 'amex.json'
    myList = [(nyse, 'NYSE'), (nasdaq, 'NASDAQ'), (amex, 'AMEX')]
    myDict = {}
    for item in myList:
        myData = unpack_json_data(item[0])
        for item in myData:
            myDict[item['Symbol']] = {'name': item['Name'], 'last_sale': item['LastSale'], 'market_cap': item['MarketCap'], 'ipo_year': item[
                'IPOyear'], 'sector': item['Sector'], 'industry': item['industry'], 'summary_quote': item['Summary Quote'], 'exchange': item[1]}

    return myDict

#takes a string formatted in yahoo finance structure, and returns it as a datetime.date type. 
def get_date(datestring):
	return datetime.datetime.strptime(myDate,"%Y,%m,%d").date()

#get companies defined by a list of ticker symbols. 
def get_companies(company_list_json):
	myArr = []
	for item in company_json_list:
		myArr.append(item['Symbol'])
	return Company.objects.get(ticker_symbol__in=myArr)


