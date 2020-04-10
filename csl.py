import selenium
from selenium import webdriver
import time
import random
import yaml

class User:
    def __init__(self, name):
        self.name = name

class Users:
    def __init__(self, u, p, url):
        #driver
        c_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        c_options.add_experimental_option("prefs", prefs)
        c_options.add_argument("--headless")
        self.driver = webdriver.Chrome(chrome_options=c_options)

        #login
        self.driver.get(url)
        nameBox = self.driver.find_element_by_id("username")
        passwordBox = self.driver.find_element_by_id("password")
        nameBox.send_keys(u)
        passwordBox.send_keys(p)
        loginButton = self.driver.find_element_by_xpath('//*[@value="Belépés"]')
        loginButton.click()
        time.sleep(1)

        #get users
        self.driver.get(url+"/Home/OnlineUsers")
        self.users = []
        data = self.driver.find_elements_by_class_name("onlineuser")
        for i in data:
            name = i.find_element_by_class_name("data").find_element_by_class_name("name").find_element_by_tag_name("a").text
            self.users.append(User(name))

    def SelectRandom(self):
        i = random.randrange(0, len(self.users))
        return self.users[i]

if __name__ == "__main__":
    secret = None
    with open("./secret.yaml", "r") as f:
        secret = yaml.load(f.read(), Loader=yaml.CLoader)

    t = Users(secret["username"], secret["password"], secret["url"])
    print("A kiválasztott: ", t.SelectRandom().name)