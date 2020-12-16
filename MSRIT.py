import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


class MSRIT_RES():
    url = 'http://exam.msrit.edu/index.php'
    values = {'usn': '',
              'option': 'com_examresult',
              'task': 'getResult'}

    # Constructor to Get the USN
    def __init__(self, usn) -> str:
        self.values["usn"] = usn
        # get the page source and parse it
        re = requests.get(self.url, params=self.values).text
        soup = BeautifulSoup(re, 'html.parser')
        self.soup = soup

    # Funtion to Get Name

    def Name(self):
        name = self.soup.find(
            "div", {"class": "uk-card uk-card-body stu-data stu-data1"}).find("h3").getText()
        return name

    # Funtion to Get semister
    def sem(self):
        data = self.soup.find(
            "div", {"class": "uk-card uk-card-body stu-data stu-data2"}).find("p").getText()
        sem = (data.split(","))
        return sem[1]

    # Funtion to Get registered Credits
    def credits_reg(self):
        credits_reg = self.soup.find(
            "div", {"class": "uk-card uk-card-default uk-card-body credits-sec1"}).find("p").getText()
        return credits_reg

    # Funtion to Get Earned Credits
    def credits_earned(self):
        credits_earn = self.soup.find(
            "div", {"class": "uk-card uk-card-default uk-card-body credits-sec2"}).find("p").getText()
        return credits_earn

    # Funtion to Get SGPA
    def sgpa(self):
        sgpa = self.soup.find(
            "div", {"class": "uk-card uk-card-default uk-card-body credits-sec3"}).find("p").getText()
        return sgpa

    # Funtion to Get CGPA
    def cgpa(self):
        cgpa = self.soup.find(
            "div", {"class": "uk-card uk-card-default uk-card-body credits-sec4"}).find("p").getText()
        return cgpa

    # Funtion to Get Provisional grade card
    def markscardpdf(self):
        url = "http://exam.msrit.edu/index.php/component/report/?task=getReport&id=procard&usn=" + \
            self.values["usn"]
        return url

    def result_table(self):
        res = self.soup.find(
            "table", {"class", "uk-table uk-table-striped res-table"}).find_all("tr")[1:]
        results = []
        for item in res:
            r = []
            data = item.find_all('td')
            for x in data:
                r.append(x.get_text(strip=True))
            r[1] = r[1].replace(' ', '\n')
            results.append([r[1], r[3], r[4]])
        respList = [['C N', 'C E', 'G']] + results
        respList = tabulate(respList, headers='firstrow', tablefmt="grid")
        return respList
