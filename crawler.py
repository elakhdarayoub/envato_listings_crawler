### before running this script please read the comments carefully and do the neccessary settings

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import requests

#Starts the driver and goes to our starting webpage
## use the webdriver version that corresponds to your browsers version
### if you want to use a browser other than chrome change .Chrome() with the name of the browser you want
driver = webdriver.Chrome('') #put the driver path between ()
driver.get('https://elements.envato.com/graphic-templates/print-templates+ux-and-ui-kits+websites+logos/sort-by-latest')

#Inputs to search box, you can totally omit it if you don't want to make any search
searchBox = driver.find_element_by_xpath('//*[@id="autosuggest"]')
searchBox.send_keys('', Keys.ENTER) #put the keywords inside the single quoatation

#This loop goes through every page and grabs all the details of each listing
#Loop will only end when there are no more pages to go through
while True:  
    #Imports the HTML of the current page into python
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    #Grabs the HTML of each listing
    listings = soup.find_all('li', class_ = 'Z9wqao0i leU0q2Sr')
    
    #grabs all the link for each listing and access it to start grabing the images and tags
    for item in listings:
        link = 'https://elements.envato.com'+item.find('a', class_ = '_MwuC0KD').get('href')
        driver.get(link)
        sleep(3)
        
        #getting the info of the new page
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        #grabing the header to use it later into file naming
        header = soup.find('h1', class_ = 'D9ao138P').text
        header = header.replace(' ', '_')
        
        #grabing the all the tags and put them in file.txt with the same naming as the header
        tags = soup.find_all('a', class_ = 'd0KA3Wtv')
        with open(f'path/{header}.txt', 'a') as f:
            #change path with the location you want
            for tag in tags:
                f.write(tag.text+'\n')
            f.close()
        
        #clicking on the image to start getting all the other images
        driver.find_element_by_xpath('//*[@id="app"]/div[1]/main/div/div[1]/section[1]/div[2]/div/div[1]/div/div/div[3]/img').click()
        WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[9]/div/div/div/div[1]/div[2]/div/button[1]')))
        images = soup.find_all('button', class_ = 'OaSBRYFO')
        sleep(1)
        for i in range(1, len(images)+1):
            sleep(1)
            driver.find_element_by_xpath(f'/html/body/div[9]/div/div/div/div[1]/div[2]/div/button[{i}]').click()
            soup = BeautifulSoup(driver.page_source, 'lxml')
            image = soup.find('img', class_ = 'AjQn4Il1 undefined').get('srcset')
            sleep(2)
            response = requests.get(image)
            if response.status_code:
                fp = open(f'path/{header}{i}.png', 'wb') #change path with the location you want
                fp.write(response.content)
                fp.close()
    
    #checks if there is a button to go to the next page, and if not will stop the loop
    try:
        nextButton = soup.find('a', class_ = 'LQ9zKnGb vHgjkrLA').get('href')
        driver.get('https://elements.envato.com'+nextButton)
    except:
        break