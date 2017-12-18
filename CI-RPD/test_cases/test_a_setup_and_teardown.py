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

class test_a_setup_and_teardown(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def test_a_site(self):
        driver = self.driver
        self.driver.implicitly_wait(10) # seconds
        #Go to obitest login but dont actualy login
        self.driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?bieehome")

    def tearDown(self):
        # close the browser window
        self.driver.quit()


class test_b_login_and_logout(unittest.TestCase):

    def setUp(self):
        driver = driver_setup_teardown.driver_setup()
        self.driver = driver

    def test_a_login(self):
        #sign in using sign in abstraction
        user_signin.signin(self.driver, "Username")

    def tearDown(self):
        #signout
        user_signin.signout(self.driver)
        # close the browser window
        self.driver.quit()
