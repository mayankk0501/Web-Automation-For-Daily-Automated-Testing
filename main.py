#import all neccessary modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import logging
logging.basicConfig(filename='test_log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("Script started")

#-------------------------------------------------------------------------------------------

#some extra arguments for smooth selenium functioning and preventing to get detected as bot
options = Options()
prefs = {"download.default_directory": r"C:\Users\Hp\Desktop\Project Task"}
options.add_experimental_option("prefs", prefs)
options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--incognito")
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.page_load_strategy = 'normal'

ss_path = r"C:\Users\Hp\Desktop\Project Task"


#-------------------------------------------------------------------------------------------

#open webdriver
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get('https://www.amazon.in/')
time.sleep(1)

#-------------------------------------------------------------------------------------------

# Add cookies to the WebDriver instance
with open('cookies.json', 'r') as file: 
    cookies = json.load(file)
for cookie in cookies:
    driver.add_cookie(cookie)

#-------------------------------------------------------------------------------------------

#search for product
try:
    input_product = driver.find_element("xpath", '//*[@id="twotabsearchtextbox"]')
    input_product.send_keys("case")
    input_product.send_keys(Keys.ENTER)
    driver.save_screenshot(ss_path+'\\product_search.png')
    logging.info("Test step 1 successful - Product search successful")
    time.sleep(1)
except Exception as e:
    logging.error(f"Error in test step 1: {e}")

#-------------------------------------------------------------------------------------------

#click on the first product
try:
    first_product = driver.find_elements(By.CLASS_NAME, "a-size-medium.a-color-base.a-text-normal")[0]
    first_product.click()
    time.sleep(3)
    new_tab = driver.window_handles[1]
    driver.switch_to.window(new_tab)
    logging.info("Test step 2 successful - Opened the first product")
except Exception as e:
    logging.error(f"Error in test step 2: {e}")

#-------------------------------------------------------------------------------------------

#add to cart
try:
    add_to_cart_button = driver.find_element("xpath", '//*[@id="add-to-cart-button"]')
    add_to_cart_button.click()
    driver.save_screenshot(ss_path+'\\add_to_cart.png')
    time.sleep(1)
    logging.info("Test step 3 successful - Added to cart")
except Exception as e:
    logging.error(f"Error in test step 3: {e}")

#-------------------------------------------------------------------------------------------

#proceed to buy
try:
    buy_button = driver.find_element("xpath", '//*[@id="sc-buy-box-ptc-button"]/span/input')
    buy_button.click()
    time.sleep(1)
    logging.info("Test step 4 successful - Redirected to delivery details")
except Exception as e:
    logging.error(f"Error in test step 4: {e}")

#-------------------------------------------------------------------------------------------

# Open the credentials.json file
with open('credentials.json', 'r') as file:
    credentials = json.load(file)

# Access individual credentials
email = credentials['email']
password = credentials['password']

#login to account if necessary
try:
    login_field = driver.find_element("xpath", '//*[@id="ap_email"]')
    login_field.send_keys(email)
    login_field.send_keys(Keys.ENTER)
    time.sleep(1)
    password_field = driver.find_element("xpath", '//*[@id="ap_password"]')
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    time.sleep(1)
    logging.info("Test step 5 successful - Login Successful")
except Exception as e:
    logging.error(f"No need to login or Might be error in Login. : {e}")
    try:
        password_field = driver.find_element("xpath", '//*[@id="ap_password"]')
        password_field.send_keys(password)
        password_field.send_keys(Keys.ENTER)
        time.sleep(1)
        logging.info("Test step 5 successful - Login Successful")
    except Exception as e:
        logging.error(f"No need of login. Cookies working fine. : {e}")

#-------------------------------------------------------------------------------------------

driver.save_screenshot(ss_path+'\\delivery_details.png')

#-------------------------------------------------------------------------------------------

#select address
try:
    address_selection = driver.find_element("xpath", '//*[@id="orderSummaryPrimaryActionBtn"]/span/input')
    address_selection.click()
    time.sleep(10)
    logging.info("Test step 6 successful - Address selected")
except Exception as e:
    logging.error(f"Error in test step 6 / Might be no need: {e}")

#-------------------------------------------------------------------------------------------

#select payment method
try:
    payment_method = driver.find_element("xpath", '//*[@id="orderSummaryPrimaryActionBtn"]/span/input')
    payment_method.click()
    time.sleep(10)
    logging.info("Test step 7 successful - Payment method selected")
except Exception as e:
    logging.error(f"Error in test step 7 / Might be no need: {e}")

#-------------------------------------------------------------------------------------------

#place order
try:
    place_order = driver.find_element("xpath", '//*[@id="submitOrderButtonId"]/span/input')
    place_order.click()
    time.sleep(10)
    logging.info("Test step 8 successful - Order Placed")
except Exception as e:
    logging.error(f"Error in test step 8: {e}")

#-------------------------------------------------------------------------------------------

driver.save_screenshot(ss_path+'\\order_placed.png')

#-------------------------------------------------------------------------------------------

#confirmation message
try:
    confirmation_message = driver.find_elements(By.CLASS_NAME, "a-alert-heading")[0].text
    if 'thank' in confirmation_message:
        logging.info("Test step 9 successful - Order Placed Successfully")
except Exception as e:
    logging.error(f"Error in test step 9: {e}")

#-------------------------------------------------------------------------------------------

logging.info("Script finished")
time.sleep(20)
driver.quit()
