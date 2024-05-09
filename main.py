import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def setup_driver():
    chrome_options = Options()
    chrome_binary_path = os.getenv("CHROME_BINARY_PATH", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    chrome_driver_path = os.getenv("CHROME_DRIVER_PATH", "/Users/jameschan/PycharmProjects/webscraping/chromedriver/chromedriver-mac-arm64/chromedriver")

    chrome_options.binary_location = chrome_binary_path
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    return driver


def navigate_to_page(driver, url):
    driver.get(url)
    try:
        continue_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="mat-dialog-0"]/app-welcome-disclaimer/div/div/div[5]/button'))
        )
        continue_button.click()
    except Exception as e:
        print(f"Error navigating to page: {e}")


def search_location(driver, location):
    try:
        search_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.search-location'))
        )
        search_input.clear()
        search_input.send_keys(location)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "search-button")]'))
        ).click()
    except Exception as e:
        print(f"Error searching location: {e}")


def scrape_data(driver):
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.data-grid tbody'))
        )
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, 'lxml')
        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            crime_type = row.find('td', headers='UCRGroup').get_text(strip=True)
            print(crime_type)
    except Exception as e:
        print(f"Failed to scrape data: {e}")


def main():
    driver = setup_driver()
    try:
        navigate_to_page(driver, "https://communitycrimemap.com")
        search_location(driver, "West Valley City, UT")
        scrape_data(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
