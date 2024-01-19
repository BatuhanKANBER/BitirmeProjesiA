import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import urllib

def urlDiveder(url):
    index = url.find("/yorumlar")
    if index != -1:
        newUrl = url[:index]
        print(newUrl)
        return newUrl
    else:
        return url

def soup(url):
    newUrl = urlDiveder(url)    
    response = requests.get(newUrl)
    soup = BeautifulSoup(response.content, 'html.parser')    
    return soup  

def nameScrape(url):
    s = soup(url) 
    productName = s.find('h1', class_='pr-new-br').getText()
    words = productName.split()
    productName = ' '.join(words[1:])       
    print("Product Name:", productName)
    return productName

def brandScrape(url):
    s = soup(url) 
    brandName = s.find('h1', class_='pr-new-br').getText()
    brandName = brandName.split()[0]        
    print("Brand Name:", brandName)
    return brandName


def priceScrape(url):
    s = soup(url)
    productPrice = s.find('span', class_ = 'prc-dsc').getText()   
    print("Product Price: ", productPrice)
    return productPrice

def imageScrape(url):
    s = soup(url)
    image_tags = s.find('img', class_ = 'detail-section-img')
    img_url = image_tags['src']
    print(img_url)
    urllib.request.urlretrieve(img_url, "assets/images/product.jpg")
