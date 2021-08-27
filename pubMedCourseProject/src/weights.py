import scrapy
from scrapy.crawler import CrawlerProcess


def callScraper(spider):
    process = CrawlerProcess(settings={

    })

    process.crawl(spider)
    process.start()


if __name__ == "__main__":
    print("start")
    # call the crower of pubMed
    callScraper('scrapePubMed\\pubMedImages')
