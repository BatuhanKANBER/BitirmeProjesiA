import pandas as pd
import gensim 
from gensim import corpora
from gensim.models.coherencemodel import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim

def topicLda(inputFile,topicCount):
    
    processedDf = pd.read_csv(inputFile)
    
    tokenized = [comment.split() for comment in processedDf["text"].astype(str)]

    dictionary = corpora.Dictionary(tokenized)
    dictionary.filter_extremes(no_below=1, no_above=0.8)

    corpus = [dictionary.doc2bow(tokens) for tokens in tokenized]

    ldamodel = gensim.models.ldamodel.LdaModel(corpus, topicCount, id2word=dictionary, passes=15)
    topics = ldamodel.print_topics(num_words=15)

    #Topicleri konsola yazdırma
    for topic in topics:
        print(topic)
 
    #Topicleri csv dosyasına yazdırma
    topicsDf = pd.DataFrame(topics, columns=['topic_id', 'top_words'])
    topicsDf.to_csv('results/lda/topicler.csv', index=False)
    
    topicDistsList = []
    documentTopicsList = []
    
    for i, docTopics in enumerate(ldamodel[corpus]):
        #Yorumlarda dominant olan topici bulma
        dominantTopic = max(docTopics, key=lambda x: x[1])[0]
        topicDistsList.append((processedDf.iloc[i]["text"], dominantTopic))
        
        #Topic dağılımları
        documentTopics = ldamodel.get_document_topics(corpus[i])
        documentTopicsList.append(documentTopics)

    #Dominant topicleri yorumlarla yazdırma
    topicDistsDf = pd.DataFrame(topicDistsList, columns=['document_text', 'topic_id'])
    topicDistsDf.to_csv('results/lda/yorumlarda_topic_dagilimlari.csv', index=False)

    #Topic dağılımlarını csvye yazdırma
    documentTopicsDf = pd.DataFrame(documentTopicsList, columns=[f'topic_{i}' for i in range(ldamodel.num_topics)])
    documentTopicsDf.insert(0, 'document_id', range(1, len(documentTopicsDf) + 1))
    documentTopicsDf.to_csv('results/lda/topic_dagilimlari.csv', index=False)
   
    #Topicleri görselleştirme
    lda_viz = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
    pyLDAvis.save_html(lda_viz, 'lda_topic_modeling_visualization.html')
    #pyLDAvis.display(lda_viz)
    
    #En çok eşleşen topicin idsini buldurma
    mostDominantTopicId = topicDistsDf['topic_id'].value_counts().idxmax()
    print("En fazla eşleşen topic: ", mostDominantTopicId)
    
    #En çok eşleşen topici konsola ve txtye yazdırma yazdırma
    try:
        data = pd.read_csv("results/lda/topicler.csv")
        goal = data[data['topic_id'] == mostDominantTopicId][['top_words']]

        if not goal.empty:
            print(goal.iloc[0]['top_words'])
            #result = goal.iloc[0]['top_words']
            with open("results/lda/en_yuksek_skor.txt", "w") as txt_file:
                txt_file.writelines(["Yorumlarlarla en çok eşleşen topic: ",str(mostDominantTopicId),"\n","Kelimeler: ",goal.iloc[0]['top_words']])
            #return result
        else:
            print(f"Topic {str(mostDominantTopicId)} bulunamadı.")
            #return "Topic is not found."
        
    except FileNotFoundError:
        print(f"topicler.csv adlı dosya bulunamadı.")
    except KeyError:
        print("Topic veya Words sütunu bulunamadı.")

    coherence_model_lda = CoherenceModel(model=ldamodel, texts=tokenized, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()

    # Coherence score'larını yazdır
    print('\nCoherence Score: ', coherence_lda)

    return str(coherence_lda)





