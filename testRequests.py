import requests
import os
import sys
from io import BytesIO
import json
import base64


pathswxevd = str(input("Enter the directory path for swxevd(Leave empty if not applicable):"))
pathacd = str(input("Enter the directory path for acd-avaya node(Leave empty if not applicable):"))
pathascws = str(input("Enter the directory path for ascws(Leave empty if not applicable):"))

ascwsList = []
acdList = []
swxevdList = []
if(pathascws):
    ascwsList = os.listdir(pathascws)
    print(ascwsList)
if(pathacd):
    acdList = os.listdir(pathacd)
    print(acdList)
if(pathswxevd):
    swxevdList = os.listdir(pathswxevd)
    print(swxevdList)

AgentId = '2'

# 1 - time, 2 - threads, 3 - log levels
filterList = ['2']
# Send in a list of fields to be filtered by in filtered list...



startDatetime = "2023-01-27 14:30:21.220"
endDatetime = "2023-01-27 15:30:21.220"
# send in starting and ending datetime if 1 chosen.


threadIds = ['ttp-nio-20200-exec-6']  #send in the list of threads you want to be filtered out


#

ascwsList = [base64.b64encode(open(f"{pathascws}/{f}", 'rb').read()).decode() for f in ascwsList]
acdList = [base64.b64encode(open(f"{pathacd}/{f}", 'rb').read()).decode()for f in acdList]
swxevdList = [base64.b64encode(open(f"{pathswxevd}/{f}", 'rb').read()).decode() for f in swxevdList]

files = {
    'ascwsfiles':ascwsList,
    'acdavayafiles':acdList,
    'swxevdfiles':swxevdList
}

BASE = "http://127.0.0.1:8111/"

response = requests.post(BASE+'logAggregator', json={
    "AgentId": AgentId,
    "filterList": filterList,
    # "startDatetime": startDatetime,
    # "endDatetime": endDatetime,
   #"threadIds": threadIds,
    "files": files
})
# structure of performance data: [ threadId, customerid, acdid, agentid, agentlogonId, performance_time ]
print(response.json())



#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/swxevd'
#/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/acd-avaya'
#'/Users/samirhendre/Desktop/NICE LOG AGGREGTOR/ascws'

#2023-01-27 14:30:21.220

#receiver.2 Service5 indexDeleteSchld1

#TRACE DEBUG
# /Users/samirhendre/Downloads/NICE LOG AGGREGTOR/acd-avaya
# /Users/samirhendre/Downloads/NICE LOG AGGREGTOR/swxevd
# /Users/samirhendre/Downloads/NICE LOG AGGREGTOR/ascws
