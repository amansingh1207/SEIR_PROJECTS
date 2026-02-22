import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def do_scrapping():
    if len(sys.argv) < 2:
        print("Enter the url that you want to extract information!")
        return
    url = sys.argv[1]
    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service = s)
    try:
        driver.get(url)
        time.sleep(6)
        print("\n--- Title ---")
        print(driver.title)

        print("\n--- BODY ---")
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(body_text.replace('\n', ' '))

        print("\n--- ALL LINKS ---")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href:
                print(href)
    except Exception as e:
        print("Something went wrong:", e)
    driver.quit()

if __name__ == "__main__":
    do_scrapping()
        
            

