# Unifi Client Scanner

A simple python app to query Unifi controller API endpoint to scan wlan clients and notify by email if new clients join the network. You will need some email account to send & receive emails. The app will also expose port 8080 for monitoring the health of the unifi client scanner thread with GET /health. If the unifi thread is healthy, 200ok is returned and if the unifi thread is declaired dead, a 500 error is returned to the client. This health monitoring is useful if the app is deployed in a k8s environment and you want to use liveness and readiness probes.

## First create .env file locally for your script secrets. Content of the .env file as below.
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

## Then build the image

docker build -t unifi-client-scanner:latest .

## Finally run with the local .env file you created at the beginning
(This example is for a quick run - it also removes the container after running)

```docker run --env-file .env -it --rm unifi-client-scanner:latest```

(To start the container in detatched mode use something like this)

```docker run --env-file .env -e TZ=Europe/Helsinki -d --restart unless-stopped --name unifi-client-scanner unifi-client-scanner:latest```

## Or if you prefer docker compose...
(introducing the envs like below should get you going. I try to keep the pre generated docker hub image up to date as well)

```
# On your docker-compose.yml file:
services:
  unifi-client-scanner:
    image: attley86/unifi-client-scanner:latest
    environment:
      - TZ=Europe/Helsinki
      - CONTROLLER_URL=https://your.unifi.url
      - USERNAME=unifiusername
      - PASSWORD=unifipassword
      - SITE_ID=default
      - EMAIL_SENDER=unifi@somedomain.com
      - SMTP_USERNAME=emailusername
      - SMTP_PASSWORD=emailpassword
      - EMAIL_RECIPIENT=recipient@somedomain.com
      - SMTP_SERVER=mail.somedomain.com
      - SMTP_PORT=465
```

## Example output of the program running
(The program first lists all of the clients on the network and fires an email of all the clients detected. Then after a short period, the program checks if any new clients have joined the network and if so, the program creates another email alert. In the example below, no new clients have been detected on the second scanning. Once a client has been seen on the network, there wont be an alert about the same client again if it reconnects to network.)

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

