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

    def test_finacial_trial_balance(self):

        driver = self.driver
        self.driver.implicitly_wait(7) #seconds

        #sign in using sign in abstraction
        user_signin.signin(driver, "Username")

        #go directly to 2.0.3 Financial Reports, Trial Balance
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?dashboard&PortalPath=%2Fshared%2F2.0%20-%20Finance%2F_portal%2F2.0.3%20-%20Financial%20Reports")

        #Sleep for 5 seconds to insure page loads before getting the dropdown, becuase its css it may grab the wrong dropdown becuase of how the page is loading on the emulated display
        time.sleep(5) 

        #Store dropdown for selecting fiscal year.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(3) > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > input.promptTextField.promptTextFieldReadOnly")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["2016-2017"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)


        #Store dropdown for selecting fund year.
        dropdown = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(2) > table > tbody > tr > td > table > tbody > tr:nth-of-type(2) > td > span > span.data.promptControlNarrowView > div > div.promptChoiceListBox > input.promptTextField.promptTextFieldReadOnly.textFieldHelper")))
        #create a list of elements we want to select in our dropdown
        list_to_select = ["N4500"]
        #use moreSearchHandler abstraction to do de selects and selects
        user_signin.moreSearchHandler(driver, dropdown, list_to_select)

        #Click apply to get our records we are asking for(gobtn)
        user_signin.clickgobtn(driver,"//td[contains(text(),'(50,631.00)')]")

        #Copy Reveniue Total Using dynamic wait with maximum time of 120
        #rev_total = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@class='TTHT PTHT OORT' and @id='e_saw_2609_c_1_2_5']"))).text
        #rev_total = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'(50,631.00)') and @id='e_saw_2609_c_1_2_5']"))).text
        rev_total = WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr:nth-of-type(8) > td.TTHT.PTHT.PTLC.OORT"))).text
        #Copy Expendetures total Using dynamic wait
        #exp_total = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@class='TTHT PTHT OORT' and @id='e_saw_2609_c_1_2_20']"))).text
        #exp_total = WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),'50,631.00') and @id='e_saw_2609_c_1_2_20']"))).text
        exp_total = WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr:nth-of-type(23) > td.TTHT.PTHT.PTLC.OORT"))).text


        time.sleep(2)
        str(rev_total)
        str(exp_total)
        rev_total_stripped = rev_total.strip("()")
        exp_total_stripped = exp_total.strip("()")
        try:
            assert rev_total_stripped == exp_total_stripped
        except:
            path_name = get_datetime_path("obidev-intern-josh", "finacial_trial_bal_FAILURE")
            driver.save_screenshot(path_name)
            assert rev_total_stripped == exp_total_stripped


    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
