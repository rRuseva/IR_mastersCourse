import scrapy
import urllib.parse
import os


class PubMedImagesSpider(scrapy.Spider):

    name = 'pubMedImages'
    start_urls = [
        #'https://ncbi.nlm.nih.gov/pmc/issues/359201/'
        #'https://www.ncbi.nlm.nih.gov/pmc/journals/1876/'
        'https://www.ncbi.nlm.nih.gov/pmc/journals/',
        'https://www.ncbi.nlm.nih.gov/pmc/journals/1558/'
    ]
    root_url = 'https://www.ncbi.nlm.nih.gov'
    articleUrls = []
    articleUrlsCount = 0
    imagesCount = 0
    issuesCount = 0
    journalsCount = 0

    def parse(self, response):
        pagesCount = 5
        article = response.xpath('//div[contains(@class, "article")]//h1[contains(@class, "content-title")]/text()')
        figures = response.xpath('//div[contains(@class, "fig ")]')

        articleList = response.xpath('//div[contains(@class, "rprt")]/div[contains(@class, "title")]/a/@href').getall()
        if articleList:
            for articleUrl in articleList:
                yield response.follow(articleUrl, callback=self.parseArticle)

        issueList = response.xpath('//td/a[contains(@class, "arc-issue")]/@href').getall()
        if(issueList):
            for i, iUrl in enumerate(issueList):
                if(i < pagesCount):
                    self.issuesCount += 1
                    yield response.follow(self.root_url + iUrl, callback=self.parse)

        journalList = response.xpath('//td[contains(@class, "jlist-title")]/a/@href').getall()
        if(journalList):
            for i, jUrl in enumerate(journalList):
                if(i < pagesCount):
                    self.journalsCount += 1
                    yield response.follow(self.root_url + jUrl, callback=self.parse)

    def parseArticleList(self, response):
        urls = response.xpath('//div[contains(@class, "rprt")]/div[contains(@class, "title")]/a/@href')
        for article in urls:
            url = self.root_url + article.get()
            self.articleUrls.append(url)

        articlesCount = len(self.articleUrls)
        self.articleUrlsCount += articlesCount

    def parseArticle(self, response):
        result = {}
        articleUrl = response.request.url
        print("__________________________________________________________________________")
        print("Processing: " + articleUrl)
        articleTitle = response.xpath('normalize-space(//h1[contains(@class, "content-title")])').extract_first()
        # print("articleTitle: " + articleTitle)

        articleId = articleUrl.split("/")
        articleId = articleId[len(articleId) - 2]
        #print("articleId: " + articleId)

        result['articleId'] = articleId
        result['articleUrl'] = articleUrl
        result['articleTitle'] = articleTitle
        result['image_path'] = []
        result['image_url'] = []
        result['caption'] = []

        figures = response.xpath('//div[contains(@class, "fig ")]')

        n = len(figures)
        #print("{n} figures are found".format(n=n))
        if n > 0:
            i = 0
            for figure in figures:
                imgUrl = self.root_url + figure.xpath('.//img/@src').get()
                imgName = imgUrl.split("/")
                imgName = articleId + "-" + str(i + 1) + "_" + imgName[len(imgName) - 1]

                text = figure.xpath('normalize-space(.//div[contains(@class, "caption")]/p)').extract_first()
                # print(text)
                result['image_path'].append(imgName)
                result['image_url'].append(imgUrl)
                result['caption'].append(text)

                i += 1
            self.imagesCount += i
            yield result

        print("*************************************************************")
        print("Total journals count: " + str(self.journalsCount))
        print("Total issues count: " + str(self.issuesCount))
        print("Total articles count: " + str(self.articleUrlsCount))
        print("Total figures count: " + str(self.imagesCount))

        print("*************************************************************")
