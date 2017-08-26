import requests
import json
import time

base_url="http://192.168.4.29:5000/get_pill_by_user_for_pi?user_id=1"
response = requests.get(base_url)
json_data = json.loads(response.text)
i = int(json_data["size"])
k = 1
medicinList = []
while(k<=i):
	obj = json_data[str(k)]
	timing = None
	if(obj['cycle']=="100"):
		timing = 1
	elif(obj['cycle']=="010"):
		timing = 2
	else:
		timing = 3
	value = [obj["partition_number"],timing,obj["count"],obj["pill_id"]]
	medicinList.append(value)
	k+=1


