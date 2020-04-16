from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import numpy as np
from selenium import webdriver



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": 'chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)



   
def scrape():
    Mars_dict = {} 
    browser = init_browser()   

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=\
           publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    

    News_title= soup.find('ul', class_="item_list").find('div').find('h3').get_text()
    News_paragraph =soup.find('div',class_='article_teaser_body').get_text()
    
    Mars_dict["News_title"]=News_title
    Mars_dict["News_paragraph"]=News_paragraph
    #return Mars_dict

    # featured_image():
    
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
   

    imagelink_raw =soup.find('div', class_="carousel_items").find('article')['style']
    imagelink_loc=imagelink_raw.split("(")[1].split(")")[0].replace("'", "")

    site_link ="https://www.jpl.nasa.gov"
    img_link = f'{site_link}{imagelink_loc}'
    #print(f'featured_image_url = {img_link}')
    Mars_dict["img_link"]=img_link
    #return Mars_dict
   
   
    url='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    
    
    time.sleep(2)   
    
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    #print(soup3.prettify())


    latest_twit =soup.find('div', class_="css-1dbjc4n").find('div', class_="css-1dbjc4n").\
                find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").\
                find('span', class_="css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0").get_text()

    Mars_dict["lastest_twit"]=latest_twit
    
    # Mars Facts
    
    url='https://space-facts.com/mars/'
    html_table_read=pd.read_html(url)
    #print(html_table_read)

    Mars_facts_df= html_table_read[0]
    Mars_facts_df.columns = ['Facts', 'Values']
    Mars_facts = Mars_facts_df.to_html(index=False)
    Mars_dict['Mars_facts'] = Mars_facts
    
    # Hemisphere
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html =browser.html
    soup = BeautifulSoup(html,'html.parser')
    #four_hems=[]

    four_hems = soup.find_all(['<div class ="description">', 'h3'])
    
    hemisphere_image_urls=[] 
    i=0
    for hem in four_hems:
       
        hemsphere=four_hems[i].text
        url5="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(url5)
      
        browser.click_link_by_partial_text(hemsphere)
        title =hemsphere.rsplit(' ', 1)[0]
        
        print(title)
        browser.click_link_by_partial_text("Open")
        html_5 =browser.html
        soup5 = BeautifulSoup(html_5,'html.parser')
        imglink = soup5.find('div', class_="downloads").find('a')["href"]
        i+=1
        print(imglink)
        hem_img_data=dict({'title':title, 'img_url':imglink})
        hemisphere_image_urls.append(hem_img_data)
        
        Mars_dict["Hemisphere_img_urls"] = hemisphere_image_urls
    

    return Mars_dict
    
 
    
    
    
    
    
    
    
    