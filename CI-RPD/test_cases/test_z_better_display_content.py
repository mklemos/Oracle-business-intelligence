#!/usr/bin/env python
import unittest
import time
from format_filename_time import get_datetime_path
import os.path
import socket
import user_signin
import driver_setup_teardown
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#modeled after test_operating_fund_orig_budge using xpath instead of css selectors
# I know that for the year fiscal year of 2015-2016 the operating fund budget is
# 644,238.00, this test knows to verify that amount.


class test_z_better_display_content(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def test_z_better_display_content(self):
        driver = self.driver
        #self.driver.implicitly_wait(10) # seconds

        #sign in using sign in abstraction
        user_signin.signin(driver, "Username")

        # go directly to general fund dashboard.
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?dashboard&PortalPath=%2Fshared%2F2.0%20-%20Finance%2F_portal%2F2.0.1%20-%20General%20Fund")

        #Sleep for 5 seconds to insure page loads before getting the dropdown, becuase its css it may grab the wrong dropdown becuase of how the page is loading on the emulated display
        time.sleep(5)

        #Clear fields via clear fields abstraction
        user_signin.clearfields(driver)

        #Store dropdown for selecting fiscal year.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:first-child > table > tbody > tr:first-child > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["2015-2016"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)

        #Store dropdown for selecting Department year.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:first-child > table > tbody > tr:nth-of-type(4) > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["D10001"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)



        #Click apply to get our records we are asking for(gobtn)
        user_signin.clickgobtn(driver,"//td[contains(text(),'644,238.00')]", True)

        # Store known value '644,238.00' in spreadsheet into variable.
        try:
            time.sleep(1)
            operating_fund_orig_budge = WebDriverWait(driver, 240).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'644,238.00')]"))).text
            time.sleep(1)
        except:
            path_name = get_datetime_path("obidev-intern-max", "operating_fund_orig_budge")
            self.driver.save_screenshot(path_name)
            operating_fund_orig_budge = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'644,238.00')]"))).text
            self.driver.save_screenshot(path_name)

        # Casting this variable to a string because it is brought in as UNICODE type.
        str(operating_fund_orig_budge)

        #verify that amount is the known correct value 644,238.00.A
        assert operating_fund_orig_budge == "644,238.00"


    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
