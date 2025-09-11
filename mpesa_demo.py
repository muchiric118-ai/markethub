import requests
from requests.auth import HTTPBasicAuth

consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()['access_token']

def register_urls():
    access_token = get_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    payload = {
        "ShortCode": "600981",
        "ResponseType": "Completed",
        "ConfirmationURL": "https://random-id.ngrok.io/confirm",
        "ValidationURL": "https://random-id.ngrok.io/validate"
    }

    response = requests.post(url, headers=headers, json=payload)
    print(response.json())

if __name__ == "__main__":
    register_urls()
