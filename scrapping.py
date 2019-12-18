# coding: utf-8
import packages
import requests
from bs4 import BeautifulSoup
import pickle
import re
from tqdm import tqdm
import logging
import re
import stringUtils as s
import os.path

def getTechNewsFromTheVerge(saveFileInDir, numberOfArticles):
    dictionary = {}
    dTempComment = {}

    r = requests.get("http://www.theverge.com/tech")
    soup = BeautifulSoup(r.content, 'html5lib')
    divs = soup.findAll('div', {"class": "c-compact-river__entry"})
    for tag in tqdm(divs):
        divOfArticle = tag.findAll("div", {"class": "c-entry-box--compact__body"})
        for tag in divOfArticle:
            #pega url
            h2 = tag.find("h2", {"class": "c-entry-box--compact__title"})
            dictionary[h2.text] = h2.find("a").get("href")

            #pega número de comentários
            dataComment = tag.find("div", {"class": "c-entry-stat--words"})
            if not (dataComment is None):
                dataComment = dataComment.get("data-cdata")
                dTempComment[h2.text] = int(re.findall(r'\d+', dataComment)[1])
            else:
                dTempComment[h2.text] = 0

    newDict = {}
    ii = 1
    for key, comments in sorted(dTempComment.items(), key=lambda i: i[1], reverse=True):
        if ii == 0:
            continue
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
        return "janeiro"
    elif(m.lower() == "fev"):
        return "fevereiro"
    elif(m.lower() == "mar"):
        return "março"
    elif(m.lower() == "apr"):
        return "abril"
    elif(m.lower() == "may"):
        return "maio"
    elif(m.lower() == "jun"):
        return "junho"
    elif(m.lower() == "jul"):
        return "julho"
    elif(m.lower() == "aug"):
        return "agosto"
    elif(m.lower() == "sep"):
        return "setembro"
    elif(m.lower() == "oct"):
        return "outubro"
    elif(m.lower() == "nov"):
        return "novembro"
    elif(m.lower() == "dec"):
        return "dezembro"

def extractTextFromNews(dictionary, saveFileInDir):
    dictionaryOfArticles = {}
    listToIgnore = ('Credits', 'Vice president:', 'Deputy editor:' , 'Director of audience development:',
    'Writers:', 'Intern:', 'Social media managers:', '         ', 'Vox Media has affiliate partnerships. These do not influence editorial content, though Vox Media may earn commissions for products purchased via affiliate links. For more information, see our ethics policy.',
    'Verge Deals on Twitter', 'Related')

    iterations = 0
    for text, url in tqdm(dictionary.items()):
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
                temp = s.cleanSentence(eachH1.text)
                if(isinstance(temp, list)):
                    temp = temp[0]
                dictionaryOfArticles[iterations]["titulo"] = s.cleanSentence(eachH1.text)
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
            totalDePalavras = 0
            paragrafos = 0
            dictionaryOfArticles[iterations]["texto"] = ""
            for p in allP:
                textParagraph = s.cleanSentence(p.text)
                if not textParagraph:
                    continue
                if "   Related" in textParagraph:
                    continue
                if(textParagraph.startswith(listToIgnore)):
                    continue

                if(isinstance(textParagraph, list)):
                    textParagraph = textParagraph[0]

                dictionaryOfArticles[iterations]["texto"] += textParagraph
            logging.debug(dictionaryOfArticles[iterations]["texto"])
            iterations += 1

    if(saveFileInDir):
        f = open("vergearticles.pkl", "wb")
        pickle.dump(dictionaryOfArticles, f)
        f.close()

    return dictionaryOfArticles

def scrapDataFromTheVerge():
    if(os.path.isfile('vergenews.pkl')):
        logging.info('Carregando manchetes do site salvos em disco')
        try:
            f = open("vergenews.pkl", "rb")
        except IOError:
            logging.error("ERRO: Arquivo vergenews.pkl não encontrado")
            exit()

        dictionaryTechNews = pickle.load(f)
        f.close()
    else:
        logging.info('Carregando manchetes do site')
        dictionaryTechNews = getTechNewsFromTheVerge(True, 10)

    if(os.path.isfile('vergearticles.pkl')):
        logging.info('Carregando artigos do site salvos em disco')
        try:
            f = open("vergearticles.pkl", "rb")
        except IOError:
            logging.error("ERRO: Arquivo vergearticles.pkl não encontrado")
            exit()
        dictionaryArticles = pickle.load(f)
        f.close()
    else:
        logging.info('Carregando artigos do site')
        dictionaryArticles = extractTextFromNews(dictionaryTechNews, True)

    return dictionaryTechNews, dictionaryArticles
