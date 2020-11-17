import scrapy
import urllib.parse
import os


class QuotesSpider(scrapy.Spider):
    name = "fmi_staff"
    start_urls = [
        'https://www.fmi.uni-sofia.bg/bg/faculty-staff'
    ]

    def parse(self, response):
        staff = response.('YOUR_FIRST_SELECTOR')
        if staff:
            # parse the teacher's info from reponse

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

        faculty_staff = # Follow all the staff members custom URL's

        next_page = # Get next page and follow it