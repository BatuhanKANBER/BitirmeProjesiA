import pandas as pd
import gensim 
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt


def calculateCoharances(inputFilePath):
    topicCountRange = range(8,40,2)

    coherenceCountList = list()
    topicCountList = list()

    #LDA Model Parametreleri
    df = pd.read_csv(inputFilePath)
    tokenized = [comment.split() for comment in df["text"].astype(str)]
    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=1, no_above=0.7)
    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]

    for topicCount in topicCountRange:
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, topicCount, id2word=dictionary)
        coherenceModelLda = CoherenceModel(model=ldamodel, texts=tokenized, dictionary=dictionary, coherence='c_v')
        mockCoherenceModelLda = coherenceModelLda.get_coherence()
        coherenceCountList.append(mockCoherenceModelLda)
        topicCountList.append(topicCount)

    #En iyi tutarlılık sonucunu veren topic sayısı grafiği
    plt.plot(topicCountList, coherenceCountList, '-')
    plt.xlabel('Topic Sayısı')
    plt.ylabel('Tutarlılık Skoru')
    plt.show()