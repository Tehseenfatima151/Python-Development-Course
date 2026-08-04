import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# ---------------------------- LOAD ENVIRONMENT VARIABLES ------------------------------- #

load_dotenv()

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")
GRAPH_ID = os.getenv("GRAPH_ID")

PIXELA_ENDPOINT = "https://pixe.la/v1/users"

headers = {
    "X-USER-TOKEN": TOKEN
}

# ---------------------------- CREATE USER (Run Only Once) ------------------------------- #

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes"
}

# Uncomment to create a new user
# response = requests.post(url=PIXELA_ENDPOINT, json=user_params)
# print(response.text)

# ---------------------------- CREATE GRAPH (Run Only Once) ------------------------------- #

graph_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs"

graph_config = {
    "id": GRAPH_ID,
    "name": "Coding Graph",
    "unit": "Hours",
    "type": "float",
    "color": "ajisai"
}

# Uncomment to create graph
# response = requests.post(
#     url=graph_endpoint,
#     json=graph_config,
#     headers=headers
# )
# print(response.text)

# ---------------------------- ADD PIXEL (POST) ------------------------------- #

today = datetime.now()

pixel_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}"

pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": "5"
}

response = requests.post(
    url=pixel_endpoint,
    json=pixel_data,
    headers=headers
)

print("POST Response:")
print(response.text)

# ---------------------------- UPDATE PIXEL (PUT) ------------------------------- #

update_endpoint = f"{PIXELA_ENDPOINT}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime('%Y%m%d')}"

new_data = {
    "quantity": "6"
}

# Uncomment to update today's data
# response = requests.put(
#     url=update_endpoint,
#     json=new_data,
#     headers=headers
# )
#
# print("PUT Response:")
# print(response.text)

# ---------------------------- DELETE PIXEL (DELETE) ------------------------------- #

# Uncomment to delete today's data
# response = requests.delete(
#     url=update_endpoint,
#     headers=headers
# )
#
# print("DELETE Response:")
# print(response.text)