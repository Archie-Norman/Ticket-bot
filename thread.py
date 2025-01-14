from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import time
from selenium.webdriver.common.action_chains import ActionChains


# Function to run automation on a specific emulator
def run_automation_on_emulator(emulator_name, appium_port):
    # Set up the desired capabilities for each emulator
    options = UiAutomator2Options()
    options.set_capability('platformName', 'Android')
    options.set_capability('deviceName', emulator_name)

    # Start the Appium driver for the specific emulator
    try:
        driver = webdriver.Remote(f'http://127.0.0.1:{appium_port}', options=options)
        print(f"Appium driver started successfully for {emulator_name}.")
    except Exception as e:
        print(f"Error starting Appium driver for {emulator_name}: {e}")
        return

    # Open the Fixr app
    try:
        driver.execute_script('mobile: shell', {'command': 'am start -n com.fixr.app/.MainActivity'})
        print(f"Opened Fixr app successfully on {emulator_name}.")
    except Exception as e:
        print(f"Error opening Fixr app on {emulator_name}: {e}")
        return

    # Wait for the search button and click it
    try:
        search_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Search']"))
        )
        search_button.click()
        print(f"Clicked the search button successfully on {emulator_name}.")
    except Exception as e:
        print(f"Error clicking the search button on {emulator_name}: {e}")

    # Type "timepiece" directly into the input field
    try:
        driver.execute_script('mobile: shell', {'command': 'input text "timepiece"'})
        print(f"Typed 'timepiece' into the search input successfully on {emulator_name}.")
    except Exception as e:
        print(f"Error typing in the search input on {emulator_name}: {e}")

    # Wait for the results to load
    try:
        timepiece_option = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//android.widget.TextView[@text='Timepiece']"))
        )
        timepiece_option.click()
        print("Clicked on the 'Timepiece' option successfully.")
    except Exception as e:
        print("Error clicking the 'Timepiece' option:", e)

    # Function to scroll and find an element
    def scroll_and_find(text):
        scroll_attempts = 0
        max_attempts = 10

        while scroll_attempts < max_attempts:
            try:
                # Attempt to find the specific day immediately
                day_option = driver.find_element(By.XPATH, f"//android.widget.TextView[contains(@text, '{text}')]")
                print(f"Found '{text}' option.")
                day_option.click()  # Click on it
                return True  # Return success
            except Exception:
                print(f"Scrolling down... Attempt {scroll_attempts + 1}")
                # Perform a swipe gesture to scroll down
                if scroll_attempts == 0:
                    # First scroll with longer distance
                    driver.execute_script('mobile: shell', {
                        'command': 'input swipe 540 1800 540 200 3000'  # 1080
                    })
                else:
                    # Subsequent scrolls with normal distance
                    driver.execute_script('mobile: shell', {
                        'command': 'input swipe 540 1800 540 200 1000'  # 1080
                    })

                # Increment scroll attempts
                scroll_attempts += 1

        print(f"Reached maximum scroll attempts without finding '{text}'.")
        return False  # Return failure

    # Call the scroll function to find "Monday"
    scroll_and_find("Monday")

    time.sleep(10)

    ################################################################################################

    start_time = time.time()

    start_time1 = time.time()

    def wait_for_any_clickable_element(timeout=5):
        try:
            # Wait for any clickable element (not just buttons)
            clickable_element = WebDriverWait(driver, timeout, poll_frequency=0.1).until(
                EC.presence_of_element_located((By.XPATH, "//android.widget.Button | //android.widget.TextView"))
            )
            print("At least one clickable element is visible on the page.")
            return clickable_element
        except Exception as e:
            print(f"Error while waiting for any clickable element: {e}")
            return None

    # Usage
    time.sleep(2)

    # Button bounds
    # 1080
    button_bounds = (635, 2086, 1042, 2228)
    # 720
    # button_bounds = (424, 1391, 695, 1485)
    center_x = (button_bounds[0] + button_bounds[2]) // 2
    center_y = (button_bounds[1] + button_bounds[3]) // 2


    try:
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)  # Move to coordinates
        actions.w3c_actions.pointer_action.click()  # Perform the tap
        actions.perform()
        print("Clicked the 'Tickets' button using W3C Actions.")
    except Exception as e:
        print("Error clicking the 'Tickets' button using W3C Actions:", e)

    end_time1 = time.time()

    ################################################################################################

    start_time2 = time.time()
 
    # Wait for a moment to ensure the page is loaded
    wait_for_any_clickable_element()

    try:
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(919, 758)  # Move to coordinates
        actions.w3c_actions.pointer_action.click()  # Perform the tap
        actions.perform()
        print("Clicked the 'add' button using W3C Actions.")
    except Exception as e:
        print("Error clicking the 'add' button using W3C Actions:", e)

    end_time2 = time.time()

    ################################################################################################

    start_time3 = time.time()

    wait_for_any_clickable_element()



    # Perform the tap using W3C Actions
    try:
        actions = ActionChains(driver)
        actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)  # Move to coordinates
        actions.w3c_actions.pointer_action.click()  # Perform the tap
        actions.perform()
        print("Clicked the 'View Cart' button using W3C Actions.")
    except Exception as e:
        print("Error clicking the 'View Cart' button using W3C Actions:", e)

    end_time3 = time.time()

    ################################################################################################
    ######################
    # still need to test #
    ######################

    start_time4 = time.time()

    # Function to check if the "Order summary" element is visible
    def is_order_summary_visible():
        try:
            # Check for the "Order summary" text element
            element = driver.find_element(By.XPATH, "//android.view.View[@text='Order summary']")
            return element.is_displayed()  # Return True if displayed
        except Exception:
            return False  # If the element is not found or not visible, return False

    # Click the "Reserve" button until the "Order summary" is no longer visible
    max_clicks = 10  # Optional limit to avoid infinite loops
    clicks = 0

    while clicks < max_clicks:
        try:
            # Perform the click action at the specified coordinates
            actions = ActionChains(driver)
            actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)  # Move to coordinates
            actions.w3c_actions.pointer_action.click()  # Perform the tap
            actions.perform()
            print("Clicked the 'Reserve' button using W3C Actions.")

            # Wait for a brief moment to allow for any potential UI updates
            time.sleep(1)

            # Check if the "Order summary" element is still visible
            if not is_order_summary_visible():
                print("Order summary is no longer visible. Page has changed!")
                break  # Exit the loop if the page has changed

            clicks += 1

        except Exception as e:
            print("Error clicking the 'View Cart' button using W3C Actions:", e)
            break  # Exit the loop if an error occurs

    if clicks >= max_clicks:
        print("Reached the maximum number of clicks without page change.")

    end_time4 = time.time()
    end_time = time.time()

    # Clean up and close the app
    driver.quit()
    print("Driver closed successfully.")

    # Elapsed time for both steps
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    elapsed_time = end_time1 - start_time1
    print(f"ticket time: {elapsed_time:.2f} seconds")

    elapsed_time = end_time2 - start_time2
    print(f"plus button time: {elapsed_time:.2f} seconds")

    elapsed_time = end_time3 - start_time3
    print(f"view cart time: {elapsed_time:.2f} seconds")

    elapsed_time = end_time4 - start_time4
    print(f"res time: {elapsed_time:.2f} seconds")

    print(f"Driver closed successfully for {emulator_name}.")

# Run automation on two emulators concurrently using threading
emulator_1_name = 'emulator-5554'
emulator_1_port = 4723

# Create threads to run automation on both emulators
thread_1 = threading.Thread(target=run_automation_on_emulator, args=(emulator_1_name, emulator_1_port))

# Start both threads
thread_1.start()

# Wait for both threads to finish
thread_1.join()

print("Automation completed on both emulators.")
