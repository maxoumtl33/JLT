from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

def get_gps_data():
    # Initialize WebDriver (ensure that you have downloaded the chromedriver executable)
    service = Service('listings/chromedriver')  # Change to your actual path to chromedriver
    driver = webdriver.Chrome(service=service)

    try:
        # Open the FINDER portal and log in
        driver.get('https://v2.finder-portal.com')

        # Wait for the login page to load and perform login if needed
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))
        time.sleep(10)  # Allow manual login or automate it

        # Wait for the map tab link to be present
        try:
            map_tab = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//a[@href="/tabs/map"]')))
            map_tab.click()
        except Exception as e:
            print(f"Error: {e}")

        # Extract GPS data (update the selectors based on actual class names in the portal)
        gps_data_elements = driver.find_elements(By.CLASS_NAME, 'gps-data-class')  # Update class name
        
        gps_data = []
        for element in gps_data_elements:
            latitude = element.get_attribute('data-lat')
            longitude = element.get_attribute('data-lng')
            gps_data.append({'lat': float(latitude), 'lng': float(longitude)})

        return gps_data

    finally:
        driver.quit()
