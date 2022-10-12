#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor as Pool

import os
import re
import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self):
        self.links = self.find_urls()
        self.loader()

    @staticmethod
    def find_urls():
        page = BeautifulSoup(requests.get("https://www.mirea.ru/schedule/").text, "html.parser")
        return re.findall('<a class="uk-link-toggle" href="([\S]+.xl[\w]+)" target="_blank">', str(page))

    def loader(self):
        self.check_directory()
        with Pool(max_workers=len(self.links)) as executor:
            executor.map(self.download, self.links)

    @staticmethod
    def download(link):
        with open("temp/" + link.split("/")[-1].split(".xls")[0] + ".xlsx", "wb") as file:
            link_content = requests.get(link)
            count_request = 0
            while link_content.status_code != 200 and count_request != 100:
                link_content = requests.get(link)
                count_request += 1
            file.write(link_content.content)

    @staticmethod
    def remove_file(file):
        os.remove("temp/" + file)

    def check_directory(self):
        if not os.path.exists("temp"):
            os.mkdir("temp")
        elif len(os.listdir("temp")) != 0:
            with Pool(max_workers=len(os.listdir("temp"))) as executor:
                executor.map(self.remove_file, os.listdir("temp"))


def main():
    Parser()


main()