from io import StringIO
import xml.etree.ElementTree as ET
import os
import time
from pprint import pprint
import socket
import requests

def get_ci_events_operational():
	return os.popen("wevtutil qe Microsoft-Windows-CodeIntegrity/Operational").read()

flag=1  # No FPs yet
count=1
while(flag):
	directoryNew="D:\\FalsePositive\\New"
	if not os.path.exists(directoryNew):
		os.makedirs(directoryNew)
	os.popen("copy D:\\FalsePositive\\AzureProfilerExtension.exe D:\\FalsePositive\\New\\AzureProfilerExtension.exe")
	os.popen("copy D:\\FalsePositive\\AzureProfiler.dll D:\\FalsePositive\\New\\AzureProfiler.dll")
	os.popen("copy D:\\FalsePositive\\WaSecAgentProv.exe D:\\FalsePositive\\New\\WaSecAgentProv.exe")
	file1='D:\\FalsePositive\\New\\AzureProfilerExtension.exe'
	file2='D:\\FalsePositive\\New\\AzureProfiler.dll'
	file3='D:\\FalsePositive\\New\\WaSecAgentProv.exe'
	os.system('"' + file1 + '"')
	os.system('"' + file3 + '"')
	url = 'https://aka.ms/'
	print("Running executable for %d time"%(count))
	print(socket.gethostbyname(socket.gethostname()))
	print(time.asctime())
	headers = {'Content-type': 'application/json',}
	data = '{"tm":"'+time.asctime()+'", "ip":"'+socket.gethostbyname(socket.gethostname())+'", "text":"Running successfully"}'
	response1 = requests.get(url+'cifalsepositivetest', headers=headers, data=data)
	#print(response1)
	xml=get_ci_events_operational().splitlines()
	for each in xml:
        #pprint(each)
		eve = ET.fromstring(each)
        #print(eve[0][1].text)
		try:
            #print(eve[1][3].text)
			if eve[1][3].text=='0' and eve[0][1].text in ['3076','3077']:
				data = '{"tm":"'+time.asctime()+'", "ip":"'+socket.gethostbyname(socket.gethostname())+'","text":"'+eve+'"}'
				response2 = requests.get(url+'cifalsepositivecheck', headers=headers, data=data)
				flag=0
		except:
			pass
		if flag==0:
			break
        #print(eve[1][1].text)
	time.sleep(60)
	if flag:
		os.remove(file1)
		os.remove(file2)
		os.remove(file3)
		count+=1
