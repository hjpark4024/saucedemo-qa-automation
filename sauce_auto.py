from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import datetime


def login(driver, username, password):
    driver.get("https://www.saucedemo.com")
    id_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    )
    id_box.send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_duplicate_add():
    driver = webdriver.Chrome()
    login(driver, "standard_user", "secret_sauce")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
    )

    add_btn = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_btn.click()
    time.sleep(1)

    try:
        add_btn.click()
        result = "예상과 다름: 중복 클릭이 에러 없이 통과됨"
    except Exception as e:
        result = f"확인됨: 중복 클릭 시 {type(e).__name__} 발생 (버튼이 Remove로 교체되어 재클릭 불가)"

    driver.quit()
    return "[시나리오1: 중복 담기]", result


def test_logout_back():
    driver = webdriver.Chrome()
    login(driver, "standard_user", "secret_sauce")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "add-to-cart-sauce-labs-backpack"))
    )

    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    logout_link = driver.find_element(By.ID, "logout_sidebar_link")
    driver.execute_script("arguments[0].click();", logout_link)
    time.sleep(1)

    driver.back()
    time.sleep(1)

    try:
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        result = "발견: 뒤로가기 후 상품 목록 화면이 재노출됨 (캐시 위험)"
    except Exception:
        result = "확인됨: 로그아웃 후 뒤로가기 시 상품 목록이 재노출되지 않음"

    driver.quit()
    return "[시나리오2: 로그아웃 후 뒤로가기]", result


def test_login_fail_input_retained():
    driver = webdriver.Chrome()
    login(driver, "locked_out_user", "secret_sauce")

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )

    id_value = driver.find_element(By.ID, "user-name").get_attribute("value")
    pw_value = driver.find_element(By.ID, "password").get_attribute("value")

    if id_value != "" or pw_value != "":
        result = f"발견: 로그인 실패 후 입력값 미초기화 (아이디:{repr(id_value)}, 비밀번호:{repr(pw_value)})"
    else:
        result = "확인됨: 로그인 실패 후 입력값이 정상적으로 초기화됨"

    driver.quit()
    return "[시나리오3: 로그인 실패 시 입력값 유지]", result


# 전체 실행 및 리포트 저장
report_lines = []
now = datetime.datetime.now()
report_lines.append(f"테스트 실행 시각: {now}\n\n")

tests = [test_duplicate_add, test_logout_back, test_login_fail_input_retained]

for test_func in tests:
    title, result = test_func()
    line = f"{title} {result}"
    print(line)
    report_lines.append(line + "\n")

folder = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(folder, "saucedemo_test_report.txt")

f = open(path, "w", encoding="utf-8")
f.writelines(report_lines)
f.close()

print("\n리포트 저장 완료:", path)