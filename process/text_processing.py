from typing import List
from jpype import JClass, getDefaultJVMPath, startJVM
import string
import csv
from process.covert_to_csv import txtToCsv


ZEMBEREK_PATH = r'zemberek/zemberek-full.jar' 
startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))

TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()

#Türkçe gereksiz kelimeler
filePath = 'assets/turkish-stop-words.txt'
def readWordsFromFile(filePath):
    words = []

    try:
        with open(filePath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.lower().strip()
                line = ''.join(char for char in line if char.isalnum() or char.isspace())
                words.extend(line.split())

    except FileNotFoundError:
        print(f"{filePath} bulunamadı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

    return words


stopWords = readWordsFromFile(filePath)

#Gereksiz kelimeleri kaldır
def removeStopWords(words):
    return [word for word in words if word.lower() not in stopWords]

#Noktalama işaretlerini kaldır
def removePunctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def analyzeAndDisambiguate(text):
    return morphology.analyzeAndDisambiguate(text).bestAnalysis()

#UNK etiketini kaldır
def removeUnkLabels(words_list):
    return [word for word in words_list if word != 'UNK']

def writeToFile(filePath, content):
    with open(filePath, 'w', encoding='utf-8') as file:
        file.write(content)


def processWords(line, outputFilePath):
    wordsWithoutPunctuation = removePunctuation(line)

    analysisWords = analyzeAndDisambiguate(wordsWithoutPunctuation)

    pos: List[str] = []
    for i, analysis in enumerate(analysisWords, start=1):
        print(f'\nAnalysis {i}: {analysis}')
        print(f'Primary POS {i}: {analysis.getPos()}')
        print(f'Primary POS (Short Form) {i}: {analysis.getPos().shortForm}')

        pos.append(str(analysis.getLemmas()[0]))

    withoutUnk = removeUnkLabels(pos)
    withoutStopWords = removeStopWords(withoutUnk)
    withoutNumericals = [word for word in withoutStopWords if not word.isdigit()]
    result_content = " ".join(withoutNumericals)

    with open(outputFilePath, 'a', encoding='utf-8') as file:
        file.write(result_content + '\n')


def processText():
    inputFilePath = 'assets/comments/comment.csv'
    outputFilePath = 'assets/processed_comments/processed_comment.txt'

    with open(outputFilePath, 'w', encoding='utf-8') as file:
        file.write('')

    with open(inputFilePath, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        headers = next(csv_reader)  # Read the header row
        try:
            text_column_index = headers.index('text')
        except ValueError:
            raise ValueError(f"Column text not found in the CSV file.")

        # Read the specified column
        lines = [line[text_column_index] for line in csv_reader]

    for line in lines:
        processWords(line, outputFilePath)

    print(f'\nAnaliz edilen kelimeler (UNK olmayanlar) dosyaya yazıldı: {outputFilePath}')

    txtFilePath = 'assets/processed_comments/processed_comment.txt'
    csvFilePath = 'assets/processed_comments/processed_comment.csv'
    txtToCsv(txtFilePath, csvFilePath)