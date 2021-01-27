import scrapy
import urllib.parse
import os


class PubMedImagesSpider(scrapy.Spider):
    name = 'pubMedImages'
    start_urls = [
        #'https://www.ncbi.nlm.nih.gov/pmc/journals/'
        'https://ncbi.nlm.nih.gov/pmc/issues/359201/'
    ]
    root_url = 'https://www.ncbi.nlm.nih.gov'
    articleUrls = []
    articleUrlsCount = 0
    imagesCount = 0

    def parse(self, response):
        article = response.xpath('//div[contains(@class, "article")]//h1[contains(@class, "content-title")]')
        figures = response.xpath('//div[contains(@class, "fig ")]')

        # if it is an article page parse the figures from it: // USE this idea for the journal pages
        # if article or figures:  # or ? and?
        #     articles = self.parseArticle(response)
        #     print("article or figure")
        #     for article in articles:
        #         print(article['docId'])

        articleUrls = self.parseArticleList(response)
        print("*************************************************************")
        print(self.articleUrls)
        print("*************************************************************")
        for articleUrl in self.articleUrls:
            yield response.follow(articleUrl, callback=self.parseArticle)

    def parseArticleList(self, response):
        urls = response.xpath('//div[contains(@class, "title")]/a/@href')
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
        docTitle = response.xpath('//h1[contains(@class, "content-title")]/text()').get()
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

            text = figure.xpath('.//div[contains(@class, "caption")]/p/text()').get()
            # print(text)

            yield {
                'docId': docId,
                'articleUrl': articleUrl,
                'docTitle': docTitle,
                'image_url': imgUrl,
                'image_path': imgName,
                'caption': text
            }

            i += 1
        self.imagesCount += i
        # print("*************************************************************")
        print("Total articles count:" + str(self.articleUrlsCount))
        print("Total figures count:" + str(self.imagesCount))
        print("*************************************************************")
