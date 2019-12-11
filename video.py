import cv2
import numpy as np

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

def synthetizeVideo(finalAudio):
    frameIAsmim = generateTextInFrame("IAsmim")
    frameGPT2 = generateTextInFrame("GPT-2")
    frameMusica = generateTextInFrame("Musica")

    while(True):
        if writer is None:
            pass
