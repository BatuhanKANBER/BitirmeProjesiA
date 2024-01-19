import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def wordCloudGraph(inputFilePath):
    df = pd.read_csv(inputFilePath)
    text_data = ' '.join(df['text'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()