from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# -----------------------------
# Start Chrome
# -----------------------------

driver = webdriver.Chrome()

driver.get("https://tinder.com/")

print("Tinder opened!")

# Wait for page to load
time.sleep(5)


# -----------------------------
# Manual Login
# -----------------------------

print("Please login to Tinder manually.")
input("After login, press ENTER here...")


# -----------------------------
# Swiping Bot
# -----------------------------

print("Swiping bot started...")

for i in range(20):

    try:

        # Find Like button
        like_button = driver.find_element(
            By.XPATH,
            "//button[@aria-label='Like']"
        )

        # Click Like
        like_button.click()

        print(f"Liked profile {i + 1}")

        # Wait before next swipe
        time.sleep(2)

    except Exception:

        print("Like button not found.")

        # Try to find Dislike button
        try:

            dislike_button = driver.find_element(
                By.XPATH,
                "//button[@aria-label='Nope']"
            )

            dislike_button.click()

            print("Swiped left.")

        except:

            print("Swipe buttons not found.")

    time.sleep(1)


# -----------------------------
# Finish
# -----------------------------

print("Swiping bot finished!")

driver.quit()