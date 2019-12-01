import scrapping as scrap
import translateNews as trans
import speech
import gpt2

def main():
    return
    model = loadGPT2Model()
    a = generateText(model)
    print(a)
    '''
    dHeader, dArticle = scrap.scrapDataFromTheVerge()
    dFinal = trans.getTranslateData(dHeader, dArticle, True)
    speech.speechNews(dFinal)
    '''

if __name__ == "__main__":
    main()
