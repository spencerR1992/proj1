import json
import random
from special.models import Company, Industry, Sector
import datetime
from yahoo_finance import Share
import time
import numpy as np
import pandas as pd



def getRandComp():
    myI = Industry.objects.order_by('?').first()
    myCs = Company.objects.filter(industry = myI)
    return myCs

# gets data structured as a json file and unpacks it


def unpackJsonData(datafile):
    try:
        with open(datafile) as data_file:
            myData = json.load(data_file)
        return myData
    except Exception, e:
        print str(e)

# helper function for getting set up to test methods
# takes a company symbol, and a number of days back as an integer.
# returns a transformed array (hopefully!)


def quickGet(company, days_back):
    today = datetime.date.today()
    start = today - datetime.timedelta(days=days_back)
    data = getCompanyData(company, start, today)
    return transformData(data)


def createDataFrame(first_data):
    df = pd.DataFrame(first_data)
    df = df.set_index('date_string')
    keys = first_data[0].keys()
    for item in keys:
        if item != 'date_string':
            del df[item]
    return df


def convertMarketCap(string):
    if 'B' in string:
        return float(string[:-1])*1000000000
    else:
        return float(string[:-1])*1000000

# create summary stats for daily entries over a set of companies
# total_transaction_vol,


def summStats(new_entry, mc, summ_dict={}):
	summ_dict['total_value_change']+=mc*new_entry['proportion_change']
	summ_dict['total_value_range'] +=mc*new_entry['proportion_range']
	summ_dict['total_shares'] += mc/new_entry['average_price']
	summ_dict['total_volume'] += new_entry['volume']
	return summ_dict

#takes a company object, and a data frame, and tries a regression. 
# def regress_lasso(df, y):
# 	new = df.copy()
# 	new[y.symbol] = new[y.symbol].shift(-1)
# 	new=new[:-1]

def getIndustryData(industry):
    try:
        now = datetime.datetime.now()
        print industry.name
        myCs = Company.objects.filter(industry=industry)
        print myCs.count()
        myData = createDataSet(myCs,365)
        data = myData.to_json()
        industry.data = data
        industry.save()
        print datetime.datetime.now()-now
    except Exception, e:
        print str(e)



#this takes as its input a QuerySet of companies, and returns a dataframe with those companies, and summary statistics about them. 
def createDataSet(company_set, days_back,include_summary=True, df = None):
    rand = company_set.order_by('?').first()
    data = quickGet(rand, days_back)
    df = createDataFrame(data)
    summaries = {}
    for item in df.index.tolist():
    	summaries[item]={'total_value_change':0.0, 'total_value_range':0.0, 'total_shares':0.0, 'total_volume':0.0}
    mc = 0.0
    for company in company_set.all():
        try:
            mc += convertMarketCap(Share(company.symbol).get_market_cap())
        except:
            pass
        data = quickGet(company, days_back)
        df[str(company.symbol)]=0.0
        for day in data:
        	date_string=day['date_string']
        	if include_summary:
        		summaries[date_string] = summStats(day,mc,summaries[date_string])
        	df.set_value(date_string, company.symbol, day['proportion_change'])
    df['ind_pct_ov_ch'] = 0.0
    df['ind_pct_ov_rg'] = 0.0
    df['ind_pct_vol'] = 0.0
    if include_summary:
    	try:
    		for key, value in summaries.iteritems():
    			df.set_value(key, 'ind_pct_ov_ch', (value['total_value_change']/mc))
    			df.set_value(key, 'ind_pct_ov_rg', (value['total_value_range']/mc))
    			df.set_value(key, 'ind_pct_vol', (value['total_volume']/value['total_shares']))
    	except Exception,e:
    		print str(e)
    return df



# takes a string formatted in yahoo finance structure, and returns it as a
# datetime.date type.
def getDate(datestring):
    return datetime.datetime.strptime(datestring, "%Y-%m-%d").date()

# takes a datetime.date, and returns a string formatted for yahoo finance


def getToString(date):
    return "%s-%s-%s" % (date.year, date.month, date.day)

# get companies defined by a list of company data, where the company's smybol is in each company dict under the key 'Symbol'.
# returns as a query set of companies.


def getCompanies(company_list_json):
    myArr = []
    for item in company_list_json:
        myArr.append(item['Symbol'])
    return Company.objects.filter(symbol__in=myArr)

# takes as input a company object, start date and end_date (as datetime.date)
# returns an array of daily stock information.


def getCompanyData(company, start_date, end_date):
    start_date = getToString(start_date)
    end_date = getToString(end_date)
    share = Share(company.symbol)
    return share.get_historical(start_date, end_date)

# takes standad output of yahoo finance data points in an array, and transforms the data dicts
# it adds additional data fields to the dictionaries


def transformData(data_array):
    for day in data_array:
        day['close'] = float(day['Close'])
        day['open'] = float(day['Open'])
        day['high'] = float(day['High'])
        day['low'] = float(day['Low'])
        day['volume'] = float(day['Volume'])
        day['change'] = day['close'] - day['open']
        day['price_range'] = day['high'] - day['low']
        day['proportion_change'] = day['change']/day['open']
        # this is effectively a metric of volatility.
        day['proportion_range'] = day['price_range']/day['open']
        day['average_price'] = (day['high'] + day['low'])/2.0
        day['date'] = getDate(day['Date'])
        day['date_string'] = getToString(day['date'])
        del day['Close'], day['Open'], day['High'], day[
            'Low'], day['Date'], day['Adj_Close']
    return data_array


# needs to be tested
# this unpacks all company information from the json files provided.
# def company_info_to_dict():
#     nyse = 'nyse.json'
#     nasdaq = 'nasdaq.json'
#     amex = 'amex.json'
#     myList = [(nyse, 'NYSE'), (nasdaq, 'NASDAQ'), (amex, 'AMEX')]
#     myDict = {}
#     for item in myList:
#         myData = unpackJsonData(item[0])
#         for item in myData:
#             myDict[item['Symbol']] = {'name': item['Name'], 'last_sale': item['LastSale'], 'market_cap': item['MarketCap'], 'ipo_year': item[
#                 'IPOyear'], 'sector': item['Sector'], 'industry': item['industry'], 'summary_quote': item['Summary Quote'], 'exchange': item[1]}

#     return myDict
