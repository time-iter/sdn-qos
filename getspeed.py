#!/usr/bin/python
#-*-coding:utf-8-*-

'''
this file shows how to get the rate right now of an opwndaylight controller
wwhen this script run one time, it will cost 100s
we compute the rate of the controller every 10s and output the outcome
when compute ten times we got a mean rate and return 
'''
'''
in the function get_rate():
we use the Restful API ("url") of the opendaylight controller
use  package "requests" as a crawler to communicate with the controller
use package "BeautiSoup" to parse the contents crawed by "requests"
'''
import requests 
from requests.auth import HTTPBasicAuth 
from bs4 import BeautifulSoup as bs
import time

headers = {'Accept': 'application/xml'}
#
def get_rate(switch,port):
	'''
	get the rate of network 
	'''
	url='http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+str(switch)+'/node-connector/openflow:'+str(switch)+':'+str(port)+'/opendaylight-port-statistics:flow-capable-node-connector-statistics/bytes/' 
	rate_mean = 0
	for i in range(0,3):
		r1=requests.get(url, auth=HTTPBasicAuth('admin', 'admin'),headers=headers) 

		getstring1 = r1.text

		soup = bs(getstring1,"html.parser")

		rvdata_b=int(soup.received.string)
		transdata_b=int(soup.transmitted.string)
		#
		time.sleep(3)
		#
		r2=requests.get(url, auth=HTTPBasicAuth('admin', 'admin'),headers=headers) 

		getstring2 = r2.text

		soup = bs(getstring2,"html.parser")

		rvdata_a=int(soup.received.string)
		transdata_a=int(soup.transmitted.string)

		#

		indata = rvdata_a-rvdata_b
		outdata = transdata_a-transdata_b


		#used to spy on the data flow
		rate_of_flow_sec= (indata+outdata)/3
		rate_mean +=rate_of_flow_sec
		'''
		print(str(rate_of_flow_sec) + ' bytes/s')
		print(str(rate_of_flow_sec/1000000) + ' MB/s')
		print("***********************")
		'''

	#rate per 6s
	rate = rate_mean/3

	return rate
