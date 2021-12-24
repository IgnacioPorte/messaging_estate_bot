from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import uniform
from selenium.webdriver.common.action_chains import ActionChains
import requests, time

class Bot():
    def __init__(self, name, last_name, email, phone, place="metropolitana"):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.place = place
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_home_page(self):
        self.driver.get('https://www.portalinmobiliario.com/')
        sleep(uniform(2, 3))

    def login(self, api_key):
        API_KEY = api_key
        data_sitekey_1 = "6LchwzUaAAAAAI3Am_n1zyxszhpA9zA2_BZ9feFH"
        action = "login"
        page_url ="https://www.mercadolibre.com/jms/mlc/lgz/msl/login/H4sIAAAAAAAEAzWNsW7DMAxE_4WzEe0aC3QP0C6dBNqibaKUKFB0lCDIvxdG0O0Od_fuCaIb1-SPRhCB7k14YYcJmqCvaiVxhgiNYYLOTm9bZDkraFjIyTrE5wnaKH_QqnaiVpROMAEevqdVdEB8f8EE3BPdnayipEHzjelM_xebQoTdvfUYwhjj0tQchWvRmYXRWC-LlnCj6hgyNTTHQtU1nJKXQ9BCITdtKuxYMaTrMQv3nfK3Znykn88veE2wYvfkhssvRLeDXn-zXHLJEAEAAA/user-recaptcha"
        self.driver.get(page_url)

        mail = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="user_id"]')))
        mail.send_keys(Keys.CONTROL + "a")
        mail.send_keys(Keys.DELETE)
        mail.send_keys(self.email)

        submit = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="login_user_form"]/div[2]/button')))
        submit.click()
        # print("just")
        def call_api_captcha():
            # print("principio")

            u1 = f"https://2captcha.com/in.php?key={API_KEY}&method=userrecaptcha&action={action}&googlekey={data_sitekey_1}&pageurl={page_url}&json=1&enterprise=1"
            r1 = requests.get(u1)
            # print("fin")

            rid = r1.json()["request"]
            print(r1.json())
            u2 = f"https://2captcha.com/res.php?key={API_KEY}&action=get&id={rid}&json=1"
            time.sleep(5)
            # print("aca")
            while True:
                r2 = requests.get(u2)
                print(f'first: {r2.json()}')
                if r2.json().get("status") == 1:
                    form_tokon_1 = r2.json().get("request")
                    return form_tokon_1
                elif r2.json().get("request") == "ERROR_CAPTCHA_UNSOLVABLE":
                    print("new request")
                    return call_api_captcha()
                time.sleep(5)
        form_tokon_1 = call_api_captcha()

        self.driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML="%s"'% form_tokon_1)
        sleep(1)
        submit = self.driver.find_element(By.XPATH,'//*[@id="login_user_form"]/div[2]/button')
        submit.click()



    def search_place(self):
        self.driver.get('https://www.portalinmobiliario.com/')
        sleep(uniform(2, 3))
        search = self.driver.find_element(By.XPATH,'//*[@id="location-autocomplete"]/div/label/div[1]/input')
        search.click()
        sleep(uniform(2, 3))
        for i in self.place:
            search.send_keys(i)
            sleep(uniform(0.05, 0.25))
        sleep(uniform(0.5, 1))

        select_option = self.driver.find_element(By.XPATH,'//*[@id="location-autocomplete"]/div/div/div/ul/li[1]')
        select_option.click()

        submit = self.driver.find_element(By.XPATH,'//*[@id="search-submit"]/button')
        submit.click()
        sleep(uniform(2, 5))

        try:
            today_publication = self.driver.find_element(By.XPATH,"//a//span[text()='Publicados hoy']")
            today_publication.click()
        except:
            pass

        try:
            particular_publication = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,"//a//span[text()='Particular']")))
            particular_publication.click()

        except:
            pass

        try:
            not_proyect_publication = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH,"//a//span[text()='Propiedades usadas']")))
            not_proyect_publication.click()
        except:
            pass

    
    def send_messages(self):
        try:
            next_page = self.driver.find_element(By.XPATH, "//div//div//section//div//ul//li//a//span[text()='Siguiente']")
            actions = ActionChains(self.driver)
            actions.move_to_element(next_page).perform()
            pages = int(self.driver.find_element(By.CSS_SELECTOR, '.andes-pagination__page-count').text.split(" ")[1])
        except Exception:
            pages = 1
        count = 0
        current_url = self.driver.current_url
        for i in range(pages):
            print(f"page: {i + 1}")
            div_pages = self.driver.find_elements(By.CSS_SELECTOR, '.ui-search-layout__item>div>div')
            page_links = list(map(lambda x: x.find_element(By.CSS_SELECTOR, 'div>a').get_attribute('href'), div_pages))
            # print(page_links)
            for element in page_links:
                property_link = element
                print(property_link)
                self.driver.get(property_link)
                # send message
                sleep(uniform(3, 4))
                try:
                    contact = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#questions_short_description > form > button > span')))
                    actions = ActionChains(self.driver)
                    actions.move_to_element(contact).perform()
                    contact.click()
                    count += 1
                    if count == 24:
                        print("24")
                    sleep(uniform(13, 14))
                    continue
                except:
                    pass

            if pages == 1:
                break
            self.driver.get(current_url)
            next_page = self.driver.find_element(By.XPATH, "//div//div//section//div//ul//li//a//span[text()='Siguiente']")
            actions = ActionChains(self.driver)
            actions.move_to_element(next_page).perform()
            next_page.click()
            sleep(uniform(2, 3))
            current_url = self.driver.current_url
            if count % 10 == 0:
                print(count)
        print(count)