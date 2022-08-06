from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
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

    #Collecting Headlines as per the mission-to-mars.ipynb
    headlines = {}
    url = "https://redplanetscience.com"

    soup = scrape1(url)
    try:
        headlines["headline"] = soup.find("div", class_="content_title").get_text().strip()
        headlines["text"] = soup.find("div", class_="article_teaser_body").get_text().strip()
    except Exception as e:
        print(e)
    

    #Collecting the featured Mars image as per the mission-to-mars.ipynb
    url = "https://spaceimages-mars.com/"
    soup = scrape1(url)
    try:
        relative_image_path = soup.find_all('img')[1]["src"]
        featured_image_url = url + relative_image_path
    except Exception as e:
        print(e)

    #Collecting the Galaxy facts as per the mission-to-mars.ipynb
    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)

    df = tables[0]
    df = pd.DataFrame([{0:'',1:'Mars',2:'Earth'}, {0:'Description',1:'',2:''}]).append(df)
    df.columns = df.iloc[0]
    df = df.iloc[1: , :]
    df = df.set_index('')
    htmltable = (df.to_html()).replace('\n', '')

    #Collecting the high res images from the hemisphere website as per the mission-to-mars.ipynb
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
    
        new_url = url + img_url
        soup = scrape1(new_url)
    
        n = soup.find_all('li')[0]
        hemi['img_url'] = (url + n.find('a')['href'])
        hemispheres.append(hemi)

    browser.quit()

    # Return definition as ans
    ans = {"headline": headlines['headline'],
        "text": headlines['text'],
        "featured_image": featured_image_url,
        "facts_table": htmltable,
        "hemisphere_images": hemispheres}
    
    return ans

if __name__ == "__main__":
    scrape()