"""
fn.py
Define functions
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

def download_wait(path_to_downloads):
    """
    From https://stackoverflow.com/questions/34338897/python-selenium-find-out-when-a-download-has-completed
    """
    seconds = 0
    dl_wait = True
    while dl_wait:
        time.sleep(15)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds


def find_by_day_elements(driver):
    """
    Capture all "headers" for pictures by day
    Returns dictionary of {day_as_string: select "all" button for that day}
    """
    select_all_by_day_buttons = \
        driver.find_elements_by_xpath("//div[@class='infinite-loader']//div[@class='section-header']/button[@class='count-select']")

    # If above returns an empty list, scroll/page down and try again until reach the bottom of the page
    # This ensures cases where a day's photos expand beyond full frame of the window, and thus the next
    # day's photo's are not yet loaded in the DOM
    while len(select_all_by_day_buttons) == 0:

        # Quit when you get to bottom of window
        window_position_before = int(driver.execute_script("return window.pageYOffset;"))
        # if window_position == window_height:
        #   exit
        # Scroll down 1 page
        html = driver.find_element_by_tag_name('html')
        html.send_keys(Keys.END)
        time.sleep(.5)
        window_position_after = int(driver.execute_script("return window.pageYOffset;"))
        if window_position_after == window_position_before: # Were already at bottom of page
            break

        select_all_by_day_buttons = \
            driver.find_elements_by_xpath("//div[@class='infinite-loader']//div[@class='section-header']/button[@class='count-select']")

    return select_all_by_day_buttons
