#!/usr/bin/python
#-*-coding:utf-8-*-

'''
this file shows the first speed control strategy(mod1)
this strategy will compute the network speed 
the variable "isBusy" means how busy the network is
the lesser this variable is,the network is more busy
'''

from action import *
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import time



headers = {'Accept': 'application/xml'}

def do_qos1(rate,rate_list,switch,inport,outport):
	
#	get current rate and apply qos-strategy

	url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(switch)+'/table/0/flow/1'
	rtest = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers)
	containrate = rtest.text
	soup = bs(containrate,"html.parser")

	queue_now = int(soup.queue.string)

	isBusy = (rate_list[queue_now-1] - rate)/(rate_list[queue_now-1]+1)

	if isBusy <= 0.1:
		if queue_now == len(rate_list):
			print("now the max rate!")
		else:
			flow(str(queue_now+1),switch,inport,outport)
	elif isBusy >= 0.25:
		if queue_now == 2:
			print("now the lowest rate!")
		else:
			flow(str(queue_now-1),switch,inport,outport)
	else: pass



#do add
#queue_id_default = 2
#= 1

#action_ready(rate_list,qos_id)
#flow(str(queue_id_default))
#start qos


