from selenium import webdriver
import os
from .message import message

# 執行chrome_driver
def open_driver():
    try:
        now_path = os.getcwd()  # 查看現在在哪一個路徑
        PATH = now_path + "/chromedriver 2"
        chrome_options = webdriver.ChromeOptions()
        # capabilities = DesiredCapabilities.CHROME
        # capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        # 開啟開發人員工具
        # chrome_options.add_argument("--auto-open-devtools-for-tabs")
        # chrome_options.add_argument('--headless') # 無頭
        # chrome_options.add_experimental_option("detach", True)
        # 隱藏selenium的自動控制功能, 防止被偵測
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        # 設置修改selenium的特徵值, 防止被偵測
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])

        driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        # driver = webdriver.Remote(
        #     command_executor=f'http://10.4.17.43:4444/wd/hub',
        #     options=chrome_options
        # )
        return driver
    except Exception as err:
        message(f'chrome_diver開啟失敗, 錯誤碼: {err}')