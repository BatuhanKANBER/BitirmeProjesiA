import pandas as pd
import matplotlib.pyplot as plt
import mplcursors
import sys

def ldaTopicScoreGraph(filePath,documentId):
    df = pd.read_csv(filePath)
    
    topicColumns = [col for col in df.columns if col.startswith('topic_')]
    topicCount = int(len(topicColumns))
    print("TOPIC SAYISI: ",topicCount)

    topicColumns = [f'topic_{i}' for i in range(topicCount-1)] 
    topicIds = []
    topicScores = []

    for col in topicColumns:
        if not pd.isnull(df[df['document_id'] == documentId][col].values[0]):
            topicInfo = df[df['document_id'] == documentId][col].values[0]
            topicIdStr, scoreStr = topicInfo.split(",")
            topicId = int(topicIdStr.strip("()"))
            score = float(scoreStr.strip(")"))
            topicIds.append(topicId)
            topicScores.append(score)

    fig, ax = plt.subplots()
    bars = plt.bar(topicIds, topicScores, color='black', alpha=0.3)
    plt.title(f"{documentId}'idli Dökümanın Topic Skor Grafiği - lda")
    plt.xlabel("Topic ID")
    plt.ylabel("Skor")

    def showTopicsLDA(sel):
        topicsDf = pd.read_csv("results/lda/topicler.csv")
        topicInfo = topicsDf[topicsDf['topic_id'] == topicId]
        topWords = topicInfo.iloc[0]['top_words']
        x_val = int(sel.target[0])
        y_val = sel.target[1]
        sel.annotation.set_text(f'Score: {y_val:.4f}\nTopic ID: {x_val}\nKelimeler: {topWords}')

    mplcursors.cursor(hover=True).connect("add", showTopicsLDA)
    
    if sys.platform.startswith("linux"):
        plt.gcf().canvas.set_window_title('BAR GRAFİĞİ')
    elif sys.platform.startswith("windows"):
        plt.gcf().canvas.setWindowTitle('BAR GRAFİĞİ')
    
    plt.show()
