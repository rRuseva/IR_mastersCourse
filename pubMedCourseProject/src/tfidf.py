import math
# import import_ipynb
import pandas as pd


def createTitleCapHash(corpus):
    docCaptionsDict = []
    captionCount = 0
    caption_idx = 0

    for i, doc in enumerate(corpus):
        docCaptionsDict.append({i: []})
        for j in range(len(doc['caption'])):
            docCaptionsDict[i][i].append(caption_idx + j)

        caption_idx += len(doc['caption'])

    return docCaptionsDict


# Returns tuple(title_idx, values_idx) - title_idx from cap_doc_dict; values_idx number of caption in document captions
def getTitleByCap(cap_doc_dict, cap_idx):

    # cap_doc_dict = createTitleCapHash(corpus)
    for pair in cap_doc_dict:
        value_iterator = iter(pair.values())
        values = value_iterator.__next__()
        if cap_idx in values:
            key_iterator = iter(pair.keys())
            return (key_iterator.__next__(), values.index(cap_idx))


# def getCapByTitle(cap_doc_dict, title_idx):
#     import pdb
#     pdb.set_trace()
#     # cap_doc_dict = createTitleCapHash(corpus)
#     return cap_doc_dict[title_idx]


# computes the friquency of a term in the given document
def computeTermFreq(term, doc):

    if len(doc) > 0:
        return doc.count(term) / len(doc)
    else:
        return 0


# for a given document (title or caption) computes the term frequency for each term
# returns dictionary with all terms from all documents for keys and TF for the values
def computeTFperDoc(doc_, bow):
    term_dict = dict.fromkeys(bow, 0)
    # import pdb
    # pdb.set_trace()
    for term in doc_:
        if term_dict.get(term) is not None:
            term_dict[term] = computeTermFreq(term, doc_)
        else:
            term_dict[term] = 0
    return term_dict


def computeCorpusTF(corpus, bow):
    tf_dict = []
    term_dict = dict.fromkeys(bow, 0)
    for i, doc in enumerate(corpus):
        term_dict = computeTFperDoc(doc, bow)
        tf_dict.append(term_dict)
    return tf_dict


# computes the IDF for a given term in given document list
def computeTerm_IDF(term, corpus):
    term_frequency = 0
    for doc in corpus:
        if term in doc:
            term_frequency += 1
    return math.log10(float(len(corpus)) / (term_frequency + 1))


# computes the idf for each term in the corpus
# returns a dictionary of the terms and their inverted index frequency
def computeCorpusIDF(corpus, bow):
    idf_dict = {}
    for i, doc in enumerate(corpus):
        for term in doc:
            if idf_dict.get(term) is not None:
                idf_dict[term].append(i)
            else:
                idf_dict[term] = [i]

    total_n = len(corpus)
    for term in bow:
        if idf_dict.get(term) is not None:
            idf_dict[term] = 1 + math.log10(total_n + 1 / (len(idf_dict[term])))
        else:
            idf_dict[term] = 0
    return idf_dict


def computeTermTfIDF(term, doc, corpus_idf):
    return computeTermFreq(term, doc) * corpus_idf[term]


def computeTFIDF(corpus, bow):

    tfidfs = []
    idf_dict = computeCorpusIDF(corpus, bow)
    tf_dict = computeCorpusTF(corpus, bow)
    total_n = len(corpus)

    for i in range(total_n):
        tfidf_doc = dict.fromkeys(bow, 0)
        for term in bow:
            tfidf_doc[term] = tf_dict[i][term] * idf_dict[term]
        tfidfs.append(tfidf_doc)

    return tfidfs


def computeFinal_TFIDF(titles_list, captions_list, alpha, bow, cap_title_dict):
    tfidf = []
    title_tfidf = computeTFIDF(titles_list, bow)
    caption_tfidf = computeTFIDF(captions_list, bow)
    n = len(caption_tfidf)
    # m = len(title_tfidf)
    doc_idx = 0
    for i in range(n - 1):
        doc_tfidf = dict.fromkeys(bow, 0)
        title_idx = getTitleByCap(cap_title_dict, i)[1]
        for term in bow:
            doc_tfidf[term] = alpha * caption_tfidf[i][term] + title_tfidf[title_idx][term] * (1 - alpha)
        tfidf.append(doc_tfidf)

    return tfidf
