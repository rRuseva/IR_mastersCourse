import json
import re
import regex

from copy import deepcopy
from string import punctuation
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, TweetTokenizer

tokenizer = TweetTokenizer()

nltk.download('stopwords')
nltk.download('punkt')
stopW = stopwords.words('english')


def createDocList(results_list, corpus):
    results = list()
    for result in results_list:
        doc = corpus[result[0][1]]
        results.append(doc)

    return results


def createTitleCapList(corpus):
    titles_list = []
    captions_list = []
    for doc in corpus:
        titles_list.append(doc['articleTitle'])
        for cap in doc['caption']:
            captions_list.append(cap)

    return titles_list, captions_list


# a method to Read a json file with img captions and article titles and parse it into set of documents


def getDocs(sourcePath):
    medDocs = []
    with open(sourcePath, 'r') as sourceFile:

        count = 1
        for line in sourceFile:
            medDocs.append(json.loads(line))
            count += 1

    return medDocs


# method that cleans the title and caption text in each document
# the result is tokenized titles and caption without unwanted brackets, numbers, spaces, tags, unicode charts;
# result includes no punctuation and stopwards and tokens with length less than 2 symbols
# all tokens are lower case
def preprocessContent(content):
    ps = PorterStemmer()
    sentences = sent_tokenize(content)
    tokens = []
    for sent in sentences:
        # removes unicode
        cleanedTokens = re.sub(r'[^\x00-\x7F]+', ' ', sent)
        # removes menions
        cleanedTokens = re.sub(r'@\w+', '', cleanedTokens)
        # removes numbers
        cleanedTokens = re.sub('[0-9]+', '', cleanedTokens)
        # removes nested brackets
        cleanedTokens = regex.sub(r'\([^()]*+(?:(?R)[^()]*)*+\)', '', cleanedTokens)
        # removes nested currly brackets
        cleanedTokens = regex.sub('\{(?:[^}{]|\{[^}{]*\})*\}', '', cleanedTokens)
        # removes html tags
        cleanedTokens = re.sub('\<+/*\w*/*\>+', '', cleanedTokens)
        # removes punctuation
        cleanedTokens = re.sub(r'[%s]' % re.escape(punctuation), ' ', cleanedTokens)
        # removes doubled spaces
        cleanedTokens = re.sub(r'\s{2,}', ' ', cleanedTokens)
        sentTokens = tokenizer.tokenize(cleanedTokens)
        # lower case each token and removes tokens with length less than 2
        sentTokens = [tok.lower() for tok in sentTokens if len(tok) > 2]
        # removes stop words
        # sentTokens2 = [ps.stem(tok) for tok in sentTokens if not tok.lower() in stopW ]
        sentTokens2 = [tok for tok in sentTokens if not tok.lower() in stopW]
        tokens += sentTokens2
    return tokens


def cleanDocs(medDocs):
    cleanedDocs = deepcopy(medDocs)
    for i, doc in enumerate(cleanedDocs):
        doc['articleTitle'] = preprocessContent(doc['articleTitle'])
        for j, cap in enumerate(doc['caption']):
            doc['caption'][j] = preprocessContent(cap)
    return cleanedDocs


# create a bag of words
def createBagsOfWOrds(corpus):
    bagOfWordsTitle = []
    bagOfWordsCaption = []
    for doc in corpus:
        for term in doc['articleTitle']:
            if term not in bagOfWordsTitle:
                bagOfWordsTitle.append(term)
        for cap in doc['caption']:
            for term in cap:
                if term not in bagOfWordsCaption:
                    bagOfWordsCaption.append(term)

    return bagOfWordsTitle, bagOfWordsCaption


# def capDicts(corpus):
#     captionsDict = {}
#     captionCount = 0
#     caption_idx = 0
#     for i, doc in enumerate(corpus):
#         for j in range(len(doc['caption'])):
#             captionsDict[caption_idx] = (i, j)
#             caption_idx += 1

#     return captionsDict
