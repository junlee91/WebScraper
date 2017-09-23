import scrapy


class Course(scrapy.Item):
    Subject = scrapy.Field()
    Number = scrapy.Field()
    Title = scrapy.Field()
    Hours = scrapy.Field()