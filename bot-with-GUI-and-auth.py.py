import requests
import datetime
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet, InvalidToken
import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import json
import re
import os
import time
from datetime import datetime
import hashlib
import platform
import sys
import threading

# Function to generate and store AES key
def generate_aes_key():
    key = Fernet.generate_key()
    with open("aes_key.txt", "wb") as key_file:
        key_file.write(key)
    return key

# Function to retrieve the stored AES key
def get_stored_aes_key():
    try:
        with open("aes_key.txt", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        return generate_aes_key()

# Function to encrypt data using AES
def aes_encrypt(data, key):
    cipher = Fernet(key)
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data using AES
def aes_decrypt(encrypted_data, key):
    cipher = Fernet(key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to get hardware information
def get_hardware_info():
    processor = platform.processor()
    platform_info = platform.platform()
    hardware_info = f"{processor}-{platform_info}"
    return hashlib.sha256(hardware_info.encode()).hexdigest()

# Function to check if key is accepted
def is_key_accepted():
    try:
        with open("activation_status.txt", "rb") as file:
            lines = file.read().splitlines()
            file.close()  # Close the file before attempting to delete it
            if len(lines) == 3:
                encrypted_status, stored_hw, encrypted_expiry_date = lines
                current_hw = get_hardware_info()
                aes_key = get_stored_aes_key()
                decrypted_status = aes_decrypt(encrypted_status, aes_key)
                expiry_date_str = aes_decrypt(encrypted_expiry_date, aes_key)
                
                if decrypted_status == "accepted" and stored_hw.decode() == current_hw:
                    expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d')
                    if datetime.now() < expiry_date:
                        days_left = (expiry_date - datetime.now()).days
                        return True, expiry_date_str, days_left
                    else:
                        os.remove("activation_status.txt")
                        return False, None, None
            return False, None, None
    except (FileNotFoundError, InvalidToken):
        return False, None, None

# Function to mark key as accepted
def mark_key_accepted(expiry_date):
    with open("activation_status.txt", "wb") as file:
        key_status = "accepted"
        aes_key = get_stored_aes_key()
        encrypted_status = aes_encrypt(key_status, aes_key)
        encrypted_expiry_date = aes_encrypt(expiry_date, aes_key)
        hardware_info = get_hardware_info()
        file.write(encrypted_status + b"\n" + hardware_info.encode() + b"\n" + encrypted_expiry_date)

# Function to activate product
def activate_product():
    product_key = entry_product_key.get()
    if product_key:
        url = "https://leading-kind-panther.ngrok-free.app/activate"
        payload = {
            "product_key": product_key
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            response = requests.post(url, json=payload)
            data = response.json()
            
            if response.status_code == 200:
                expiry_date = data.get("expiry_date")
                mark_key_accepted(expiry_date)
                global key_validated
                key_validated = True
                root.quit()
                root.destroy()
            else:
                messagebox.showerror("Activation Failed", "Invalid product key. Please try again.")
        except (ValueError, requests.RequestException) as e:
            messagebox.showerror("Activation Failed", f"An error occurred: {e}")

def on_closing():
    if not key_validated:
        root.destroy()
        sys.exit()

# Create main window for activation
def create_activation_window():
    global root, entry_product_key, key_validated
    root = tk.Tk()
    root.title("Product Activation")

    key_validated = False

    label_product_key = tk.Label(root, text="Product Key:", font=("Helvetica", 12))
    label_product_key.grid(row=0, column=0, pady=(10, 5), padx=(10, 5), sticky="w")
    entry_product_key = tk.Entry(root, font=("Helvetica", 12))
    entry_product_key.grid(row=0, column=1, pady=(10, 5), padx=(5, 10), sticky="ew")

    button_activate = tk.Button(root, text="Activate", command=activate_product, font=("Helvetica", 12))
    button_activate.grid(row=1, column=0, columnspan=2, pady=(5, 10), padx=(10, 10), sticky="ew")

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

# Create form for account and ticket details
def create_form():
    def on_submit():
        nonlocal email, password, website, ticket_time, selected_date, selected_interval

        email_error_label.config(text="")
        website_error_label.config(text="")
        ticket_time_error_label.config(text="")

        email = email_entry.get()
        password = password_entry.get()
        website = website_entry.get()
        ticket_time = ticket_time_entry.get() if ticket_time_entry.winfo_ismapped() else None
        selected_interval = interval_var.get() if interval_menu.winfo_ismapped() else None
        selected_date = date_entry.get_date() if option_var.get() == 2 else None

        error_messages = []

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            error_messages.append("Invalid email format")

        if option_var.get() == 1:
            if not (website.startswith("http://") or website.startswith("https://")):
                error_messages.append("Invalid website URL format")
            elif not website.endswith("/tickets"):
                error_messages.append("Website URL must end with '/tickets'")


        if ticket_time is not None:
            try:
                ticket_time_int = int(ticket_time)
                if ticket_time_int <= 0:
                    raise ValueError
            except ValueError:
                error_messages.append("Ticket time must be a positive number")

        if not website and not selected_date:
            error_messages.append("You must either pick a date or enter a link")

        if error_messages:
            for message in error_messages:
                if "email" in message:
                    email_error_label.config(text=message, fg="red")
                elif "website" in message:
                    website_error_label.config(text=message, fg="red")
                elif "Ticket" in message:
                    ticket_time_error_label.config(text=message, fg="red")
                else:
                    messagebox.showerror("Error", message)
            return

        if remember_var.get() == 1:
            with open("credentials.json", "w") as file:
                json.dump({"email": email, "password": password}, file)

        messagebox.showinfo("Submission Successful", "Your details have been submitted successfully!")
        root.quit()

    def toggle_input_fields():
        if option_var.get() == 1:
            website_entry.config(state=tk.NORMAL)
            date_entry.config(state=tk.DISABLED)
        else:
            website_entry.config(state=tk.DISABLED)
            date_entry.config(state=tk.NORMAL)

    def toggle_time_fields():
        if ticket_time_var.get() == 1:
            ticket_time_entry.grid()
            interval_menu.grid_remove()
        else:
            ticket_time_entry.grid_remove()
            interval_menu.grid()

    root = tk.Tk()
    root.title("Account and Ticket details")
    root.geometry('650x700')

    bg_color = "#f8f9fa"
    entry_bg_color = "#ffffff"
    fg_color = "#495057"
    font = ('Helvetica', 12)
    small_font = ('Helvetica', 10)

    frame = tk.Frame(root, padx=20, pady=20, bg=bg_color, bd=0)
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Email", font=font, bg=bg_color, fg=fg_color).grid(row=0, column=0, sticky='w', pady=(0, 10))
    email_entry = tk.Entry(frame, font=font, bg=entry_bg_color, fg=fg_color, bd=2, relief=tk.FLAT)
    email_entry.grid(row=0, column=1, padx=10, pady=(0, 10))
    email_error_label = tk.Label(frame, text="", font=small_font, bg=bg_color, fg="red")
    email_error_label.grid(row=0, column=2, sticky='w', pady=(0, 10))

    tk.Label(frame, text="Password", font=font, bg=bg_color, fg=fg_color).grid(row=1, column=0, sticky='w', pady=(0, 10))
    password_entry = tk.Entry(frame, show="*", font=font, bg=entry_bg_color, fg=fg_color, bd=2, relief=tk.FLAT)
    password_entry.grid(row=1, column=1, padx=10, pady=(0, 10))

    def toggle_password_visibility():
        current_state = password_entry.cget("show")
        new_state = "" if current_state else "*"
        password_entry.config(show=new_state)

    show_password_button = tk.Button(frame, text="Show Password", command=toggle_password_visibility, font=small_font)
    show_password_button.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="w")

    remember_var = tk.IntVar()
    tk.Checkbutton(frame, text="Remember me", variable=remember_var, font=small_font, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, bd=0).grid(row=2, column=1, sticky='w', padx=10, pady=(0, 20))

    tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN, bg="#e0e0e0").grid(row=3, column=0, columnspan=3, pady=20, sticky="we")

    tk.Label(frame, text="Pick a Date (TP Tickets Only) or Enter a Link", font=font, bg=bg_color, fg=fg_color).grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 10))

    option_var = tk.IntVar(value=1)
    tk.Radiobutton(frame, text="Enter a Link", variable=option_var, value=1, command=toggle_input_fields, font=small_font, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, bd=0).grid(row=5, column=0, sticky='w', padx=10, pady=(0, 10))
    tk.Radiobutton(frame, text="Pick a Date", variable=option_var, value=2, command=toggle_input_fields, font=small_font, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, bd=0).grid(row=5, column=1, sticky='w', padx=10, pady=(0, 10))

    tk.Label(frame, text="Select Date", font=font, bg=bg_color, fg=fg_color).grid(row=6, column=0, sticky='w', pady=(0, 10))
    date_entry = DateEntry(frame, font=font, bg=entry_bg_color, fg=fg_color, bd=2, relief=tk.FLAT, date_pattern='yyyy-mm-dd')
    date_entry.grid(row=6, column=1, padx=10, pady=(0, 10))
    date_entry.config(state=tk.DISABLED)

    tk.Label(frame, text="Website URL", font=font, bg=bg_color, fg=fg_color).grid(row=7, column=0, sticky='w', pady=(0, 10))
    website_entry = tk.Entry(frame, font=font, bg=entry_bg_color, fg=fg_color, bd=2, relief=tk.FLAT)
    website_entry.grid(row=7, column=1, padx=10, pady=(0, 10))
    website_error_label = tk.Label(frame, text="", font=small_font, bg=bg_color, fg="red")
    website_error_label.grid(row=7, column=2, sticky='w', pady=(0, 10))

    tk.Label(frame, text="Example:", font=font, bg=bg_color, fg=fg_color).grid(row=8, column=0, columnspan=2, sticky='w', pady=(0, 10))
    example_text = tk.Text(frame, height=1, width=40, font=small_font, wrap=tk.WORD, bd=0, bg=root.cget('bg'))
    example_text.grid(row=9, column=0, columnspan=2, pady=(0, 20))
    example_text.tag_configure('highlight', font=(small_font[0], small_font[1], 'bold'), foreground='red')
    example_text.insert(tk.END, "https://fixr.co/event/saturday/")
    example_text.insert(tk.END, "tickets", 'highlight')
    example_text.config(state='disabled')

    tk.Frame(frame, height=2, bd=1, relief=tk.SUNKEN, bg="#e0e0e0").grid(row=10, column=0, columnspan=3, pady=20, sticky="we")

    tk.Label(frame, text="Choose Ticket Time or Interval(TP Tickets Only)", font=font, bg=bg_color, fg=fg_color).grid(row=11, column=0, columnspan=2, sticky='w', pady=(0, 10))

    ticket_time_var = tk.IntVar(value=1)
    tk.Radiobutton(frame, text="Enter Ticket Time", variable=ticket_time_var, value=1, command=toggle_time_fields, font=small_font, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, bd=0).grid(row=12, column=0, sticky='w', padx=10, pady=(0, 10))
    tk.Radiobutton(frame, text="Select Interval", variable=ticket_time_var, value=2, command=toggle_time_fields, font=small_font, bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color, bd=0).grid(row=12, column=1, sticky='w', padx=10, pady=(0, 10))

    tk.Label(frame, text="Ticket Time", font=font, bg=bg_color, fg=fg_color).grid(row=13, column=0, sticky='w', pady=(0, 10))
    ticket_time_entry = tk.Entry(frame, font=font, bg=entry_bg_color, fg=fg_color, bd=2, relief=tk.FLAT)
    ticket_time_entry.grid(row=13, column=1, padx=10, pady=(0, 10))
    ticket_time_error_label = tk.Label(frame, text="", font=small_font, bg=bg_color, fg="red")
    ticket_time_error_label.grid(row=13, column=2, sticky='w', pady=(0, 10))

    tk.Label(frame, text="Select Interval", font=font, bg=bg_color, fg=fg_color).grid(row=14, column=0, sticky='w', pady=(0, 10))
    intervals = ["7:00", "7:30", "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", "12:00"]
    interval_var = tk.StringVar(value=intervals[0])
    interval_menu = tk.OptionMenu(frame, interval_var, *intervals)
    interval_menu.grid(row=14, column=1, padx=10, pady=(0, 10))
    interval_menu.grid_remove()

    def get_expiry_info():
        accepted, expiry_date_str, days_left = is_key_accepted()
        if accepted:
            return f"Expiry Date: {expiry_date_str} ({days_left} days left)"
        else:
            return "No active subscription"

    expiry_info = get_expiry_info()

    if os.path.exists("credentials.json"):
        with open("credentials.json", "r") as file:
            credentials = json.load(file)
            email_entry.insert(0, credentials.get("email", ""))
            password_entry.insert(0, credentials.get("password", ""))

    email, password, website, ticket_time, selected_date, selected_interval = None, None, None, None, None, None

    submit_button = tk.Button(frame, text="Submit", command=on_submit, font=font)
    submit_button.grid(row=15, column=0, columnspan=3, pady=20, sticky="ew")

    expiry_label = tk.Label(frame, text=expiry_info, font=small_font, bg=bg_color, fg="red")
    expiry_label.grid(row=16, column=0, columnspan=3, sticky='w', padx=10, pady=(0, 20))

    root.mainloop()
    root.destroy()

    return email, password, website, ticket_time, selected_date, selected_interval


# Check if key has already been accepted
if is_key_accepted()[0]:
    print("Key already accepted.")
else:
    # Create the main window
    root = tk.Tk()
    root.title("Product Activation")

    key_validated = False

    # Create and pack labels and entry widget for the product key
    label_product_key = tk.Label(root, text="Product Key:", font=("Helvetica", 12))
    label_product_key.grid(row=0, column=0, pady=(10, 5), padx=(10, 5), sticky="w")
    entry_product_key = tk.Entry(root, font=("Helvetica", 12))
    entry_product_key.grid(row=0, column=1, pady=(10, 5), padx=(5, 10), sticky="ew")

    # Create and pack activate button
    button_activate = tk.Button(root, text="Activate", command=activate_product, font=("Helvetica", 12))
    button_activate.grid(row=1, column=0, columnspan=2, pady=(5, 10), padx=(10, 10), sticky="ew")

    # Set padding and resizing behavior
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.resizable(False, False)

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Run the Tkinter event loop
    root.mainloop()

print("hello world")


# Convert date to formatted string
def convert_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%A %d %B %Y').upper()
    return formatted_date

# Search for a specific date on the website
def search_for_date(driver, formatted_date, url):
    found = False
    while not found:
        driver.get(url)
        date_elements = driver.find_elements(By.CSS_SELECTOR, "div.sc-ebb15909-0.eKFHCO > main > div.sc-6a27bf4a-0.qOmWz > div.sc-df7c1e03-0.dQKvOn > div > a > div > div > div > div.sc-72238a8b-2.jrmrur > div.sc-72238a8b-3.JzjJ > span")
        for element in date_elements:
            text = element.text.strip()
            if text == formatted_date:
                parent_element = element.find_element(By.XPATH, '..')
                parent_element.click()
                found = True
                return driver.current_url + '/tickets'
        if not found:
            time.sleep(300)  # Wait for 5 minutes before retrying

# Create a popup GUI window
def create_gui_window(date_str):
    window = tk.Tk()
    window.title("Popup Window")
    window.geometry("400x100")
    label = tk.Label(window, text=f"Looking for {date_str}.\nWindow will close once found.")
    label.pack(expand=True)
    window.update()
    return window

def format_time(time_str):
    """
    If the time is on the hour (e.g., '14:00'), this function removes the ':00'.
    Otherwise, it returns the time as is.

    Args:
    time_str (str): Time in 'HH:MM' format.

    Returns:
    str: Formatted time.
    """
    if time_str.endswith(':00'):
        return time_str[:-3]  # Remove the ':00'
    return time_str

# Main function
def main():
    email, password, website, ticket_time, selected_date, selected_interval = create_form()  # Ensure create_form() is defined elsewhere

    def create_webdriver_options():
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--headless")
        options.add_argument("--disable-extensions")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-background-timer-throttling")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        return options

    def display_gui_window(message):
        window = create_gui_window(message)  # Ensure create_gui_window() is defined elsewhere
        return window

    final_url = website
    options = create_webdriver_options()

    if selected_date:
        formatted_date = convert_date(selected_date.strftime('%Y-%m-%d'))  # Ensure convert_date() is defined elsewhere
        window = display_gui_window(formatted_date)

        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            url = 'https://fixr.co/organiser/timepiece'
            tickets_url = search_for_date(driver, formatted_date, url)  # Ensure search_for_date() is defined elsewhere
            driver.quit()
            
            if tickets_url:
                final_url = tickets_url
        except Exception as e:
            print(f"Error during web scraping for date: {e}")
        finally:
            window.destroy()

    if selected_interval:
        window = display_gui_window(selected_interval)

        try:
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
            
            print(tickets_url)
            print(final_url)
            print(selected_interval)
            formatted_interval = format_time(selected_interval)  # Ensure format_time() is defined elsewhere
            print(formatted_interval)

            driver.get(f"{tickets_url}/tickets")

            elements = driver.find_elements(By.CLASS_NAME, "sc-131cfbab-0.gEAfja")
            target_element = None
            index = -1
            for i, element in enumerate(elements):
                if f"Entry strictly between {formatted_interval}" in element.text:
                    target_element = element
                    index = i
                    break

            if target_element:
                print(f"Element found at position: {index + 1}")
            else:
                print("Element with the specific text not found.")

        except Exception as e:
            print(f"Error during web scraping for interval: {e}")
        finally:
            driver.quit()
            window.destroy()

        if index != -1:
            ticket_time = index + 1 

    output_data = {
        "final_url": final_url,
        "email": email,
        "password": password,
        "ticket_time": ticket_time
    }

    return output_data


if __name__ == "__main__":
    output_data = main()

    print(output_data)

    # Now you can use output_data dictionary to access the results

    # Edge WebDriver options
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-background-timer-throttling")
    # Disable images
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.page_load_strategy = 'eager'

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    login_url = "https://fixr.co/login"

    try:
        # Open the login page
        driver.get(login_url)

        # Set page load timeout
        driver.set_page_load_timeout(10)

        # Wait for the cookie button to be clickable and click it
        cook_xpath = '/html/body/div[2]/section/div/div[2]/button'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cook_xpath))).click()

        # Wait for the username field to be visible and fill in the fields
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-email"))).send_keys(output_data["email"])
        driver.find_element(By.ID, "login-password").send_keys(output_data["password"])

        # Locate and click the login button
        driver.find_element(By.XPATH, "//span[text()='Sign in']").click()
        # Keep the delay so it saves cookies and stays logged in
        time.sleep(2.5)

        start_time = time.time()

        # Put the ticket page here
        driver.get(output_data["final_url"])

        # Wait for the ticket list items to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid^='ticket-list-item-']"))
        )

        # Specify which button you want to click (0-based index)
        index_to_click = int(output_data["ticket_time"]) - 1  # Change this index based on which button you want to click

        # Count the number of buttons
        while True:
            try:
                # Find all the elements with the specified class
                elements = driver.find_elements(By.CSS_SELECTOR, 'div.sc-131cfbab-0.gEAfja')
                element_count = len(elements)
                # Check if the number of elements is sufficient
                if element_count > index_to_click:
                    # Find the nth element
                    target_element = elements[index_to_click]
                    # Find the button within the nth element
                    button = target_element.find_element(By.CSS_SELECTOR, 'button:nth-of-type(2)')
                    
                    # Wait until the button is clickable and then click it
                    WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(button)
                    ).click()
                    break  # Exit loop if successful
                else:
                    driver.refresh()  # Refresh the page if not enough elements are found
            except (TimeoutException, NoSuchElementException, ElementClickInterceptedException):
                driver.refresh()

        #time.sleep(0.1)

        button_xpath = "//button[contains(., 'Reserve')]"

        button_present = True
        while button_present:
            try:
                # Attempt to find and click the 'Reserve' button
                reserve_button = WebDriverWait(driver, 1200, poll_frequency=0.1).until(
                    EC.element_to_be_clickable((By.XPATH, button_xpath))
                )
                reserve_button.click()
                button_present = False
            except TimeoutException:
                # Button isn't clickable or not found within the specified time
                button_present = False
            except Exception:
                # Other exceptions (can be more specific if needed)
                button_present = False

        end_time = time.time()
        elapsed_time = end_time - start_time

        time.sleep(60)

    finally:
        # Wait before closing the browser
        time.sleep(300)
        driver.quit()
