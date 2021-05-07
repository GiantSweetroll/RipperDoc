from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from pathlib import Path

def get_images(chrome_driver_loc:str, query:str, export_path:str, img_count:int = 10):

    driver = webdriver.Chrome(chrome_driver_loc)
    driver.get('https://www.google.ca/imghp?hl=en&tab=ri&authuser=0&ogbl')

    box = driver.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')

    box.send_keys(query)
    box.send_keys(Keys.ENTER)

    #Will keep scrolling down the webpage until it cannot scroll no more
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    # Check if export location exists, if not create it
    images_destination_path = export_path + '/' + query
    Path(images_destination_path).mkdir(parents=True, exist_ok=True)

    # Take screenshot and export it to path
    for i in range(1, img_count+1):
        try:
            driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').screenshot(images_destination_path + '/' + query + ' (' + str(i) + ').png')
        except:
            pass

if __name__ == '__main__':
    chrome_driver_loc:str = 'K:/chromedriver.exe'
    query:str = 'dell logo'
    export_path:str = 'L:/For Machine Learning/Logo Recognition/selenium'
    image_count:int = 1000

    get_images(chrome_driver_loc, query, export_path, image_count)