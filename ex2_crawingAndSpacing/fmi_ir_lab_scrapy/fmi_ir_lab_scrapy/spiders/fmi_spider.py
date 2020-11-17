import scrapy
import urllib.parse
import os


class QuotesSpider(scrapy.Spider):
    name = "fmi_staff"
    start_urls = [
        'https://www.fmi.uni-sofia.bg/bg/faculty-staff'
    ]

    def parse(self, response):
        staff = response.css('div.faculty-content-wrapper')
        if staff:
            # The rules are automatically extracted from Firefox's inspector.
            name = staff.css('.node-title::text').get()
            titles = staff.css('div.field:nth-child(1) > div:nth-child(1) > div::text').getall()
            department = staff.css('h3 > a::attr(href)').get()
            email = staff.css('div.field:nth-child(3) > div:nth-child(2) > div:nth-child(1)::text').get()
            phone = staff.css('div.field:nth-child(4) > div:nth-child(2) > div:nth-child(1)::text').get()
            office = staff.css('div.field:nth-child(5) > div:nth-child(2) > div:nth-child(1)::text').get()
            image_url = staff.css('a.image-popup::attr(href)').get()

            path = urllib.parse.urlparse(image_url).path
            ext = os.path.splitext(path)[1]
            img_path = ''.join((name, ext))

            yield {
                'name': name,
                'title': titles,
                'department': department,
                'email': email,
                'phone': phone,
                'office': office,
                'image_path': img_path,
                'image_url': image_url
            }

        faculty_staff = response.css('div.views-row > div > h3 > a::attr(href)').getall()
        for href in faculty_staff:
            yield response.follow(href, callback=self.parse)

        next_page = response.css('.pager-next > a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
