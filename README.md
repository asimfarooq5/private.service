# private.service


## Getting Started



```shell
sudo apt install httpie python3-pip 
pip3 install -r requirements.txt
```

###Api:
```shell
http "http://15.188.52.38/api/content/ device_id=001 nick_name=test body=thisistext datetime=01-01-21 sender_number=0300 status=1"
```

###Result
```
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 5
Content-Type: application/json
Date: Wed, 17 Mar 2021 12:59:14 GMT
Server: nginx/1.18.0 (Ubuntu)

"OK"
```
