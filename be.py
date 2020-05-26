import time
import Url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
from dotenv import load_dotenv

project_folder = os.path.expanduser('/Users/glenfordnunez/Documents/GitHub/BeAp/')
load_dotenv(os.path.join(project_folder, '.env'))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1420,1080')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

b = webdriver.Chrome(chrome_options=chrome_options)
# b = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)
# '/usr/local/bin/chromedriver'

b.implicitly_wait(10)

# Without being logged in. Go to job search page and enter reginon
#  and positon that you are applying for.
# Click login and copy URL when you get to Adobe login page.
# This URL is for graphic design jobs in Baltimore.
# created a module to put URL in seperate file.
# because the Adobe Login URL's are dumb long!

website = Url.br
# Login Credentials
email = os.getenv('BE_EMAIL')
password = os.getenv('BE_PASSWORD')

def site_login(ws, e, p):
    b.get(ws)
    b.find_element_by_id("EmailPage-EmailField").send_keys(e)
    b.find_element_by_xpath("//form[@id='EmailForm']/section[2]/div[2]/button/span").click()
    b.find_element_by_xpath("//form[@id='PasswordForm']/section/div/div/input").send_keys(p)
    b.implicitly_wait(30)
    b.find_element_by_xpath("//form[@id='PasswordForm']/section[2]/div[2]/button/span").click()


def scroll_to_bottom():
    # Scroll to bottom to get all job listings
    b.maximize_window()
    SCROLL_PAUSE_TIME = 2

    # Get scroll height
    last_height = b.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        b.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = b.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def apply(s, f):
    for i in range(s, f):
        try:
            scroll_to_bottom()
            jobPostMore = b.find_element(By.XPATH, "//li[" + str(i + 5) + "]/div/a")
            actions = ActionChains(b)
            actions.move_to_element(jobPostMore).perform()
            jobPost = b.find_element(By.XPATH, "//li[" + str(i) + "]/div/a")
            # p= jobPost.location();
            actions.move_to_element(jobPost).perform()
            b.implicitly_wait(12)
            postTest = "//li[" + str(i) + "]/div/a"
            actions.move_to_element(jobPostMore).click().perform()
            actions.move_to_element(b.find_element(By.XPATH, postTest)).click().perform()
            # if apply button is displayed then do this stuff
            if b.find_element_by_xpath("//div[2]/button/div/div").is_displayed():
                ActionChains(b).move_to_element(jobPost).perform()
                jobApply = b.find_element_by_xpath("//div[2]/button/div/div")
                jobApply.click()
                jobConfirm = b.find_element_by_xpath("//div[3]/div/button/div/div")
                jobConfirm.click()
                exitOut = b.find_element_by_css_selector(".Overlay-closeIcon-2jb")
                exitOut.click()
                ActionChains(b).move_to_element(jobPost).perform()
                b.implicitly_wait(12)
                # I print this to show what jobs were applied for.
                # I could export this to a file but I want to see in real time.
                print(i)

        # close pop-up if there is no apply button
        except NoSuchElementException:
            exitOut = b.find_element_by_css_selector(".Overlay-closeIcon-2jb")
            exitOut.click()
            ActionChains(b).move_to_element(jobPostMore).perform()
    # Close Browser
    b.close()


site_login(website, email, password)

# The job search page is numbered from 1 - max job postings on that page.
# Range of jobs jobs you want to apply for starting number and ending number.
# Bug allert. Job starting number is 6 for now becuase when it starts at "1"
# It opens the project editor for some reason.

apply(6, 100)
