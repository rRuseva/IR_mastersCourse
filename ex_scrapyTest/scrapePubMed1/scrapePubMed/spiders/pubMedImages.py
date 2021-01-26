import scrapy
import urllib.parse
import os


class PubMedImagesSpider(scrapy.Spider):
    name = 'pubMedImages'
    start_urls = [
        #'https://www.ncbi.nlm.nih.gov/pmc/journals/'
        #'https://ncbi.nlm.nih.gov/pmc/issues/359201/'
        #'https://www.ncbi.nlm.nih.gov/pmc/journals/1876/'
        'https://www.ncbi.nlm.nih.gov/pmc/journals/'
    ]
    root_url = 'https://www.ncbi.nlm.nih.gov'
    articleUrls = []
    articleUrlsCount = 0
    imagesCount = 0
    issuesCount = 0
    journalsCount = 0

    def parse(self, response):
        article = response.xpath('//div[contains(@class, "article")]//h1[contains(@class, "content-title")]')
        figures = response.xpath('//div[contains(@class, "fig ")]')

        # if(article or figures):
        #     print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        #     self.parseArticle(response)

        articleList = response.xpath('//div[contains(@class, "rprt")]/div[contains(@class, "title")]/a/@href').getall()
        if articleList:
            # articleUrls = self.parseArticleList(response)
            # print("*************************************************************")
            # print(self.articleUrls)
            # print("*************************************************************")
            # for articleUrl in self.articleUrls:
            for articleUrl in articleList:
                print(articleUrl)
                # yield response.follow(self.root_url + articleUrl, callback=self.parse)
                yield response.follow(articleUrl, callback=self.parseArticle)

        issueList = response.xpath('//td/a[contains(@class, "arc-issue")]/@href').getall()
        if(issueList):
            for i, iUrl in enumerate(issueList):
                if(i < 2):
                    #print(self.root_url + issueUrl)
                    self.issuesCount += 1
                    yield response.follow(self.root_url + iUrl, callback=self.parse)

        journalList = response.xpath('//td[contains(@class, "jlist-title")]/a/@href').getall()
        if(journalList):
            for i, jUrl in enumerate(journalList):
                if(i < 2):
                    self.journalsCount += 1
                    print(jUrl)
                    yield response.follow(self.root_url + jUrl, callback=self.parse)

    def parseArticleList(self, response):
        urls = response.xpath('//div[contains(@class, "rprt")]/div[contains(@class, "title")]/a/@href')
        for article in urls:
            url = self.root_url + article.get()
            self.articleUrls.append(url)

        articlesCount = len(self.articleUrls)
        print("articlesCount: ", articlesCount)
        # yield articleUrls
        self.articleUrlsCount += articlesCount

    def parseArticle(self, response):
        print("*************************************************************")
        articleUrl = response.request.url
        print("Parsing URL: " + articleUrl)
        docTitle = response.xpath('//h1[contains(@class, "content-title")]').get()
        # print("docTitle: " + docTitle)

        docId = articleUrl.split("/")
        docId = docId[len(docId) - 2]
        #print("docId: " + docId)
        figures = response.xpath('//div[contains(@class, "fig ")]')

        n = len(figures)
        print("{n} figures are found".format(n=n))
        i = 0
        for figure in figures:
            imgUrl = self.root_url + figure.xpath('.//img/@src').get()
            # print(imgUrl)
            imgName = imgUrl.split("/")
            imgName = docId + "-" + str(i + 1) + "_" + imgName[len(imgName) - 1]

            text = figure.xpath('.//div[contains(@class, "caption")]').get()
            # print(text)

            yield {
                'articleUrl': articleUrl,
                'docTitle': docTitle,
                'docId': docId,
                'image_url': imgUrl,
                'image_path': imgName,
                'caption': text
            }

            i += 1
        self.imagesCount += i
        # print("*************************************************************")
        print("Total issues count:" + str(self.issuesCount))
        print("Total articles count:" + str(self.articleUrlsCount))
        print("Total figures count:" + str(self.imagesCount))
        print("*************************************************************")
