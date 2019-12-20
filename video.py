# coding: utf-8
import cv2
import numpy as np
import time
import re
import os
import os.path
import logging
from pydub import AudioSegment

def showImage(frame):
    cv2.imshow('imagem exibida', frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def generateTextInFrame(whichBot):
    font     = cv2.FONT_HERSHEY_SIMPLEX
    position = (0, 50)
    fontScale = 2
    lineType = 2

    logging.debug("Sintetizando frames de " + whichBot)
    if(whichBot == "IAsmim"):
        img = cv2.imread("iasmim.png")
        fontColor = (255, 0, 0)
    elif(whichBot == "GPT-2"):
        img = cv2.imread("gpt2.jpg")
        fontColor = (0, 0, 255)
    else:
        img = cv2.imread("music.jpg")
        fontColor = (0, 255, 0)

    img = cv2.resize(img, (1280, 720))
    cv2.putText(img, whichBot, position, font, fontScale, fontColor, lineType)

    return img

def generateVideoFile(mp3FilesList, finalVideoFilename):
    logging.debug(finalVideoFilename)
    if(os.path.exists(finalVideoFilename) == False):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(finalVideoFilename, fourcc, 20.0, (1280, 720))

        try:
            for mp3 in mp3FilesList:
                audio = AudioSegment.from_mp3(mp3)
                seconds = audio.duration_seconds
                logging.debug(seconds)

                import math
                frac, whole = math.modf(seconds)
                remaining = 1.0 - frac
                silence = AudioSegment.silent(duration=remaining)
                audio = audio + silence

                seconds = int(round(audio.duration_seconds))
                logging.debug(seconds)
                whoIsTalking = mp3.split("_")[1]
                if re.search("iasmim", whoIsTalking):
                    logging.debug(whoIsTalking)
                    frame = generateTextInFrame("IAsmim")
                elif re.search("gpt2", whoIsTalking):
                    logging.debug(whoIsTalking)
                    frame = generateTextInFrame("GPT-2")
                elif re.search("music", whoIsTalking):
                    logging.debug(whoIsTalking)
                    frame = generateTextInFrame("Musica")
                else:
                    logging.debug(whoIsTalking)
                    frame = generateTextInFrame("Unknown")

                totalFrames = 20 * seconds
                for i in range(0, totalFrames):
                    writer.write(frame)
        except OSError:
            print("Não foi possível abrir o arquivo mp3duration")
        writer.release()
    else:
        logging.info("Vídeo já existe em disco")

def addAudioInVideo(audioFile, videoFile):
    import moviepy.editor as mp
    video = mp.VideoFileClip(videoFile)
    video.write_videofile("final.mp4", audio=audioFile)

def synthetizeVideo(mp3FilesList, finalAudioFilename, finalVideoFilename):
    generateVideoFile(mp3FilesList, finalVideoFilename)
    addAudioInVideo(finalAudioFilename, finalVideoFilename)
