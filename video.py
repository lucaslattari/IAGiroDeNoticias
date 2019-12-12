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
    img = np.full((480, 640, 3), 0, np.uint8)

    font     = cv2.FONT_HERSHEY_SIMPLEX
    position = (100, 260)
    fontScale = 4
    lineType = 2

    if(whichBot == "IAsmim"):
        fontColor = (255, 0, 0)
    elif(whichBot == "GPT-2"):
        fontColor = (0, 0, 255)
    else:
        fontColor = (0, 255, 0)

    cv2.putText(img, whichBot, position, font, fontScale, fontColor, lineType)

    return img

def generateVideoFile(finalVideoFilename):
    if(os.path.exists(finalVideoFilename)):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter(finalVideoFilename, fourcc, 20.0, (640, 480))

        try:
            f = open("mp3duration", "r")
            for line in f:
                line = line.replace("\n", "")
                seconds, whoIsTalking = line.split(" : ")
                if re.search("iasmim", whoIsTalking):
                    frame = generateTextInFrame("IAsmim")
                elif re.search("gpt2", whoIsTalking):
                    frame = generateTextInFrame("GPT-2")
                elif re.search("music", whoIsTalking):
                    frame = generateTextInFrame("Musica")
                else:
                    frame = generateTextInFrame("Unknown")

                durationofMP3 = float(seconds)
                countTime = time.time()
                frames = 0
                logging.debug("%d %d", int(20.0 * durationofMP3), frames)
                while(int(20.0 * durationofMP3) > frames):
                    writer.write(frame)
                    frames += 1
            f.close()
        except OSError:
            print("Não foi possível abrir o arquivo mp3duration.txt")
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
