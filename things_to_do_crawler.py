import json
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

url = "https://www.tripadvisor.co.kr/"
place_keyword = input("여행지: ")
number_of_items = int(input("몇 개의 항목을 가져올까요? "))

# ChromeOptions 객체 생성 및 설정
options = Options()
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--headless")  # 창 없이 실행

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15) # 묵시적 대기
driver.get(url)

# 여행지 검색창 누르기
search_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#lithium-root > main > div:nth-child(4) > div > div > div.ctKgY > div > form > div > div > input"))
)
search_input.clear()
search_input.send_keys(place_keyword)
search_input.send_keys(Keys.ENTER)

time.sleep(0.9)

# 즐길거리 클릭
things_to_do = driver.find_element(By.CSS_SELECTOR, "#search-filters > ul > li:nth-child(4) > a")
things_to_do.click()

time.sleep(0.9)
# 결과 데이터 추출
attractions_data = []
attractions_blocks = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".location-meta-block"))
)[:number_of_items]

for block in attractions_blocks:
    name = block.find_element(By.CSS_SELECTOR, ".result-title").text.strip()
    address = block.find_element(By.CSS_SELECTOR, ".address-text").text.strip()
    attractions_data.append({"name": name, "address": address})

# 결과 출력
print(json.dumps(attractions_data, ensure_ascii=False, indent=4))


# 드라이버 종료
driver.quit()
