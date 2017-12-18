import socket
import time
import secrets
from format_filename_time import get_datetime_path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

#Signs in a user to obi
def signin(driver, user_name):

    #Go to obitest login
    driver.get("https://obitest.humboldt.edu:9804/analytics/saw.dll?bieehome")

    #input User
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@name='Username']"))).send_keys(str(user_name))
    #input Password
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@name='pwd']"))).send_keys(secrets.userpass[str(user_name)])
    #click sign in
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@type='submit' and @value='Sign In']"))).click()
    #Sleep for a second to let sign in do its thing
    time.sleep(1)

#Clicks on the singout button in the top right of the page
def signout(driver):
    time.sleep(3) #This sleep is to make sure we dont get this test done so fast that obi think we are loging out while still retreaving data.
    try:
        #Trys to click on singout via xpath, if sucess we are done
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[contains(text(),'Sign Out')]"))).click()
    except:
        try:
            #If xpath fails try to click on sinout via css, if sucsess we are done
            WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#logout > span.HeaderMenuBarText > span"))).click()
        except:
            #If we failed to click via css after trying xpath we take a screenshot and try again to throw an exption failing the test
            path_name = get_datetime_path("obidev-intern-josh", "SignOutFAILURE")
            driver.save_screenshot(path_name)
            WebDriverWait(driver, 1).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#logout > span.HeaderMenuBarText > span"))).click()


def waitforload(driver, counter = 0):
    try:
        if counter < 120:
            time.sleep(1)
            WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[contains(text(),'Searching... To cancel, click')]")))
            counter = counter + 1
            waitforload(driver, counter)
        else:
            #Well we can find the loading thing but it has taken more then 2 minutes for the default querry so something is very broken.
            #TODO: Screenshot on this failurecase
            assert 1 == 2
    except:
        time.sleep(1)

#Clears all fields via using the reset button
def clearfields(driver, screenshot = False):

    #Wait for the defualt search to finish
    waitforload(driver)

    #Click on reset button
    try:
        #Try to click on reset via css
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@class='button' or @class='button buttonOver' and @name='reset']"))).click()
    except:
        #Try to click rest css if xpath fails
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "[name='reset']"))).click()
        if screenshot:
            path_name = get_datetime_path("obidev-intern-josh", "rest_fields_css_click")
            driver.save_screenshot(path_name)
    
    #Click on Clear all option
    try:
        #Try to click on clear all via xpath
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[contains(text(),'Clear All')]"))).click()
    except:
        #Try to click clear all css if xpath fails
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.floatingWindowDiv.contextMenu > div:nth-of-type(5) > table.ContextMenuOptionTable > tbody > tr > td.contextMenuOptionTextCell > span.contextMenuOptionText"))).click()
        if screenshot:
            path_name = get_datetime_path("obidev-intern-josh", "clear_fields_css_click")
            driver.save_screenshot(path_name)

    #Wait 3 seconds for the clear to finish
    time.sleep(3)


        

#Clicks on the gobtn then checks if we are searching or if we have already got our result
#Input: Driver, "Xpath of element we are searching for", (Optional) bool to enable screenshots
def clickgobtn(driver, xpath_to_search, screenshot = False):
    #Call our recersive gobtn helper with a counter starting at 0
    gobtn_helper(driver, xpath_to_search, 0, screenshot)

#This is our recersive gobtn press, it will try to press the button again if it detects that there was no search or if it is currently not searching
def gobtn_helper(driver, xpath_to_search, counter, screenshot):

    #Wait for 3 seconds to provent a "There is a pending request to the server" Error
    time.sleep(3)

    try:
        #Try to click on gobtn via css
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='button' or @class='button buttonOver' and @name='gobtn' or @value='Apply']"))).click()
    except:
        #Try to click gobtn css if xpath fails
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#gobtn"))).click()
        if screenshot:
            path_name = get_datetime_path("obidev-intern-josh", "gobtn_helper_css_click")
            driver.save_screenshot(path_name)
    try:
        #Can we find the xpath element that tells the user that the search is currently being preformed? If so move on and wait for our querry to finish like normal
        WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[contains(text(),'Searching... To cancel, click')]")))
        if screenshot:
            path_name = get_datetime_path("obidev-intern-josh", "gobtn_helper_loading")
            driver.save_screenshot(path_name)

    except:
        try:
            #Was the search fast enough that we can already see our results? If so move on now to the next part of the script as we are sure the gobtn worked
            WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.XPATH, xpath_to_search)))
            if screenshot:
                path_name = get_datetime_path("obidev-intern-josh", "gobtn_helper_check_element")
                driver.save_screenshot(path_name)
        except:
            #If we reach this point we can asume something went wrong with the gobtn press, so lets try this whole process again but with a max of 2 atempts
            if counter < 3:
                counter = counter + 1
                if screenshot:
                    path_name = get_datetime_path("obidev-intern-josh", "gobtn_helper_couter_triggerd")
                    driver.save_screenshot(path_name)
                gobtn_helper(driver, xpath_to_search, counter, screenshot)
            else:
                #Our test has failed lets take a screenshot and fail the test
                path_name = get_datetime_path("obidev-intern-josh", "gobtn_FAILURE")
                driver.save_screenshot(path_name)
                assert 2 == 1


# moreSearchHandler: This function modulizes the process of click on the search/more.. button you have on long drop down selections. It can handle mutiple things to select
# Input: driver, dropdown element, list of things we want selected
# Output: Nothing
# side efect: Selects everything in the more/search list we inputed on the dropdown element we inputed
def moreSearchHandler(driver, dropdownElement, list_to_search, screenshot = False):
    #Open our drop element
    dropdownElement.click()

    #Open the search/more... option
    try:
        #Try to open search/more.. option via css
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "div.floatingWindowDiv > div > div.DropDownSearch > span"))).click()
    except:
        #Try to open search/more.. option via xpath taking a screenshot to show we had to use xpath
        path_name = get_datetime_path("obidev", "search_more_except_xpath")
        driver.save_screenshot(path_name)
        WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='DropDownSearch' and @style='display: block;']"))).click()

    #Click the remove all button
    WebDriverWait(driver, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@title='Remove All']"))).click()

    for search_item in list_to_search:
        #Enter our string to search for into the search box
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchStringSearchEditBoxFieldWidth' and @name='choiceListSearchString']"))).send_keys(str(search_item))

        #Press the Search button
        try:
            #Via css
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#searchButton"))).click()
        except:
            #if css fails try xpath
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@type='button' and @name='searchButton' and @id='searchButton']"))).click()

        #wait for our search to finish by waiting for the searched element to be highlighted
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//span[@class='searchHighlightedText']"))).click()

        #Click move all button now that our search is done
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//td[@title='Move All']"))).click()

        #Screenshot for debuging if the function was handed a true as the last input
        if screenshot:
            path_name = get_datetime_path("obidev-intern-josh", search_item)
            driver.save_screenshot(path_name)

        #Clear the search field in preperation for the next test
        WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, "//input[@class='promptEditBoxField promptEditBoxFieldWidth promptSearchStringSearchEditBoxFieldWidth' and @name='choiceListSearchString']"))).clear()


    #click OK on the button of the More/search window element to finish our more/search selection
    driver.find_element_by_css_selector('[name="OK"]').click()
