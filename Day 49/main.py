from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# -----------------------------
# Start Chrome
# -----------------------------

driver = webdriver.Chrome()

driver.get("https://www.linkedin.com/jobs/")

# Give the browser time to load
time.sleep(5)


# -----------------------------
# Manual Login
# -----------------------------

print("Please login to LinkedIn manually.")
input("After login, press ENTER here...")


# -----------------------------
# Search for Jobs
# -----------------------------

search_box = driver.find_element(
    By.CSS_SELECTOR,
    "input[placeholder*='Search job']"
)

search_box.click()
search_box.send_keys("Python Developer")
search_box.send_keys(Keys.ENTER)

time.sleep(5)


# -----------------------------
# Find Job Cards
# -----------------------------

job_cards = driver.find_elements(
    By.CSS_SELECTOR,
    "div.job-card-container"
)

print("Jobs found:", len(job_cards))


# -----------------------------
# Open Jobs
# -----------------------------

for job in job_cards:

    try:

        # Get job title
        title = job.find_element(
            By.CSS_SELECTOR,
            "a.job-card-list__title"
        ).text

        print("Job:", title)

        # Click job
        job.click()

        time.sleep(3)

        # Find Easy Apply button
        easy_apply_buttons = driver.find_elements(
            By.XPATH,
            "//button[contains(., 'Easy Apply')]"
        )

        if easy_apply_buttons:

            print("Easy Apply available!")

            easy_apply_buttons[0].click()

            time.sleep(2)

            print("Application opened.")
            print("Review the application manually.")

            input("Press ENTER to continue to next job...")

            # Close application dialog if possible
            try:
                close_button = driver.find_element(
                    By.CSS_SELECTOR,
                    "button[aria-label='Dismiss']"
                )

                close_button.click()

            except:
                pass

        else:

            print("Easy Apply not available.")

    except Exception as error:

        print("Could not process this job.")
        print(error)

    print("-" * 40)


# -----------------------------
# Finish
# -----------------------------

print("Job search automation finished!")

driver.quit()