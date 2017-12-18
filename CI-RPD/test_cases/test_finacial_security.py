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

class test_finacial_trial_balance(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def test_finacial_security(self):

        driver = self.driver
        self.driver.implicitly_wait(7) #seconds

        user_signin.signin(driver, "Username")

        #go directly to 2.0.3 Financial Reports, Trial Balance
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?dashboard&PortalPath=%2Fshared%2F2.0%20-%20Finance%2F_portal%2F2.0.3%20-%20Financial%20Reports")

        #Sleep for 5 seconds to insure page loads before getting the dropdown, becuase its css it may grab the wrong dropdown becuase of how the page is loading on the emulated display
        time.sleep(5) 

        #Clear all fields
        user_signin.clearfields(driver)

        #Store dropdown for selecting fiscal year.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(3) > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["2016-2017"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)

        #Store dropdown for selecting Fund.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(2) > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > img.promptDropDownButton")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["Y1002"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)

        #Click apply to get our records we are asking for(gobtn)
        user_signin.clickgobtn(driver, "//td[contains(text(),'No Results')]")

        #Check the page for a no results error message(There should be one do to a lack of permisons on this acount)
        #This is using the dynamic wait inplace of just sleeping with a timeout with 120
        try:
            error_text = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'No Results')]"))).text
        except:
            driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/fin_security_failure_post_gotbn.png')
            error_text = WebDriverWait(driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'No Results')]"))).text

        str(error_text)

        assert error_text == "No Results"


    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
