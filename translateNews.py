# coding: utf-8
import packages
from translate import Translator
import sys
import time
import pickle
import logging
import os
import requests
import os.path
from os import path
import stringUtils as s

def countdown(seconds, printMessage = True):
    for i in range(seconds, 0, -1):
        if(printMessage):
            logging.info("Aguarde " + str(i) + " segundos para tentar traduzir de novo...")
        time.sleep(1)

def returnBytes(str):
    return len(str.encode('utf-8'))

def translateConsideringAPILimit(text, langPair):
    if(langPair == "en_to_pt"):
        langPair = "en|pt"
    elif(langPair == "pt_to_en"):
        langPair = "pt|en"

    try:
        f = open("email", "r")
    except IOError as err:
        print("I/O error: {0}".format(err))
        exit()
    email = f.readline()
    f.close()

    #ip
    ip = requests.get('https://api.ipify.org').text
    text = text.replace(" ", '%20')

    #get translated text in json
    url_mymemory = "https://api.mymemory.translated.net/get?q=" + text + "&langpair=" + langPair + "&ip=" + ip + "&de=" + email
    logging.debug(url_mymemory)
    jDict = requests.get(url_mymemory).json()
    jDict["responseData"]["translatedText"] = s.cleanSentence(jDict["responseData"]["translatedText"])
    logging.info(jDict)

    if(jDict["quotaFinished"] == True):
        logging.info("Você estourou a cota!")
        exit()

    return jDict["responseData"]["translatedText"]
    '''
    if en_to_pt == "True":
        translator = Translator(to_lang = "pt")
    else:
        translator = Translator(to_lang = "en")
    translated = translator.translate(text)
    if "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN" in translated:
        h,m,s = [int(s) for s in translated.split() if s.isdigit()]
        countdown(s + m * 60 + h * 60 * 60)
    else:
        return translated
    return translator.translate(text)
    '''

def constructDictionary(dHeader, dArticle, totalOfArticles = 3):
    i = 0
    dFinal = {}
    for headline, url in dHeader.items():
        logging.debug("Manchete: " + headline)
        dFinal[i] = {}
        if(path.exists("traduzidos/manchete" + str(i)) == False):
            logging.debug("CUIDADO: Você está gastando a cota da API de tradução!")
            f = open("traduzidos/mancheteingles" + str(i), "w")
            f.write(headline)
            f.close()

            logging.info(headline)
            dFinal[i]["manchete"] = translateConsideringAPILimit(headline, "en_to_pt")
            logging.info(dFinal[i]["manchete"])
            f = open("traduzidos/manchete" + str(i), "w")
            f.write(dFinal[i]["manchete"])
            f.close()
        else:
            f = open("traduzidos/manchete" + str(i), "r")
            dFinal[i]["manchete"] = f.readlines()
            f.close()

        logging.debug(dFinal[i]["manchete"])

        dFinal[i]["url"] = url
        dFinal[i]["autor"] = dArticle[i]["autor"]
        dFinal[i]["data"] = dArticle[i]["data"]

        maxBytes = 480
        tempText = ""
        countBytes = 0
        stringOverflowBytes = 0
        dFinal[i]["texto traduzido"] = ""
        dFinal[i]["texto original"] = dArticle[i]["texto"]
        dArticle[i]["texto"] = dArticle[i]["texto"].replace("...", ".")
        fileTextExists = path.exists("traduzidos/corpodotexto" + str(i))
        for word in dArticle[i]["texto"].split():
            if(fileTextExists == False):
                logging.debug("CUIDADO: Você está gastando a cota da API de tradução!")
                if(countBytes + returnBytes(word + " ") < maxBytes):
                    tempText += word + " "
                    countBytes = returnBytes(tempText)
                else:
                    #totalizou > de 500 bytes
                    stringOverflowBytes += 1

                    logging.debug(tempText)
                    positionLastPeriod = tempText.rindex(".") + 1
                    afterPeriodString = tempText[positionLastPeriod:]
                    tempText = tempText[:positionLastPeriod]
                    logging.debug(tempText)
                    logging.debug(returnBytes(tempText))
                    logging.debug(afterPeriodString)

                    f = open("traduzidos/corpodotextoingles" + str(i), "a")
                    f.write(tempText)
                    f.close()

                    logging.debug(tempText)
                    tempText = translateConsideringAPILimit(tempText, "en_to_pt")
                    logging.debug(tempText)
                    f = open("traduzidos/corpodotexto" + str(i), "a")
                    f.write(tempText)
                    f.close()
                    logging.info(tempText)

                    if(isinstance(tempText, list)):
                        tempText = tempText[0]

                    dFinal[i]["texto traduzido"] += tempText
                    logging.debug(dFinal[i]["texto traduzido"])

                    if(stringOverflowBytes == 2):
                        break
                    tempText = afterPeriodString + word + " "
                    countBytes = returnBytes(tempText)
            else:
                f = open("traduzidos/corpodotexto" + str(i), "r")
                dFinal[i]["texto traduzido"] = f.readlines()
                f.close()
        i += 1
        if(i == totalOfArticles):
            f = open("articles.pkl", "wb")
            pickle.dump(dFinal, f)
            f.close()
            break
    return dFinal

def getTranslatedData(dHeader, dArticle):
    if(os.path.isfile('articles.pkl')):
        logging.info('Carregando tradução de artigos do disco')
        try:
            f = open("articles.pkl", "rb")
        except IOError:
            logging.error("ERRO: Arquivo artickesl.pkl não encontrado")
            exit()
        dFinal = pickle.load(f)
        f.close()
        return dFinal
    else:
        logging.info('Gerando tradução de artigos do site')
        return constructDictionary(dHeader, dArticle)
