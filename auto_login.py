# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "000404283BB21E02759A2ED5370ECDED2DD0393F26640E73CE22CACC0661C1DC00A0933BC9A43DEC0DB167316FB019EDAA3E7BD861E7C195346768BD7DE7CF8D18EB24AE2FA78BF124FE05BCC6A006E0B54FC7761A852831B47134D94A2D9282F0B9A78FD4E6F653E733716A1D3FBFAD6EA2D44EF418AA7807952C1EF2384C7EA27C7F7DC3DE3C36C351683FB3F899C8D270519532F5DE1E1A7516DE0CCEFC53566E128D6A839D0BA45B210234B0153B9D3AB24997FF62DFBC699FE59C6ADA18CBA7807190476DFC962E06A7A763DA782C328A0767ECC86F71C303EE774297D131F03011FDA8F4BDF8A9CDAFF686A11052FDE788AD999F9DAA1365A51DEEA65C0E73835A3DF03060ADD6E0084C05A3B0B7960898F724E05F49F0EDB96D289817665F0F201F2DA79BD1160897E4F617D9956B5F81E1514AC440049A014E7D77D5FF7540F909E0D25F3C22957231E6224E00"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
