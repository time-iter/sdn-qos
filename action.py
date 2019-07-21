#!/usr/bin/python
#-*-coding:utf-8-*-

'''
this file shows how to apply the qos strategy we listed
queue : we apply the list of our strategy to the queue
    queue sotre the qos-strategy and service as a member of a qos block
    all the queues we  create match only one qos
qos : we create a qos block with these queues we have already created
    the qos contain all thes queues it communicate with queue with queue_uuid
termination : we use this to apply our qos to the switch port 
    termination contains the qos block we created
flow : flow is used to apply the qos to the flowtable of our switch
    flow contains the flow that control the rate of our switch port
'''

'''

'''
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
import time

#put_use
headers1={'Accept':'application/json','Content-Type':'application/json'}
#get_use
headers2={'Accept':'application/xml','Content-Type':'application/xml'}

def queue(queue_id,max_rate):
    '''
    add queue of rate and get the uuid of queue
    '''
    queue_uri='http://127.0.0.1:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640/ovsdb:queues/QUEUE-'+str(queue_id)+'/'
    queue_url='http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640/ovsdb:queues/QUEUE-'+str(queue_id)+'/'
    #push_body
    queue_data = '{"ovsdb:queues": [{"queue-id": "QUEUE-' + str(queue_id) + '",' + '"queues-other-config": [{"queue-other-config-key": "max-rate","queue-other-config-value": "' + str(max_rate)+ '"}]}]}'
    #add_queue
    r1=requests.put(queue_uri, auth=HTTPBasicAuth('admin', 'admin'),headers=headers1,data=queue_data)
    time.sleep(2)
    if r1.status_code==200:
        print("queue " + str(queue_id) + " added successfully! <"+str(max_rate)+">")
        #get_queue_uuid
        r2 = requests.get(queue_url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers2)
        if r2.status_code==200:
            print("queue " + str(queue_id) + " uuid got successfully! <"+str(max_rate)+">")
            contain_uuid = r2.text
            soup_uuid = bs(contain_uuid,"html.parser")
            queue_uuid = soup_uuid.find_all("queue-uuid")[0].string
            return queue_uuid
        else:
            print("queue " + str(queue_id) + " uuid get failed!")
    else:
        print("queue " + str(queue_id) + " added failed!!!")


def qos(queue_uuid_dic,qos_id):
    '''
    apply queue information to the qos and get uuid of qos
    '''
    qos_uri = 'http://127.0.0.1:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640/ovsdb:qos-entries/QOS-'+str(qos_id)+'/'
    qos_url = 'http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640/ovsdb:qos-entries/QOS-'+str(qos_id)+'/'
    qos_data1 = '{"ovsdb:qos-entries": [{"qos-id":"QOS-'+ str(qos_id) +'",'
    queue_list_data = ''
    for key,value in queue_uuid_dic.items():
        queue_number = key
        queue_uuid = value
        queue_list_item = '{"queue-number":"'+str(queue_number)+'","queue-uuid":"'+str(queue_uuid)+'"},'
        queue_list_data = queue_list_data + queue_list_item
    queue_list_data = queue_list_data[:-1]
    qos_data = qos_data1 + '"queue-list":[' + queue_list_data + ']}]}'

    r1 = requests.put(qos_uri, auth=HTTPBasicAuth('admin', 'admin'), headers=headers1, data=qos_data)
    time.sleep(2)
    if r1.status_code == 200:
        print("qos "+ str(qos_id) +" added successfully!")
        # get_queue_uuid
        r2 = requests.get(qos_url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers2)
        if r2.status_code == 200:
            print("qos "+str(qos_id)+" uuid got successfully!")
            contain_uuid = r2.text
            soup_uuid = bs(contain_uuid, "html.parser")
            qos_uuid = soup_uuid.find_all("qos-uuid")[0].string
            return qos_uuid
        else:
            print("qos " +str(qos_id)+"uuid get failed!")
    else:
        print("qos "+str(qos_id)+" added failed!!!")


def termination(qos_uuid,switch,port):
    '''
    apply the qos to the termination
    '''
    t_uri = 'http://127.0.0.1:8181/restconf/config/network-topology:network-topology/topology/ovsdb:1/node/ovsdb:%2F%2F192.168.25.147:6640%2Fbridge%2Fs1/termination-point/s'+str(switch)+'-eth' + str(port)
    tdata = '{"network-topology:termination-point": [{"ovsdb:name": "s'+str(switch)+'-eth'+str(port)+'","tp-id": "s'+str(switch)+'-eth'+str(port)+'","qos": "' + str(qos_uuid) + '"}]}'
    r1 = requests.put(t_uri, auth=HTTPBasicAuth('admin', 'admin'), headers=headers1, data=tdata)
    time.sleep(2)

    if r1.status_code==200:
        print("add to termination point <s"+str(switch)+"-eth"+str(port)+"> success")
    else:
        print("add to termination point <s"+str(switch)+"-eth"+str(port)+"> failed")

def flow(queue_id,switch,inport,outport):
    '''
    add the flow to chage the rate
    '''
    url = 'http://127.0.0.1:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:'+str(switch)+'/table/0/flow/1'
    flow_content = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><flow xmlns="urn:opendaylight:flow:inventory"><priority>20</priority><flow-name>flow2</flow-name><flags>SEND_FLOW_REM</flags><match><in-port>openflow:'+str(switch)+':'+str(inport)+'</in-port></match><hard-timeout>0</hard-timeout><idle-timeout>0</idle-timeout><cookie>30</cookie><id>1</id><table_id>0</table_id><instructions><instruction><order>0</order><apply-actions><action><order>1</order><set-queue-action><queue-id>'+str(queue_id)+'</queue-id><queue>'+str(queue_id)+'</queue></set-queue-action></action><action><order>2</order><output-action><output-node-connector>openflow:'+str(switch)+':'+str(outport)+'</output-node-connector></output-action></action></apply-actions></instruction></instructions></flow>'
    r = requests.put(url, auth=HTTPBasicAuth('admin', 'admin'), headers=headers2, data=flow_content)
    if r.status_code==200:
        print("flow added success!! <QUEUE-"+queue_id+">")
    else:
        print("flow added failed!!! <QUEUE-"+queue_id+">")


