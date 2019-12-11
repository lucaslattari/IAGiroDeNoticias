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

def saveMP3Duration(mp3File):
    from mutagen.mp3 import MP3
    audio = MP3(mp3File)
    f = open("mp3duration.txt", "a+")
    f.write(str(audio.info.length) + " : " + mp3File + "\n")
    f.close()

def generatePodcastEndingMP3Files(file, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    listOfFiles = []
    f = open(file, "r")
    talks = 0
    for line in f:
        mp3File = "ending" + str(talks) + ".mp3"
        if(line[0] == '1'):
            line = line[2:]
            listOfFiles.append(mp3File)
            logging.info("IAsmim: " + line)
            fSub.write("IAsmim: " + line)
            fSub.write("\n")
            speech.speechNews(line, mp3File, "iasmim")
            saveMP3Duration(mp3File)
        else:
            line = line[2:]
            if "%comentariogpt2" in line:
                if GAMBIARRA_DO_PROBLEMA_DA_API == True:
                    if talks == 1:
                        gpt2Talk = "The joke of the day is"
                    elif talks == 3:
                        gpt2Talk = "The tip of the day is the book"
                else:
                    pass
                    gpt2Talk = translateConsideringAPILimit(line, False)
                    gpt2Talk += tg.generateText(gpt2Talk)
                if GAMBIARRA_DO_PROBLEMA_DA_API == True:
                    if talks == 1:
                        gpt2Talk = "A piada do dia é que o \"mundo real\" se tornou mais \"baseado na realidade\" nas últimas décadas e isso não é uma coisa ruim, mas acho que devemos ter isso em mente. A realidade é que a maioria do que consideramos \"real\" não é de fato \"realidade\"."
                    elif talks == 3:
                        gpt2Talk = "A dica do dia é o livro de Jó, que, se você é cristão, impedirá que você tenha mais alguma esperança em sua vida. Para aqueles que não são cristãos, gostaria de deixar uma coisa clara: é um ótimo livro. Não é um livro ruim, lembre-se (embora eu não o tenha lido), mas um ótimo livro."
                else:
                    pass
                    #gpt2Talk = translateConsideringAPILimit(gpt2Talks)
            else:
                gpt2Talk = line[2:]
            listOfFiles.append(mp3File)
            logging.info("GPT-2: " + gpt2Talk)
            fSub.write("GPT-2: " + gpt2Talk)
            fSub.write("\n")
            speech.speechNews(gpt2Talk, mp3File, "GPT2")
            saveMP3Duration(mp3File)
        talks += 1
        AudioSegment.from_mp3(mp3File)
    return listOfFiles

def generatePodcastOpeningMP3Files(file, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    listOfFiles = []
    f = open(file, "r")
    talks = 0
    for line in f:
        mp3File = "opening" + str(talks) + ".mp3"
        if(line[0] == '1'):
            line = line[2:]
            listOfFiles.append(mp3File)
            logging.info("IAsmim: " + line)
            fSub.write("IAsmim: " + line)
            fSub.write("\n")
            speech.speechNews(line, mp3File, "iasmim")
            saveMP3Duration(mp3File)
        else:
            line = line[2:]
            if "%comentariogpt2" in line:
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
            else:
                gpt2Talk = line[2:]
            listOfFiles.append(mp3File)
            logging.info("GPT-2: " + gpt2Talk)
            fSub.write("GPT-2: " + gpt2Talk)
            fSub.write("\n")
            speech.speechNews(gpt2Talk, mp3File, "GPT2")
            saveMP3Duration(mp3File)
        AudioSegment.from_mp3(mp3File)
        talks += 1
    return listOfFiles

def generateHeadlines(dFinal):
    headlines = ""
    for i in range(3):
        if "manchete" in dFinal[i]:
            headlines += "\"" + dFinal[i]["manchete"] + "\". "
    mp3File = "headlines.mp3"
    logging.info("IAsmim: " + headlines)
    fSub.write("IAsmim: " + headlines)
    fSub.write("\n")
    speech.speechNews(headlines, mp3File, "iasmim")
    saveMP3Duration(mp3File)
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
    logging.info("IAsmim: " + talk)
    fSub.write("IAsmim: " + talk)
    fSub.write("\n")
    speech.speechNews(talk, mp3File, "iasmim")
    saveMP3Duration(mp3File)
    return mp3File

def generateGPT2Comment(prefix, idNews, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    prefixToGPT2 = ""
    mp3File = "comment" + str(idNews) + ".mp3"
    if(GAMBIARRA_DO_PROBLEMA_DA_API):
        prefixToGPT2 = "About \"Previous complaints of the 16-inch MacBook Pro include speaker 'crackling' and ghost display\" I have to say that:"
        if idNews == 0:
            text = "acredito muito na idéia de uma boa experiência do usuário e não importa se a empresa é Microsoft, Apple, Google ou algum outro jogador importante."
        elif idNews == 1:
            text = "Eu não tenho ideia do que isso significa. Estamos em uma guerra entre Apple e Spotify? Parece que o recurso de revisão da Apple agora é mais proeminente que o tocador de música do Spotify."
        else:
            text = "Eu não entendo. A Apple nunca forneceu um único exemplo de ruído de áudio ou fantasma (ou seja, uma imagem não visível a olho nu)."
    else:
        prefix = prefix.replace("\"", "")
        prefixToGPT2 = translateConsideringAPILimit(prefix, False)
        text = tg.generateText(prefixToGPT2)
        text = translateConsideringAPILimit(text)
    logging.info("GPT-2: " + text)
    fSub.write("GPT-2: " + text)
    fSub.write("\n")
    speech.speechNews(text, mp3File, "GPT2")
    saveMP3Duration(mp3File)
    return mp3File

def concatenateMP3s(mp3List):
    i = 0
    for mp3 in mp3List:
        if(i == 0):
            finalmp3 = AudioSegment.from_mp3(mp3)
        else:
            if(mp3 != 'intro.mp3'):
                finalmp3 += AudioSegment.from_mp3(mp3)
            else:
                finalmp3 += AudioSegment.from_mp3(mp3) - 3
        i += 1
    finalmp3.export("final.mp3", format="mp3")
    #for mp3 in mp3List:
    #    os.remove(mp3)

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    dHeader, dArticle = scrap.scrapDataFromTheVerge()
    dFinal = trans.getTranslatedData(dHeader, dArticle)
    logging.info('Gerando abertura do podcast em MP3')
    mp3FilesList = generatePodcastOpeningMP3Files("abertura.txt")
    logging.info('Gerando anúncio das notícias em MP3')
    mp3FilesList.append(generateHeadlines(dFinal))
    logging.info('Adicionando música de abertura')
    fSub.write("Música de Abertura!")
    fSub.write("\n")
    mp3FilesList.append("intro.mp3")

    for i in range(0, 3):
        logging.info('Gerando notícia ' + str(i) + ' em MP3')
        mp3File = generateNewsByID(dFinal, i)
        mp3FilesList.append(mp3File)

        mp3File = generateGPT2Comment("Sobre \"" + dFinal[i]["manchete"] + "\" eu tenho a dizer que: ", i)
        mp3FilesList.append(mp3File)
    logging.info('Gerando encerramento do podcast em MP3')
    mp3Files = generatePodcastEndingMP3Files("encerramento.txt")
    mp3FilesList = mp3FilesList + mp3Files
    logging.info('Adicionando música de encerramento')
    fSub.write("Música de Encerramento!")
    fSub.write("\n")
    mp3FilesList.append("ending.mp3")
    logging.info('Sintetizando programa final em MP3')
    concatenateMP3s(mp3FilesList)

    video.synthetizeVideo("final.mp3")

    #opening = tg.generateText("")

    #tg.downloadGPT2Model()
    #tg.trainModel(dArticle)

    #tg.finetuneModel()
    #tg.textGeneration()

if __name__ == "__main__":
    open("mp3duration.txt", 'w').close()

    fSub = open("subtitles.txt", "w")
    main()
    fSub.close()
