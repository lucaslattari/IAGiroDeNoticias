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

def convertMonthFromStrToNumber(m):
    if(m.lower() == "jan"):
        return 1
    elif(m.lower() == "fev"):
        return 2
    elif(m.lower() == "mar"):
        return 3
    elif(m.lower() == "apr"):
        return 4
    elif(m.lower() == "may"):
        return 5
    elif(m.lower() == "jun"):
        return 6
    elif(m.lower() == "jul"):
        return 7
    elif(m.lower() == "aug"):
        return 8
    elif(m.lower() == "sep"):
        return 9
    elif(m.lower() == "oct"):
        return 10
    elif(m.lower() == "nov"):
        return 11
    elif(m.lower() == "dec"):
        return 12

def extractTextFromNews(dictionary, totalArticles, saveFileInDir):
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
            mo = time[1:4]
            mo = convertMonthFromStrToNumber(mo)
            d = time[4:6]
            y = time[7:11]
            h = int(time[12:13])
            mi = time[14:16]
            am_pm = time[16:18]

            if am_pm == "pm":
                h += 12

            dataPublicacao = {"dia" : d, "mes" : mo, "ano" : y, "horas" : h, "minutos" : mi}
            dictionaryOfArticles[iterations]["data"] = dataPublicacao

        #pega parte do texto da reportagem
        divText = soup.find('div', {"class": "c-entry-content"})
        allP = divText.findAll('p')
        conteudo = ""
        totalDePalavras = 0
        paragrafos = 0
        dictionaryOfArticles[iterations]["texto"] = {}
        for p in allP:
            conteudo += p.text + "\n"
            dictionaryOfArticles[iterations]["texto"][paragrafos] = p.text
            totalDePalavras += len(re.findall(r'\w+', conteudo))
            if(totalDePalavras > 50):
                break
            paragrafos += 1

        dictionaryOfArticles[iterations]["total de palavras"] = totalDePalavras

        iterations += 1
        if(iterations == 5):
            break

    if(saveFileInDir):
        f = open("vergearticles.pkl", "wb")
        pickle.dump(dictionaryOfArticles, f)
        f.close()

    return dictionaryOfArticles


def scrapDataFromTheVerge():
    openFileInDir = True

    if(openFileInDir):
        f = open("vergenews.pkl", "rb")
        dictionaryTechNews = pickle.load(f)
        f.close()
    else:
        dictionaryTechNews = getTechNewsFromTheVerge(True)

    if(openFileInDir):
        f = open("vergearticles.pkl", "rb")
        dictionaryArticles = pickle.load(f)
        f.close()
    else:
        dictionaryArticles = extractTextFromNews(dictionaryTechNews, 5, True)

    return dictionaryTechNews, dictionaryArticles
