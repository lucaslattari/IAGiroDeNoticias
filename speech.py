from gtts import gTTS

def speechNews(dictionary):
    for eachItem in dictionary.items():
        for eachItemArticle in eachItem:
            if(type(eachItemArticle) == int):
                continue
            else:
                print(eachItemArticle["manchete"])
                input()
    #tts = gTTS(text='Oi pessoal!', lang='pt-br')
    #tts.save("ola.mp3")
