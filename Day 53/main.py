from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --------------------------------
# Google Form
# --------------------------------

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdaLzzKF1VRMVXM-3ax8IM5o-n-K9JNBP4emO5Gyaf054xb3g/viewform"


# --------------------------------
# Sample Property Data
# --------------------------------

properties = [
    {
        "address": "123 Main Street",
        "price": "$2,500",
        "link": "https://example.com/property1"
    },
    {
        "address": "456 Green Avenue",
        "price": "$3,000",
        "link": "https://example.com/property2"
    },
    {
        "address": "789 Lake Road",
        "price": "$3,500",
        "link": "https://example.com/property3"
    }
]


# --------------------------------
# Start Chrome
# --------------------------------

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 15)


try:

    for property_data in properties:

        print("\nOpening Google Form...")

        driver.get(FORM_URL)

        # Wait for form to load
        wait.until(
            EC.presence_of_element_located(
                (By.TAG_NAME, "form")
            )
        )

        # Find all text inputs
        inputs = wait.until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "input[type='text']")
            )
        )

        print("Form loaded.")

        # --------------------------------
        # Fill Address
        # --------------------------------

        inputs[0].send_keys(property_data["address"])

        # --------------------------------
        # Fill Price
        # --------------------------------

        inputs[1].send_keys(property_data["price"])

        # --------------------------------
        # Fill Link
        # --------------------------------

        inputs[2].send_keys(property_data["link"])

        print("Data entered:")
        print("Address:", property_data["address"])
        print("Price:", property_data["price"])
        print("Link:", property_data["link"])

        # --------------------------------
        # Submit Form
        # --------------------------------

        submit_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//span[contains(text(),'Submit')]"
                )
            )
        )

        submit_button.click()

        print("Form submitted successfully! ✅")


    print("\nAll properties processed! 🎉")

    input("\nPress ENTER to close the browser...")


except Exception as error:

    print("\nSomething went wrong ❌")
    print(error)

    input("\nPress ENTER to close the browser...")


finally:

    driver.quit()
    print("Browser closed.")