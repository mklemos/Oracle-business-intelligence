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


class test_finance_totals(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def test_finance_totals(self):
        driver = self.driver
        self.driver.implicitly_wait(7) # seconds

        #sign in using sign in abstraction
        user_signin.signin(driver, "Username")

        #Navigate the driver to the 2.0.1 General Fun
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?Dashboard&PortalPath=%2Fshared%2F2.0%20-%20Finance%2F_portal%2F2.0.1%20-%20General%20Fund&page=General%20Fund%20Expenditures")

        #Sleep for 5 seconds to insure page loads before getting the dropdown, becuase its css it may grab the wrong dropdown becuase of how the page is loading on the emulated display
        time.sleep(5)

        #Clear fields via clear fields abstraction
        user_signin.clearfields(driver)

        #Open dropdown for selecting Fiscal Year.
        dropdownyear = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:first-child > table > tbody > tr:first-child > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))

        #create a list of elements we want to select in our dropdown
        list_to_search_year = ["2015-2016"]

        user_signin.moreSearchHandler(driver, dropdownyear, list_to_search_year)

        #get dropdown for mbu
        dropdownMBU = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:first-child > table > tbody > tr:nth-of-type(3) > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))

        #create a list of elements we want to select in our dropdown
        list_to_search_MBU = ["ACADEMIC AFFAIRS - VP"]

        user_signin.moreSearchHandler(driver, dropdownMBU, list_to_search_MBU)


        #get dropdown for department
        dropdownMBU = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:first-child > table > tbody > tr:nth-of-type(4) > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))

        #create a list of elements we want to select in our dropdown(This time we dont want to select anything, only remove so we have an empty list)
        emptylist = []

        user_signin.moreSearchHandler(driver, dropdownMBU, emptylist)

        # #Click apply to get our records we are asking for(gobtn)
        user_signin.clickgobtn(driver, "//a[contains(text(),'1,435,290.56')]", True)

        #Dynamic wait for our element with a max time of 120 seconds, then we store that element[HM500 - OPERATING FUND | 601 - Regular Salaries and Wages]
        try:
            actuals = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[contains(text(),'1,435,290.56')]"))).text
        except:
            path_name = get_datetime_path("obidev-intern-josh", "test_finance_totals_FAILURE")
            driver.save_screenshot(path_name)
            actuals = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[contains(text(),'1,435,290.56')]"))).text

        # Casting this variable to a string because it is brought in as UNICODE type.
        str(actuals)

        #verify that amount is the known correct value 1,435,290.56.
        assert actuals == "1,435,290.56"

    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
