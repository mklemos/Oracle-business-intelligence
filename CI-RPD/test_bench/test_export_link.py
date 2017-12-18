#!/usr/bin/env python
import unittest
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class test_export_link(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_export_link(self):
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

        #Click on general fund through dashboard dropdown in the upper right corner of the application.
        self.driver.find_element_by_css_selector("#dashboard > span.HeaderMenuBarText.HeaderMenuNavBarText > span").click()
        time.sleep(2)

		    #Go to correct dashboard
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/general_fund_link.png')
        self.driver.find_element_by_link_text("2.0.1 General Fund").click()
        time.sleep(2)

		    #Select the fiscal year dropdown
        self.driver.find_element_by_css_selector("tr > td:first-child > table > tbody > tr:first-child > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton").click()
        time.sleep(2)

		    #Deselect year 2017-2018
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:first-child > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)

		    #Select year 2016-2017
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(16) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)

		    #Click apply to set fields
        self.driver.find_element_by_css_selector("#gobtn").click()
        time.sleep(2)

		    #select export at bottom of page
        self.driver.find_element_by_css_selector("div.ViewContent > table > tbody > tr > td:nth-of-type(3) > a").click()

		    #Select Excel 2007+
        self.driver.find_element_by_css_selector("body > div:nth-of-type(10) > table.menuShadowWrapper > tbody > tr:first-child > td.shadowMenuCell > a:nth-of-type(2) > table.MenuItemTable > tbody > tr > td.MenuItemTextCell").click()

		    #Check to see if file exists
        os.path.exists("Downloads\General Fund Journal.xlsx")

    def tearDown(self):
        # close the browser window
        self.driver.quit()
        
if __name__ == '__main__':
    unittest.main()
