import packages
from translate import Translator
import sys
import time
import pickle
import logging

def countdown(seconds, printMessage = True):
    for i in range(seconds, 0, -1):
        if(printMessage):
            print("Aguarde " + str(i) + " segundos para tentar traduzir de novo...")
        time.sleep(1)

def translateConsideringAPILimit(text, en_to_pt = True):
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

def constructDictionary(dHeader, dArticle, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    i = 0
    dFinal = {}
    for headline, url in dHeader.items():
        print(headline)
        dFinal[i] = {}
        if(GAMBIARRA_DO_PROBLEMA_DA_API):
            if(i == 0):
                dFinal[i]["manchete"] = "Microsoft quer que todos sigam sua liderança com seu novo design móvel"
            elif(i == 1):
                dFinal[i]["manchete"] = "Spotify vence a Apple em seu próprio jogo com seu ano finalizado em recurso de revisão"
            elif(i == 2):
                dFinal[i]["manchete"] = "As queixas anteriores do MacBook Pro de 16 polegadas incluem 'estalo' do alto-falante e exibição de fantasmas"
            elif(i == 3):
                dFinal[i]["manchete"] = "O Galaxy S11 da Samsung supostamente possui uma câmera de 108 megapixels e uma teleobjetiva de 5x"
            elif(i == 4):
                dFinal[i]["manchete"] = "O Google Fiber não oferece mais seu plano mais barato para novos clientes"
        else:
            dFinal[i]["manchete"] = translateConsideringAPILimit(headline)

        dFinal[i]["url"] = url
        dFinal[i]["autor"] = dArticle[i]["autor"]
        dFinal[i]["data"] = dArticle[i]["data"]

        length = 420
        tempText = ""
        count = 0
        countEnd = 0
        dFinal[i]["texto traduzido"] = ""
        for word in dArticle[i]["texto"].split():
            if(count + len(word) < length):
                tempText += word + " "
                count += len(word + " ")
            else:
                if(GAMBIARRA_DO_PROBLEMA_DA_API):
                    dFinal[i]["texto traduzido"] = "O notável analista da Apple Ming Chi Kuo tem uma nova nota de pesquisa prevendo os próximos dois anos de iPhones da Apple, e há um novo detalhe: o iPhone da Apple em 2021 matará a porta Lightning, mas os fãs de USB C (como eu) não devem muito animado. De acordo com a nota de Kuo, a Apple não substituirá a porta proprietária por USB C; em vez disso, dependerá de uma experiência totalmente sem fio para carregar e"
                    dFinal[i]["texto traduzido"] += "sincronização, via 9to5Mac. A mudança seria grande para a Apple, que conta com a porta Lightning para todos os seus telefones desde que foi lançada no iPhone 5 em 2013. E enquanto os iPhones modernos são menos dependentes fisicamente sincronizando dados, ir para um modelo totalmente sem fio teria enormes ramificações em todo o setor de tecnologia, com tudo, desde cobrar empresas de cabo até fones de ouvido"
                    dFinal[i]["texto traduzido"] += "fabricantes sendo impactados. Obviamente, ainda estamos muito longe de 2021 - os iPhones 2020 da Apple ainda não estão aqui - mas Kuo tem uma boa reputação por prever os planos da Apple, o que significa que é perfeitamente possível que seja assim que o futuro dos iPhones será ."
                else:
                    countEnd += tempText.count(".")
                    dFinal[i]["texto traduzido"] += translateConsideringAPILimit(tempText)
                    if countEnd >= 5:
                        break
                tempText = word + " "
                count = len(word)

        i += 1
        if(i >= 5):
            f = open("articles.pkl", "wb")
            pickle.dump(dFinal, f)
            f.close()
            break
    return dFinal

def getTranslatedData(dHeader, dArticle, openFileInDir = True):
    if(openFileInDir):
        logging.info('Carregando tradução de artigos do disco')

        f = open("articles.pkl", "rb")
        dFinal = pickle.load(f)
        f.close()
        return dFinal
    else:
        logging.info('Gerando tradução de artigos do site')
        return constructDictionary(dHeader, dArticle)
