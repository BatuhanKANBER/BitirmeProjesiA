import os
import sys
import webbrowser

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QPixmap, QIcon
from PyQt5.QtWidgets import *

from graphs.topicdoc import barGraph, plotGraph, pieGraph
from graphs.topicscore import ldaTopicScoreGraph
from modelling.lda_modelling import topicLda
from process.text_processing import processText
from scraping.comment_scrape import commentScrape
from scraping.info_scrape import nameScrape, priceScrape, brandScrape, imageScrape
from graphs.worldcloud import wordCloudGraph
from modelling.model_coherences import calculateCoharances

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout()
        self.layoutElements()
        self.scrapeButton.clicked.connect(self.scrapeButtonClick)
        self.processButton.clicked.connect(self.processButtonClick)
        self.wCloudButton.clicked.connect(self.wCloudButtonClick)
        self.restartButton.clicked.connect(self.restartButtonClick)
        self.cohButton.clicked.connect(self.cohButtonClick)
        self.topicButton.clicked.connect(self.topicButtonClick)
        self.resultsButton.clicked.connect(self.resultsButtonClick)
        self.vizButton.clicked.connect(self.vizButtonClick)
        self.infoButton.clicked.connect(self.infoButtonClick)
        self.ldaTopicDocGraphButton.clicked.connect(self.ldaTopicDocGraphButtonClick)
        self.ldaTopicScoreGraphButton.clicked.connect(self.ldaTopicScoreGraphButtonClick)
        self.processButton.setEnabled(False)
        self.cohButton.setEnabled(False)
        self.topicButton.setEnabled(False)
        self.numTopicInput.setEnabled(False)
        self.barRadioButton.setEnabled(False)
        self.plotRadioButton.setEnabled(False)
        self.pieRadioButton.setEnabled(False)

        if os.path.exists("lda_topic_modeling_visualization.html"):
            self.vizButton.setEnabled(True)
        else:
            self.vizButton.setEnabled(False)

        if os.path.exists("assets/processed_comments/processed_comment.csv"):
            self.wCloudButton.setEnabled(True)
        else:
            self.wCloudButton.setEnabled(False)

        if os.path.exists("assets/comments/comment.txt"):
            self.processButton.setEnabled(True)
        else:
            self.processButton.setEnabled(False)

        if os.path.exists("results/lda/yorumlarda_topic_dagilimlari.csv"):
            self.ldaTopicDocGraphButton.setEnabled(True)
            self.barRadioButton.setEnabled(True)
            self.plotRadioButton.setEnabled(True)
            self.pieRadioButton.setEnabled(True) 
        else:
            self.ldaTopicDocGraphButton.setEnabled(False)
    
        if os.path.exists("results/lda/topic_dagilimlari.csv"):
            self.ldaTopicScoreGraphButton.setEnabled(True)
        else:
            self.ldaTopicScoreGraphButton.setEnabled(False)
            
    def mainLayout(self):
        self.setWindowTitle('201307048 - Batuhan KANBER')
        self.setMinimumSize(400, 1000)  #Minimum boyutu belirle

    def layoutElements(self):
        mainLayout = QVBoxLayout(self)

        inputLayout = QHBoxLayout()
        self.input = QLineEdit("", self)
        self.input.setPlaceholderText("Ürün URL")
        inputLayout.addWidget(self.input)
        
        self.infoButton = QPushButton("", self)
        self.infoButton.setIcon(QIcon("assets/images/info.png"))
        inputLayout.addWidget(self.infoButton)

        buttonLayout = QHBoxLayout()
        self.scrapeButton = QPushButton("YORUMLARI ÇEK", self)
        self.scrapeButton.setIcon(QIcon("assets/images/scrape.png"))
        buttonLayout.addWidget(self.scrapeButton)

        self.processButton = QPushButton("ÖN İŞLEME", self)
        self.processButton.setIcon(QIcon("assets/images/text_p.png"))
        buttonLayout.addWidget(self.processButton)

        wCloudButtonLayout = QHBoxLayout()
        self.wCloudButton = QPushButton("KELİME BULUTU",self)
        self.wCloudButton.setIcon(QIcon("assets/images/word_cloud.png"))
        wCloudButtonLayout.addWidget(self.wCloudButton)

        cohoranceButtonLayout = QHBoxLayout()
        self.cohButton = QPushButton("EN İYİ TOPIC SAYISI",self)
        self.cohButton.setIcon(QIcon("assets/images/calculate.png"))
        cohoranceButtonLayout.addWidget(self.cohButton)
        
        topicCountsLayout = QHBoxLayout() 
        self.numTopicInput = QLineEdit("", self)
        self.numTopicInput.setValidator(QIntValidator())
        self.numTopicInput.setPlaceholderText("Topic sayısı?")
        topicCountsLayout.addWidget(self.numTopicInput)
        
        topicButtonLayout = QHBoxLayout()
        self.topicButton = QPushButton("TOPIC MODELLEME",self)
        self.topicButton.setIcon(QIcon("assets/images/modelling.png"))
        topicButtonLayout.addWidget(self.topicButton)
        
        restartButtonLayout = QHBoxLayout()
        self.restartButton = QPushButton("RESTART",self)
        self.restartButton.setIcon(QIcon("assets/images/restart.png"))
        restartButtonLayout.addWidget(self.restartButton)

        resultsbuttonLayout = QHBoxLayout()
        self.resultsButton = QPushButton("SONUÇLAR",self)
        self.resultsButton.setIcon(QIcon("assets/images/results.png"))
        resultsbuttonLayout.addWidget(self.resultsButton)

        modelVizButtonLayout = QHBoxLayout()
        self.vizButton = QPushButton("MODEL AYRIMLARI",self)
        self.vizButton.setIcon(QIcon("assets/images/results.png"))
        modelVizButtonLayout.addWidget(self.vizButton)
        
        self.horizontalLine1 = QFrame(self)
        self.horizontalLine1.setFrameShape(QFrame.HLine)
        self.horizontalLine1.setFrameShadow(QFrame.Sunken)
        
        #Yorumlara en çok eşleşen topic
        topicInfoTitleLayout = QVBoxLayout()
        topicInfoTitleLayout.addWidget(self.horizontalLine1)
        self.topictitleLabel = QLabel("", self)
        self.topictitleLabel.setAlignment(Qt.AlignCenter)
        topicInfoTitleLayout.addWidget(self.topictitleLabel)
        
        topicLdaLayout = QHBoxLayout()
        self.ldaLabel = QLabel("", self)
        self.ldaLabel.setAlignment(Qt.AlignLeft)
        topicLdaLayout.addWidget(self.ldaLabel)
        
        self.ldaResultLabel = QLabel("", self)
        self.ldaResultLabel.setAlignment(Qt.AlignLeft)
        topicLdaLayout.addWidget(self.ldaResultLabel)
        
        self.horizontalLine2 = QFrame(self)
        self.horizontalLine2.setFrameShape(QFrame.HLine)
        self.horizontalLine2.setFrameShadow(QFrame.Sunken)
        
        productInfoTitleLayout = QVBoxLayout()
        productInfoTitleLayout.addWidget(self.horizontalLine2)
        self.titleLabel = QLabel("********** ÜRÜN BİLGİLERİ **********", self)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        productInfoTitleLayout.addWidget(self.titleLabel)
        
        brandNameLayout = QHBoxLayout()
        self.brandLabel = QLabel("Marka Adı: ", self)
        self.brandLabel.setAlignment(Qt.AlignLeft)
        brandNameLayout.addWidget(self.brandLabel)

        self.brandResultLabel = QLabel("", self)
        self.brandResultLabel.setAlignment(Qt.AlignRight)
        brandNameLayout.addWidget(self.brandResultLabel)
        
        productNameLayout = QHBoxLayout()
        self.nameLabel = QLabel("Ürün Adı: ", self)
        self.nameLabel.setAlignment(Qt.AlignLeft)
        productNameLayout.addWidget(self.nameLabel)

        self.nameResultLabel = QLabel("", self)
        self.nameResultLabel.setAlignment(Qt.AlignRight)
        productNameLayout.addWidget(self.nameResultLabel)
        
        productPriceLayout = QHBoxLayout()
        self.priceLabel = QLabel("Fiyat: ", self)
        self.priceLabel.setAlignment(Qt.AlignLeft)
        productPriceLayout.addWidget(self.priceLabel)

        self.priceResultLabel = QLabel("", self)
        self.priceResultLabel.setAlignment(Qt.AlignRight)
        productPriceLayout.addWidget(self.priceResultLabel)
        
        commentCountLayout = QHBoxLayout()
        self.commentCountLabel = QLabel("Çekilen Yorum Sayısı: ", self)
        self.commentCountLabel.setAlignment(Qt.AlignLeft)
        commentCountLayout.addWidget(self.commentCountLabel)
        
        self.commentCountLabel = QLabel("", self)
        self.commentCountLabel.setAlignment(Qt.AlignRight)
        commentCountLayout.addWidget(self.commentCountLabel)

        #Ürün resmi
        productImageLayout = QHBoxLayout()
        pixmap = QPixmap("assets/images/default_img.jpg")
        self.imageLabel = QLabel(self)
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.imageLabel.setScaledContents(True)
        productImageLayout.addWidget(self.imageLabel)
        
        topicDocGraphsTitle_layout = QVBoxLayout()
        self.graphsLabel = QLabel("********** TOPIC DÖKÜMAN SAYISI GRAFİĞİ **********", self)
        self.graphsLabel.setAlignment(Qt.AlignCenter)
        topicDocGraphsTitle_layout.addWidget(self.graphsLabel)
        
        graphsTypeLayout = QHBoxLayout()
        self.barRadioButton = QRadioButton("BAR", self)
        self.plotRadioButton = QRadioButton("ÇİZGİ", self)
        self.pieRadioButton = QRadioButton("PASTA", self)
        graphsTypeLayout.addWidget(self.barRadioButton)
        graphsTypeLayout.addWidget(self.plotRadioButton)
        graphsTypeLayout.addWidget(self.pieRadioButton)
        
        topicDocGraphLayout = QHBoxLayout()
        self.ldaTopicDocGraphButton = QPushButton("LDA",self)
        self.ldaTopicDocGraphButton.setIcon(QIcon("assets/images/graphs.png"))
        topicDocGraphLayout.addWidget(self.ldaTopicDocGraphButton)

        topicScoreGraphsTitleLayout = QVBoxLayout()
        self.graphsLabel = QLabel("********** DÖKÜMANIN TOPIC SKOR GRAFİĞİ **********", self)
        self.graphsLabel.setAlignment(Qt.AlignCenter)
        topicScoreGraphsTitleLayout.addWidget(self.graphsLabel)
        
        documentIdLayout = QHBoxLayout()
        self.docIdInput = QLineEdit("", self)
        self.docIdInput.setValidator(QIntValidator())
        self.docIdInput.setPlaceholderText("Döküman ID?")
        documentIdLayout.addWidget(self.docIdInput)
        
        topicScoreGraphLayout = QHBoxLayout()
        self.ldaTopicScoreGraphButton = QPushButton("LDA",self)
        self.ldaTopicScoreGraphButton.setIcon(QIcon("assets/images/graphs.png"))
        topicScoreGraphLayout.addWidget(self.ldaTopicScoreGraphButton)

        mainLayout.addLayout(inputLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addLayout(wCloudButtonLayout)
        mainLayout.addLayout(cohoranceButtonLayout)
        mainLayout.addLayout(topicCountsLayout)
        mainLayout.addLayout(topicButtonLayout)
        mainLayout.addLayout(resultsbuttonLayout)
        mainLayout.addLayout(modelVizButtonLayout)
        mainLayout.addLayout(restartButtonLayout)
        mainLayout.addLayout(topicInfoTitleLayout)
        mainLayout.addLayout(topicLdaLayout)
        mainLayout.addLayout(productInfoTitleLayout)
        mainLayout.addLayout(brandNameLayout)
        mainLayout.addLayout(productNameLayout)
        mainLayout.addLayout(productPriceLayout)
        mainLayout.addLayout(commentCountLayout)
        mainLayout.addLayout(productImageLayout)
        mainLayout.addLayout(topicDocGraphsTitle_layout)
        mainLayout.addLayout(graphsTypeLayout)
        mainLayout.addLayout(topicDocGraphLayout)
        mainLayout.addLayout(topicScoreGraphsTitleLayout)
        mainLayout.addLayout(documentIdLayout)
        mainLayout.addLayout(topicScoreGraphLayout)

    def scrapeButtonClick(self):
        self.processButton.setEnabled(True)
        url = self.input.text()
        
        try:
            self.commentCount = commentScrape(url)
            self.commentCountLabel.setText(str(self.commentCount))
            self.showMessageBox("İşlem Tamamlandı", str(self.commentCount)+" adet yorum çekildi.")
        except:
            print("Error for commentScrape")
            self.showErrorBox("İşlem Tamamlanamadı", "Scraping işlemi sırasında hata oluştu.")
            
        try:
            self.brandName = brandScrape(url)
            self.brandResultLabel.setText(self.brandName)
        except:
            print("Error for brandScrape")
            
        try:
            self.productName = nameScrape(url)
            self.nameResultLabel.setText(self.productName)
        except:
            print("Error for nameScrape")
        
        try:
            self.price = priceScrape(url)
            self.priceResultLabel.setText(self.price)
        except:
            print("Error for priceScrape")
        
        try:
            imageScrape(url)
            newPixmap = QPixmap('assets/images/product.jpg')
            self.imageLabel.setPixmap(newPixmap)
        except:
            print("Error for imageScrape")

    def processButtonClick(self):
        self.scrapeButton.setEnabled(False)
        self.processButton.setEnabled(False)
        self.topicButton.setEnabled(True)
        self.numTopicInput.setEnabled(True)
        self.wCloudButton.setEnabled(True)

        try:
            processText()
            self.showMessageBox("İşlem Tamamlandı", "Metin ön işlendi.")
        except:
            print("Error for processText")
            self.showErrorBox("İşlem Tamamlanamadı","Metin ön işleme sırasında hata oluştu.")

    def wCloudButtonClick(self):
        inputFilePath = "assets/processed_comments/processed_comment.csv"
        wordCloudGraph(inputFilePath)

    def cohButtonClick(self):
        inputFilePath = 'assets/processed_comments/processed_comment.csv'
        try:
            calculateCoharances(inputFilePath)
        except:
            print('Error for calculateCoharances.')   

    def topicButtonClick(self):
        inputFilePath = 'assets/processed_comments/processed_comment.csv'
        topicsCount = int(self.numTopicInput.text())
        self.topictitleLabel.setText("********** EN DOMİNANT TOPİCLER **********")
        try:
            mostMatchingTopicLda = topicLda(inputFilePath, topicsCount)
            self.ldaLabel.setText("LDA TUTARLILIK SKORU: ")
            self.ldaResultLabel.setText(mostMatchingTopicLda)
            self.showMessageBox("İşlem Tamamlandı", "Topic modelling(LDA) yapıldı.")
            self.ldaTopicDocGraphButton.setEnabled(True)
            self.ldaTopicScoreGraphButton.setEnabled(True)
        except:
            print("Error for processText")
            self.showErrorBox("İşlem Tamamlanamadı","LDA modelleme sırasında hata oluştu.")

        self.barRadioButton.setEnabled(True)
        self.plotRadioButton.setEnabled(True)
        self.pieRadioButton.setEnabled(True) 

    def  restartButtonClick(self):
        self.restart()
        
    def restart(self):
        QtCore.QCoreApplication.quit()
        status = QtCore.QProcess.startDetached(sys.executable, sys.argv)
        print(status)
        
    def resultsButtonClick(self):
        currentDirectory = os.getcwd()
        resultPage = os.path.join(currentDirectory, 'results')
        webbrowser.open(resultPage)
    
    def vizButtonClick(self):
        currentDirectory = os.getcwd()
        resultPage = os.path.join(currentDirectory, 'lda_topic_modeling_visualization.html')
        webbrowser.open(resultPage)
        
    def showMessageBox(self, title, message):
        msgBox = QMessageBox() 
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()
    
    def showErrorBox(self, title, message):
        errorBox = QMessageBox()
        errorBox.setIcon(QMessageBox.Critical)
        errorBox.setWindowTitle(title)
        errorBox.setText(message)
        errorBox.exec_()
    
    def showInfoBox(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()
        
    def infoButtonClick(self):
        self.showInfoBox("UYARI!!!","Ürün linkini ürünün yorumlar sayfasından veriniz. Aksi halde yorumlar çekilemeyecektir.")
        
    def ldaTopicDocGraphButtonClick(self):
        inputFilePath = "results/lda/yorumlarda_topic_dagilimlari.csv"
        topicsFilePath = "results/lda/topicler.csv"
        if self.barRadioButton.isChecked():
            barGraph(inputFilePath, topicsFilePath, title="lda")
        elif self.plotRadioButton.isChecked():
            plotGraph(inputFilePath, topicsFilePath, title="lda")    
        elif self.pieRadioButton.isChecked():
            pieGraph(inputFilePath, topicsFilePath, title="lda") 
        
    def ldaTopicScoreGraphButtonClick(self):
        topicDistsFilePath = "results/lda/topic_dagilimlari.csv"
        document_id = int(self.docIdInput.text())
        ldaTopicScoreGraph(topicDistsFilePath, document_id)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

