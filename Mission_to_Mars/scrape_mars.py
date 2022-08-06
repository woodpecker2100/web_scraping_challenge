
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd

import requests

def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Avoid repeating code and launching broswer multiple times 
    def scrape1(url_str):
        browser.visit(url_str)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        return soup

    # Get latest news headline and blurb
    listings = {}

    url = "https://redplanetscience.com"

    soup = scrape1(url)
    try:
        listings["headline"] = soup.find("div", class_="content_title").get_text().strip()
        listings["text"] = soup.find("div", class_="article_teaser_body").get_text().strip()
    except Exception as e:
        print(e)
    

    # Get featured Mars image
    url = "https://spaceimages-mars.com/"
    soup = scrape1(url)
    try:
        relative_image_path = soup.find_all('img')[1]["src"]
        featured_image_url = url + relative_image_path
    except Exception as e:
        print(e)

    # Galaxy facts tables
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)

    df = tables[0]
    df = pd.DataFrame([{0:'',1:'Mars',2:'Earth'}, {0:'Description',1:'',2:''}]).append(df)
    df.columns = df.iloc[0]
    df = df.iloc[1: , :]
    df = df.set_index('')
    htmltable = (df.to_html()).replace('\n', '')

    # Hemisphere high res images
    url = "https://marshemispheres.com/"
    hemispheres = []

    soup = scrape1(url)
    try:
        sidebar = soup.find_all('div', class_='item')
    except Exception as e:
        print(e)

    for item in sidebar:
        hemi = {}
        img_url = item.find('a')['href']
        hemi['title'] = (item.find('h3').get_text().strip())
    
        newurl = url + img_url
        soup = scrape1(newurl)
    
        n = soup.find_all('li')[0]
        hemi['img_url'] = (url + n.find('a')['href'])
        hemispheres.append(hemi)

    # quit browser
    browser.quit()

    # Return dict
    ans = {"headline": listings['headline'],
        "text": listings['text'],
        "featured_image": featured_image_url,
        "facts_table": htmltable,
        "hemisphere_images": hemispheres}
    
    return ans

if __name__ == "__main__":
    scrape()