import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class OnlineShopTezt(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_shop_in_sample(self):
        user = "jaxew"
        pwd = "exterminatew00d"
        email = "jaxhappywood@yahoo.com"        
        driver = self.driver
        driver.get("https://shopmyown.herokuapp.com/accounts/signup/")
        # self.assertIn("Products", driver.title)
        elem = driver.find_element_by_id("id_username")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_email")
        elem.send_keys(email)
        elem = driver.find_element_by_id("id_password1")
        elem.send_keys(pwd)
        elem = driver.find_element_by_id("id_password2")
        elem.send_keys(pwd)
        elem = driver.find_element_by_xpath("//*[@id='signup_form']/button")
        elem.send_keys(Keys.RETURN)
        # driver.get("http://127.0.0.1:8000")
        time.sleep(60)
        assert "Logged In"

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
