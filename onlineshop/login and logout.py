import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class OnlineShopTezt(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_shop_in_sample(self):
        #This wont run until you input correct facebook username and password
        user = "admin"
        pwd = "nollywood"        
        driver = self.driver
        driver.get("https://shopmyown.herokuapp.com/accounts/login/")
        # self.assertIn("Products", driver.title)
        elem = driver.find_element_by_partial_link_text("Facebook")
        elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_id("email")
        elem.send_keys(user)
        elem = driver.find_element_by_id("pass")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        # elem = driver.find_element_by_id("continue")
        # elem.send_keys(Keys.RETURN)
        elem = driver.find_element_by_partial_link_text("logout")
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        elem = driver.find_element_by_xpath("/html/body/form/button")
        elem.send_keys(Keys.RETURN)
        time.sleep(20)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
