import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from gfinance_scraper.spiders.gainers_spider import GainersSpider


def run_spider():
    # Set up the Scrapy settings
    process = CrawlerProcess(get_project_settings())

    # add spider
    process.crawl(GainersSpider)

    # additional options
    # process.settings.set("USER_AGENT", "my-custom-user-agent")

    process.start()


if __name__ == "__main__":
    run_spider()
