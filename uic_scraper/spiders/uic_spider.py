__author__="Jun"

import scrapy

from uic_scraper.Course import Course
from uic_scraper.links import Links

# how to run:
# scrapy crawl uic_scraper -o filename.json

class tutorialSpider(scrapy.Spider):
    name = "uic_scraper"

    allowed_domains = ["ossswebcs.admin.uillinois.edu"]

    url = "http://ossswebcs.admin.uillinois.edu/portal_uic/class_schedule/classscheduledisplay.asp?"

    start_urls = [
        url
    ]

    def parse(self, response):
        # Format
        # subjvalue: ALL|ALL  =>  subject | course
        # sec_sel: ALL        =>  all sections
        # term: 220178        =>  Fall 2017
        # pterm: ALL          =>  full term + part term

        data = {'subjvalue': 'ASP|ALL', 'sec_sel': 'ALL', 'term': '220178', 'pterm': 'ALL',}
        yield scrapy.FormRequest(url=self.url, formdata=data, callback=self.parse_link)

    # extract every link of 'View All Sections'
    def parse_link(self, response):
        print '-'*50

        links = []
        for rows in response.xpath('//table[@id="mytable"]'):
            for row in rows.xpath('.//tr'):
                link = row.xpath('.//a/@href').re(r'coursecall.*ALL')

                for l in link:
                    detail_link = self.url + l
                    links.append(detail_link)

        for link in links:
            item = Links()
            item['Link'] = link
            yield item

    print '-' * 50

    # ----------------------------------------------------------------------------------#

    def parse_course(self, response):
        print '-'*50
        courses = []
        for rows in response.xpath('//table[@id="mytable"]'):
            for row in rows.xpath('.//tr'):
                course = row.xpath('.//a/text()').extract()
                credit = row.xpath('.//td/text()').extract_first()
                course.insert(3, credit)
                courses.append(course[0:4])

        for course in courses:
            item = Course()
            item['Subject'] = course[0:1]
            item['Number'] = course[1:2]
            item['Title'] = course[2:3]
            item['Hours'] = course[3:4]
            yield item



