from gtts import gTTS
import os

def saveMP3OfTextGoogle(speechText, mp3File, language = 'pt-br'):
    tts = gTTS(text=speechText, lang=language, slow=False)
    tts.save(mp3File)

def speechNews(dictionary):
    item = 0
    for eachItem in dictionary.items():
        for eachItemArticle in eachItem:
            if(type(eachItemArticle) == int):
                continue
            else:
                saveMP3OfTextGoogle(eachItemArticle["manchete"], "headline_" + str(item) + "br.mp3")
                saveMP3OfTextGoogle(eachItemArticle["manchete"], "headline_" + str(item) + "pt.mp3", 'pt-pt')
        item+=1
