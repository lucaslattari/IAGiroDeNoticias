import packages
import requests
from bs4 import BeautifulSoup
import pickle
import re
from tqdm import tqdm
import logging
import re

def getTechNewsFromTheVerge(saveFileInDir, numberOfArticles):
    dictionary = {}
    dTempComment = {}

    r = requests.get("http://www.theverge.com/tech")
    soup = BeautifulSoup(r.content, 'html5lib')
    divs = soup.findAll('div', {"class": "c-compact-river__entry"})
    for tag in tqdm(divs):
        divOfArticle = tag.findAll("div", {"class": "c-entry-box--compact__body"})
        for tag in divOfArticle:
            h2 = tag.find("h2", {"class": "c-entry-box--compact__title"})
            dictionary[h2.text] = h2.find("a").get("href")

            dataComment = tag.find("div", {"class": "c-entry-stat--words"})
            if not (dataComment is None):
                dataComment = dataComment.get("data-cdata")
                dTempComment[h2.text] = int(re.findall(r'\d+', dataComment)[1])
            else:
                dTempComment[h2.text] = 0

    newDict = {}
    ii = 1
    for key, comments in sorted(dTempComment.items(), key=lambda i: i[1], reverse=True):
        for name, url in dictionary.items():
            if(name == key):
                newDict[name] = {}
                newDict[name] = dictionary[name]
        if(ii == numberOfArticles):
            break
        ii += 1

    del(dTempComment)
    del(dictionary)

    if(saveFileInDir):
        f = open("vergenews.pkl", "wb")
        pickle.dump(newDict, f)
        f.close()

    return newDict

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

def extractTextFromNews(dictionary, saveFileInDir):
    dictionaryOfArticles = {}
    listToIgnore = ('Credits', 'Vice president:', 'Deputy editor:' , 'Director of audience development:',
    'Writers:', 'Intern:', 'Social media managers:', '         ', 'Vox Media has affiliate partnerships. These do not influence editorial content, though Vox Media may earn commissions for products purchased via affiliate links. For more information, see our ethics policy.',
    'Verge Deals on Twitter', 'Related')

    iterations = 0
    for text, url in tqdm(dictionary.items()):
        print(url)
        dictionaryOfArticles[iterations] = {}
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html5lib')
        divHeader = soup.findAll('div', {"class": "c-entry-hero c-entry-hero--default"})
        if len(divHeader) == 0:
            divHeader = soup.findAll('div', {"class": "l-root l-reskin"})
        for eachDiv in divHeader:
            #pega título da matéria
            h1HeaderTitle = eachDiv.findAll('h1', {"class": "c-page-title"})
            for eachH1 in h1HeaderTitle:
                dictionaryOfArticles[iterations]["titulo"] = eachH1.text
            logging.debug(eachH1.text)

            #pega autor da matéria
            spanHeaderTitle = eachDiv.find('span', {"class": "c-byline__item"})
            dictionaryOfArticles[iterations]["autor"] = spanHeaderTitle.find("a").text
            logging.debug(spanHeaderTitle.find("a").text)

            #pega data da publicacao
            time = eachDiv.find('time', {"class": "c-byline__item"}).text.replace(" ", "")
            mo = time[1:4]
            mo = convertMonthFromStrToNumber(mo)
            if(time[5] == ','):
                d = time[4:5]
                y = time[6:10]
                h = int(time[11:12])
                mi = time[13:15]
                am_pm = time[15:17]
            else:
                d = time[4:6]
                y = time[7:11]
                h = int(time[12:13])
                mi = time[14:16]
                am_pm = time[16:18]

            if am_pm == "pm":
                h += 12

            dataPublicacao = {"dia" : d, "mes" : mo, "ano" : y, "horas" : h, "minutos" : mi}
            dictionaryOfArticles[iterations]["data"] = dataPublicacao
            logging.debug(dataPublicacao)

            #pega texto da reportagem
            divText = soup.find('div', {"class": "c-entry-content"})
            allP = divText.findAll('p')
            conteudo = ""
            totalDePalavras = 0
            paragrafos = 0
            dictionaryOfArticles[iterations]["texto"] = ""
            for p in allP:
                textParagraph = p.text
                if not textParagraph:
                    continue
                if "   Related" in textParagraph:
                    continue
                if(textParagraph.startswith(listToIgnore)):
                    continue

                conteudo += p.text + "\n"
                dictionaryOfArticles[iterations]["texto"] += textParagraph
            logging.debug(dictionaryOfArticles[iterations]["texto"])
            iterations += 1

    if(saveFileInDir):
        f = open("vergearticles.pkl", "wb")
        pickle.dump(dictionaryOfArticles, f)
        f.close()

    return dictionaryOfArticles


def scrapDataFromTheVerge(openFileInDir = True):
    if(openFileInDir):
        f = open("vergenews.pkl", "rb")
        logging.info('Carregando manchetes do site salvos em disco')
        dictionaryTechNews = pickle.load(f)
        f.close()
    else:
        logging.info('Carregando manchetes do site')
        dictionaryTechNews = getTechNewsFromTheVerge(True, 5)

    if(openFileInDir):
        logging.info('Carregando artigos do site salvos em disco')
        f = open("vergearticles.pkl", "rb")
        dictionaryArticles = pickle.load(f)
        f.close()
    else:
        logging.info('Carregando artigos do site')
        dictionaryArticles = extractTextFromNews(dictionaryTechNews, True)

    return dictionaryTechNews, dictionaryArticles
