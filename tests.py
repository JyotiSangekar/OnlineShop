import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class OnlineShopTezt(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_shop_in_sample(self):
        user = "admin"
        pwd = "nollywood"        
        driver = self.driver
        driver.get("http://127.0.0.1:8000/accounts/login/")
        # self.assertIn("Products", driver.title)
        elem = driver.find_element_by_id("id_login")
        elem.send_keys(user)
        elem = driver.find_element_by_id("id_password")
        elem.send_keys(pwd)
        elem.send_keys(Keys.RETURN)
        # driver.get("http://127.0.0.1:8000")
        time.sleep(8)
        assert "Logged In"
        driver.get("http://127.0.0.1:8000/1/panties/")
        elem = driver.find_element_by_xpath("/html/body/div[2]/div/form/input[3]").click()
        time.sleep(5)
        assert "Goods added to cart"
        elem = driver.find_element_by_xpath("/html/body/div[2]/p/a[2]").click()
        time.sleep(5)
        firstname = "Apurva"
        lastname = "Chimbili"
        email = "apurvachimbili@gmail.com"
        address = "929 S 70th Plaza, Apt 28"
        postalcode = "68106"
        city = "Omaha"
        elem = driver.find_element_by_id("id_first_name")
        elem.send_keys(firstname)
        elem = driver.find_element_by_id("id_last_name")
        elem.send_keys(lastname)
        elem = driver.find_element_by_id("id_email")
        elem.send_keys(email)
        elem = driver.find_element_by_id("id_address")
        elem.send_keys(address)
        elem = driver.find_element_by_id("id_postal_code")
        elem.send_keys(postalcode)
        elem = driver.find_element_by_id("id_city")
        elem.send_keys(city)
        elem = driver.find_element_by_xpath("/html/body/div[2]/form/p[7]/input")
        elem.send_keys(Keys.RETURN)
        time.sleep(10)
        elem = driver.find_element_by_xpath("/html/body/div[2]/form/input[13]")
        elem.send_keys(Keys.RETURN)
        time.sleep(60)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
