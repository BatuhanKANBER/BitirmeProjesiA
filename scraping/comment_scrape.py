from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from process.covert_to_csv import txtToCsv


def commentScrape(url):
    comment_count = 0

    commentsFile = open("assets/comments/comment.txt", "a", encoding='utf-8')

    webDriver = webdriver.Chrome()
    webDriver.maximize_window()
    webDriver.get(url)

    wait = WebDriverWait(webDriver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))  # Örneğin, 'p' elementini bekleyebilirsiniz


    # <------ EKRAN TARAMA ------>
    lenOfPage = webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
    match = False
    while match == False:
        wait = WebDriverWait(webDriver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, 'p')))
        lastCount = lenOfPage
        time.sleep(20)
        lenOfPage = webDriver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
        if lastCount == lenOfPage:
            match = True
    time.sleep(3)
    # <------ EKRAN TARAMA SON ------>
    html_content = webDriver.page_source
    webDriver.quit()

    soup = BeautifulSoup(html_content, "html.parser")
    comments = soup.find_all("p")

    for comment in comments:
        if not comment.has_attr("class") and not comment.has_attr("div") and not comment.has_attr("span") and not comment.has_attr("id"):
                if comment.text != "10.000’lerce yeni ürünü ve sezon trendlerini büyük indirimlerle yakalamak için,":
                    if comment.text != "Sepetinizde Ürün Bulunmamaktadır.":
                        if comment.text != "Popüler Marka ve Mağazalar":
                            if comment.text != "Popüler Sayfalar":
                                commentsFile.write(comment.text+"\n")
                                print(comment.text)
                                comment_count +=1

    commentsFile.close()

    txtFilePath = 'assets/comments/comment.txt'
    csvFilePath = 'assets/comments/comment.csv'
    txtToCsv(txtFilePath,csvFilePath)

    return comment_count
    
    
