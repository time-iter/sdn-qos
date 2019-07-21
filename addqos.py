#!/usr/bin/python
#-*-coding:utf-8-*-

'''
this file shows how to add queue qos and apply qos strategy 
to flowtable of opendaylight contrioller
to add qos a rate_list is need 
the first element of rate_list is used to implementate
a specil speed control strategy 
the strategy is implementated in file "control_mod2.py"
in ordinary mod the first element will not be used 
and it is invisible
'''
from action import *
import time

def action_ready(rate_list,qos_id,switch,port):
  '''
  add the queue,qos and apply them to the termination
  '''
  queue_uuid_dic = {}
  num = 1
  for rate in rate_list:
    queue_uuid_dic[num] = queue(num,rate)
    num = num + 1
    time.sleep(3)

  qos_uuid = qos(queue_uuid_dic,qos_id)
  termination(qos_uuid,switch,port)


#do add
'''
queue_id_default = 2
qos_id_default = 1
set_rate_list()
action_ready(rate_list,qos_id)
flow(queue_id_default)
'''