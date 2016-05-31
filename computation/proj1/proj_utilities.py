import boto
from boto.s3.key import Key 
from django.conf import settings
import utils 
from utils import *
from django.core.management import call_command
import time



myId = settings.AWS_ACCESS_KEY_ID
myPw = settings.AWS_SECRET_ACCESS_KEY


def dumpDbToS3():
	myFile = str(time.time()) + '.json'
	output = open(myFile, 'w')
	call_command('dumpdata', format='json', stdout=output)
	output.close()
