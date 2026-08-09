from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# Start Chrome
driver = webdriver.Chrome()

# Open Cookie Clicker Classic
driver.get("https://orteil.dashnet.org/cookieclicker/v10466/")


# Wait for cookie to appear
cookie = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (By.ID, "bigCookie")
    )
)

print("Cookie found!")
print("Bot started...")


# Run bot for 5 minutes
start_time = time.time()

while time.time() - start_time < 300:

    # Click cookie
    for _ in range(20):
        cookie.click()

    # Find available products
    products = driver.find_elements(
        By.CSS_SELECTOR,
        "#products .product.unlocked.enabled"
    )

    # Buy available product
    if products:
        products[-1].click()

    time.sleep(0.1)


print("Bot finished!")

driver.quit()