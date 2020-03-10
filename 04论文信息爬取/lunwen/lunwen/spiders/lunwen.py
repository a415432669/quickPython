import scrapy
#导入定义的论文item结构
from lunwen.items import LunwenItem;

class Lunwen(scrapy.Spider):
    #定义爬虫的名字
    name = "lunwen"
    #定义爬取论文的网站名称
    host = 'https://www.xzbu.com'
    #论文的关键词
    keyword = "java"
    #从第一页开始爬取
    page = 1

    #设置开始爬虫页面
    def start_requests(self):
        start_url = 'https://www.xzbu.com/search/{}/{}'.format(self.keyword,self.page)
        yield  scrapy.Request(url=start_url,callback=self.parse) 

    
    #设置解析列表页的函数
    def parse(self,response):
        #提取页面的列表元素
        linka = response.css('.article_left .main2 ul li')
        #获取列表的所有论文的a链接
        for item in linka:
            title = item.css('a::text').extract_first()
            link = self.host + item.css('a::attr(href)').extract_first()
            #将a链接以scrapy请求对象作为返回的迭代内容
            yield scrapy.Request(link,callback=self.parsePage)
        #判断当前页面论文的链接数是否是15篇，如果为15篇，即会有下一篇，因此将下一篇链接返回
        if(len(list(linka.extract()))==15):
            self.page+=1
            nextLink = 'https://www.xzbu.com/search/{}/{}'.format(self.keyword,self.page)
            yield scrapy.Request(nextLink,callback=self.parse)
    
    #解析页面，获取论文的标题和论文内容
    def parsePage(self,response):
        title = response.css('body > div.article > div > div.article_left > div.article_leftBox > h2::text').extract_first()
        content = response.css('body > div.article > div > div.article_left > div.article_leftBox > p').extract_first()
        item = LunwenItem()
        item['title'] = title
        item['content'] = content
        #将提取的内容以item的形式返回迭代内容
        yield item
