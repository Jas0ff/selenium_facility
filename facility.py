from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import pickle
import keyboard
import undetected_chromedriver as uc


def chrome_init_set(gui):
    options = uc.ChromeOptions()
    options.add_argument("--mute-audio")  # 靜音
    if gui:
        chrome = uc.Chrome(options=options)
    else:
        # not available TODO
        chrome = uc.Chrome(headless=True, options=options)
    """
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")  # 關閉自動測試提示
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")  # 無痕
    options.add_argument("--mute-audio")  # 靜音

    ua = 'Mozilla/5.0 ' \
         '(Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    options.add_argument("user-agent={}".format(ua))

    chrome = webdriver.Chrome('./chromedriver.exe', options=options)

    chrome.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    # chrome.minimize_window()

    if not gui:
        options.add_argument("--headless")  # 無視窗模式
        options.add_argument("--disable-gpu")
    """

    return chrome


def get_cookies(url, chrome):
    chrome.get(url)
    print('登入中，按esc結束登入')
    keyboard.wait('esc')
    print('登入結束')

    cookies = chrome.get_cookies()
    print(cookies)
    with open('temp_cookies', 'wb') as f:
        pickle.dump(cookies, f)


def use_cookies(url, chrome):
    chrome.get(url)
    chrome.delete_all_cookies()
    with open('temp_cookies', 'rb') as f:
        cookies = pickle.load(f)
    for cookie in cookies:
        chrome.add_cookie(cookie)
    chrome.get(url)


def locate_item(keyword, chrome):
    target = WebDriverWait(chrome, 5).until(
        EC.presence_of_element_located((By.XPATH,
                                        f'//*[contains(text(), "{keyword}")]'
                                        )))
    # most efficient way to locate
    return target


def locate_item_adv(attr, keyword, chrome):
    target = WebDriverWait(chrome, 5).until(
        EC.presence_of_element_located((By.XPATH,
                                        f'//*[contains(@{attr}, "{keyword}")]'
                                        )))
    # most efficient way to locate
    return target


def check_item_exist(keyword, chrome):
    try:
        target = WebDriverWait(chrome, 0.5).until(
            EC.presence_of_element_located((By.XPATH,
                                            f'//*[contains(text(), "{keyword}")]'
                                            )))
    except Exception:
        return False
    return True


def check_item_exist_adv(attr, keyword, chrome):
    try:
        target = WebDriverWait(chrome, 0.5).until(
            EC.presence_of_element_located((By.XPATH,
                                            f'//*[contains(@{attr}, "{keyword}")]'
                                            )))
    except Exception:
        return False
    return True


def page_bottom(chrome):
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def page_size(percentage, chrome):
    chrome.execute_script(f"document.body.style.zoom='{str(percentage)}%'")


# item operation
def select_item(item, chrome):
    action = ActionChains(chrome)
    action.move_to_element(item)
    action.click()
    # action.click_and_hold(item) if you want
    action.send_keys(Keys.ENTER)
    # item.send_keys(Keys.ENTER) also work
    action.perform()


def item_attr(attr, item):
    # ex, image.get_attribute('src')
    return item.get_attribute(attr)


def item_style(property, item):
    return item.value_of_css_property(property)
