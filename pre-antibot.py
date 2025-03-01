import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import time
from selenium.common.exceptions import TimeoutException
import datetime
import subprocess

# Define a list of user credentials
user_credentials = [
    #{"username": "bang.dive@gmail.com", "password": "PW"},
    #{"username": "tune.pulp@gmail.com", "password": "PW"},
   # {"username": "pair.sunk@gmail.com", "password": "PW"},
  #  {"username": "pull.bout@gmail.com", "password": "PW"},
 #   {"username": "goal.wipe@gmail.com", "password": "PW"},
#    {"username": "ruin.band@gmail.com", "password": "PW"},
    #{"username": "self.cent@gmail.com", "password": "PW"},
   # {"username": "plot.drag@gmail.com", "password": "PW"},
  #  {"username": "shed.grip@gmail.com", "password": "PW"},
 #   {"username": "laid.dean@gmail.com", "password": "PW"},
#    {"username": "bath.sail@gmail.com", "password": "PW"}
    {"username": "tune.pulp@gmail.com  ", "password": "PW"}
]

def sync_time_ntp():
    server = "time.windows.com"  # You can choose another NTP server if you prefer
    try:
        subprocess.run(["w32tm", "/resync", "/nowait"], check=True)
        print("Time synchronized successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to synchronize time: {e}")

        
def wait_until(target_hour, target_minute):
    now = datetime.datetime.now()
    target_time = now.replace(hour=target_hour, minute=target_minute, second=0, microsecond=0)

    if now >= target_time:
        target_time += datetime.timedelta(days=1)

    wait_time = (target_time - now).total_seconds()
    time.sleep(wait_time)


def run_selenium_script(username, password):
    # Edge WebDriver options
    options = webdriver.EdgeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-timer-throttling")
#    options.add_argument("--headless")
    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = 'eager'
    
    driver_path = r"C:\Users\archi\Desktop\ADSAS\Untitled Folder\edgedriver_win64.exe"
    driver = webdriver.Edge(options=options)
    
    
    login_url = "https://fixr.co/login"

    try:
        sync_time_ntp()
        
        # Open the login page
        driver.get(login_url)

        # Set page load timeout
        driver.set_page_load_timeout(10)

        # Wait for the cookie button to be clickable and click it
        cook_xpath = '/html/body/div[2]/section/div/div[2]/button'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, cook_xpath))
        ).click()

        # Wait for the username field to be visible and fill in the fields
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        ).send_keys(username)

        driver.find_element(By.ID, "login-password").send_keys(password)

        # Locate and click the login button
        driver.find_element(By.XPATH, "//span[text()='Sign in']").click()
        #keep the delay so it saves cookies and stays logged in
        time.sleep(2.5)
        
        driver.get("https://fixr.co/event/sketch-1503-tickets-143345295/")
               
        # Wait until 4 PM
    #    wait_until(17, 0)
        
        start_time = time.time()
        
        # Navigate to the ticket page after the wait
        driver.get("https://fixr.co/event/sketch-1503-tickets-143345295/tickets")

    
        print('ffs bro')
               

        while True:
            try:
                button_css_selector = 'div:nth-child(1) div.sc-328e2afc-2.sc-328e2afc-5.fZFdjC.lGvJu div:nth-child(2) > div > button:nth-child(3)'
                WebDriverWait(driver, 1).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, button_css_selector))
                ).click()

                break  # Exit loop if successful
            except TimeoutException:
                driver.refresh()

        print('fukcckckckfsdjflsdjfhkjdshf')

                    
                    
        button_xpath = "//button[contains(., 'Reserve')]"

        button_present = True
        while button_present:
            try:
                # Attempt to find and click the 'Reserve' button
                reserve_button = WebDriverWait(driver, 1200, poll_frequency=0.1).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                    )
                reserve_button.click()
            except TimeoutException:
                # Button isn't clickable or not found within the specified time
                print("Button not clickable or not found.")
                button_present = False
            except Exception as e:
                # Other exceptions (can be more specific if needed)
                print(f"Exception occurred: {e}")
                button_present = False
                
        print('now ?')

        if not button_present:
            print("Button no longer present.")
        else:
            print("Max attempts reached without the button disappearing.")

        
        end_time = time.time()
            
        # Locate and click the button by finding the div with the specific structure
        button_div_xpath = "//div[contains(@class, 'sc-fb16c420-3 buMFJU')]//strong[contains(text(), 'No, do not protect my tickets')]"
        button_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_div_xpath))
        )
        button_element.click()
        
        # Locate and click the button using an XPath expression
        button_xpath = '//button[contains(@class, "sc-d03939e3-0") and contains(@style, "--background: #cc013e;") and contains(span, "Continue")]'
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        ).click()
        
        time.sleep(3)

        button_xpath = "//button[contains(@class, 'sc-d03939e3-0') and contains(@style, '--background: #cc013e;') and .//span[contains(text(), 'Pay now')]]"
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        ).click()


        elapsed_time = end_time - start_time
        print(f"Thread took {elapsed_time} seconds to complete after halfway point.")
        
        time.sleep(600)

    
    finally:
        # Wait before closing the browser
        time.sleep(3000)

def execute_script(user_cred):
    try:
        run_selenium_script(user_cred['username'], user_cred['password'])
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("Thread completed its task.")

# Creating threads
threads = []
for cred in user_credentials:
    thread = threading.Thread(target=execute_script, args=(cred,))
    threads.append(thread)
    thread.start()

# Waiting for all threads to complete
for thread in threads:
    thread.join()

print("All threads have completed.") 
