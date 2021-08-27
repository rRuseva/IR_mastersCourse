# import

import preProcess as pp


# constructing inverted index
def getInvertedIdx(medDocs):
    invertedIdx = {}

    caption_idx = 0

    for i, doc in enumerate(medDocs):
        for term in doc['articleTitle']:
            if term in invertedIdx:
                # invertedIdx[term].add((i, 't'))
                invertedIdx[term].add(((doc['articleId'], i), 't'))
            else:
                invertedIdx[term] = {((doc['articleId'], i), 't')}
                # invertedIdx[term] = {(i, 't')}
        for j, cap in enumerate(doc['caption']):
            for term in cap:
                if term in invertedIdx:
                    # invertedIdx[term].add((caption_idx + j, 'c'))
                    invertedIdx[term].add((((doc['articleId'], i), (caption_idx + j, 'c'))))
                else:
                    # invertedIdx[term] = {(caption_idx + j, 'c')}
                    invertedIdx[term] = {((doc['articleId'], i), (caption_idx + j, 'c'))}
        caption_idx += 1
    for term in invertedIdx:
        invertedIdx[term] = sorted(invertedIdx[term], key=lambda x: x[0][1])

    return invertedIdx


# Boolean operations:
def orPostings(posting1, posting2):
    p1 = 0
    p2 = 0
    result = list()
    n1 = len(posting1)
    n2 = len(posting2)
    while p1 < n1 and p2 < n2:
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1
    while p1 < n1:
        result.append(posting1[p1])
        p1 += 1
    while p2 < n2:
        result.append(posting2[p2])
        p2 += 1
    return result


def andPostings(posting1, posting2):
    p1 = 0
    p2 = 0
    n1 = len(posting1)
    n2 = len(posting2)
    result = list()

    while p1 < n1 and p2 < n2:
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            p2 += 1
        else:
            p1 += 1

    return result


# create a bag of words
def createBagsOfWOrds(coprus):
    bagOfWordsTitle = []
    bagOfWordsCaption = []
    for doc in coprus:
        for term in doc['articleTitle']:
            if term not in bagOfWordsTitle:
                bagOfWordsTitle.append(term)
        for cap in doc['caption']:
            for term in cap:
                if term not in bagOfWordsCaption:
                    bagOfWordsCaption.append(term)

    return bagOfWordsTitle, bagOfWordsCaption
