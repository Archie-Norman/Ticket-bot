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

    # Button bounds
    # 1080
    button_bounds = (635, 2086, 1042, 2228)
    # 720
    # button_bounds = (424, 1391, 695, 1485)
    center_x = (button_bounds[0] + button_bounds[2]) // 2
    center_y = (button_bounds[1] + button_bounds[3]) // 2

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



    ################################################################################################

    start_time = time.time()

    start_time1 = time.time()

# Initialize a flag to control the loop
    element_visible = False
    max_clicks = 100  # Set a limit to avoid infinite loops
    clicks = 0
    element_id = "00000000-0000-00d9-ffff-ffff00000471"  # The element ID to check for

    print("Starting the clicking loop...")

    # Continue clicking the button until the element with the given ID is no longer visible or max_clicks is reached
    while not element_visible and clicks < max_clicks:
        print(f"Click attempt {clicks + 1}")
        try:
            # Perform the click action at the specified coordinates
            actions = ActionChains(driver)
            actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)  # Move to coordinates
            actions.w3c_actions.pointer_action.click()  # Perform the tap
            actions.perform()
            print("Clicked the 'add' button using W3C Actions.")

            # Wait for the element with the specified ID to disappear
            try:
                WebDriverWait(driver, 5).until_not(
                    EC.presence_of_element_located((By.ID, element_id))
                )
                print(f"Element with ID '{element_id}' is no longer visible.")
                element_visible = True  # Exit the loop when the element is no longer present
            except Exception as e:
                print(f"Element with ID '{element_id}' is still visible. Clicking again...")

            clicks += 1  # Increment the click count

        except Exception as e:
            print("Error clicking the 'add' button using W3C Actions:", e)
            break  # Exit the loop if there is an unexpected error

    if not element_visible:
        print(f"Successfully detected that the element with ID '{element_id}' is no longer visible.")
    else:
        print(f"Reached the maximum number of clicks ({max_clicks}) without the element disappearing.")


    end_time1 = time.time()

    ################################################################################################

    start_time2 = time.time()

#    text_vis = False
    
 #   while text_vis == False:  # Use '==' for comparison
  #      try:
   #         found = driver.find_element(By.XPATH, "//android.view.View[contains(@text, 'Individual tickets')]")
    #        print("Found Individual tickets text")
     #       text_vis = True  # Set to True to exit the loop
      #  except Exception:
       #     print("Individual tickets not found")
    

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

    #check if the "Individual tickets" element is visible

# Initialize flag to control the loop
    cart_vis = False

    # First, wait until the "£6.00" element is visible
    while not cart_vis:
        try:
            found = driver.find_element(By.XPATH, "//android.view.View[contains(@text, '£6.00')]")
            print("Found '£6.00' text")
            cart_vis = True  # Exit the loop when "£6.00" is found
        except Exception:
            print("'£6.00' text not found, retrying...")

    # Now, click repeatedly until "Summary" is found
    order_summary_vis = False
    max_clicks = 100  # Optional: Set a maximum number of clicks to avoid infinite loops
    clicks = 0

    while not order_summary_vis and clicks < max_clicks:
        try:
            # Perform the tap using W3C Actions
            actions = ActionChains(driver)
            actions.w3c_actions.pointer_action.move_to_location(center_x, center_y)  # Move to coordinates
            actions.w3c_actions.pointer_action.click()  # Perform the tap
            actions.perform()
            print(f"Clicked the 'View Cart' button using W3C Actions. Attempt {clicks + 1}")

            # Check immediately if the "Summary" is visible
            try:
                found = driver.find_element(By.XPATH, "//android.view.View[contains(@text, 'Summary')]")
                print("Found 'Summary' text")
                order_summary_vis = True  # Exit the loop if found
            except Exception:
                # No delay, keep clicking until it's found
                pass

            clicks += 1  # Increment click count

        except Exception as e:
            print("Error clicking the 'View Cart' button using W3C Actions:", e)
            break  # Exit if there's an unexpected error

    if order_summary_vis:
        print("Successfully found 'Summary' text and stopped clicking.")
    else:
        print(f"Stopped after {clicks} clicks without finding 'Summary'.")

    end_time3 = time.time()
    
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
    print(f"view cart and reserve time: {elapsed_time:.2f} seconds")

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
