import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import NMF
import numpy as np

def topicNmf(inputFilePath, topicCount):
    processedDf = pd.read_csv(inputFilePath)

    vectorizer = CountVectorizer(max_df=0.8, min_df=1, stop_words='english')
    X = vectorizer.fit_transform(processedDf["text"].astype(str))
    
    nmfModel = NMF(n_components=topicCount, random_state=42)
    nmfModel.fit(X)

    featureNames = vectorizer.get_feature_names_out()

    topicsDf = pd.DataFrame(columns=['topic_id', 'top_words'])
    
    #Topicleri csv dosyasına yazdırma
    for topicIdx, topic in enumerate(nmfModel.components_):
        topWords = [featureNames[i] for i in topic.argsort()[:-15 - 1:-1]]
        topicsDf = pd.concat([topicsDf, pd.DataFrame({'topic_id': [topicIdx], 'top_words': [', '.join(topWords)]})], ignore_index=True)
        print(f"Topic #{topicIdx}: {', '.join(topWords)}")
    topicsDf.to_csv("results/nmf/topicler.csv", index=False)

    #Dominant topicleri yorumlarla yazdırma
    docTopicMatrix = nmfModel.transform(X)
    topicDists = np.argmax(docTopicMatrix, axis=1)
    topicDistsDf = pd.DataFrame({"Document_Text": processedDf["text"], "topic_id": topicDists})
    topicDistsDf.to_csv('results/nmf/yorumlarda_topic_dagilimlari.csv', index=False)
    
    #Topic dağılımlarını csvye yazdırma
    documentTopicsDf = pd.DataFrame(docTopicMatrix, columns=[f'topic_{i}' for i in range(topicCount)])
    documentTopicsDf.insert(0, 'document_id', range(1, len(processedDf) + 1))
    documentTopicsDf.to_csv('results/nmf/topic_dagilimlari.csv', index=False)
    
    #Yorumlarla en çok eşleşen topicin idsini yazdırma
    mostDominantTopicId = topicDistsDf['topic_id'].value_counts().idxmax()
    print("En fazla eşleşen topic: ", mostDominantTopicId)
    
    #En çok eşleşen topici yazdırma
    try:
        data = pd.read_csv("results/nmf/topicler.csv")
        goal = data[data['topic_id'] == mostDominantTopicId][['top_words']]

        if not goal.empty:
            print(goal.iloc[0]['top_words'])
            result = goal.iloc[0]['top_words']
            with open("results/nmf/en_yuksek_skor.txt", "w") as txt_file:
                txt_file.writelines(["Yorumlarlarla en çok eşleşen topic: ",str(mostDominantTopicId),"\n","Kelimeler: ",goal.iloc[0]['top_words']])
            return result
        else:
            print(f"Topic {str(mostDominantTopicId)} bulunamadı.")
            return "Topic is not found."
        
    except FileNotFoundError:
        print(f"topicler.csv adlı dosya bulunamadı.")
    except KeyError:
        print("topic_id veya top_words sütunu bulunamadı.")
    
