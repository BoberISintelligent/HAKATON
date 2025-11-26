from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import pandas as pd
import time

def searcheng():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1,1")

    service = Service('chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.minimize_window()
    driver.get("https://duckduckgo.com/?q=lastelaager+korraldaja+Eesti")

    results = []
    max_pages = 10
    current_page = 1
    driver.implicitly_wait(5)

    while current_page <= max_pages:
        try:
            more_button = driver.find_element(By.ID, "more-results")
            driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
            time.sleep(1) 
            more_button.click()
            current_page += 1
            time.sleep(2)
        except (NoSuchElementException, ElementClickInterceptedException):
            break 

    items = driver.find_elements(By.CSS_SELECTOR, 'li[data-layout="organic"]')
    for item in items:
        try:
            title_elem = item.find_element(By.CSS_SELECTOR, 'h2 a[data-testid="result-title-a"] span')
            link_elem = item.find_element(By.CSS_SELECTOR, 'h2 a[data-testid="result-title-a"]')
            title = title_elem.text
            link = link_elem.get_attribute("href")
            results.append({"title": title, "link": link})
        except:
            continue

    driver.quit()

    df = pd.DataFrame(results)
    keywords = ["laager", "suvelaager", "päevalaager", "laagrid", "noortelaager", "suvelaagrid", "päevalaagrid", "noortelaagrid"]
    pattern = "|".join(keywords)
    df_filtered = df[df['title'].str.contains(pattern, case=False, na=False)].drop_duplicates(subset='title')

    camps = [["title", "link"]] + df_filtered[["title", "link"]].values.tolist()
    return camps
