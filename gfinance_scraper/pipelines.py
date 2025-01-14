# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json
import csv
from itemadapter import ItemAdapter


class GfinanceScraperPipeline:
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    """
    Pipeline dumping all results in a json file.
    """

    def open_spider(self, spider):
        self.file = open("output/items.jsonl", "w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item


class CsvWriterPipeline:
    def open_spider(self, spider):
        # Open a CSV file when the spider starts
        self.file = open("output/items.csv", "w", newline="", encoding="utf-8")
        self.writer = None

    def close_spider(self, spider):
        # Close the file when the spider ends
        self.file.close()

    def process_item(self, item, spider):
        # Initialize the CSV writer with headers on the first item
        if self.writer is None:
            self.writer = csv.DictWriter(self.file, fieldnames=item.keys())
            self.writer.writeheader()

        # Write the item to the CSV file
        self.writer.writerow(item)
        return item
