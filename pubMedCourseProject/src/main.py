import scrapy
import pandas as pd

import tfidf as tf_idf
import preProcess as pp
import extraction as ext
import invertedIndex as idx

from extraction import cosine_similarity
from scrapy.crawler import CrawlerProcess


source_path = '../assets/medImages.jl'

if __name__ == "__main__":
        # call scrapy spider for https://www.ncbi.nlm.nih.gov/pmc/journals
        # cd scrapePubMed
        # scrapy crawl pubMedImages

    medDocs = pp.getDocs(source_path)
    cleaned_docs = pp.cleanDocs(medDocs)

    termInvIdx = idx.getInvertedIdx(cleaned_docs)
    term1 = 'lung'
    term2 = 'cancer'
    pl_1 = list(termInvIdx[term1])
    pl_2 = list(termInvIdx[term2])

    # import pdb
    # pdb.set_trace()

    query_result = idx.orPostings(pl_1, pl_2)
    print("\nQuery: {} or {} ".format(term1, term2))
    print("Results: ")
    for result in query_result:
        print(result)
    print("\n________________________________________________\n")

    result_list = pp.createDocList(query_result, cleaned_docs)
    # result_list = cleaned_docs
    result_title_list, result_cap_list = pp.createTitleCapList(result_list)
    cap_title_dict = tf_idf.createTitleCapHash(result_list)

    bag_of_words_title, bag_of_words_caption = pp.createBagsOfWOrds(result_list)
    bow = set(bag_of_words_title).union(set(bag_of_words_caption))

    corpus_idf = tf_idf.computeCorpusIDF(result_cap_list, bow)

    # title_tfidf = tf_idf.computeTFIDF(result_title_list, bow)
    # cap_tfidf = tf_idf.computeTFIDF(result_title_list, bow)

    # import pdb
    # pdb.set_trace()
    finalTFIDF = tf_idf.computeFinal_TFIDF(result_title_list, result_cap_list, 0.85, bow, cap_title_dict)
    df_finalTFIDF = tf_idf.pd.DataFrame(finalTFIDF)
    print("TFIDF: {}x{}".format(len(finalTFIDF), len(bow)))
    print(df_finalTFIDF)
    print("\n________________________________________________\n")
    # documentCosSimilarity = cosine_similarity(df_finalTFIDF, df_finalTFIDF)

    queryTerms = ["histopatology", "photomicrographs", "scanning", "biopsy", "tissues", "images", "sem", "materials", "optical", "microscope", "photographs", "magnification", "histologic", "report"]
    query_tfs = tf_idf.computeTFperDoc(queryTerms, bow)

    query_idf = dict()
    for term in queryTerms:
        if corpus_idf.get(term) is not None:
            query_idf[term] = corpus_idf[term]
        else:
            query_idf[term] = 0

    # df_qIDF = pd.DataFrame.from_dict(query_idf, orient='index')
    # df_qIDF.sort_values(by=[0], ascending=False)

    query_tfidf = dict.fromkeys(bow, 0)

    for term in queryTerms:
        query_tfidf[term] = query_tfs[term] * query_idf[term]

    cosS = ext.computeCosineSimilarity(list(query_tfidf.values()), list(finalTFIDF[0].values()))

    query_similarity = []

    for i in range(len(finalTFIDF)):
        cosS = ext.computeCosineSimilarity(list(query_tfidf.values()), list(finalTFIDF[i].values()))
        query_similarity.append(cosS)

    df_q_score = pd.DataFrame(query_similarity, columns=['score'])
    sdf_q_score = df_q_score.sort_values(by='score', ascending=False)
    print("\nCosine similarity ranking:")
    for i, score in enumerate(sdf_q_score.values):
        if score[0] > 0:
            img_idx = tf_idf.getTitleByCap(cap_title_dict, sdf_q_score.index[i])
            img_path = result_list[img_idx[0]]['image_path'][img_idx[1]]
            print("Score: {}	----	IMG_path: {}".format(score, img_path))

    print("\n________________________________________________\n")

    # import pdb
    # pdb.set_trace()
# preprocesing
# returns:
# list of processed docs - cleanedDocs
# list of captions, list of titles
# bow_titles, bow_cap, bow=union(bow_t, bow_cap) m+n
# getTitle by capIdx
# getCaptions by capIdx

# indexing
# construct inverted index for all docs
# (('PMC4309823', 156), 't'),
# (('PMC4706291', 74), (74, 'c'))

# excute bool operations - AND / OR (posting1, posting2)
# returns result after query search

# weigts:
# tf-idf for titles (M, m+n)
# tf-idf for cap (N, m+n)
### final_TFIDF (N, m+n)
# cosSimilarity( all captions, query)
