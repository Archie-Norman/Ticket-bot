from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    options.add_argument("--ignore-certificate-errors")
    return webdriver.Edge(options=options)

def count_elements_every_5_minutes(url, parent_xpath):
    previous_number_of_elements = None
    
    try:
        while True:
            driver = setup_driver()  # Start a new browser session

            # Navigate to the URL
            driver.get(url)
            

            # Locate the parent div using the provided XPath
            parent_div = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, parent_xpath))
            )


            # Count the number of child elements inside the parent div
            child_elements = parent_div.find_elements(By.XPATH, "./*")
            number_of_elements = len(child_elements)

            print(f"Number of elements inside the div: {number_of_elements}")

            # Check if the number of elements has changed
            if previous_number_of_elements is not None and number_of_elements != previous_number_of_elements:
                print("Number of elements has changed. Keeping the page open.")
                time.sleep(99999999)
                break  # Exit the loop and keep the page open if the number has changed

            # Update the previous count
            previous_number_of_elements = number_of_elements

            # Close the browser after checking
            driver.quit()

            # Wait for 5 minutes (300 seconds) before the next check
            print("Waiting for 5 minutes before the next check...")
            time.sleep(300)
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
# URL and parent div's XPath
url = "https://fixr.co/organiser/timepiece"
parent_xpath = "/html/body/div[2]/div[1]/main/div[2]/div[2]"

# Start checking every 5 minutes
count_elements_every_5_minutes(url, parent_xpath)
