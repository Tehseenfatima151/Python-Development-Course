import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

TWITTER_EMAIL = os.environ.get("TWITTER_EMAIL")
TWITTER_PASSWORD = os.environ.get("TWITTER_PASSWORD")
COMPLAINT_TEXT = "Hey @Airline, my flight was delayed 3 hours with zero communication. #CustomerService"


def post_complaint_tweet():
    """Launches a browser, logs into Twitter/X, and posts a pre-written complaint tweet."""

    if not TWITTER_EMAIL or not TWITTER_PASSWORD:
        print("Missing TWITTER_EMAIL or TWITTER_PASSWORD in your .env file.")
        return

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Open Twitter/X login page
        driver.get("https://twitter.com/login")

        # Step 2: Enter email/username
        email_field = wait.until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        email_field.send_keys(TWITTER_EMAIL)
        email_field.submit()

        # Step 3: Enter password
        password_field = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.submit()

        # Step 4: Wait for the home timeline / tweet box to load
        tweet_box = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-testid='tweetTextarea_0']")
            )
        )

        # Step 5: Compose the complaint tweet
        tweet_box.click()
        tweet_box.send_keys(COMPLAINT_TEXT)
        time.sleep(1)

        # Step 6: Post the tweet
        tweet_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "[data-testid='tweetButton']")
            )
        )
        tweet_button.click()
        time.sleep(2)

        print("Complaint tweet posted successfully!")

    except Exception as error:
        print(f"Something went wrong: {error}")

    finally:
        driver.quit()


if __name__ == "__main__":
    post_complaint_tweet()