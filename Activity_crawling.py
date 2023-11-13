from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json

url = "https://kr.trip.com/things-to-do/ttd-home/?districtId=234&ctm_ref=vactang_page_23810&locale=ko-KR&curr=KRW"
activity_place_keyword = input("액티비티 여행지")
# hotel_destination_keyword = input("숙박 도착 장소")
# start_day = input("체크인(비행기 가는 편) 날짜(아직 해당 달의 날짜만 선택 가능)")
# end_day = input("체크아웃(비행기 오는 편) 날짜(아직 해당 달의 날짜만 선택 가능)")
# ChromeOptions 객체 생성
options = Options()

# 원하는 기능 설정
options.capabilities["browserName"] = "chrome"

# 원하는 기능을 가진 Chrome 드라이버 객체 생성
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(15) # 묵시적 대기

# 페이지 가져오기(이동)
driver.get(url)

driver.implicitly_wait(15) # 묵시적 대기

## 여행지 검색창 누르고 여행지 입력, 검색
activity_place_search_btn = driver.find_element(By.CSS_SELECTOR, "#ticket_header_pic > div.ticket_header_search > div.trip-search > div > div > div.ol_citypage_height > div.header_search_content > div.switch_header > div.ol_cityselect_region_search.ol_cityselect_search > i")
activity_place_search_btn.click()
time.sleep(0.15)

activity_place_input = driver.find_element(By.CSS_SELECTOR, "#tnt-online-input")
activity_place_input.clear()
time.sleep(0.15)

activity_place_input.send_keys(activity_place_keyword)
activity_place_input.click()
activity_place_input.send_keys(" ")
time.sleep(0.15)

activity_place_input_click = driver.find_element(By.CSS_SELECTOR, "#ticket_header_pic > div.ticket_header_search > div.trip-search > div > div > div.ol_citypage_layer > div > div > div > div:nth-child(2) > div > div.m_searchengine_item.m_searchengine_item_hover > div.m_searchengine_item_wrapper")
activity_place_input_click.click()
activity_place_input_search_btn = driver.find_element(By.CSS_SELECTOR, "#ticket_header_pic > div.ticket_header_search > div.trip-search > div > div > div.ol_citypage_height > div.header_search_content > div.search-icon")
activity_place_input_search_btn.click()

## 어트랙션 목록 가져오기

# # 더보기 버튼 존재 여부 확인 및 클릭
# try:
#     # 더보기 버튼이 로드될 때까지 최대 0.01초간 대기
#     attraction_more_btn = WebDriverWait(driver, "1").until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, "#ibuact-10650012671-filter-add-294-0-more"))
#     )
#     # 버튼 클릭
#     attraction_more_btn.click()
#     # 어트랙션 요소 찾기
#     attractions = driver.find_elements(By.CSS_SELECTOR, ".filter-select-name")
#
#     # 각 요소의 텍스트 추출
#     attractions_names = [attraction.text for attraction in attractions]
#
#     # 추출된 텍스트 출력
#     for attraction_name in attractions_names:
#         print(attraction_name)
#
# except TimeoutException:
#     # 어트랙션 요소 찾기
#     attractions_section = driver.find_element(By.XPATH, "//div[contains(text(), '어트랙션')]/ancestor::div[contains(@class, 'filter-container')]")
#     attractions = attractions_section.find_elements(By.CLASS_NAME, "filter-select-name")
#
#     # 각 요소의 텍스트 추출
#     attractions_names = [attraction.text for attraction in attractions]
#
#     # 추출된 텍스트 출력
#     for attraction_name in attractions_names:
#         print(attraction_name)


attraction_more_buttons = driver.find_elements(By.CSS_SELECTOR, "#ibuact-10650012671-filter-add-294-0-more")
if attraction_more_buttons:
    # 버튼 클릭
    attraction_more_buttons[0].click()
    time.sleep(0.3)  # 페이지가 업데이트 될 시간을 기다립니다.

# 어트랙션 요소 찾기
attractions_section = driver.find_element(By.XPATH, "//div[contains(text(), '어트랙션')]/ancestor::div[contains(@class, 'filter-container')]")
attractions = attractions_section.find_elements(By.CLASS_NAME, "filter-select-name")

# 각 요소의 텍스트 추출
attractions_names = [attraction.text for attraction in attractions]

# 추출된 텍스트 출력
for attraction_name in attractions_names:
    print(attraction_name)
