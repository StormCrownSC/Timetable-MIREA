#!/usr/bin/env python3
from concurrent.futures import ThreadPoolExecutor as Pool
import os
import re
import requests
from bs4 import BeautifulSoup
import openpyxl
import time
import json
from datetime import datetime


class Parser:
    def __init__(self):
        self.log("start parser")
        self.links = self.find_urls()
        self.timetable = {}
        self.loader()
        self.read_data()

    @staticmethod
    def log(text):
        print(datetime.utcnow().isoformat(sep=' ', timespec='milliseconds') + " UTC LOG: " + text)

    @staticmethod
    def find_urls():
        page = BeautifulSoup(requests.get("https://www.mirea.ru/schedule/").text, "html.parser")
        return re.findall('<a class="uk-link-toggle" href="([\S]+.xl[\w]+)" target="_blank">', str(page))

    def loader(self):
        self.log("start loader")
        self.check_directory()
        with Pool(max_workers=len(self.links)) as executor:
            executor.map(self.download, self.links)

    @staticmethod
    def download(link):
        with open("temp/" + link.split("/")[-1], "wb") as file:
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
        if os.path.exists("success"):
            os.remove("success")
        if not os.path.exists("temp"):
            os.mkdir("temp")
        elif len(os.listdir("temp")) != 0:
            with Pool(max_workers=len(os.listdir("temp"))) as executor:
                executor.map(self.remove_file, os.listdir("temp"))

    def read_files(self, file):
        book = openpyxl.load_workbook("temp/" + file)
        day_of_the_week = {0: "Понедельник", 1: "Вторник", 2: "Среда", 3: "Четверг", 4: "Пятница", 5: "Суббота"}
        for name in book.sheetnames:
            sheet = book[name]
            flag = False
            for index, arr in enumerate(sheet):
                flag_optimize = False
                global_col = None
                max_row = sheet.max_row
                first_len_flag = True
                for elem in arr:
                    if len(re.findall(r"\w\w\w\w\-\d\d\-\d\d", str(elem.value))) != 0:
                        flag = True
                        flag_optimize = True
                        col = elem.column
                        letter = elem.row
                        if global_col is None:
                            global_col = elem.column - 4
                        temp_dict = {"I": {}, "II": {}}
                        day_index = -1
                        for item in range(letter + 2, max_row):
                            if first_len_flag is True and sheet.cell(row=item, column=global_col).value is None \
                                and sheet.cell(row=item-1, column=global_col).value is None:
                                first_len_flag = False
                                max_row = item
                                break
                            if sheet.cell(row=item, column=global_col).value == 1:
                                day_index += 1
                                temp_dict["I"][day_of_the_week.get(day_index)] = {}
                                temp_dict["II"][day_of_the_week.get(day_index)] = {}

                            type_of_week, lesson_number, tmp_data = self.data_of_lesson(sheet, item, col, global_col)
                            temp_dict[type_of_week][day_of_the_week.get(day_index)][lesson_number] = tmp_data

                        self.timetable[elem.value] = temp_dict
                    if flag_optimize is False and index > 8:
                        break
                if flag is True:
                    break

    def data_of_lesson(self, sheet, item, col, global_col):
        new_item = item
        if sheet.cell(row=new_item, column=global_col).value is None:
            new_item -= 1
        lesson_number = sheet.cell(row=new_item, column=global_col).value
        if sheet.cell(row=new_item-2, column=col).value == 7 or lesson_number == 8:
            lesson_number += 1

        temp_array = [sheet.cell(row=item, column=col).value, sheet.cell(row=item, column=col+1).value,
            sheet.cell(row=item, column=col+2).value, sheet.cell(row=item, column=col+3).value]
        return sheet.cell(row=item, column=global_col+3).value, lesson_number, temp_array
        
    def read_data(self):
        self.log("start read data")
        with Pool(max_workers=len(os.listdir("temp"))) as executor:
            executor.map(self.read_files, os.listdir("temp"))
    
    def __del__(self):
        self.check_directory()
        if os.path.exists("temp"):
            os.rmdir("temp")
        with open("success", "w") as file:
            file.write("")
        self.log("end")


if __name__ == "__main__":
    while True:
        Parser()
        time.sleep(14400)
