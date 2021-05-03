
# Import Splinter and BeautifulSoup
import pandas as pd
import datetime as dt
import pymongo
import requests
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "images": mars_images(browser),
        "scrape_hemisphere": scrape_hemisphere(html_text),
        "hemisphere_image_urls": hemisphere_image_urls(browser)
    }
    
    # End the automated browsing session. 
    # Stop webdriver and return data
    browser.quit()
    return data

# Create a function for hemisphere image url to scrape data
#def hemisphere_image_urls (browser):
#    url = browser


# Declare and define the function.
def mars_news(browser):
    #Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object, then quit the browser.
    # set up the HTML parser:
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

    # ### Featured Images

# Declare and define the function.
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup so we can continue and scrape 
    # the full-size image URL.
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Scrape the entire table with Pandas' .read_html() function.
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert DataFrame back into HTML-ready code using the .to_html() function. 
    return df.to_html(classes="table table-striped")

def hemisphere_image_urls(browser):
   
    # Use browser to visit the URL 
    url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    hemisphere_image_urls = []
    links = browser.find_by_css(#'a.product-item img')

    for i in range(len(links)):
        hemisphere = {}
        # Find the elements on each loop
        browser.find_by_css('a.product-item img')[i].click()
        # Next, find the sample image tag and extract the href
        slide_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = slide_elem['href']
        # Get the hemisphere title
        hemisphere['title'] = browser.find_by_css('h2.title').text
        # Append hemispher object to list
        hemisphere_image_urls.append(hemisphere)
        # Navigate backwards
        browser.back()
    return hemisphere_image_urls
    

def images(browser):
    try:
        url = 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/index.html'
        
    except:
        hemisphere_image_urls = [{'img_url': 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/images/full.jpg',
      'title': 'Cerberus Hemisphere Enhanced'},
     {'img_url': 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/images/schiaparelli_enhanced-full.jpg',
      'title': 'Schiaparelli Hemisphere Enhanced'},
     {'img_url': 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/images/syrtis_major_enhanced-full.jpg',
      'title': 'Syrtis Major Hemisphere Enhanced'},
     {'img_url': 'https://data-class-mars-hemispheres.s3.amazonaws.com/Mars_Hemispheres/images/valles_marineris_enhanced-full.jpg',
      'title': 'Valles Marineris Hemisphere Enhanced'}]
    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    souph = soup(html_text, "html.parser")
    try:
        title_elem=souph.find("h2", class_="title").get_text()
        sample_elem=souph.find("a", text="Sample").get("href")
    except AttributeError:
        title_elem=None
        sample_elem=None

    hemispheres=[]
    hemispheres={
        "title": title_elem,
        "img_url": sample_elem
    }    
    return hemispheres


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
 # Close the browser after scraping    
browser.quit()