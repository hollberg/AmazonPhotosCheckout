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

# 1) Navigate to Amazon Photos Home Page

driver.get(base_url)


# login logic here...
driver.find_element_by_id('ap_email').send_keys('myemail@mail.com')
driver.find_element_by_id('ap_password').send_keys('Mypa33wr!d')
# driver.find_element_by_id('signInSubmit').click()

time.sleep(2)


years = list(range(2011,2020))
months = list(range(1,13))

for year in years:
    for month in months:
        url = f'https://www.amazon.com/photos/all?lcf=time&timeYear={year}&timeMonth={month}'
        driver.get(url=url)

        time.sleep(5)


        days_list = fn.find_by_day_elements(driver=driver)

        time.sleep(.5)

        if len(days_list) == 0: # No photos for this month
            continue
        else:
            first_day = days_list[0]



        # Find button location - scroll to that
        button_x, button_y = first_day.location['x'], first_day.location['y']
        driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')

        time.sleep(.5)
        # Select all pictures for first day. Will cause a "Select All" button to appear
        first_day.click()

        select_all_button = driver.find_elements_by_xpath("//header[@class='selection-header']//button[@class='select-all']")
        try:
            select_all_button[0].click()
        except:
            pass

        # Get Download Button
        download_button = driver.find_elements_by_xpath("//header[@class='selection-header']//button[@class='download']")
        download_button[0].click()

        # Spawns a new download window (or might)
        download_buttons = \
            driver.find_elements_by_xpath("//div[@class='dialog-content']//div[@class='download-link']/button[@class='download']")

        number_of_downloads = len(download_buttons)
        if number_of_downloads == 0:    # Didn't spawn multiple download window - can just click top download button

            # Check download directory for the new file. When it appears, rename by year_month, and continue
            default_filename = f'AmazonPhotos.zip'
            new_filename = f'AmazonPhotos_{year}_{month}.zip'

            download_time = fn.download_wait(save_path)
            print(f'Downloaded {month} {year}')
            time.sleep(1)

            # Rename "AmazonPhotos.zip" file
            os.rename(f'{save_path}\{default_filename}', f'{save_path}\{new_filename}')
            print(f'Downloaded Photos from {month}, {year}.')

        else:   # Launched window with multiple download buttons
            for i, dl_button in enumerate(download_buttons):
                dl_button.click()

                # Check download directory for the new file. When it appears, rename by year_month, and continue
                default_filename = f'AmazonPhotos.zip'
                new_filename = f'AmazonPhotos_{year}_{month}_{str(i+1)}_of_{number_of_downloads}.zip'

                download_time = fn.download_wait(save_path)
                print(f'Downloaded {month} {year} #{i+1}/{number_of_downloads}')
                time.sleep(1)

                # Rename "AmazonPhotos.zip" file
                os.rename(f'{save_path}\{default_filename}', f'{save_path}\{new_filename}')
                print(f'Downloaded Photos from {month}, {year}.')

            # When all items are downloaded, click the "Close" button on the
            # "Download large number of files" popup window
            close_button = driver.find_elements_by_xpath("//div[@id='dialog-container']//button[@class='close-downloader']")
            close_button[0].click()

#
#
# skip_years = ['2020'
#               ,'2019'
#               ,'2018'
#               ,'2017'
#               ]
#
# skip_months = [
#     'Jan',
#     'Feb',
#     # 'Mar',
#     # 'Apr',
#     # 'May',
#     # 'Jun',
#     # 'Jul',
#     # 'Aug',
#     # 'Sep',
#     # 'Oct',
#     # 'Nov'
# ]
#
#
#
# # driver.find_elements_by_xpath("//span[text()='Date Taken']")
#
# #  Expand to view all years under "Date Taken" Filter in left navbar
# driver.find_elements_by_xpath\
#     ("//div[@name='year-month-filter']/div"
#      "/button[@class='show-more-button']")[0].click()
#
# # Get all "Year" Buttons, loop over each
# year_buttons = driver.find_elements_by_xpath("//div[@name='years']/ul/ul/li/button")
# for year_button in year_buttons:
#     current_year = year_button.text[:4]  # Left 4 characters of YYYY### where ### is # of photos
#
#     # Skip if year data already downloaded
#     if current_year in skip_years:
#         continue
#
#     number_of_photos = year_button.text[4:]
#     # Find button location - scroll to that
#     button_x, button_y = year_button.location['x'], year_button.location['y']
#     driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
#     year_button.click()  # Will expand to display year by month taken
#
#     time.sleep(.5)
#
#     # Get all "by month" buttons.
#     month_buttons = driver.find_elements_by_xpath("//div[@name='years']/ul/ul/li/ul/li/button")
#     for month_button in month_buttons:
#         # Find button location - scroll to that
#         button_x, button_y = month_button.location['x'], month_button.location['y']
#         driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
#         current_month = month_button.text[:3]
#         if current_month in skip_months:
#             continue
#
#         month_button.click()
#         time.sleep(.5)
#
#         days_list = fn.find_by_day_elements(driver=driver)
#
#         time.sleep(.5)
#
#         first_day = days_list[0]
#
#
#
#         # Find button location - scroll to that
#         button_x, button_y = first_day.location['x'], first_day.location['y']
#         driver.execute_script(f'window.scrollTo({button_x}, {button_y - 125})')
#
#         time.sleep(.5)
#         # Select all pictures for first day. Will cause a "Select All" button to appear
#         first_day.click()
#
#         select_all_button = driver.find_elements_by_xpath("//header[@class='selection-header']//button[@class='select-all']")
#         select_all_button[0].click()
#
#         # Get Download Button
#         download_button = driver.find_elements_by_xpath("//header[@class='selection-header']//button[@class='download']")
#         download_button[0].click()
#
#         # Spawns a new download window (or might)
#         download_buttons = \
#             driver.find_elements_by_xpath("//div[@class='dialog-content']//div[@class='download-link']/button[@class='download']")
#
#         number_of_downloads = len(download_buttons)
#         if number_of_downloads == 0:    # Didn't spawn multiple download window - can just click top download button
#
#             # Check download directory for the new file. When it appears, rename by year_month, and continue
#             default_filename = f'AmazonPhotos.zip'
#             new_filename = f'AmazonPhotos_{current_year}_{current_month}.zip'
#
#             download_time = fn.download_wait(save_path)
#             print(f'Downloaded {current_month} {current_year}')
#             time.sleep(1)
#
#             # Rename "AmazonPhotos.zip" file
#             os.rename(f'{save_path}\{default_filename}', f'{save_path}\{new_filename}')
#             print(f'Downloaded Photos from {current_month}, {current_year}.')
#
#         else:   # Launched window with multiple download buttons
#             for i, dl_button in enumerate(download_buttons):
#                 dl_button.click()
#
#                 # Check download directory for the new file. When it appears, rename by year_month, and continue
#                 default_filename = f'AmazonPhotos.zip'
#                 new_filename = f'AmazonPhotos_{current_year}_{current_month}_{str(i)}_of_{number_of_downloads}.zip'
#
#                 download_time = fn.download_wait(save_path)
#                 print(f'Downloaded {current_month} {current_year} #{i+1}/{number_of_downloads}')
#                 time.sleep(1)
#
#                 # Rename "AmazonPhotos.zip" file
#                 os.rename(f'{save_path}\{default_filename}', f'{save_path}\{new_filename}')
#                 print(f'Downloaded Photos from {current_month}, {current_year}.')
#
#             # When all items are downloaded, click the "Close" button on the
#             # "Download large number of files" popup window
#             close_button = driver.find_elements_by_xpath("//div[@id='dialog-container']//button[@class='close-downloader']")
#             close_button[0].click()
#
#
#
# moo = 'boo'
#
#
#
