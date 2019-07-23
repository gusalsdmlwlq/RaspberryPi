# 빈 좌석 수 요청
# response.py


import requests

IP = "172.29.148.137"
PORT = 5001

res = requests.post(url="http://{}:{}/api/displayEmptySeats".format(IP,PORT))
res = res.text
res = res.split(':')[1]
res = res.split('}')[0]
res = int(res)
print(res)