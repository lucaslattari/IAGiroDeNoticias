import packages
import requests
from bs4 import BeautifulSoup
import pickle
import re

def getTechNewsFromTheVerge(saveFileInDir):
    dictionary = {}

    r = requests.get("http://www.theverge.com/tech")
    soup = BeautifulSoup(r.content, 'html5lib')
    divs = soup.findAll('div', {"class": "c-compact-river__entry"})
    for tag in divs:
        divOfArticle = tag.findAll("div", {"class": "c-entry-box--compact__body"})
        for tag in divOfArticle:
            h2 = tag.findAll("h2", {"class": "c-entry-box--compact__title"})
            for eachH2 in h2:
                dictionary[eachH2.text] = eachH2.find("a").get("href")

    if(saveFileInDir):
        f = open("vergenews.pkl", "wb")
        pickle.dump(dictionary, f)
        f.close()

    return dictionary

def extractTextFromNews(dictionary, totalArticles):
    dictionaryOfArticles = {}

    iterations = 0
    for text, url in dictionary.items():
        dictionaryOfArticles[iterations] = {}
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        divHeader = soup.findAll('div', {"class": "c-entry-hero c-entry-hero--default"})
        for eachDiv in divHeader:
            #pega título da matéria
            h1HeaderTitle = eachDiv.findAll('h1', {"class": "c-page-title"})
            for eachH1 in h1HeaderTitle:
                dictionaryOfArticles[iterations]["titulo"] = eachH1.text

            #pega autor da matéria
            spanHeaderTitle = eachDiv.find('span', {"class": "c-byline__item"})
            dictionaryOfArticles[iterations]["autor"] = spanHeaderTitle.find("a").text

            #pega data da publicacao
            time = eachDiv.find('time', {"class": "c-byline__item"}).text.replace(" ", "")
            mes = time[1:4]
            dia = time[4:6]
            ano = time[7:11]
            horas = time[12:13]
            minutos = time[14:16]
            am_pm = time[16:18]
            dataPublicacao = {"dia" : dia, "mes" : mes, "ano" : ano, "horas" : horas, "minutos" : minutos, "AM_PM" : am_pm}
            dictionaryOfArticles[iterations]["data"] = dataPublicacao
        iterations += 1

        if(iterations == 5):
            break
    print(dictionaryOfArticles)

if __name__ == '__main__':
    openFileInDir = True

    if(openFileInDir):
        f = open("vergenews.pkl", "rb")
        dictionaryTechNews = pickle.load(f)
        f.close()
    else:
        dictionaryTechNews = getTechNewsFromTheVerge(True)

    extractTextFromNews(dictionaryTechNews, 5)
