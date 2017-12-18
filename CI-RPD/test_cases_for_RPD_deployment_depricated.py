#!/usr/bin/env python
import unittest
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class test_finance_totals(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_finance_totals(self):
        driver = self.driver
        self.driver.implicitly_wait(10) # seconds
        #Go to obitest login
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/gotoobi.png')
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?bieehome")
        time.sleep(2)

        #input User
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/user.png')
        time.sleep(1)
        user_element = self.driver.find_element_by_name('Username')
        time.sleep(1)
        user_element.send_keys("Username")
        time.sleep(1)

        #input Password
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/pass.png')
        psw_element = self.driver.find_element_by_name('pwd')
        psw_element.send_keys("pwd")
        time.sleep(2)

        #click sign in
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/sign_in.png')
        sign_in_button = self.driver.find_element_by_xpath("//input[@type='submit' and @value='Sign In']")
        sign_in_button.click()
        time.sleep(2)

        #Click on general fund thorugh dashboard dropdown in the upper right corner of the application.
        self.driver.find_element_by_css_selector("#dashboard > span.HeaderMenuBarText.HeaderMenuNavBarText > span").click()
        time.sleep(2)
        self.driver.find_element_by_link_text("2.0.1 - General Fund").click()
        time.sleep(2)

        #Check boxes in dropdown for fiscal year "2015-2016".
        self.driver.find_element_by_css_selector("tr > td:first-child > table > tbody > tr:first-child > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(15) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(14) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)

        #Check the MBU (current)
        self.driver.find_element_by_css_selector("tr > td:first-child > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.floatingWindowDiv > div > div.DropDownValueList > div:nth-of-type(3) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()

		#deselect the D10001 from department (current)
        self.driver.find_element_by_css_selector("tr > td:first-child > table > tbody > tr:nth-of-type(4) > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(2) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()

		#Click go
        self.driver.find_element_by_css_selector("#gobtn").click()
        time.sleep(2)

        # Store actuals value in spreadsheet into this variable.
        actuals = self.driver.find_element_by_css_selector("tbody > tr:nth-of-type(3) > td:nth-of-type(5)").text
        time.sleep(2)

        # Casting this variable to a string because it is brought in as UNICODE type.
        str(actuals)

        #Screenshot of the final page before test ends.
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/actuals.png')
        time.sleep(2)

        #verify that amount is the known correct value 1,772,536.42.
        assert actuals == "1,772,536.42"
        time.sleep(2)
        self.driver.find_element_by_css_selector("#logout > span.HeaderMenuBarText > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("td > a").click()

    def tearDown(self):
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
