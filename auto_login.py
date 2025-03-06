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
    browser.add_cookie({"name": "MUSIC_U", "value": "00B0C783178FCB6317143F1ACC3238A66978BB91C6173E396381E6DB00BF2FD7A92C9A857B16341769B4F2FFBEFCFDF766FBB36066B0C8F60BAA57F280E80F061B565A0A4EB2D6B823610B49AEEFA1B542CDF82D8C1EDB8E9CA2A8CAEE9618DBBB14566E535E1C02E8052F65A4341FC94B490D8311BB86F4B40A6B59E4FFA4C9A75F8904FBA14B1EF136E07C09F23202549463C61542FD58CF5B94AAC506751C3B91BE5C1D76B5DF38FD75E309E1913ED64B0EF81B0C89D12C0B03552ECB8271A234F6D526F8E06BF12067EE260B8B3F9EC6C16AE8197A01AAA1B1BC5A287A90709D52A088ED2E8DD36FE9518C73E99D9E10B2ED76C993614ADD03376FB401CFF7218EA0670B3FBFB0125675A2FCF2AAC1AEC2F1B807E02BBD32F2501F3739CC9A9C21D343461967815E080C45C1C7D229DADB029F0104354C5056DF88217883563A6044FC83CB64A5232C6822058D697349E65B986E98D3EECFCF5EB1C3D4C1B3"})
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
