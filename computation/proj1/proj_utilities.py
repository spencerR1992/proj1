import boto
from boto.s3.key import Key 
from django.conf import settings
import utils 
from utils import *
from django.core.management import call_command
import time



my_id = settings.AWS_ACCESS_KEY_ID
my_pw = settings.AWS_SECRET_ACCESS_KEY
bucket_name=settings.AWS_BUCKET_NAME


#function dumps the entire contents of the DB to a local JSON file that is timestamped. 
def dumpToJSON():
	myFile = str(time.time()) + '.json'
	output = open(myFile, 'w')
	call_command('dumpdata', format='json', stdout=output)
	output.close()
	return myFile

# def saveToS3(file_name):
# 	conn = boto.connect_s3(my_id,my_pw)
# 	my_bucket=conn.get_bucket(bucket_name)
# 	k = Key(my_bucket, file_name)
# 	with open(file_name) as f:
# 		k.send_file(f)



