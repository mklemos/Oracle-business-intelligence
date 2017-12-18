# Documentation
### Sample docs
---
### Starting a Selenium Server
>Selenium is a browser automation tool, we'll be using the Selenium Python library to write scripts that navigate "headlessly" on the server. While, locally we'll be running selenium and launching an actual browser window on our machine to write and test our scripts.

#### Running Selenium on the server
Normally, the Selenium sever will start on boot with the server, however, for access to the location of the server and the driver look below:

###### Prerequisites:

* xvfb, selenium, and firefox are installed on DISPLAY:99
* Java version "1.7.0_101"
* Port 4444 is open
* A softlink created at /usr/bin/geckodriver to point to /usr/local/bin/geckodriver. It should work even if /usr/local/bin is not in the PATH of the Jenkins user
* Make sure you have access, speak with Ravi or any other sysadmin

#### Steps
1. Logon to server:     dw-autotest-dev.humboldt.edu
2. Selenium webdriver jar file is located: /opt/selenium/selenium-server-standalone-3.4.0.jar
3. Run command    ```java -jar .\selenium-server-standalone-3.4.0.jar```
4. View sessions at: http://dw-autotest-dev.humboldt.edu:4444/wd/hub - This port is good for viewing sessions starting and stopping.
---

#### Installing and Running Selenium locally

#### Steps
1. Download and install selenium server  
2. Using the node packet manager you can download this jar file here:   ```npm install selenium-server-standalone-jar@3.4.0```
3. Install locally, for example:    ```C:\selenium\selenium-server-standalone-3.4.0.jar```
   Be sure to add this to your Path variable.

**Pro tip**: Make sure that any other zombie selenium servers from past runs are killed via the task manager before you start a fresh run of the server. You will likely need admin access to your computer to kill these tasks. Ask for an elevation of your privileges if needed.

4. Run command:    ```java -jar .\selenium-server-standalone-3.4.0.jar```
5. View active sessions on the local Selenium server at:   http://localhost:4444/wd/hub

### Creating and Running a Selenium Test script
Selenium scripts can be written in a few languages, however, for this guide we will focus on Python.

Name the file with the word "test_" in the name, this will signify to the pytest framework that it is a test to be run.

At the start of each script ensure you've imported the libraries you will be using.

       import unittest

       import time

       import os.path

       import socket

       from selenium import webdriver

       from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

You'll want to ensure that you create a setup and teardown function at the beginning and end of each test.

Look to the ```test_a_setup_and_teardown.py``` as an example.



### Checking Selenium Test script results

Within a terminal window you will run the command:

 ```pytest .```

 This runs the entire directory of tests.

 Once the pytest framework collects and runs the tests it will output the results in the terminal that you started the tests in.
