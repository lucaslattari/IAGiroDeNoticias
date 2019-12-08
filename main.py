import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import scrapping as scrap
import translateNews as trans
import speech
import textgeneration as tg
from pydub import AudioSegment

def generatePodcastOpeningMP3Files(file, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    listOfFiles = []
    f = open("abertura.txt", "r")
    talks = 0
    for line in f:
        if(line[0] == '1'):
            line = line[2:]
            logging.info('IAsmim está falando')
            mp3File = "opening" + str(talks) + ".mp3"
            listOfFiles.append(mp3File)
            print("IAsmim: " + line)
            speech.speechNews(line, mp3File, "iasmim")
        else:
            logging.info('GPT-2 está falando')
            line = line[2:]
            if GAMBIARRA_DO_PROBLEMA_DA_API == True:
                gpt2Talk = "And I am GPT 2, I am an artificial intelligence capable of making pertinent comments. For example, I think this podcast"
            else:
                pass
                #gpt2Talk = translateConsideringAPILimit(line, False)
                #gpt2Talk += tg.generateText(gpt2Talk)
            if GAMBIARRA_DO_PROBLEMA_DA_API == True:
                gpt2Talk = "E eu sou GPT 2, sou uma inteligência artificial capaz de fazer comentários pertinentes. Por exemplo, acho que este podcast é absolutamente fabuloso, mas não é tão bom quando o convidado é um velho branco que quer falar sobre por que odeia tudo que não é a Apple."
            else:
                pass
                #gpt2Talk = translateConsideringAPILimit(gpt2Tals)

            mp3File = "opening" + str(talks) + ".mp3"
            listOfFiles.append(mp3File)
            print("GPT-2: " + gpt2Talk)
            speech.speechNews(gpt2Talk, mp3File, "GPT2")
        mp3File = AudioSegment.from_mp3("opening"+str(talks)+".mp3")
        if talks == 0:
            finalmp3File = mp3File
        else:
            finalmp3File += mp3File
        talks += 1
    #for mp3File in listOfFiles:
    #    os.remove(mp3File)
    #finalmp3File.export("abertura.mp3", format="mp3")
    return listOfFiles

def generateHeadlines(dFinal):
    headlines = ""
    for i in range(5):
        if "manchete" in dFinal[i]:
            headlines += "\"" + dFinal[i]["manchete"] + "\". "
    mp3File = "headlines.mp3"
    print("IAsmim: " + headlines)
    speech.speechNews(headlines, mp3File, "iasmim")
    return mp3File

import codecs
def generateNewsByID(dFinal, idNews):
    talk = ""
    mp3File = "news" + str(idNews) + ".mp3"
    with codecs.open("noticia.txt", 'r', encoding='utf8') as fp:
        line = fp.readline()
        if '%texto traduzido%' in line:
            line = line.replace("%texto traduzido%", dFinal[idNews]["texto traduzido"])
        talk += line
        while line:
            line = fp.readline()
            if '%autor%' in line:
                line = line.replace("%autor%", dFinal[idNews]["autor"])
            if '%dia%' in line:
                line = line.replace("%dia%", str(dFinal[idNews]["data"]["dia"]))
            if '%mes%' in line:
                line = line.replace("%mes%", str(dFinal[idNews]["data"]["mes"]))
            if '%ano%' in line:
                line = line.replace("%ano%", str(dFinal[idNews]["data"]["ano"]))
            talk += line
    print(talk)
    speech.speechNews(talk, mp3File, "iasmim")
    return mp3File

def generateGPT2Comment(prefix, idNews, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    prefixToGPT2 = ""
    if(GAMBIARRA_DO_PROBLEMA_DA_API):
        prefixToGPT2 = "About \"Microsoft wants everyone to follow their lead with its new mobile design\" I have to say that:"
    else:
        prefixToGPT2 = translateConsideringAPILimit(headline, False)
    text = tg.generateText(prefixToGPT2)
    print(prefix)

def concatenateMP3s(mp3List):
    i = 0
    for mp3 in mp3List:
        if(i == 0):
            finalmp3 = AudioSegment.from_mp3(mp3)
        else:
            finalmp3 += AudioSegment.from_mp3(mp3)
        i += 1
    finalmp3.export("final.mp3", format="mp3")
    #for mp3 in mp3List:
    #    os.remove(mp3)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    dHeader, dArticle = scrap.scrapDataFromTheVerge()
    dFinal = trans.getTranslatedData(dHeader, dArticle)

    '''
    logging.info('Gerando abertura do podcast em MP3')
    mp3FilesList = generatePodcastOpeningMP3Files("abertura.txt")
    logging.info('Gerando anúncio das notícias em MP3')
    mp3FilesList.append(generateHeadlines(dFinal))
    '''
    logging.info('Gerando notícia 0 em MP3')
    #mp3FilesList.append(generateNewsByID(dFinal, 0))
    #generateNewsByID(dFinal, 0)
    generateGPT2Comment("Sobre \"" + dFinal[0]["manchete"] + "\" eu tenho a dizer que: ", 0)
    '''
    logging.info('Sintetizando programa final em MP3')
    concatenateMP3s(mp3FilesList)
    Na edição de hoje, falaremos das seguintes notícias: "
    for i in range(5):
        if "manchete" in dFinal[i]:
            opening += "\"" + dFinal[i]["manchete"] + "\". "
    print(opening)
    input()
    '''
    #opening = tg.generateText("")

    #tg.downloadGPT2Model()
    #tg.trainModel(dArticle)

    #tg.finetuneModel()
    #tg.textGeneration()

if __name__ == "__main__":
    main()
