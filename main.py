import os
from datetime import datetime, timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():	
	# Set up the Chrome WebDriver (make sure you have the correct driver installed and in your PATH)
	driver = webdriver.Chrome()

	# Open reservation website
	driver.get("https://reserve.et.byu.edu/reservations/Web/dashboard.php")

	# Select username and password fields
	username_field = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "email"))
	)
	password_field = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "password"))
	)

	# Get username and password from environement variables
	# Before using this code, set the environment variables MY_USERNAME and MY_PASSWORD
	# in your .bashrc or equivalent file (.zshrc, etc.)
	username = os.getenv("MY_USERNAME")
	password = os.getenv("MY_PASSWORD")

	# Input username and password
	username_field.send_keys(username)
	password_field.send_keys(password)

	# Press enter to log in
	password_field.send_keys(Keys.RETURN)

	###########################################################################################################
	# I haven't encountered the issue yet, but if DuoPush 2FA pops up at this point after entering credentials
	# I don't have an automatic solution yet
	###########################################################################################################

	# If there's no wait time here, the reserve button hasn't loaded yet so it crashes so
	# I use WebDriverWait to wait until the button is clickable before trying to select it
	# This is for EB 407. To select a different room, change the CSS_SELECTOR to the reservation
	# string for the room you want, you'll have to go to the reservation page and inspect the code
	# for your room's string
	reserve_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='reservation.php?rid=5']"))
	)
	reserve_button.click()

	# Add the reservation title and description
	title_field = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "reservationTitle"))
	)
	title_field.send_keys("Capstone Team 22")

	description_field = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "reservationDescription"))
	)
	description_field.send_keys("Capstone Team 22 Meeting")


	# open the start date calendar, we don't have to adjust the end date
	# because it auto-fills based on the start date
	start_date_input = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.ID, "BeginDate"))
	)
	start_date_input.click()

	# by default, this selects 2 days ahead, optionally takes days ahead as an argument
	day, month, year = get_reservation_day()

	# build an XPath that matches the correct <td> by data-month, data-year, and day number
	xpath = f"//td[@data-month='{month}'][@data-year='{year}']/a[text()='{day}']"

	# wait until the date is clickable and click the button for 2 days ahead
	date_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.XPATH, xpath))
	)
	date_button.click()

	# Open the dropdowns and select the begin and end times (8-10 AM)
	begin_dropdown = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "beginPeriod"))
	)
	end_dropdown = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.NAME, "endPeriod"))
	)
	begin_dropdown = Select(begin_dropdown)
	end_dropdown = Select(end_dropdown)
	begin_dropdown.select_by_value("08:00:00")
	end_dropdown.select_by_value("10:00:00")

	# Make sure the create button is clickable and submit the reservation
	create_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btnCreate"))
	)
	create_button.click()

	# TODO: Add a check to see if the reservation is successful. If not, automate trying a different room like 405 or 409
	try:
		message = WebDriverWait(driver, 10).until(
			EC.presence_of_element_located(
				(By.CSS_SELECTOR, "#created-message, #failed-message")
			)
		)
		if message.get_attribute("id") == "created-message":
			print("Reservation created successfully!")
		else:
			print("Reservation could not be made.")
	except:
		print("No success or failure message appeared")


###########################################################################################################
# ADJUST THIS IF THE RESERVATION LIMIT IS MORE THAN 2 DAYS
# JUST CHANGE days=2 TO HOWEVER MANY DAYS AHEAD YOU WANT
###########################################################################################################
def get_reservation_day(days_ahead=2):
	two_days_later = datetime.now() + timedelta(days=days_ahead)
	day = two_days_later.day
	month = two_days_later.month - 1
	year = two_days_later.year

	return day, month, year

def check_for_success():




if __name__ == "__main__":
	main()


