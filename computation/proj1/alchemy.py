import requests
from django.conf import settings
import datetime
import time
from special.models import *


def timestampToDatetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))


def datetimeToTimestamp(datetime):
    return int(time.mktime(datetime.timetuple()))


# this function makes a request of the alchemy news api.
# it looks for mentions of a company in the news in the last 60 days, and returns all articles.
# it takes as input a special.Company object, and returns the dictionary
# of data from alchemy news.
def gc():
    return Company.objects.get(symbol='IBM')
    
# This function takes a concept to search on, and an optional param next, and then calls the alchemy news API. 
def makeNewsRequest(company_name,next=None):
	query_endpoint = settings.ALCHEMY_API_ENDPOINT + '/data/GetNews?outputMode=json'
	apikey = settings.ALCHEMY_API_KEY
	today = datetime.datetime.now()
	start = today - datetime.timedelta(days=60)
	start = datetimeToTimestamp(start)
	end = datetimeToTimestamp(today)
	dedup = 1
	dedupThreshold = 0.4
	rank = 'high^medium'
	retrn = 'enriched.url.title,'
	retrn = retrn + 'enriched.url.publicationDate,enriched.url.entities,'
	retrn = retrn + 'enriched.url.docSentiment,enriched.url.concepts,enriched.url.taxonomy'
	myDict = {}
	for i in ('start', 'end', 'apikey', 'dedup', 'dedupThreshold', 'rank'):
		myDict[i] = locals()[i]
	if next is not None:
		myDict['next']=next
	myDict['return'] = retrn
	myDict['q.enriched.url.text'] = company_name	
	myDict['q.enriched.url.cleanedTitle'] = company_name
	return requests.get(query_endpoint, params=myDict).json()

# takes a special.Company object, and returns an alchemy request for information about that company.
# returns the documents as a JSON object.
def getDocs(company, docs=[], next=None):
	# print 'function start. Total Docs: %s' % len(docs)
	data = makeNewsRequest(company.name,next)
	if 'result' in data:
		new_docs = data['result']['docs']
		docs =  docs + new_docs
		if 'next' in data['result']:
			newsApiRequest(company,docs,data['result']['next'])
		else:
			return docs
	else:
		return docs
