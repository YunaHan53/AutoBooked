from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
import os
from dotenv import load_dotenv
from datetime import datetime

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

# ----------------  Step 3 - Book a Class: Boot Upcoming Tuesday Class ----------------

# Find a class for Tuesday at 6pm
day_group_search = driver.find_elements(By.CSS_SELECTOR, "div[id^='day-group-']")
for day_group in day_group_search:
    day_date = day_group.text.split("\n")[0]
    # Check if it is a Tuesday
    if "Tue" in day_date:
        # Get the date and current year
        date = day_date.split(",")[1].strip()
        current_year = datetime.now().year
        date_year = f"{date} {current_year}"

        # Format the date with the current year
        formatted_date = datetime.strptime(date_year, "%b %d %Y").strftime("%Y-%m-%d")
        # Check for a 6:00 pm class
        times_on_date = driver.find_elements(By.CSS_SELECTOR, f"div[id^='class-card-'][id*='{formatted_date}']")

        for times in times_on_date:
            if "Time: 6:00 PM" in times.text:
                # Get the class name
                class_name = times.text.split("\n")[0]

                # Find the time text and format it
                timeline = times.text.split("\n")[1]
                time = f"{timeline.split(" ")[1].strip()} {timeline.split(" ")[2].strip()}"
                formatted_time = datetime.strptime(time, "%I:%M %p").strftime("%H%M")
                # Find a click the book OR join waitlist button
                date_time = f"{formatted_date}-{formatted_time}"
                book_button = driver.find_element(By.CSS_SELECTOR, f"button[id^='book-button'][id$='{date_time}']")
                book_button.click()

                print(f"✓ Booked: {class_name} on {date_year}")

# driver.close()