from seleniumbase import SB
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
from selenium.common.exceptions import StaleElementReferenceException
#import pyautogui


output_data = {
    "email": "email",
    "password": "password",
    "final_url": "https://fixr.co/event/sketch-christmas-1312-tickets-307045051/tickets",
    "ticket_time": "1"  # Update based on ticket time
}

with SB(uc=True) as sb:
    # Enable network tracking to control network traffic
    sb.driver.execute_cdp_cmd("Network.enable", {})

    # Block all unnecessary resources
    sb.driver.execute_cdp_cmd("Network.setBlockedURLs", {
        "urls": [
            # Images
            "*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg",
            
            # CSS
            "*.css",
            
            # Fonts
            "*.woff", "*.woff2", "*.ttf", "*.otf",
            
            # Videos and Audio
            "*.mp4", "*.webm", "*.ogg", "*.mp3",
            
            # JavaScript (use with caution as it might break the page functionality)
            "*.js",
            
            # Ads and Tracking Scripts
            "*.ad", "*.tracker", "https://www.google-analytics.com/*", "https://stats.g.doubleclick.net/*", 
            "https://connect.facebook.net/*", "https://platform.twitter.com/*",
            
            # AJAX/JSON/XHR
            "*.json", "*.xhr",
            
            # WebSockets (for real-time communication)
            "ws://*", "wss://*"
        ]
    })
    # Enable caching (cacheDisabled: False means caching is ON)
    sb.driver.execute_cdp_cmd('Network.setCacheDisabled', {"cacheDisabled": False})
    
    # Throttle image loading to prevent them from being prioritized
    sb.driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
        "offline": False,
        "latency": 200,  # Add a delay for image loading
        "downloadThroughput": 500 * 1024,  # Limit download speed for resources
        "uploadThroughput": 500 * 1024
    })



        # put this in the main function
    ticket_time = output_data["ticket_time"]
    index_to_click = int(ticket_time) - 1  # 0-based index for the button to click


    url = "https://fixr.co/login"

    # Open login page with reconnection
    sb.uc_open_with_reconnect(url, 4)

    # Accept cookies
    cook_xpath = '/html/body/div[2]/section/div/div[2]/button'
    WebDriverWait(sb, 10).until(EC.element_to_be_clickable((By.XPATH, cook_xpath))).uc_click()
    
    #Wait until the button is clickable and click it
#    WebDriverWait(sb, 10).until(
 #       EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-d03939e3-0.eaVubj"))
  #  ).uc_click()

    # Retry loop for entering email and clicking continue
    retries = 5  # Maximum number of retries for email
    for attempt in range(retries):
        try:
            WebDriverWait(sb, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.sc-d03939e3-0.eaVubj"))
            ).uc_click()

            # Fill in the login credentials
            email_input = sb.wait_for_element_visible("#login-email", timeout=10)
            email_input.clear()
            email_input.send_keys(output_data["email"])

            time.sleep(5)

            # Click the continue button
            continue_button = sb.wait_for_element_clickable("//button[.//span[contains(text(),'Continue')]]", timeout=10)
            continue_button.uc_click()

            # Wait for the button to disappear (indicating progress)
            sb.wait_for_element_not_visible("//button[.//span[contains(text(),'Continue')]]", timeout=5)
            print("Continue button disappeared, moving forward.")
            break  # Exit the loop if the button disappears
        except Exception as e:
            print(f"Attempt {attempt + 1}: {str(e)}, refreshing...")
            sb.refresh()  # Refresh the page
            time.sleep(2)  # Pause to let the page reload

    # Retry loop for entering password and clicking sign in
    for attempt in range(retries):
        try:
            initial_url = sb.driver.current_url

            # Fill in the password
            password_input = sb.wait_for_element_visible("#login-password", timeout=10)
            password_input.clear()
            password_input.send_keys(output_data["password"])

            # Click the sign in button
            sign_in_button = sb.wait_for_element_clickable("//span[text()='Sign in']", timeout=10)
            sign_in_button.uc_click()

            
            if sb.driver.current_url != initial_url:
                print("Logged in successfully.")
                break  # Exit the loop if sign in was successful
            else:
                print("URL did not change, refreshing...")
                sb.refresh()
                time.sleep(2)  # Pause to let the page reload

        except Exception as e:
            print(f"Attempt {attempt + 1}: {str(e)}, refreshing...")
            sb.refresh()  # Refresh the page
            time.sleep(2)  # Pause to let the page reload




    url = "https://fixr.co/event/boujee-0810-tickets-793041422/tickets"
    time.sleep(3)
    sb.uc_open_with_reconnect(url, 4)





    time.sleep(20)






    # Keep session alive to save cookies
    time.sleep(60)

