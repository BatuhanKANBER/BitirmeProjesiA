import pandas as pd
from gensim import corpora
from gensim.models import LsiModel
from gensim.matutils import corpus2dense
from gensim.models.coherencemodel import CoherenceModel


def topicLsa(inputFilePath, topicCount):
    
    processedDf = pd.read_csv(inputFilePath)
    
    tokenized = [comment.split() for comment in processedDf["text"].astype(str)]

    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=1, no_above=0.8)

    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]

    lsimodel = LsiModel(corpus, topicCount, id2word=dictionary)

    topics = lsimodel.print_topics(num_words=15)

    #Topicleri konsola yazdır
    for topic in topics:
        print(topic)
 
    #Topicleri csv dosyasına yazdır
    topicsDf = pd.DataFrame(topics, columns=['topic_id', 'top_words'])
    topicsDf.to_csv('results/lsa/topicler.csv', index=False)
    
    topicDistsList = []
    documentTopicsList = []
    
    for i, docBow in enumerate(corpus):
        #Yorumlarda dominant olan topici bulma
        docTopics = lsimodel[docBow]
        dominantTopic = max(docTopics, key=lambda x: abs(x[1]))[0]
        topicDistsList.append((processedDf.iloc[i]["text"], dominantTopic))
        
        #Topic dağılımları
        documentTopicsList.append(docTopics)

    #Dominant topicleri yorumlarla yazıdırma
    topicDistsListDf = pd.DataFrame(topicDistsList, columns=['document_text', 'topic_id'])
    topicDistsListDf.to_csv('results/lsa/yorumlarda_topic_dagilimlari.csv', index=False)
        

    #Topic dağılımlarını csv'ye yazdırma
    documentTopicsMatrix = corpus2dense(documentTopicsList, num_terms=topicCount).T
    documentTopicsDf = pd.DataFrame(documentTopicsMatrix, columns=[f'topic_{i}' for i in range(topicCount)])
    documentTopicsDf.insert(0, 'document_id', range(1, len(documentTopicsDf) + 1))
    documentTopicsDf.to_csv('results/lsa/topic_dagilimlari.csv', index=False)

    #En çok eşleşen topicin idsini bulma
    mostDominantTopicId = topicDistsListDf['topic_id'].value_counts().idxmax()
    print("En fazla eşleşen topic: ", mostDominantTopicId)
    
    #En çok eşleşen topici konsola yazdırma
    try:
        data = pd.read_csv("results/lsa/topicler.csv")
        goal = data[data['topic_id'] == mostDominantTopicId][['top_words']]

        if not goal.empty:
            print(goal.iloc[0]['top_words'])
            #result = goal.iloc[0]['top_words']
            with open("results/lsa/en_yuksek_skor.txt", "w") as txt_file:
                txt_file.writelines(["Yorumlarlarla en çok eşleşen topic: ",str(mostDominantTopicId),"\n","Kelimeler: ",goal.iloc[0]['top_words']])
            #return result
        else:
            print(f"Topic {str(mostDominantTopicId)} bulunamadı.")
            #return "Topic is not found."
        
    except FileNotFoundError:
        print(f"topicler.csv adlı dosya bulunamadı.")
    except KeyError:
        print("Topic veya Words sütunu bulunamadı.")

    # Tutarlılık puanını hesapla
    coherence_model = CoherenceModel(model=lsimodel, texts=tokenized, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model.get_coherence()

    print(f"LSA Model Tutarlılık Puanı: {coherence_score}")

    return str(coherence_score)