# coding: utf-8
import cv2
import numpy as np
import time
import re
import os
import os.path
import logging

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

    img = cv2.resize(img, (640, 480))
    cv2.putText(img, whichBot, position, font, fontScale, fontColor, lineType)

    return img

def generateVideoFile(finalVideoFilename):
    logging.debug(finalVideoFilename)
    if(os.path.exists(finalVideoFilename) == False):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(finalVideoFilename, fourcc, 20.0, (640, 480))

        try:
            f = open("mp3duration", "r")
            for line in f:
                line = line.replace("\n", "")
                seconds, whoIsTalking = line.split(" : ")
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

                durationofMP3 = float(seconds)
                frames = 0

                import math
                while(int(20.0 * (durationofMP3 + 1)) > frames):
                    writer.write(frame)
                    frames += 1
            f.close()
        except OSError:
            print("Não foi possível abrir o arquivo mp3duration")
        writer.release()
    else:
        logging.info("Vídeo já existe em disco")

def addAudioInVideo(audioFile, videoFile):
    import moviepy.editor as mp
    video = mp.VideoFileClip(videoFile)
    video.write_videofile("final.mp4", audio=audioFile)

def synthetizeVideo(finalAudioFilename, finalVideoFilename):
    generateVideoFile(finalVideoFilename)
    addAudioInVideo(finalAudioFilename, finalVideoFilename)
