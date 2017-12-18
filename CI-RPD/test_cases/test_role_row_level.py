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

class test_PI_role_row_level(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def moreSearchHandler(self, driver, dropdownElement, list_to_search):
        #Open our drop element
        dropdownElement.click()

        #Open the search/more... option
        try:
            # path_name = get_datetime_path("obidev-intern-max", "search_more_try_css_role_row")
            # driver.save_screenshot(path_name)
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.floatingWindowDiv > div > div.DropDownSearch > span"))).click()
        except:
            path_name = get_datetime_path("obidev-intern-max", "search_more_try_xpath_role_row")
            driver.save_screenshot(path_name)
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='DropDownSearch' and @style='display: block;']"))).click()

        #Click the remove all button
        driver.find_element_by_xpath("//td[@title='Remove All']").click()

        for search_item in list_to_search:
            #Enter our string to search for into the search box
            #driver.find_element_by_xpath("//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchStringSearchEditBoxFieldWidth' and @name='choiceListSearchString']").send_keys(str(search_item))
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchNumericalSearchEditBoxFieldWidth' and @name='numericSearchValue_1']"))).send_keys(str(search_item))

            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchNumericalSearchEditBoxFieldWidth' and @name='numericSearchValue_2']"))).send_keys(str(search_item))

            #Press the Search button
            #driver.find_element_by_xpath("//input[@type='button' and @name='searchButton' and @id='searchButton']").click()
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@type='button' and @name='searchButton' and @id='searchButton']"))).click()


            #Click move all button
            #driver.find_element_by_xpath("//td[@title='Move All']").click()
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@title='Move All']"))).click()

            #Clear search field
            #driver.find_element_by_xpath("//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchStringSearchEditBoxFieldWidth' and @name='choiceListSearchString']").clear()
            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchNumericalSearchEditBoxFieldWidth' and @name='numericSearchValue_1']"))).clear()

            WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchNumericalSearchEditBoxFieldWidth' and @name='numericSearchValue_2']"))).clear()
        #click OK on the button of the More/search window element
        driver.find_element_by_css_selector('[name="OK"]').click()


    def test_PI_role_row_level(self):
        # Normal abstraction does not work here we need anothr function to handle the "date" and dept style moreSearchHandler

        driver = self.driver
        self.driver.implicitly_wait(7) #seconds

        #sign in using sign in abstraction
        user_signin.signin(driver, "Username")

        #go directly to 2.0.0 Chartfields and Vendors dashboard
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?dashboard&PortalPath=%2Fshared%2F2.0%20-%20Finance%2F_portal%2F2.0.0%20Chartfields%20and%20Vendors")

        #Click on the Departments tab
        try:
            WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(2) > table.tabContainer > tbody > tr > td.secondaryTabEnabled > span"))).click()
        except:
            WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Departments')]"))).click()

        #Sleep a bit to insure the departments tab has loaded
        time.sleep(5)

        #Open dropdown for selecting Fiscal Year.
        try:
            dropdownyear = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div.promptChoiceListBox > input.promptTextField.promptTextFieldReadOnly")))
        except:
            dropdownyear = WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div.promptChoiceListBox > img.promptDropDownButton")))


        #create a list of elements we want to select in our dropdown
        list_to_search_year = ["2016"]

        self.moreSearchHandler(driver, dropdownyear, list_to_search_year)

        #select the dropdown for Dept_ID (Point in Time)
        WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(2) > table > tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div:first-child > img.promptComboBoxButtonMoz"))).click()
        #select the proper dept_ID "D10001"
        try:
            WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='checkboxRadioButton' and @value='D10001']"))).click()
        except:
            try:
                WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.floatingWindowDiv > div > div.DropDownValueList > div:nth-of-type(4) > div.promptDropdownNoBorderDiv > input.checkboxRadioButton"))).click()
            except:
                WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".floatingWindowDiv > div:nth-child(1) > div:nth-child(2) > div:nth-child(4)"))).click()

        #de-select the dropdown for Dept_ID (Point in Time)
        WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "tr > td:nth-of-type(2) > table > tbody > tr:first-child > td:nth-of-type(2) > table > tbody > tr > td.data.promptControl > div > div:first-child > img.promptComboBoxButtonMoz"))).click()

        #Screenshot before gobtn
        self.driver.save_screenshot('/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/PI_test_before_click_apply.png')

        #Click apply to get our records we are asking for(gobtn)
        user_signin.clickgobtn(driver, "//td[contains(text(),\"PRESIDENT'S OFFICE\")]")


        #Check to make sure that the presidents office is the department we got
        try:
            WebDriverWait(driver, 120).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),\"PRESIDENT'S OFFICE\")]")))
        except:
            path_name = get_datetime_path("obidev-intern-josh", "role_row_FAILURE")
            driver.save_screenshot(path_name)
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[contains(text(),\"PRESIDENT'S OFFICE\")]")))

        #We found presidents office so pass via a assertion
        assert 2 == 2

    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()
