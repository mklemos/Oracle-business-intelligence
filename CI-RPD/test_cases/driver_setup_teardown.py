import socket
import time
import secrets
from format_filename_time import get_datetime_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Setup takes the driver to let the calling class know which session it's controlling
# at the time it's called. We then modify this session, based on host.
#

def driver_setup():
    server_hostname = "dwdb2-dev.humboldt.edu"
    
    if socket.gethostname() == server_hostname:
        # driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX) #dw-autotest-dev or localhost
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
             "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 "
             "(KHTML, like Gecko) Chrome/15.0.87"
             )
        #self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=dcap)
        driver.set_window_size(1920,1080)

        return driver

    else:
        driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX) #dw-autotest-dev or localhost

        return driver
