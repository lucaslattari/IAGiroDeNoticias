# coding: utf-8
import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import scrapping as scrap
import translateNews as trans
import textgeneration as tg
import podcast as pod
from pydub import AudioSegment
import video
import youtube as yt
import time
from os import path
import os
import re
import math

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    if os.path.isdir("traduzidos") == False:
        os.mkdir("traduzidos")

    logging.info("Extraindo dados de sites")
    dHeader, dArticle = scrap.scrapDataFromTheVerge()

    logging.info("Traduzindo textos")
    dFinal = trans.getTranslatedData(dHeader, dArticle)

    fSub = open("subtitles", "w").close()
    open("mp3files", 'w').close()
    logging.info('Gerando abertura do podcast em MP3')
    mp3FilesList = pod.generatePodcastDialogMP3Files("abertura")

    logging.info('Gerando anúncio das notícias em MP3')
    mp3FilesList.append(pod.generateHeadlines(dFinal))

    logging.info('Adicionando música de abertura')
    fSub = open("subtitles", "a")
    fSub.write("\n-Música de Abertura-\n")
    fSub.write("\n")
    fSub.close()
    mp3FilesList.append("intro_music.mp3")

    for i in range(0, 3):
        logging.info('Gerando notícia ' + str(i) + ' em MP3')
        mp3File = pod.generateNewsByID(dFinal, i)
        mp3FilesList.append(mp3File)

        mp3File = pod.generateGPT2Comment("Sobre " + dFinal[i]["manchete"] + " eu tenho a dizer que: ", i)
        mp3FilesList.append(mp3File)

    logging.info('Gerando encerramento do podcast em MP3')
    mp3Files = pod.generatePodcastDialogMP3Files("encerramento")
    mp3FilesList = mp3FilesList + mp3Files

    logging.info('Adicionando música de encerramento')
    fSub = open("subtitles", "a")
    fSub.write("\n-Música de Encerramento-")
    fSub.write("\n")
    fSub.close()
    mp3FilesList.append("ending_music.mp3")

    logging.info('Sintetizando programa final em MP3')
    pod.concatenateMP3s(mp3FilesList)

    logging.info('Sintetizando vídeo em formato AVI')
    video.synthetizeVideo(mp3FilesList, "final.avi")

    f = open("descricao", "w")
    f.write("Link da primeira notícia: " + dFinal[0]["url"])
    f.write("\nLink da segunda notícia: " + dFinal[1]["url"])
    f.write("\nLink da terceira notícia: " + dFinal[2]["url"])
    f.close()

    yt.uploadYoutubeVideo("final.mp4")

    os.remove("generated.txt")
    os.remove("descricao")
    os.remove("mp3files")
    os.remove("gpt2.vbs")
    os.remove("final.mp4")
    os.remove("final.avi")
    os.remove("temp.wav")
    for _, _, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                if((filename != 'intro_music.mp3') and (filename != 'ending_music.mp3')):
                    os.remove(filename)
            if os.path.splitext(filename)[1] == ".mp4":
                os.remove(filename)
            if os.path.splitext(filename)[1] == ".pkl":
                os.remove(filename)

    #opening = tg.generateText("")

    #tg.downloadGPT2Model()
    #tg.trainModel(dArticle)

    #tg.finetuneModel()
    #tg.textGeneration()

if __name__ == "__main__":
    main()
