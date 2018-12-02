

import scrapy
from scrapy_splash import SplashRequest


class GithubSpider(scrapy.Spider):
    name = "github"
    login_url = "https://github.com/login"
    urls = [
        'https://github.com/AIHackers/IA002',
    ]

    repo_name = "IA002"
    orig_user = "AIHackers"

    def start_requests(self):
        self.log("login: %s" % self.login_url)
        yield scrapy.Request(url=self.login_url, callback=self.login)

    def login(self, response):
        form_login = {
            "login": "wanggengjie@gmail.com",
            "password": "wgj@0122"
        }
        yield scrapy.FormRequest.from_response(response, formdata=form_login, callback=self.parse_login)

    def parse_login(self, response):
        url = "https://github.com/%s/%s/network/members" % (self.orig_user, self.repo_name)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        chapters = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5']
        for a in response.xpath('//div[@id="network"]').css(".repo").css(".d-inline-block[href]"):
            for ch in chapters:
                url_repo = "https://github.com/" + a.attrib['href'] + "/" + self.repo_name + "/tree/master/" + ch
                self.log("go to : "+url_repo)
                yield SplashRequest(url=url_repo, callback=self.parse_repo, args={'wait': 2})

    def parse_repo(self, response):
        self.log("parse repo: " + response.url)
        for item in response.css("table.files").css("tr.js-navigation-item"):
            self.log(item.getall())
            try:
                content = item.css("td.content").css("a")
                ## self.log("content:" + content[0].gatall())
                modified_time = item.css("td.age")
                self.log("%s : %s" % (content[0].attrib['title'], modified_time[0].attrib['datetime']))
            except:
                ## exit(0)
                pass

