# unifi_client_scanner

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

