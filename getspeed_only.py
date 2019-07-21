#!/usr/bin/python
#-*-coding:utf-8-*-

'''
speed test
this file is used to compute the network speed
for speed test
every 10s you will got a print
at last you will get the mean speed
'''

import requests 
from requests.auth import HTTPBasicAuth 
from bs4 import BeautifulSoup as bs
import time
#url='http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:2/node-connector/openflow:2:2/opendaylight-port-statistics:flow-capable-node-connector-statistics/bytes/' 
headers = {'Accept': 'application/xml'}


def get_rate_only(switch,port):
  #get the network rate and show the rate
  url='http://127.0.0.1:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:'+str(switch)+'/node-connector/openflow:'+str(switch)+':'+str(port)+'/opendaylight-port-statistics:flow-capable-node-connector-statistics/bytes/' 
  rate_mean = 0
  print("network speed peer 10s:")
  print()
  for i in range(0,10):
    r1=requests.get(url, auth=HTTPBasicAuth('admin', 'admin'),headers=headers) 

    getstring = r1.text

    soup = bs(getstring,"html.parser")

    rvdata_b=int(soup.received.string)
    transdata_b=int(soup.transmitted.string)
    #
    time.sleep(9)
    #
    r2=requests.get(url, auth=HTTPBasicAuth('admin', 'admin'),headers=headers) 

    getstring = r2.text

    soup = bs(getstring,"html.parser")

    rvdata_a=int(soup.received.string)
    transdata_a=int(soup.transmitted.string)

    #

    indata = rvdata_a-rvdata_b
    outdata = transdata_a-transdata_b


    #used to spy on the data flow
    rate_of_flow_sec= (indata+outdata)/9
    rate_mean +=rate_of_flow_sec
    print(str(rate_of_flow_sec) + ' bytes/s')
    print(str(rate_of_flow_sec/1000000) + ' MB/s')
    print("***********************")

  #rate per 100s
  rate = rate_mean/10
  print()
  print("mean network speed in 100s: ")
  print(str(rate) + ' bytes/s')
  print(str(rate/1000000) + ' MB/s')

get_rate_only(switch,port)
