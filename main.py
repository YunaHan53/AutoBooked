from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
import os
from dotenv import load_dotenv
import time

load_dotenv()

# ----------------  Step 1 - Setup, Chrome Profile and Basic Navigation ----------------

# Create Chrome Profile and create account manually. Put YOUR email and password here:
EMAIL = os.environ.get("ACCOUNT_EMAIL")
PASSWORD = os.environ.get("ACCOUNT_PASSWORD")
GYM_URL = os.environ.get("GYM_URL")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create a folder for the Chrome Profile Selenium will use every time
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
# Tells Chrome Driver to use the directory specified to store a profile.
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)

driver.get(GYM_URL)
driver.set_window_position(2568, 722)
driver.maximize_window()

# ----------------  Step 2 - Automated Login ----------------

# Alternate to using time.sleep():
wait = WebDriverWait(driver, 2)

# Click Login
login_button = wait.until(Ec.element_to_be_clickable((By.ID, "login-button")))
login_button.click()

# Enter Email and Password
input_email = wait.until(Ec.presence_of_element_located((By.ID, "email-input")))
input_email.clear()
input_email.send_keys(EMAIL)
input_password = wait.until(Ec.presence_of_element_located((By.ID, "password-input")))
input_password.clear()
input_password.send_keys(PASSWORD)

# Click Submit
submit_button = driver.find_element(By.ID, "submit-button")
submit_button.click()

# Wait for Schedule Page to load
wait.until(Ec.presence_of_element_located((By.ID, "schedule-page")))

# Statistics Summary counters
booked_count = 0
waitlisted_count = 0
already_booked_waitlisted_count = 0

# ----------------  Step 3 - Book a Class: Boot Upcoming Tuesday Class ----------------

# Find a class for Tuesday at 6pm
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")
for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text
    if "Tue" in day_title:
        class_time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        class_time_formatted = f"{class_time.split(" ")[1]} {class_time.split(" ")[2]}"
        if "6:00 PM" in class_time:
            # Get the class name
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            # Find the button
            button = card.find_element(By.TAG_NAME, "button")

# ----------------  Step 4 - Check if the class is already booked ----------------

            # Increment the counters for Statistics Summary
            # Check if a class is already booked (button reads "Booked")
            button_status = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
            if button_status.text == "Booked":
                already_booked_waitlisted_count += 1
                print(f"✓ Already booked: {class_name} on {day_title} at {class_time_formatted}")
            # Check if you're on the waitlist (button reads "Waitlisted")
            elif button_status.text == "Waitlisted":
                already_booked_waitlisted_count += 1
                print(f"✓ Already on waitlist: {class_name} on {day_title} at {class_time_formatted}")
            # Join the waitlist if the class is full (button says "Join Waitlist")
            elif button_status.text == "Book Class":
                button.click()
                booked_count += 1
                print(f"✓ Successfully booked: {class_name} on {day_title} at {class_time_formatted}")
                time.sleep(0.5)
            elif button_status.text == "Join Waitlist":
                button.click()
                waitlisted_count += 1
                print(f"✓ Joined waitlist for: {class_name} on {day_title} at {class_time_formatted}")
                time.sleep(0.5)
            break

# ----------------  Step 5 - Print out a booking summary ----------------

print(f"--- BOOKING SUMMARY --- \n"
      f"Classes booked: {booked_count} \n"
      f"Waitlists joined: {waitlisted_count} \n"
      f"Already booked/waitlisted: {already_booked_waitlisted_count} \n"
      f"Total Tuesday 6pm classes processed: {booked_count + waitlisted_count + already_booked_waitlisted_count} \n ")

# --- BOOKING SUMMARY ---
# Classes booked: 0
# Waitlists joined: 0
# Already booked/waitlisted: 1
# Total Tuesday 6pm classes processed: 1


# driver.close()