import logging
import speech
from os import path
import stringUtils as s
from pydub import *

def generatePodcastDialogMP3Files(dialogName):
    ff = open(dialogName, "r")

    listOfFiles = []
    talksIasmim = 0
    talksGPT2 = 0
    for line in ff:
        if(line[0] == '1'):
            mp3File = dialogName + str(talksIasmim) + "_iasmim.mp3"
            listOfFiles.append(mp3File)
            line = line[2:]
            logging.info("IAsmim: " + line)
            fSub = open("subtitles", "a")
            fSub.write("\nIAsmim: " + line + "\n")
            fSub.close()
            logging.info("Salvando arquivo " + mp3File)
            if path.exists(mp3File) == False:
                speech.speechNews(line, mp3File, "iasmim")
            talksIasmim += 1
        else:
            mp3File = dialogName + str(talksGPT2) + "_gpt2.mp3"
            listOfFiles.append(mp3File)
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
            logging.info("GPT-2: " + gpt2Talk)
            fSub = open("subtitles", "a")
            fSub.write("\nGPT-2: " + gpt2Talk + "\n")
            fSub.close()
            logging.info("Salvando arquivo " + mp3File)
            if path.exists(mp3File) == False:
                speech.speechNews(gpt2Talk, mp3File, "GPT2")
    ff.close()
    return listOfFiles

def generateHeadlines(dFinal):
    headlines = ""
    mp3File = "headlines_iasmim.mp3"

    for i in range(3):
        if "manchete" in dFinal[i]:
            if(isinstance(dFinal[i]["manchete"], list)):
                dFinal[i]["manchete"] = dFinal[i]["manchete"][0]
            if(i < 2):
                headlines += dFinal[i]["manchete"] + " , "
            else:
                headlines += dFinal[i]["manchete"]
    logging.info("IAsmim: " + headlines)
    fSub = open("subtitles", "a")
    fSub.write("\nIAsmim: " + headlines)
    fSub.write("\n")
    fSub.close()
    if path.exists(mp3File) == False:
        speech.speechNews(headlines, mp3File, "iasmim")

    return mp3File

import codecs
def generateNewsByID(dFinal, idNews):
    talk = ""
    mp3File = "news" + str(idNews) + "_iasmim.mp3"

    logging.debug(dFinal[idNews]["texto original"])
    with codecs.open("noticia", 'r', encoding='utf8') as fp:
        line = fp.readline()
        if '%texto traduzido%' in line:
            if(isinstance(dFinal[idNews]["texto traduzido"], list)):
                dFinal[idNews]["texto traduzido"] = dFinal[idNews]["texto traduzido"][0]
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
    if path.exists(mp3File) == False:
        speech.speechNews(talk, mp3File, "iasmim")
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
    if path.exists(mp3File) == False:
        speech.speechNews(text, mp3File, "GPT2")
    return mp3File

def concatenateMP3s(mp3List):
    if path.exists("final.mp3"):
        return
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
