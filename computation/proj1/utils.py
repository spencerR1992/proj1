import json
import random
from special.models import Company
import datetime
from yahoo_finance import Share

#gets data structured as a json file and unpacks it
def unpack_json_data(datafile):
    try:
        with open(datafile) as data_file:
            myData = json.load(data_file)
        return myData
    except Exception, e:
        print str(e)



#needs to be tested
#this unpacks all company information from the json files provided.
# def company_info_to_dict():
#     nyse = 'nyse.json'
#     nasdaq = 'nasdaq.json'
#     amex = 'amex.json'
#     myList = [(nyse, 'NYSE'), (nasdaq, 'NASDAQ'), (amex, 'AMEX')]
#     myDict = {}
#     for item in myList:
#         myData = unpack_json_data(item[0])
#         for item in myData:
#             myDict[item['Symbol']] = {'name': item['Name'], 'last_sale': item['LastSale'], 'market_cap': item['MarketCap'], 'ipo_year': item[
#                 'IPOyear'], 'sector': item['Sector'], 'industry': item['industry'], 'summary_quote': item['Summary Quote'], 'exchange': item[1]}

#     return myDict


#helper function for getting set up to test methods
#takes a company symbol, and a number of days back as an integer. 
#returns a transformed array (hopefully!)
def quick_get(symbol, days_back):
	today = datetime.date.today()
	start = today -datetime.timedelta(days = days_back)
	myC = Company.objects.get(ticker_symbol=symbol)
	data = get_company_data(myC, start, today)
	return transform_data(data)


#takes a string formatted in yahoo finance structure, and returns it as a datetime.date type. 
def get_date(datestring):
	return datetime.datetime.strptime(datestring,"%Y-%m-%d").date()

#takes a datetime.date, and returns a string formatted for yahoo finance
def date_to_string(date):
	return "%s-%s-%s" % (date.year, date.month, date.day)

#get companies defined by a list of company data, where the company's smybol is in each company dict under the key 'Symbol'. 
#returns as a query set of companies. 
def get_companies(company_list_json):
	myArr = []
	for item in company_list_json:
		myArr.append(item['Symbol'])
	return Company.objects.filter(ticker_symbol__in=myArr)

#takes as input a company object, start date and end_date (as datetime.date)
#returns an array of daily stock information. 
def get_company_data(company, start_date, end_date):
	start_date = date_to_string(start_date)
	end_date = date_to_string(end_date)
	share = Share(company.ticker_symbol)
	return share.get_historical(start_date, end_date)

#takes standad output of yahoo finance data points in an array, and transforms the data dicts
#it adds additional data fields to the dictionaries
def transform_data(data_array):
	for day in data_array:
		day['close'] = float(day['Close'])
		day['open'] = float(day['Open'])
		day['high'] = float(day['High'])
		day['low'] = float(day['Low'])
		day['change'] = day['close'] - day['open']
		day['price_range'] = day['high'] - day['low']
		day['proportion_change'] = day['change']/day['open']
		day['date'] = get_date(day['Date'])
		del day['Close'], day['Open'], day['High'], day['Low'], day['Date']
	return data_array


# a = Daily_Change(change = change, company = comp, volume = int(day['Volume'], price_range=price_range, date=date)




