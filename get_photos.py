from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# from bs4 import BeautifulSoup
# import re
# import pandas as pd
import os
import time
import fn


"""
Could try to navigate thusly:
https://www.amazon.com/photos/all?lcf=time&timeYear=2019&timeMonth=3
https://www.amazon.com/photos/all?lcf=time&timeYear={year}&timeMonth=3{month_num}
"""

base_url = f'https://www.amazon.com/photos/all'

save_path = r'C:\temp'

chromeOptions = Options()
chromeOptions.add_argument('disable_infobars')
chromeOptions.add_experimental_option('prefs', {'download.default_directory': save_path})
driver = webdriver.Chrome(chrome_options=chromeOptions)

skip_years =['2020'
             , '2019'
             , '2018'
            ]


skip_months = [
    'Jan',
    # 'Feb',
    # 'Mar',
    # 'Apr',
    # 'May',
    # 'Jun',
    # 'Jul',
    # 'Aug',
    # 'Sep',
    # 'Oct',
    # 'Nov'
            ]

# 1) Navigate to Amazon Photos Home Page
driver.get(base_url)

# login logic here...
driver.find_element_by_id('ap_email').send_keys('myemail@mail.com')
driver.find_element_by_id('ap_password').send_keys('Mypa33wr!d')
# driver.find_element_by_id('signInSubmit').click()
time.sleep(2)

# driver.find_elements_by_xpath("//span[text()='Date Taken']")

#  Expand to view all years under "Date Taken" Filter in left navbar
driver.find_elements_by_xpath\
    ("//div[@name='year-month-filter']/div"
     "/button[@class='show-more-button']")[0].click()

# Get all "Year" Buttons, loop over each
year_buttons = driver.find_elements_by_xpath("//div[@name='years']/ul/ul/li/button")
for year_button in year_buttons:
    current_year = year_button.text[:4] # Left 4 characters of YYYY### where ### is # of photos

    # Skip if year data already downloaded
    if current_year in skip_years:
        continue

    number_of_photos = year_button.text[4:]
    # Find button location - scroll to that
    button_x, button_y = year_button.location['x'], year_button.location['y']
    driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
    year_button.click()     # Will expand to display year by month taken

    time.sleep(.5)

    # Get all "by month" buttons.
    month_buttons = driver.find_elements_by_xpath("//div[@name='years']/ul/ul/li/ul/li/button")
    for month_button in month_buttons:
        # Find button location - scroll to that
        button_x, button_y = month_button.location['x'], month_button.location['y']
        driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
        current_month = month_button.text[:3]
        if current_month in skip_months:
            continue

        month_button.click()
        time.sleep(.5)

        days_list = fn.find_by_day_elements(driver=driver)

        time.sleep(.5)

        # Returns the buttons to click
        for day in days_list:

            # Find button location - scroll to that
            button_x, button_y = day.location['x'], day.location['y']
            driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')

            time.sleep(.5)
            day.click()

            # Now that we've scrolled, new "by day" rows may appear in the DOM, so check again
            current_days_list = fn.find_by_day_elements(driver=driver)
            for current_day in current_days_list:
                if current_day in days_list:
                    continue
                else:
                    days_list.append(current_day)


        time.sleep(2)
        # Now all are selected. Click "Download" button


        try:
            download_button = driver.find_element_by_class_name('download')
        except:
            # Couldn't Find download button - stop and find it manually
            time.sleep(2)
            download_button = driver.find_element_by_class_name('download')

        # Find button location - scroll to that
        button_x, button_y = download_button.location['x'], download_button.location['y']
        driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
        download_button.click()
        time.sleep(.5)

        # Check download directory for the new file. When it appears, rename by year_month, and continue
        default_filename = f'AmazonPhotos.zip'
        new_filename = f'AmazonPhotos_{current_year}_{current_month}.zip'

        download_time = fn.download_wait(save_path)
        print(f'Downloaded {current_month} {current_year}')
        time.sleep(1)

        # Rename "AmazonPhotos.zip" file
        os.rename(f'{save_path}\{default_filename}', f'{save_path}\{new_filename}')
        print(f'Downloaded Photos from {current_month}, {current_year}.')

moo = 'foo'



"""
Select all (appears after clicking first day of month:

//*[@id="photos"]/header/section/div/div[2]/div/button/span
** Button class = 'select-all'

--Then Download, spawns "Download Large number of files"

Xpath:
//*[@id="dialog-container"]/div[1]/div/aside

Button (1/n)
//*[@id="dialog-container"]/div[1]/div/aside/div/div/div[1]/div/div/div[2]/div[1]/button[2]

Button (2/n)
//*[@id="dialog-container"]/div[1]/div/aside/div/div/div[1]/div/div/div[2]/div[2]/button[2]

div class <download-link><button Class = "download>



"""