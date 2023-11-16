import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# 설정 파일 불러오기
with open('hotel-crawler.json', 'r') as config_file:
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

# 인원, 객실 수 입력받으면 몇 번 클릭할지 계산
def person_and_room(persons, rooms):
    persons_click_times = 0
    rooms_click_times = 0

    if persons > 2:
        persons_click_times = persons - 2
    elif persons == 1:
        persons_click_times = -1

    if rooms != 1:
        rooms_click_times = rooms - 1

    return persons_click_times, rooms_click_times


# 날짜 객체 생성 함수
def create_date(year, month, day):
    try:
        return datetime(year, month, day)
    except ValueError:
        # 잘못된 날짜 (예: 2월 30일) 처리
        return None

# 사용자 입력 받기
persons = int(input("인원"))
rooms = int(input("객실 수"))
start_place_keyword = input("출발지")
flight_destination_keyword = input("비행기 도착 장소: ")
hotel_destination_keyword = input("숙박 도착 장소: ")
# 날짜 입력 받기
checkin_month = int(input("체크인 월 (1-12): "))
checkin_day = int(input("체크인 일: "))
checkout_month = int(input("체크아웃 월 (1-12): "))
checkout_day = int(input("체크아웃 일: "))

persons_click_time, rooms_click_time = person_and_room(persons, rooms)

# 날짜 계산 전 현재 날짜 가져오기
current_date = datetime.now()

# 날짜 유효성 검사를 위한 수정된 부분
current_year = current_date.year
checkin_year = current_year if checkin_month >= current_date.month else current_year + 1
checkout_year = checkin_year if checkout_month >= checkin_month else checkin_year + 1

checkin_date = create_date(checkin_year, checkin_month, checkin_day)
checkout_date = create_date(checkout_year, checkout_month, checkout_day)

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

# 인원 수, 객실 선택
persons_and_rooms_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["persons_and_rooms_btn"])
persons_and_rooms_btn.click()

rooms_click_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["rooms_plus_btn"])
for _ in range(rooms_click_time):
    rooms_click_btn.click()
    time.sleep(0.3)

persons_plus_click = driver.find_element(By.CSS_SELECTOR, config["selectors"]["person_plus_btn"])
persons_minus_click = driver.find_element(By.CSS_SELECTOR, config["selectors"]["person_minus_btn"])

if persons_click_time == -1:
    persons_minus_click.click()
else:
    for _ in range(persons_click_time):
        persons_plus_click.click()
        time.sleep(0.3)

# 검색 시작
search_btn = driver.find_element(By.CSS_SELECTOR, config["selectors"]["search_btn"])
search_btn.click()

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

#랜덤으로 호텔 가져오기
x = 3
hotel = {"name": driver.find_element(By.CSS_SELECTOR, config["selectors"]["hotel_name"].format(x)).text, "price": driver.find_element(By.CSS_SELECTOR, config["selectors"]["price"].format(x)).text}

# 결과 데이터 구조
data = {
    "hotel": hotel,
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
