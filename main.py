# coding: utf-8
import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import scrapping as scrap
import translateNews as trans
import speech
import textgeneration as tg
from pydub import AudioSegment
import video
import youtube as yt
import time
import os.path
from os import path
import re
import stringUtils as s

def saveMP3Duration(mp3File):
    from mutagen.mp3 import MP3
    audio = MP3(mp3File)
    f = open("mp3duration", "a+")
    f.write(str(audio.info.length) + " : " + mp3File + "\n")
    f.close()

def generatePodcastDialogMP3Files(dialogName):
    listOfFiles = []
    ff = open(dialogName, "r")
    talks = 0
    talksGPT2 = 0
    for line in ff:
        if(line[0] == '1'):
            mp3File = dialogName + str(talks) + "_iasmim.mp3"
            line = line[2:]
            listOfFiles.append(mp3File)
            logging.info("IAsmim: " + line)
            fSub = open("subtitles", "a")
            fSub.write("\nIAsmim: " + line + "\n")
            fSub.close()
            logging.info("Salvando arquivo " + mp3File)
            speech.speechNews(line, mp3File, "iasmim")
            saveMP3Duration(mp3File)
        else:
            mp3File = dialogName + str(talks) + "_gpt2.mp3"
            line = line[2:]
            if "%comentariogpt2" in line:
                line = line.replace("%comentariogpt2%", "")
                if path.exists("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "ingles") == False:
                    gpt2Talk = trans.translateConsideringAPILimit(line, "pt_to_en")
                    logging.info("Tradução da GPT-2: " + gpt2Talk)
                    gpt2Talk += tg.generateText(gpt2Talk)
                    f = open("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "ingles", "a")
                    f.write(gpt2Talk)
                    f.close()
                else:
                    f = open("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "ingles", "r")
                    gpt2Talk = f.readlines()
                    if(isinstance(gpt2Talk, list)):
                        gpt2Talk = gpt2Talk[0]
                    f.close()

                if path.exists("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "portugues") == False:
                    logging.info(gpt2Talk)
                    gpt2Talk = trans.translateConsideringAPILimit(gpt2Talk, "en_to_pt")
                    f = open("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "portugues", "a")
                    f.write(gpt2Talk)
                    f.close()
                else:
                    f = open("traduzidos/" + dialogName + "_gpt2_" + str(talksGPT2) + "portugues", "r")
                    gpt2Talk = f.readlines()
                    if(isinstance(gpt2Talk, list)):
                        gpt2Talk = gpt2Talk[0]
                    f.close()
                talksGPT2 += 1
            else:
                gpt2Talk = line[2:]
            listOfFiles.append(mp3File)
            logging.info("GPT-2: " + gpt2Talk)
            fSub = open("subtitles", "a")
            fSub.write("\nGPT-2: " + gpt2Talk + "\n")
            fSub.close()
            logging.info("Salvando arquivo " + mp3File)
            speech.speechNews(gpt2Talk, mp3File, "GPT2")
            saveMP3Duration(mp3File)
        AudioSegment.from_mp3(mp3File)
        talks += 1
    ff.close()
    return listOfFiles

def generateHeadlines(dFinal):
    headlines = ""
    for i in range(3):
        if "manchete" in dFinal[i]:
            if(i < 2):
                headlines += dFinal[i]["manchete"] + " , "
            else:
                headlines += dFinal[i]["manchete"]
    mp3File = "headlines_iasmim.mp3"
    logging.info("IAsmim: " + headlines)
    fSub = open("subtitles", "a")
    fSub.write("\nIAsmim: " + headlines)
    fSub.write("\n")
    fSub.close()
    speech.speechNews(headlines, mp3File, "iasmim")
    logging.info("Salvando arquivo " + mp3File)
    saveMP3Duration(mp3File)
    return mp3File

import codecs
def generateNewsByID(dFinal, idNews):
    talk = ""
    mp3File = "news" + str(idNews) + "_iasmim.mp3"
    logging.debug(dFinal[idNews]["texto original"])
    with codecs.open("noticia", 'r', encoding='utf8') as fp:
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
    logging.info("IAsmim: " + talk)
    fSub = open("subtitles", "a")
    fSub.write("\nIAsmim: " + talk)
    fSub.write("\n")
    fSub.close()
    speech.speechNews(talk, mp3File, "iasmim")
    saveMP3Duration(mp3File)
    return mp3File

def generateGPT2Comment(prefix, idNews):
    prefixToGPT2 = ""
    mp3File = "comment" + str(idNews) + "_gpt2.mp3"

    prefix = s.cleanSentence(prefix)
    if path.exists("traduzidos/comentarios_gpt2_" + str(idNews) + "ingles") == False:
        prefixToGPT2 = trans.translateConsideringAPILimit(prefix, "pt_to_en")
        logging.info(prefixToGPT2)

        text = tg.generateText(prefixToGPT2)
        logging.info(text)

        f = open("traduzidos/comentarios_gpt2_" + str(idNews) + "ingles", "a")
        f.write(text)
        f.close()
    else:
        f = open("traduzidos/comentarios_gpt2_" + str(idNews) + "ingles", "r")
        text = f.readlines()
        if(isinstance(text, list)):
            text = text[0]
        f.close()

    if path.exists("traduzidos/comentarios_gpt2_" + str(idNews) + "portugues") == False:
        text = trans.translateConsideringAPILimit(text, "en_to_pt")
        logging.info(text)

        f = open("traduzidos/comentarios_gpt2_" + str(idNews) + "portugues", "a")
        f.write(text)
        f.close()
    else:
        f = open("traduzidos/comentarios_gpt2_" + str(idNews) + "portugues", "r")
        text = f.readlines()
        if(isinstance(text, list)):
            text = text[0]
        f.close()

    logging.info("GPT-2: " + text)
    fSub = open("subtitles", "a")
    fSub.write("\nGPT-2: " + text)
    fSub.write("\n")
    fSub.close()
    speech.speechNews(text, mp3File, "GPT2")
    saveMP3Duration(mp3File)
    return mp3File

def concatenateMP3s(mp3List):
    i = 0
    for mp3 in mp3List:
        if(i == 0):
            finalmp3 = AudioSegment.from_mp3(mp3)
        else:
            if(mp3 != 'intro_music.mp3'):
                finalmp3 += AudioSegment.from_mp3(mp3)
            else:
                finalmp3 += AudioSegment.from_mp3(mp3) - 3
        i += 1
    finalmp3.export("final.mp3", format="mp3")
    #for mp3 in mp3List:
    #    os.remove(mp3)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    logging.info("Extraindo dados de sites")
    dHeader, dArticle = scrap.scrapDataFromTheVerge()

    logging.info("Traduzindo textos")
    dFinal = trans.getTranslatedData(dHeader, dArticle)

    fSub = open("subtitles", "w").close()
    open("mp3duration", 'w').close()
    logging.info('Gerando abertura do podcast em MP3')
    mp3FilesList = generatePodcastDialogMP3Files("abertura")

    logging.info('Gerando anúncio das notícias em MP3')
    mp3FilesList.append(generateHeadlines(dFinal))

    logging.info('Adicionando música de abertura')
    fSub = open("subtitles", "a")
    fSub.write("\n-Música de Abertura-\n")
    fSub.write("\n")
    fSub.close()
    mp3FilesList.append("intro_music.mp3")
    saveMP3Duration("intro_music.mp3")

    for i in range(0, 3):
        logging.info('Gerando notícia ' + str(i) + ' em MP3')
        mp3File = generateNewsByID(dFinal, i)
        mp3FilesList.append(mp3File)

        mp3File = generateGPT2Comment("Sobre " + dFinal[i]["manchete"] + " eu tenho a dizer que: ", i)
        mp3FilesList.append(mp3File)

    logging.info('Gerando encerramento do podcast em MP3')
    mp3Files = generatePodcastDialogMP3Files("encerramento")
    mp3FilesList = mp3FilesList + mp3Files

    logging.info('Adicionando música de encerramento')
    fSub = open("subtitles", "a")
    fSub.write("\n-Música de Encerramento-")
    fSub.write("\n")
    fSub.close()
    mp3FilesList.append("ending_music.mp3")
    saveMP3Duration("ending_music.mp3")
    logging.info('Sintetizando programa final em MP3')
    concatenateMP3s(mp3FilesList)

    logging.info('Sintetizando vídeo em formato AVI')
    video.synthetizeVideo("final.mp3", "final.avi")

    f = open("descricao", "w")
    f.write("Link da primeira notícia: " + dFinal[0]["url"])
    f.write("\nLink da segunda notícia: " + dFinal[1]["url"])
    f.write("\nLink da terceira notícia: " + dFinal[2]["url"])
    f.close()

    yt.uploadYoutubeVideo("final.mp4")

    os.remove("generated.txt")
    os.remove("descricao")
    os.remove("encerramento")
    os.remove("mp3duration")
    os.remove("gpt2.vbs")
    os.remove("final.mp4")
    os.remove("final.avi")
    os.remove("temp.wav")
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                if((filename != 'intro_music.mp3') and (filename != 'ending_music.mp3')):
                    os.remove(filename)
            elif os.path.splitext(filename)[1] == ".pkl":
                os.remove(filename)

    #opening = tg.generateText("")

    #tg.downloadGPT2Model()
    #tg.trainModel(dArticle)

    #tg.finetuneModel()
    #tg.textGeneration()

if __name__ == "__main__":
    main()
