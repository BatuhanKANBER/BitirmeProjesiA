import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import sys


def barGraph(inputFilePath, topicsFilePath, title):   
    resultsDf = pd.read_csv(inputFilePath)
    topicsDf = pd.read_csv(topicsFilePath)
    topicCount = resultsDf['topic_id'].nunique()
    topicDists = resultsDf['topic_id'].value_counts().sort_index()

    plt.figure(figsize=(10, 6))
    plt.bar(topicDists.index, topicDists.values, color='black', alpha=0.3)
    plt.title('Dökümanlardaki Topic Dağılımı - ' + title)
    plt.xlabel('Topic ID')
    plt.xticks(ticks=range(0, topicCount), labels=range(0, topicCount))
    plt.ylabel('Döküman Sayısı')
    
    if sys.platform.startswith("linux"):
        plt.gcf().canvas.set_window_title('BAR GRAFİĞİ')
    elif sys.platform.startswith("windows"):
        plt.gcf().canvas.setWindowTitle('BAR GRAFİĞİ')
    
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: showTopics(sel, topicDists, topicsDf))
    plt.show()
    
def plotGraph(inputFilePath, topicsFilePath, title):   
    resultsDf = pd.read_csv(inputFilePath)
    topicsDf = pd.read_csv(topicsFilePath)
    topicCount = resultsDf['topic_id'].nunique()
    topicDists = resultsDf['topic_id'].value_counts().sort_index().to_numpy()  # Pandas Series'i NumPy dizisine çevir

    plt.figure(figsize=(10, 6))
    plt.plot(range(len(topicDists)), topicDists, marker='o', linestyle='-', color='black', label='Topic Dağılımı')
    plt.title('Dökümanlardaki Topic Dağılımı - ' + title)
    plt.xlabel('Topic ID')
    plt.xticks(ticks=range(0, topicCount), labels=range(0, topicCount))
    plt.ylabel('Döküman Sayısı')
    plt.legend()
    
    if sys.platform.startswith("linux"):
        plt.gcf().canvas.set_window_title('ÇİZGİ GRAFİĞİ')
    elif sys.platform.startswith("windows"):
        plt.gcf().canvas.setWindowTitle('ÇİZGİ GRAFİĞİ')

    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: showTopics(sel, topicDists, topicsDf))
    plt.show()

def pieGraph(inputFilePath, topicsFilePath, title):   
    resultsDf = pd.read_csv(inputFilePath)
    topicDists = resultsDf['topic_id'].value_counts().sort_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    ax1.pie(topicDists.values, labels=topicDists.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.tab10.colors)
    ax1.set_title('Dökümanlardaki Topic Dağılımı - '+title)

    ax2.text(0.1, 0.9, 'Topicler:', fontsize=8, weight='bold')
    ax2.set_xticks([])
    ax2.set_yticks([])

    for i, topic_id in enumerate(topicDists.index):
        ax2.text(0.1, 0.8 - i * 0.03, f'Topic {topic_id}, Eşleştiği Döküman Sayısı: {topicDists[topic_id]}', fontsize=8)

    if sys.platform.startswith("linux"):
        fig.canvas.set_window_title('PASTA GRAFİĞİ')
    elif sys.platform.startswith("windows"):
        fig.canvas.setWindowTitle('PASTA GRAFİĞİ')

    plt.show()


def showTopics(sel, topicDists, topicsDf):
    topicId = int(sel.target[0])
    docCount = topicDists[topicId]
    
    topic_info = topicsDf[topicsDf['topic_id'] == topicId]
    top_words = topic_info.iloc[0]['top_words']

    annotationText = f"Topic ID: {topicId}, Kelimeler: {top_words}\nDöküman Sayısı: {docCount}"
    sel.annotation.set_text(annotationText)

