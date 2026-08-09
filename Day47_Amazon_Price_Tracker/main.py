import os
import smtplib
import requests

from bs4 import BeautifulSoup
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------
# Settings
# -------------------------------------------------

PRODUCT_URL = os.getenv("PRODUCT_URL")
TARGET_PRICE = float(os.getenv("TARGET_PRICE", "100"))

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

HEADERS = {
    "User-Agent": os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

# -------------------------------------------------
# Check settings
# -------------------------------------------------

if not PRODUCT_URL:
    print("Please add PRODUCT_URL to your .env file.")
    exit()

if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not TO_EMAIL:
    print("Please add EMAIL_ADDRESS, EMAIL_PASSWORD and TO_EMAIL to .env.")
    exit()

# -------------------------------------------------
# Get Amazon product page
# -------------------------------------------------

print("Checking Amazon product price...")

response = requests.get(
    PRODUCT_URL,
    headers=HEADERS,
    timeout=20
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

# -------------------------------------------------
# Find product title
# -------------------------------------------------

title_element = soup.select_one("#productTitle")

if title_element:
    product_title = title_element.get_text(strip=True)
else:
    product_title = "Amazon Product"

# -------------------------------------------------
# Find product price
# -------------------------------------------------

price_element = (
    soup.select_one(".a-price .a-offscreen")
    or soup.select_one("#corePrice_feature_div .a-offscreen")
    or soup.select_one("#priceblock_ourprice")
    or soup.select_one("#priceblock_dealprice")
)

if not price_element:
    print("Could not find the price.")
    print("Amazon may have changed the page structure or blocked the request.")
    exit()

price_text = price_element.get_text(strip=True)

# Remove currency symbols and commas.
clean_price = (
    price_text
    .replace("PKR", "")
    .replace("$", "")
    .replace("£", "")
    .replace("€", "")
    .replace(",", "")
    .strip()
)

try:
    current_price = float(clean_price)
except ValueError:
    print("Could not convert the Amazon price to a number.")
    print("Price found:", price_text)
    exit()

print(f"Product: {product_title}")
print(f"Current price: {current_price}")
print(f"Target price: {TARGET_PRICE}")

# -------------------------------------------------
# Send email when price is low enough
# -------------------------------------------------

if current_price <= TARGET_PRICE:

    message = EmailMessage()
    message["Subject"] = "Amazon Price Alert! 🎉"
    message["From"] = EMAIL_ADDRESS
    message["To"] = TO_EMAIL

    message.set_content(
        f"The price of the product has dropped!\n\n"
        f"Product: {product_title}\n"
        f"Current Price: {current_price}\n"
        f"Your Target Price: {TARGET_PRICE}\n\n"
        f"Buy it here:\n{PRODUCT_URL}"
    )

    # Gmail SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        connection.send_message(message)

    print("\n🎉 Price is below your target!")
    print("Email alert sent successfully.")

else:
    print("\nNo alert sent.")
    print("The product is still above your target price.")
