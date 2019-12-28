# coding: utf-8
import numpy as np
import time
import re
import os
import os.path
import logging
from pydub import AudioSegment
import moviepy.editor as mp
import cv2

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
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    return img

def make_frame_iasmim(t):
    return generateTextInFrame("IAsmim")

def make_frame_gpt2(t):
    return generateTextInFrame("GPT-2")

def make_frame_music(t):
    return generateTextInFrame("Music")

def generateVideoFile(mp3Filename, mp4Filename):
    if os.path.exists(mp4Filename) == True:
        return
    logging.info(mp4Filename)

    audioOfClip = mp.AudioFileClip(mp3Filename)
    if(mp3Filename == "intro_music.mp3"):
        from moviepy.audio.fx.volumex import volumex
        audioOfClip = audioOfClip.fx(volumex, 0.5)
    seconds = audioOfClip.duration
    logging.debug(seconds)

    whoIsTalking = mp3Filename.split("_")[1]

    if re.search("iasmim", whoIsTalking):
        logging.debug(whoIsTalking)
        clip = mp.VideoClip(make_frame_iasmim, duration = seconds)
    elif re.search("gpt2", whoIsTalking):
        logging.debug(whoIsTalking)
        clip = mp.VideoClip(make_frame_gpt2, duration = seconds)
    elif re.search("music", whoIsTalking):
        logging.debug(whoIsTalking)
        clip = mp.VideoClip(make_frame_music, duration = seconds)

    #clip = clip.set_audio(audioOfClip)
    clip.write_videofile(mp4Filename, fps = 20.0, verbose = False)

def concatenateVideos(videoFilenameList, finalVideoFilename):
    if os.path.exists("final.mp4") == True:
        return

    videoList = []
    for videoFilename in videoFilenameList:
        videoList.append(mp.VideoFileClip(videoFilename))

    finalVideo = mp.concatenate_videoclips(videoList)
    finalAudio = mp.AudioFileClip("final.mp3")
    finalVideo = finalVideo.set_audio(finalAudio)
    finalVideo.write_videofile("final.mp4", verbose = False)

    #for videoFilename in videoFilenameList:
    #    os.remove(videoFilename)

def synthetizeVideo(mp3FilesList, finalVideoFilename):
    videoFilenameList = []
    for mp3Filename in mp3FilesList:
        mp4Filename = mp3Filename.split('.')[0] + ".mp4"
        logging.debug(mp3Filename)
        logging.debug(mp4Filename)

        generateVideoFile(mp3Filename, mp4Filename)
        videoFilenameList.append(mp4Filename)
    logging.debug("Gerando final.mp4")
    concatenateVideos(videoFilenameList, finalVideoFilename)
