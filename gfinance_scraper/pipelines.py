# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import csv
from itemadapter import ItemAdapter


class GfinanceScraperPipeline:
    """Default pipleine just fowrarding an item"""

    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    """
    Pipeline dumping all results in a json file
    """

    def open_spider(self, spider):
        """Oepn a JSON file when spider starts"""
        self.file = open("output/items.jsonl", "w")

    def close_spider(self, spider):
        """Close the file when the spieder ends"""
        self.file.close()

    def process_item(self, item, spider):
        """Write item dict + linebreak to the json file"""
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class CsvWriterPipeline:
    """
    Pipeline writing all results/items to a csv file
    """

    def open_spider(self, spider):
        """Open a CSV file when the spider starts"""
        self.file = open("output/items.csv", "w", newline="", encoding="utf-8")
        self.writer = None

    def close_spider(self, spider):
        """Close the file when the spieder ends"""
        self.file.close()

    def process_item(self, item, spider):
        """
        Initialize the CSV writer with headers on the first item and
        writes item by item to the csv file.
        """
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
            self.writer.writeheader()

        self.writer.writerow(item)
        return item
