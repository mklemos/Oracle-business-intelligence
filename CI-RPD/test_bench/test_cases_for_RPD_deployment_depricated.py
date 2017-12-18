#!/usr/bin/env python
import unittest
import time
import os.path
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class test_operating_fund_orig_budge(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_operating_fund_orig_budge(self):
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
        self.driver.find_element_by_css_selector("#gobtn").click()
        time.sleep(2)

        # Store value in spreadsheet into this variable.
        operating_fund_orig_budge = self.driver.find_element_by_css_selector("td.PTChildPivotTable > table > tbody > tr:nth-of-type(3) > td:nth-of-type(3)").text
        time.sleep(2)

        # Casting this variable to a string because it is brought in as UNICODE type.
        str(operating_fund_orig_budge)

        #Screenshot of the final page before test ends.
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/latest.png')
        time.sleep(2)

        #verify that amount is the known correct value 644,238.00.
        assert operating_fund_orig_budge == "644,238.00"
        time.sleep(2)
        self.driver.find_element_by_css_selector("#logout > span.HeaderMenuBarText > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("td > a").click()

    def tearDown(self):
        # close the browser window
        self.driver.quit()


class test_PI_role_row_level(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_PI_role_row_level(self):
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
        self.driver.find_element_by_link_text("2.0.0 Chartfields and Vendors").click()
        time.sleep(2)

        #Click on the Departments tab
        self.driver.find_element_by_css_selector("tr > td:nth-of-type(2) > table.tabContainer > tbody > tr > td.secondaryTabEnabled > span").click()
        time.sleep(2)

        #locate the fiscal year option and click
        self.driver.find_element_by_css_selector("img.promptDropDownButton").click()
        time.sleep(2)
        #deselect the 2017 fiscal year
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(14) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)
        #select the fiscal year "2016"
        self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(13) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)

        #select the dropdown for Dept_ID (Point in Time)
        self.driver.find_element_by_css_selector("tr > td:nth-of-type(2) > table > tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div:first-child > img.promptComboBoxButtonMoz").click()
        time.sleep(2)
        #select the proper dept_ID
        self.driver.find_element_by_css_selector("div.floatingWindowDiv > div > div.DropDownValueList > div:nth-of-type(4) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        time.sleep(2)
        #Click apply to set fields
        self.driver.find_element_by_css_selector("#gobtn").click()
        time.sleep(2)
        #Check to make sure that the presidents office is the only dept left
        presidents_office = self.driver.find_element_by_css_selector("td.PTChildPivotTable > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)").text
        str(presidents_office)
        time.sleep(2)
        assert presidents_office == "PRESIDENT'S OFFICE"
        time.sleep(2)
        self.driver.find_element_by_css_selector("#logout > span.HeaderMenuBarText > span").click()
        time.sleep(2)
        self.driver.find_element_by_css_selector("td > a").click()


    def tearDown(self):
        # close the browser window
        self.driver.quit()

class test_print_link(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)

    def test_print_link(self):
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

		#Select print button at bottom of page
        self.driver.find_element_by_css_selector("div.ViewContent > table > tbody > tr > td:nth-of-type(1) > a").click()
        time.sleep(2)

		#select "Printable PDF"
        self.driver.find_element_by_css_selector("body > div:nth-of-type(9) > table.menuShadowWrapper > tbody > tr:first-child > td.shadowMenuCell > a:first-child > table.MenuItemTable > tbody > tr > td.MenuItemTextCell").click()
        time.sleep(2)

		#Check to see if file exists
        os.path.exists("/Downloads/Untitled Analysis.pdf")
		########################################## EXPORT

		# #select export at bottom of page
		# self.driver.find_element_by_css_selector("div.ViewContent > table > tbody > tr > td:nth-of-type(3) > a").click()

		# #Select Excel 2007+
		# self.driver.find_element_by_css_selector("body > div:nth-of-type(10) > table.menuShadowWrapper > tbody > tr:first-child > td.shadowMenuCell > a:nth-of-type(2) > table.MenuItemTable > tbody > tr > td.MenuItemTextCell").click()

		# #Check to see if file exists
		# os.path.exists("Downloads\General Fund Journal.xlsx")

		######################################################

        # #Click on the Departments tab
        # self.driver.find_element_by_css_selector("tr > td:nth-of-type(2) > table.tabContainer > tbody > tr > td.secondaryTabEnabled > span").click()
        # time.sleep(2)

        # #locate the fiscal year option and click
        # self.driver.find_element_by_css_selector("img.promptDropDownButton").click()
        # time.sleep(2)
        # #deselect the 2017 fiscal year
        # self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(14) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        # time.sleep(2)
        # #select the fiscal year "2016"
        # self.driver.find_element_by_css_selector("div.DropDownValueList > div:nth-of-type(13) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        # time.sleep(2)

        # #select the dropdown for Dept_ID (Point in Time)
        # self.driver.find_element_by_css_selector("tr > td:nth-of-type(2) > table > tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div:first-child > img.promptComboBoxButtonMoz").click()
        # time.sleep(2)
        # #select the proper dept_ID
        # self.driver.find_element_by_css_selector("div.floatingWindowDiv > div > div.DropDownValueList > div:nth-of-type(4) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton").click()
        # time.sleep(2)
        # #Click apply to set fields
        # self.driver.find_element_by_css_selector("#gobtn").click()
        # time.sleep(2)
        # #Check to make sure that the presidents office is the only dept left
        # presidents_office = self.driver.find_element_by_css_selector("td.PTChildPivotTable > table > tbody > tr:nth-of-type(3) > td:nth-of-type(4)").text
        # str(presidents_office)
        # time.sleep(2)
        # assert presidents_office == "PRESIDENT'S OFFICE"
        # time.sleep(2)
        # self.driver.find_element_by_css_selector("#logout > span.HeaderMenuBarText > span").click()
        # time.sleep(2)
        # self.driver.find_element_by_css_selector("td > a").click()


    def tearDown(self):
        # close the browser window
        self.driver.quit()

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
