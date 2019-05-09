from me.robot import Execution
from multi_req import scrap
from bs4 import BeautifulSoup
from money_parser import price_str
import sys
from me.util import lookahead
#import pp
import json
import requests
import urllib.request
import time

if len(sys.argv)<2:
	raise Exception('Passar o nome do arquivo é necessário!')

exe=Execution(sys.argv[1])

exe.start()

url = 'https://apiconsultapreco.ead.br/api/v1/courses/graduation/graduacao'  
courses = urllib.request.urlopen(url+str()).read()  
courses = json.loads(courses.decode('utf-8'))

for c in courses:
	url = 'https://apiconsultapreco.ead.br/api/v1/states/course/' + json.dumps(c['post_id'])
	states = urllib.request.urlopen(url+str()).read()  
	states = json.loads(states.decode('utf-8'))

	time.sleep(0.2)

	for st in states:
		url = 'https://apiconsultapreco.ead.br/api/v1/polos/course/' + json.dumps(c['post_id']) +'/state/'+ st['initials']
		polos = urllib.request.urlopen(url+str()).read()  
		polos = json.loads(polos.decode('utf-8'))

		time.sleep(0.2)

		for p in polos:
			url = 'https://apiconsultapreco.ead.br/api/v1/courses/course/' + json.dumps(c['post_id']) +'/polo/'+ json.dumps(p['post_id'])
			prices = urllib.request.urlopen(url+str()).read()  
			prices = json.loads(prices.decode('utf-8'))

			time.sleep(0.2)

			for pr in prices['course_polos']:
				exe.add_price(
					ies_sigle='LAUREATE',
					course_name=c['name'],
					price=pr['price'],
					price_w_d=pr['promo_price'],
					state_id=st['initials'],
					state_name=st['name'],
					local_name=p['name'],
					modality='EAD'
				)

exe.end()