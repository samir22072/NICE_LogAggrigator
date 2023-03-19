import requests
import os
import sys
import os
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
if(pathacd):
    acdList = os.listdir(pathacd)
if(pathswxevd):
    swxevdList = os.listdir(pathswxevd)

AgentId = '2'

filterList = ['1','2']

startDatetime = "2023-01-27 14:30:21.220"
endDatetime = "2023-01-27 14:31:21.220"

threadIds = ["receiver.2","Service6"]

ascwsList = [(f, base64.b64encode(open(f"{pathascws}/{f}", 'rb').read()).decode()) for f in ascwsList]
acdList = [(f, base64.b64encode(open(f"{pathacd}/{f}", 'rb').read()).decode()) for f in acdList]
swxevdList = [(f, base64.b64encode(open(f"{pathswxevd}/{f}", 'rb').read()).decode()) for f in swxevdList]

files = {
    'ascwsfiles':ascwsList,
    'acdavayafiles':acdList,
    'swxevdfiles':swxevdList
}

BASE = "http://127.0.0.1:5000/"

# Refer this for request format
response = requests.post(BASE, json={
    "AgentId": AgentId,
    "filterList": filterList,
    "startDatetime": startDatetime,
    "endDatetime": endDatetime,
    "threadIds": threadIds,
    "files": files
})

print(json.dumps(response.json(), indent = 1))
