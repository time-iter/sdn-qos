#!/usr/bin/python
#-*-coding:utf-8-*-

'''
startup mod 1
'''

from action import *
from addqos import *
from getspeed import *
from controlmod1 import *
from controlmod2 import *
import time

#default
rate_list_default = [0,1000000,2000000,3000000,4000000,5000000]
#init 
rate_list = [0,]

def startup(rate_list,rate_list_default,mod,switch,inport,outport):
  '''
  set the qos rate list for speed control
  '''
  print("default rate list: ")
  print(rate_list_default)
  isdefault = input("do you want to use default rate list?(y/n)")

  if isdefault == 'y':
    rate_list = rate_list_default
  else:
    print("example:")
    print("1000000,2000000,3000000,4000000,5000000")
    inputstring = input("please input as the example:")

    inputlist = inputstring.split(",")
    for value in inputlist:
      rate = int(value)
      rate_list.append(rate)
  qos_id_default = 1
  action_ready(rate_list,str(qos_id_default),switch,outport)

  queue_id_default = 2
  #add default flow
  flow(str(queue_id_default),switch,inport,outport)

  #queue_id_one = 1
  #speed control start here
  if str(mod) == '1':
    while True:
      getrate = get_rate(switch,outport)
      #getrate = 90 
      do_qos1(getrate,rate_list,switch,inport,outport)
      print("**************************")
      #time.sleep(5)
  elif str(mod) == '2':
    while True:
      getrate = get_rate(switch,outport)
      do_qos2(getrate,rate_list,switch,inport,outport)
      print("**************************")
  else:
    print("unexcepted wrong")


#startup
mod = 1
switch = str(1)
inport = str(2)
outport = str(1)
print("*******************************************************")
print("* BEFORE SPEED CONTROL, PLEASE ADD OR CHANGE THE QOS  *")
print("*******************************************************")
print()
startup(rate_list,rate_list_default,str(mod),switch,inport,outport)
