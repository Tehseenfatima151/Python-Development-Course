from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# -----------------------------
# Instagram Selenium Demo
# -----------------------------

USERNAME = "your_username"
PASSWORD = "your_password"
TARGET_PROFILE = "instagram"

options = Options()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

try:
    # Open Instagram
    driver.get("https://www.instagram.com/")

    print("Instagram opened.")

    # Wait for page to load
    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    print("Page loaded successfully.")

    # Open target profile
    driver.get(f"https://www.instagram.com/{TARGET_PROFILE}/")

    wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "body")
        )
    )

    print(f"Target profile opened: @{TARGET_PROFILE}")

    # Keep browser open for inspection
    time.sleep(10)

except Exception as e:
    print("An error occurred:")
    print(e)

finally:
    driver.quit()
    print("Browser closed.")