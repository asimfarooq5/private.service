# private.service

## Getting Started

```shell
sudo apt install httpie python3-pip 
pip3 install -r requirements.txt
python3  -u app.py
```

### Api Test:

```shell
http "http://ip-domain:5000/api/content/ device_id=001 nick_name=test body=thisistext datetime=01-01-21 sender_number=0300 status=1"
```

### Result

```
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 5
Content-Type: application/json
Date: Wed, 17 Mar 2021 12:59:14 GMT
Server: nginx/1.18.0 (Ubuntu)

"OK"
```

## Admin

[http:/ip-domain:5000/admin](http:/ip-domain:5000/admin)

## Create systemd service

```shell
vim /etc/systemd/system/sms.service
```

### add the following text and save file

```text
[Unit]
Description=sms
After=network.target

[Service]
User=root
WorkingDirectory=/home/ubuntu/private.service
ExecStart=/usr/bin/python3 /home/ubuntu/private.service/app.py

[Install]
WantedBy=multi-user.target
```

## Enable and start systemd

```shell
sudo systemctl enable sms.service
sudo systemctl start sms.service
```

### Check service status (Active)

```shell
sudo systemctl status sms.service
```

Done!