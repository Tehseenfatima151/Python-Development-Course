"""
Day 94 — Personal Portfolio Project: Cookie Clicker Game Bot (GUI Automation)

Uses Selenium WebDriver to automate playing the browser game Cookie Clicker
(orteil.dashnet.org/cookieclicker) — clicking the cookie repeatedly and
automatically buying the cheapest affordable upgrade, on a timer, to
demonstrate real GUI/browser automation (not API calls, not HTML scraping —
actually driving a real browser like a human would).

Run: python cookie_clicker_bot.py
Requires: Google Chrome installed + `pip install selenium`
(Selenium 4.6+ auto-manages the matching chromedriver — no manual driver
download needed.)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

GAME_URL = "https://orteil.dashnet.org/cookieclicker/"
RUN_DURATION_SECONDS = 60          # how long the bot plays for
CLICK_INTERVAL_SECONDS = 0.1        # delay between cookie clicks
UPGRADE_CHECK_INTERVAL = 5          # how often (in cookie-clicks) to check for upgrades


def start_browser() -> webdriver.Chrome:
    """Launch Chrome and return the driver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver


def dismiss_cookie_consent(driver: webdriver.Chrome):
    """The game shows a cookie-consent banner on first load — click it away."""
    try:
        consent_button = WebDriverWait(driver, 8).until(
            EC.element_to_be_clickable((By.ID, "cmp-tc-btn-1"))
        )
        consent_button.click()
        print("✅ Dismissed cookie consent banner.")
    except TimeoutException:
        print("ℹ️  No consent banner appeared (or already dismissed).")


def click_big_cookie(driver: webdriver.Chrome):
    """Click the giant cookie in the center of the screen."""
    big_cookie = driver.find_element(By.ID, "bigCookie")
    big_cookie.click()


def get_current_cookie_count(driver: webdriver.Chrome) -> int:
    """Read the current cookie count from the page (format: '1,234 cookies')."""
    cookie_count_text = driver.find_element(By.ID, "cookies").text
    digits_only = "".join(char for char in cookie_count_text if char.isdigit())
    return int(digits_only) if digits_only else 0


def buy_cheapest_affordable_upgrade(driver: webdriver.Chrome) -> bool:
    """
    Look through the store for the first (cheapest, since the store is sorted
    by price) upgrade that isn't disabled, and buy it.
    Returns True if something was bought, False otherwise.
    """
    try:
        store_items = driver.find_elements(By.CSS_SELECTOR, "#products div.product.unlocked")
        for item in store_items:
            classes = item.get_attribute("class")
            if "enabled" in classes and "disabled" not in classes:
                item.click()
                item_id = item.get_attribute("id")
                print(f"🛒 Bought upgrade: {item_id}")
                return True
        return False
    except NoSuchElementException:
        return False


def run_bot():
    driver = start_browser()
    driver.get(GAME_URL)
    print(f"Opened {GAME_URL}")

    dismiss_cookie_consent(driver)
    time.sleep(1)  # let the game fully initialize

    start_time = time.time()
    click_count = 0

    print(f"\n🍪 Bot running for {RUN_DURATION_SECONDS} seconds...\n")

    while time.time() - start_time < RUN_DURATION_SECONDS:
        click_big_cookie(driver)
        click_count += 1

        if click_count % UPGRADE_CHECK_INTERVAL == 0:
            bought = buy_cheapest_affordable_upgrade(driver)
            if not bought:
                pass  # nothing affordable yet — keep clicking

        time.sleep(CLICK_INTERVAL_SECONDS)

    final_count = get_current_cookie_count(driver)
    elapsed = round(time.time() - start_time, 1)

    print(f"\n{'=' * 45}")
    print(f"  Bot finished after {elapsed}s")
    print(f"  Total clicks: {click_count}")
    print(f"  Final cookie count: {final_count:,}")
    print(f"{'=' * 45}")

    driver.quit()


if __name__ == "__main__":
    run_bot()
