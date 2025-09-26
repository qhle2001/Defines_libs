import random
import json
import re
import time
from datetime import datetime
from selenium import webdriver
from enum import Enum

class Level:
    easy   = 'easy'
    medium = 'medium'
    hard   = 'hard'

class CodeLang(Enum):
    dart   = "dart"
    swift  = "swift"
    python = "python"

class Solve:
    def __init__(self, 
                 type  : str,
                 name  : str,
                 level : Level,
                 solved: bool=False): 
        self.type   = type
        self.name   = name
        self.level  = level
        self.solved = solved

class Base:
    file_path:str = ""
    def __init__(self):
        pass
    
    def convert_sets(self, obj):
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, dict):
            return {k: self.convert_sets(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self.convert_sets(i) for i in obj]
        return obj

    def writeFile(self, data):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.convert_sets(data), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(e)

    def readFile(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(e)
        return ""  

class Random(Base):
    def __init__(self):
        super().__init__()
        self.file_path = 'leet_code.json'
        self._maxID = float('-inf')
        self._data = dict()
        self._lang_quota = {}

    def saveQuestion(self, data):
        results = data["props"]["pageProps"]["dehydratedState"]["queries"][0]["state"]["data"]["studyPlanV2Detail"]["planSubGroups"]
        for res in results:
            for question in res["questions"]:
                self._maxID = max(int(question["id"]), self._maxID)
                self._data[question["id"]] = {
                    "title": question["title"],
                    "difficulty": question["difficulty"],
                    "codeLang": "",
                    "solved": False
                }
        self.writeFile(self._data)

    def divideLangPercent(self):
        langs = list(CodeLang)
        numExcerise = len(self._data.keys())
        base = numExcerise // len(langs)
        remains = numExcerise % len(langs)

        lang_quota = {lang.value: base for lang in langs}

        for lang in random.sample(langs, remains):
            lang_quota[lang] += 1

        return lang_quota
    
    def pickCodeLang(self):
        availale = [lang for lang, remain in self._lang_quota.items() if remain > 0]
        if not availale:
            return None
        
        choice = random.choice(availale)
        self._lang_quota[choice] -= 1
        return choice

    def random(self):
        random_again = False
        while True:
            if len(self._data) == 0:
                print("Enter file name: ")
                filename = input().strip()
                if filename == "":
                    continue
                self.file_path = filename
                self._data = self.readFile()
                self._lang_quota = self.divideLangPercent()
                for key, _ in self._data.items():
                    self._maxID = max(int(key), self._maxID)

            if len(self._data) == 0:
                break
            _id = f"{random.randint(0, self._maxID)}"
            if _id not in self._data.keys():
                continue
            if self._data[f"{_id}"]["solved"] == True:
                continue

            _codeLang = self.pickCodeLang()
            print("="*30, datetime.now())
            print(f"Id: {_id} Title: {self._data[_id]['title']} -- CodeLang: {_codeLang} -- Difficulty: {self._data[_id]['difficulty']}")
            print("="*30)
            self._data[_id]["codeLang"] = _codeLang
            self.writeFile(self._data)
            while True:
                try:
                    random_again = False
                    print("Enter: ")
                    print("     (r) To Random Again.")
                    print("     (q) To Exit.")
                    print("     (m) To Mark Solved.")
                    print("     (g) Get The Number Of Solved Exercises")
                    key = input().strip().lower()
                    if key == "r":
                        random_again = True
                        self._data[_id]["codeLang"] = ""
                        self.writeFile(self._data)
                        break
                    if key == "q":
                        self._data[_id]["codeLang"] = ""
                        self.writeFile(self._data)
                        break
                    elif key == "m":
                        self._data[_id]['solved'] = True
                        self.writeFile(self._data)
                        break
                    elif key == "g":
                        numOfSolved = len([solved for _, solved in self._data.items() if solved["solved"] == True])
                        print(f"You solved {numOfSolved} excercised")
                except Exception as e:
                    print(e)
            if not random_again:
                break
            

class CrawlData(Base):
    def __init__(self):
        super().__init__()
        self.file_path = ""
        self._data = None

    def crawl(self, url):
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(5)

        html = driver.page_source
        match = re.search(
            r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
            html,
            re.S
        )
        if not match:
            raise Exception("Không tìm thấy __NEXT_DATA__")
        self._data = json.loads(match.group(1))
        driver.quit()
    
    def saveData(self):
        self.writeFile(self._data)        
    
class Controller:
    def __init__(self):
        self._randomMode = Random()
        self._crawlDataMode = CrawlData()
        self._file_name = ""
        self._urls = ""
    
    def _craw_data(self):
        while True:
            try:
                print("Enter the URLs: ")
                urls = input("")
                if urls.strip() == "":
                    print("The URLs is null, please re-enter the URLs.")
                    continue
                if urls == "q":
                    break
                self._crawlDataMode.crawl(urls)
                break
            except Exception as e:
                print(e)
    
    def _saveCrawlData(self):
        while True:
            try:
                print("Enter file name: ")
                file_name = input()
                if file_name.strip() == "":
                    print("File name is null, please re-enter file name.")
                    continue
                if file_name == "q":
                    break
                self._file_name = file_name
                self._crawlDataMode.file_path = file_name
                self._crawlDataMode.saveData()
                break
            except Exception as e:
                print(e)
    
    def _saveQuestions(self):
        while True:
            try:
                print("Enter:")
                print("     (q) To Exit.")
                if self._file_name == "":
                    print("Enter the destination file: ")
                    file_name = input().strip()
                    if file_name.strip() == "":
                        print("File name is null, please re-enter file name.")
                        continue
                    if file_name == "q":
                        break
                    self._file_name = file_name

                self._randomMode.file_path = self._file_name
                data = self._randomMode.readFile()
                # print(data)
                print("Enter the save file name: ")
                file_name1 = input().strip()
                if file_name1 == "":
                    print("File name is null, please re-enter the file name.")
                    continue
                if file_name1 == "q":
                    break
                self._file_name = file_name1
                self._randomMode.file_path = self._file_name
                self._randomMode.saveQuestion(data)
                break
            except Exception as e:
                print(e)

    def _random(self):
        self._randomMode.random()

    def run(self):
        while True:
            print("Enter:")
            print("     (q) To Exit.")
            print("     (c) To Crawl Data.")
            print("     (s) To Save Crawl Data.")
            print("     (sq) To Save Questions.")
            print("     (r) To Random Title.")

            key = input("Enter key: ").strip().lower()
            if key == 'q':
                break
            elif key == 'c':
                self._craw_data()
            elif key == "s":
                self._saveCrawlData()
            elif key == "sq":
                self._saveQuestions()
            elif key == "r":
                self._random()
            else:
                print("⚠️ Invalid key, please try again.")

if __name__ == "__main__":
    Controller().run()