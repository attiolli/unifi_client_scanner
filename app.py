import requests
import urllib3
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Disable warnings about insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# UniFi Controller Configuration
controller_url = os.getenv("CONTROLLER_URL")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
site_id = os.getenv("SITE_ID")

# Email Configuration
email_sender = os.getenv("EMAIL_SENDER")
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
email_recipient = os.getenv("EMAIL_RECIPIENT")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = os.getenv("SMTP_PORT")

# API Endpoints
login_url = f"{controller_url}/api/login"
clients_url = f"{controller_url}/api/s/{site_id}/stat/sta"

# Create a session to manage cookies
session = requests.Session()

# Path to the known clients file
known_clients_file = "known_clients.txt"

def load_known_clients(file_path):
    """Reads known clients from a text file and returns a set of MAC addresses."""
    known_macs = set()
    try:
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line.startswith("MAC:"):
                    # Extract MAC address
                    mac = line.split(",")[0].split("MAC:")[1].strip()
                    known_macs.add(mac)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    return known_macs

def login():
    payload = {"username": username, "password": password, "remember": True}
    response = session.post(login_url, json=payload, verify=False)
    response.raise_for_status()
    print("Login successful!")

def get_wifi_clients():
    """Retrieve the list of connected clients from the UniFi Controller."""
    headers = {
        "Content-Type": "application/json",
        "Referer": f"{controller_url}/manage/site/{site_id}/dashboard",
        "X-Requested-With": "XMLHttpRequest"
    }
    response = session.get(clients_url, headers=headers, verify=False)
    response.raise_for_status()
    clients = response.json()["data"]
    return clients

def get_client_details(mac_address):
    """Fetch detailed information for a specific MAC address from the UniFi Controller."""
    headers = {
        "Content-Type": "application/json",
        "Referer": f"{controller_url}/manage/site/{site_id}/dashboard",
        "X-Requested-With": "XMLHttpRequest"
    }
    # Note: UniFi API might not have a direct endpoint for querying individual MAC addresses;
    # so this function assumes all client details were obtained in get_wifi_clients()
    # If this endpoint is not available, you need to adjust the logic accordingly.
    clients = get_wifi_clients()
    for client in clients:
        if client['mac'] == mac_address:
            return client
    return None  # Return None if client details are not found

def send_alert(new_clients):
    """Send an alert email with details of new clients."""
    subject = "New Client Alert"
    body = "New clients detected on your network:\n\n"
    
    for client in new_clients:
        mac = client.get('mac', 'Unknown MAC')
        ip = client.get('ip', 'Unknown IP')
        hostname = client.get('hostname', 'Unknown')
        body += f"MAC: {mac}, IP: {ip}, Hostname: {hostname}\n"

    # Print the email content for debugging
    print("\n=== DEBUG: Email Content ===")
    print(f"Subject: {subject}")
    print(f"To: {email_recipient}")
    print(f"From: {email_sender}")
    print("Body:")
    print(body)
    print("============================\n")

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Use SMTP_SSL to connect to the SMTP server with SSL
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(smtp_username, smtp_password)  # Log in to the SMTP server with username and password
        server.sendmail(email_sender, email_recipient, msg.as_string())
        server.quit()
        print("Alert email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def log_message(message):
    """Helper function to print log messages with a timestamp."""
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def main():
    try:
        # Load known clients from the file
        known_clients = load_known_clients(known_clients_file)
        
        login()
        while True:
            log_message("Checking for new clients...")
            
            current_clients = get_wifi_clients()
            current_client_macs = {client['mac']: client for client in current_clients}

            # Find new clients
            new_clients_macs = set(current_client_macs.keys()) - known_clients

            if new_clients_macs:
                # Collect the full client info for new clients
                new_clients = [current_client_macs[mac] for mac in new_clients_macs if mac in current_client_macs]
                log_message(f"New clients detected: {new_clients_macs}")
                send_alert(new_clients)
                # Optionally, update the known clients list
                known_clients.update(new_clients_macs)
            else:
                log_message("No new clients found.")

            # Wait for a period (e.g., 5 minutes) before checking again
            time.sleep(300)

    except Exception as e:
        log_message(f"Error: {e}")

if __name__ == "__main__":
    main()

