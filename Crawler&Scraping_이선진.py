from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": "/home/user/data",  
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(executable_path="/path/to/chromedriver", options=chrome_options)

url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0"
driver.get(url)

time.sleep(3)

rows = driver.find_elements(By.XPATH, "//table[@class='type_2']/tbody/tr")


data = []

for row in rows[:50]: 
    try:

        cols = row.find_elements(By.TAG_NAME, "td")
        
        if len(cols) < 10:
            continue

        stock_name = cols[1].text.strip() 
        current_price = cols[2].text.strip().replace(",", "") 
        market_cap = cols[6].text.strip().replace(",", "")  

        stock_link = cols[1].find_element(By.TAG_NAME, "a").get_attribute("href")
        driver.get(stock_link)
        time.sleep(2)


        soup = BeautifulSoup(driver.page_source, "html.parser")
        roe = soup.find("th", text="ROE").find_next("td").text.strip() if soup.find("th", text="ROE") else "N/A"
        
        data.append([stock_name, current_price, market_cap, roe])
        
        driver.back()
        time.sleep(2)

    except Exception as e:
        print(f"Error processing row: {e}")
        continue

df = pd.DataFrame(data, columns=["종목명", "현재가", "시가총액", "ROE"])
df.to_csv("/home/user/data/kospi_market_cap_top50.csv", index=False)

driver.quit()

print("[완료] 코스피 시가총액 1~50위 데이터 CSV로 저장됨.")
