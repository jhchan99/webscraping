from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time


# Specify the path to chromedriver using Service
s = Service(r'C:\Users\jhcha\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=s)

driver.get('https://communitycrimemap.com/datagrid')

continue_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable(
        (By.XPATH, '/html/body/div[1]/div[2]/div/mat-dialog-container/app-welcome-disclaimer/div/div/div[5]/button'))
)
continue_button.click()

search_input = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/div/mat-form-field/div/div[1]/div[3]/input'))
)
search_input.clear()
search_input.send_keys('West Valley City, UT')
time.sleep(3)

search_button = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/div/mat-form-field/div/div[1]/div[4]/button[2]'))
)
search_button.click()

data_grid = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
        (By.XPATH,'/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[3]/app-navbar-actions/div/div[2]/button'))
)
data_grid.click()



try:
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/table/tbody'))
    )
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'lxml')
    rows = soup.find('tbody').find_all('tr')
    for row in rows:
        crime_type = row.find('td', headers='UCRGroup').get_text(strip=True)
        print(crime_type)

except:
    print("Failed to load the tbody element within the time frame.")
finally:
    driver.quit()
