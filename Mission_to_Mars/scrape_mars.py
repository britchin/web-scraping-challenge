from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd

#path to chromedriver
def init_browser():
    executable_path = {'executable_path':'C:/chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #visit the webpage
    browser.visit("https://mars.nasa.gov/news/")

    time.sleep(2)

    #scrape page into soup
    html = browser.html
    soup = bs(html, 'html.parser')

    #Find title
    step1 = soup.find('ul', class_='item_list')
    step2 = step1.find('li', class_='slide')
    news_title = step2.find('div', class_='content_title').text
    news_title

    # Find paragraph text
    news_p = step2.find('div', class_='article_teaser_body').text
    news_p

    # ## JPL Mars Page Space Images - Featured Image


    #visit the webpage
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")

    time.sleep(2)

    # Click featured image
    browser.click_link_by_partial_text('FULL IMAGE')


    # Click again for full large image
    time.sleep(3)
    browser.click_link_by_partial_text('more info')

    #create beautiful soup object
    html = browser.html
    soup = bs(html, 'html.parser')

    # Search for image source
    results = soup.find_all('figure', class_='lede')
    relative_img_path = results[0].a['href']
    featured_img_url = 'https://www.jpl.nasa.gov' + relative_img_path

    #print(featured_img_url)


    # ## Mars Facts


    # Use Pandas to scrape data
    table = pd.read_html('https://space-facts.com/mars/')


    #use first table for mars facts only and name table columns
    marsfacts_df = table[0]
    marsfacts_df.columns = ["Characteristic", "Value"]
    #marsfacts_df

    # Convert table to html
    marsfacts_html = marsfacts_df.to_html(classes='data table table-borderless', index=False, header=True, border=0)
    #marsfacts_html


    # ## Mars Hemispheres


    #visit the webpage
    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")

    #create beautiful soup object
    html = browser.html
    soup = bs(html, 'html.parser')


    #create an empty list to append hemispheres to 
    hemispheres = []

    #find the hemisphere names
    results = soup.find_all('div', class_="collapsible results")
    hemis = results[0].find_all('h3')

    # Get text and store in list
    for name in hemis:
        hemispheres.append(name.text)

        #hemispheres


    # Find the thumbnail images for each hemisphere
    thumbnails = results[0].find_all('a')
    thumbnail_link = []


    #create for loop to extract thumnbail paths
    for thumbnail in thumbnails:
    
        # If the thumbnail element has an image...
        if (thumbnail.img):
        
            # then grab the attached link
            thumbnail_path = 'https://astrogeology.usgs.gov/' + thumbnail['href']
        
            # Append list with links
            thumbnail_link.append(thumbnail_path)

    #thumbnail_link


    #find the path to the full sized image for each hemisphere
    tif_jpeg = []

    for url in thumbnail_link:
    
        # Click through each thumbanil link
        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
        # Scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
    
     # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
    
        # Add full image links to a list
        tif_jpeg.append(img_link)

    #tif_jpeg


    #combine the two existing lists 
    combined_hemi_jpeg = zip(hemispheres, tif_jpeg)

    hemisphere_image_urls = []

    # Iterate through the zipped object
    for title, img in combined_hemi_jpeg:
    
        mars_dict = {}
    
        # Add hemisphere title to dictionary
        mars_dict['title'] = title
    
        # Add image url to dictionary
        mars_dict['img_url'] = img
    
        # Append the list with dictionaries
        hemisphere_image_urls.append(mars_dict)

    #hemisphere_image_urls


    # Store data in a dictionary
    mars_data = {
            "news_title": news_title,
            "news_paragraph": news_p,
            "featured_image": featured_img_url,
            "mars_facts": marsfacts_html,
            "hemispheres": hemisphere_image_urls
    }

    #Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data