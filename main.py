import os
import logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"
logging.getLogger("tensorflow").setLevel(logging.ERROR)

import scrapping as scrap
import translateNews as trans
import speech
import textgeneration as tg

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    dHeader, dArticle = scrap.scrapDataFromTheVerge()
    dFinal = trans.getTranslatedData(dHeader, dArticle)

    #tg.downloadGPT2Model()
    #tg.trainModel(dArticle)

    #tg.finetuneModel()
    #tg.textGeneration()
    '''
    for i in range(0, 15):
        f = open("C:\\Users\\Pichau\\github\\IAGiroDeNoticias\\generated.txt", "r")
        text = ""
        for x in f:
            text += x
        f.close()
        print(text)

        tg.generateTextWithTransformers(text, 10, 20)
    '''
    #speech.speechNews(dFinal)

    pass

if __name__ == "__main__":
    main()
