import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# 설정 파일 불러오기
with open('HotelAndFlight_config.json', 'r') as config_file:
    config = json.load(config_file)

def select_date(date, is_checkout=False):
    # 달력 열기 (체크아웃 날짜 선택 시 이미 열려있는 경우 제외)
    if not is_checkout:
        day_open_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["day_open_btn"])
        day_open_btn.click()
        time.sleep(0.4)

    # 현재 달과 선택할 달 사이의 차이 계산
    # 체크아웃 날짜 선택 시 현재 달력 페이지를 고려
    current_month = current_date.month if not is_checkout else checkin_date.month
    target_month = date.month
    month_difference = (target_month - current_month) % 12

    # 필요한 경우 달력 페이지 넘김
    for _ in range(month_difference):
        next_month_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["month_next_btn"])
        next_month_btn.click()
        time.sleep(0.5)

    # 날짜 클릭
    day_btns = driver.find_elements(By.CSS_SELECTOR, config["selectors"]["day_btn"])
    for btn in day_btns:
        if btn.text == str(date.day):
            btn.click()
            break




# 날짜 객체 생성 함수
def create_date(year, month, day):
    try:
        return datetime(year, month, day)
    except ValueError:
        # 잘못된 날짜 (예: 2월 30일) 처리
        return None


# 사용자 입력 받기
start_place_keyword = input("출발지")
flight_destination_keyword = input("비행기 도착 장소: ")
hotel_destination_keyword = input("숙박 도착 장소: ")
# 날짜 입력 받기
checkin_month = int(input("체크인 월 (1-12): "))
checkin_day = int(input("체크인 일: "))
checkout_month = int(input("체크아웃 월 (1-12): "))
checkout_day = int(input("체크아웃 일: "))
#
# start_day_raw = input("체크인(비행기 가는 편) 날짜: ")
# end_day_raw = input("체크아웃(비행기 오는 편) 날짜: ")

# 날짜 계산 전 현재 날짜 가져오기
current_date = datetime.now()

# 체크인 및 체크아웃 날짜 생성
checkin_date = create_date(current_date.year, checkin_month, checkin_day)
checkout_date = create_date(current_date.year if checkout_month >= checkin_month else current_date.year + 1, checkout_month, checkout_day)

# 날짜 유효성 검사
if checkin_date is None or checkout_date is None:
    raise ValueError("잘못된 날짜 입력입니다.")

max_future_date = current_date + timedelta(days=11 * 30)  # 11개월 후
if not (current_date <= checkin_date <= max_future_date and checkin_date < checkout_date <= max_future_date):
    raise ValueError("잘못된 날짜입니다.")

# 웹드라이버 설정 및 페이지 열기
options = Options()
options.capabilities["browserName"] = "chrome"
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(config["implicit_wait_time"])
driver.get(config["url"])

# 출발지 입력
start_search_btn = WebDriverWait(driver, 1).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["start_search_btn"]))
)
start_search_btn.click()

start_search = WebDriverWait(driver,1).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["start_search_btn"]))
)
start_search.clear()
start_search.send_keys(start_place_keyword)

# 항공편 검색
flight_search_btn = WebDriverWait(driver, 1).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["flight_search_btn"]))
)
flight_search_btn.click()

flight_search = WebDriverWait(driver, 1).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["flight_search_btn"]))
)
flight_search.clear()
flight_search.send_keys(flight_destination_keyword)

time.sleep(0.5)

# 도착지 호텔 검색
hotel_search_btn = WebDriverWait(driver, 1).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, config["selectors"]["hotel_search_btn"]))
)
hotel_search_btn.click()

hotel_search = WebDriverWait(driver, 1).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, config["selectors"]["hotel_search_btn"]))
)

hotel_search.clear()
hotel_search.send_keys(hotel_destination_keyword)
time.sleep(0.6)

# 체크인 날짜 선택
select_date(checkin_date)

# 체크아웃 날짜 선택
select_date(checkout_date, is_checkout=True)
# day_open_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["day_open_btn"])
# day_open_btn.click()
# time.sleep(0.2)
#
# day_btn = driver.find_elements(By.CSS_SELECTOR, config["selectors"]["day_btn"])
# for btn in day_btn:
#     if btn.text == start_day:
#         btn.click()
#         break
#
# time.sleep(0.1)
#
# for btn in day_btn:
#     if btn.text == end_day:
#         btn.click()
#         break

# 검색 시작
search_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["search_btn"])
search_btn.click()

# 데이터 수집
# 호텔 정보
hotel_names = []
for x in range(1, 4):
    hotel_name_selector = config["selectors"]["hotel_name"].format(x)
    hotel_name = driver.find_element(By.CSS_SELECTOR, hotel_name_selector)
    hotel_names.append(hotel_name.text)

# 출발 항공편 정보 수집
start_flight_info = {
    "airline": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_airline"]).text,
    "start_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_start_time"]).text,
    "start_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_start_airport"]).text,
    "end_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_end_time"]).text,
    "end_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_end_airport"]).text,
    "time_required": driver.find_element(By.CSS_SELECTOR, config["selectors"]["start_flight_info_time"]).text
}

# 귀환 항공편 정보 수집
comeback_flight_info = {
    "airline": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_airline"]).text,
    "start_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_start_time"]).text,
    "start_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_start_airport"]).text,
    "end_time": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_end_time"]).text,
    "end_airport": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_end_airport"]).text,
    "time_required": driver.find_element(By.CSS_SELECTOR, config["selectors"]["comeback_flight_info_time"]).text
}

# 호텔 정보
hotel_names = []
for x in range(1, 4):
    hotel_name_selector = config["selectors"]["hotel_name"].format(x)
    hotel_name = driver.find_element(By.CSS_SELECTOR, hotel_name_selector)
    hotel_names.append(hotel_name.text)

# 가격 정보
price_list = []
for x, hotel_name in enumerate(hotel_names, start=1):
    price_selector = config["selectors"]["price"].format(x)
    total_price = driver.find_element(By.CSS_SELECTOR, price_selector)
    price_list.append({"name": hotel_name, "price": total_price.text})

# 결과 데이터 구조
data = {
    "hotels": price_list,
    "flights": {
        "departure": start_flight_info,
        "return": comeback_flight_info
    }
}

# 데이터를 JSON 형식으로 변환 후 출력
json_data = json.dumps(data, indent=4, ensure_ascii=False)
print(json_data)


# 드라이버 종료
driver.quit()
