# unifi_client_scanner

A simple python app to query Unifi controller API endpoint to scan wlan clients and notify by email if new clients join the network. You will need some email account to send & receive emails.

## First create .env file locally on your working dir for your script secrets
```
CONTROLLER_URL=https://your.unifi.url
USERNAME=unifiusername
PASSWORD=unifipassword
SITE_ID=default
EMAIL_SENDER=unifi@somedomain.com
SMTP_USERNAME=emailusername
SMTP_PASSWORD=emailpassword
EMAIL_RECIPIENT=recipient@somedomain.com
SMTP_SERVER=mail.somedomain.com
SMTP_PORT=465
```

## Then build and run (using .env file) with docker

docker build -t unifi-client-scanner:latest .

docker run --env-file .env -it --rm unifi-client-scanner:latest

## Example output of the program running
```
docker run --env-file .env -it --rm unifi-client-scanner:latest   
...
Login successful!
2024-09-10 05:16:21 - Checking for new clients...
2024-09-10 05:16:21 - New clients detected: {'xx:xx:xx:xx:xx:xx', 'yy:yy:yy:yy:yy:yy'}

=== DEBUG: Email Content ===
Subject: New Client Alert
To: recipient@somedomain.com
From: unifi@somedomain.com
Body:
New clients detected on your network:

MAC: xx:xx:xx:xx:xx:xx, IP: 192.168.1.11, Hostname: somedevice1
MAC: yy:yy:yy:yy:yy:yy, IP: 192.168.1.22, Hostname: somedevice2
============================

Alert email sent successfully!
2024-09-10 05:21:21 - Checking for new clients...
2024-09-10 05:21:22 - No new clients found.
```

