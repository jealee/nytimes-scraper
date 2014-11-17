from urllib2 import urlopen
import re
from pickle import dump
import string
import json
import optparse
import string
import time
import pandas as pd

def scrapeComments():
	current_max_outfile = 1
	print current_max_outfile
	fields_of_interest = ['display_name', 'articleURL','location', 'commentBody', 'editorsSelection', 'recommendationCount']
	m = []
	sleeptime = 0
	offset = 0
	api_idx = 0
	api_keys = []#put your API key in the list. I got a few to increase the speed of querying, but you might want to be careful doing that to avoid annoying the NYT. 
	

	while 1:
		try:
			api_key = api_keys[api_idx % len(api_keys)]
			api_idx += 1
			url = 'http://api.nytimes.com/svc/community/v2/comments/recent.json?offset=%i&api-key=%s' % (offset*25 + start, api_key) 
			print 'Offset', 25*offset + start, url
			page=urlopen(url)
			data=page.read()
			decoded_data = json.loads(data)
			for i in range(25):
				m.append([decoded_data['results']['comments'][i][a] for a in fields_of_interest])
			if offset % 10 == 1:
				for i in range(len(m)):
					for field in [0, 2, 3]:
						m[i][field] = m[i][field].encode('ascii', 'ignore')
				dataframe = pd.DataFrame(m, columns = fields_of_interest)
				dataframe['location'] 
				dataframe.to_csv(open('genderComments%i.csv' % (current_max_outfile + 1), 'wb'), index = False)
			offset += 1
			
		except:
			print 'Error scraping comments with key %s. Sleeping for %i seconds.' % (api_key, sleeptime)
			time.sleep(sleeptime)
			