from __future__ import annotations
from typing import TYPE_CHECKING
from urllib.parse import urlencode
import scrapy
from gfinance_scraper.items import Stock

if TYPE_CHECKING:
    from scrapy.http.response import Response


class GainersSpider(scrapy.Spider):
    name = "gainers"
    # start_urls = ["https://www.google.com/finance/markets/gainers"]

    def start_requests(self):
        """
        Send a post request to give consent. With the continue
        key in the body, we will be redirected to the gainers page.
        """
        yield scrapy.Request(
            url="https://consent.google.com/save",
            method="POST",
            headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "content-type": "application/x-www-form-urlencoded",
                "origin": "https://consent.google.com",
                "referer": "https://consent.google.com/",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "dnt": "1",
                "accept-encoding": "gzip, deflate, br, zstd",
            },
            body=urlencode(
                {
                    "gl": "DE",
                    "m": "0",
                    "app": "0",
                    "pc": "fgc",
                    "continue": "https://www.google.com/finance/markets/gainers",
                    "x": "6",
                    "bl": "boq_identityfrontenduiserver_20250112.08_p0",
                    "hl": "en-US",
                    "src": "1",
                    "cm": "2",
                    "set_sc": "true",
                    "set_aps": "true",
                    "set_eom": "false",
                }
            ),
            callback=self.parse,
        )

    def parse(self, response: Response):
        """
        Extracts all links from the /gainers page.
        """
        links = response.xpath('//ul[@class="sbnBtf"]/li/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_single_page)

    def parse_single_page(self, response: Response):
        """
        Gets all data from the single stock page.
        """
        stock = Stock()
        stock["name"] = response.css("div.zzDege::text").get()
        stock["cur_price"] = response.css("div.fxKbKc::text").get()
        stock["closing_price"] = response.css("div.P6K39c::text").get()
        yield stock
