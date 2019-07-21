#!/usr/bin/python
#-*-coding:utf-8-*-

'''
this file shows the second speed control strategy(mod2)
the first element of rate_list is used in this strategy
this element is used to change the speed as the program's need
this strategy will compute the network speed 
the variable "isBusy" means how busy the network is
the lesser this variable is,the network is more busy
the variable "isWaste" means the degree of the bandwidth
that is wasted, it gets bigger ,the waste raise
'''


#from getspeed import *
from action import *
from addqos import *
#from starup import *
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import time



headers = {'Accept': 'application/xml'}
headers2={'Accept':'application/xml','Content-Type':'application/xml'}


def do_qos2(rate,rate_list,switch,inport,outport,qos_id_mod2=2,queue_id_one=str(1)):
	
#	get current rate and apply qos-strategy
	qos_url = 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640/ovsdb:qos-entries/QOS-1/'
	url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(switch)+'/table/0/flow/1'
	rtest = requests.get(url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers)
	containrate = rtest.text
	soup = bs(containrate,"html.parser")

	queue_now = int(soup.queue.string)

	isBusy = (rate_list[queue_now - 1] - rate)/(rate_list[queue_now - 1]+1)


	if isBusy <= 0.1:
		if queue_now == len(rate_list):
			print("now the max rate!")
		else:
			r2 = requests.get(qos_url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers2)
			if r2.status_code == 200:
				print("qos 1 got successfully!")
				contain_uuid = r2.text
				soup_uuid = bs(contain_uuid,"html.parser")
				qos_uuid = soup_uuid.find_all("qos-uuid")[0].string
				termination(qos_uuid,switch,outport)
				flow(str(queue_now+1),switch,inport,outport)
			else:
				print("qos 1 uuid got failed!")

	elif isBusy >= 0.25 and queue_now == 2:
		if rate > (rate_list[queue_now-1] * 0.5):
			rate_zero = int(rate_list[queue_now-1] * 0.75)
			rate_queue1 = [rate_zero]
			action_ready(rate_queue1,qos_id_mod2,switch,outport)
			flow(str(queue_id_one),switch,inport,outport)
		elif rate < (rate_list[queue_now-1] * 0.25):
			rate_zero = int(rate_list[queue_now-1] * 0.25)
			rate_queue1 = [rate_zero]
			action_ready(rate_queue1,qos_id_mod2,switch,outport)
			flow(str(queue_id_one),switch,inport,outport)
		else:
			rate_zero = int(rate_list[queue_now-1] * 0.5)
			rate_queue1 = [rate_zero]
			action_ready(rate_queue1,qos_id_mod2,switch,outport)
			flow(str(queue_id_one),switch,inport,outport)
	elif isBusy >= 0.25 and queue_now > 2:
		isWaste = (rate - rate_list[queue_now-2])/(rate_list[queue_now-1] - rate_list[queue_now-2])
		if isWaste <= 0.75:
			if isWaste >= 0.5:
				rate_zero = int(rate_list[queue_now-2] + (0.75 * (rate_list[queue_now-1] - rate_list[queue_now-2])))
				rate_queue1 = [rate_zero]
				action_ready(rate_queue1,qos_id_mod2,switch,outport)
				flow(str(queue_id_one),switch,inport,outport)
			elif isWaste <=0.25:
				rate_zero = int(rate_list[queue_now-2] + (0.25 * (rate_list[queue_now-1] - rate_list[queue_now-2])))
				rate_queue1 = [rate_zero]
				action_ready(rate_queue1,qos_id_mod2,switch,outport)
				flow(str(queue_id_one),switch,inport,outport)
			else:
				rate_zero = int(rate_list[queue_now-2] + (0.5 * (rate_list[queue_now-1] - rate_list[queue_now-2])))
				rate_queue1 = [rate_zero]
				action_ready(rate_queue1,qos_id_mod2,switch,outport)
				flow(str(queue_id_one),switch,inport,outport)
		else: pass
	else: pass



#do add
#queue_id_default = 2
#qos_id_mod2= 2
#qos_id_default = 1
#queue_id_one = 1
'''
mod = 2
print("*******************************************************")
print("* BEFORE SPEED CONTROL, PLEASE ADD OR CHANGE THE QOS  *")
print("*******************************************************")
print()
startup(rate_list,rate_list_default,str(mod))
#action_ready(rate_list,qos_id)
#flow(str(queue_id_default))
#start qos
'''
'''
while True:
	rate = get_rate()
	do_qos2(rate,rate_list,queue_id_one)
'''

