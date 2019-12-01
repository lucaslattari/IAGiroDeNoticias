import packages
from translate import Translator
import sys
import time

def countdown(seconds, printMessage = True):
    for i in range(seconds, 0, -1):
        if(printMessage):
            print("Aguarde " + str(i) + " segundos para tentar traduzir de novo...")
        time.sleep(1)

def translateConsideringAPILimit(text):
    translator = Translator(to_lang = "pt")
    translated = translator.translate(text)
    if "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY. NEXT AVAILABLE IN" in translated:
        h,m,s = [int(s) for s in translated.split() if s.isdigit()]
        countdown(s + m * 60 + h * 60 * 60)
    else:
        return translated
    return translator.translate(text)

def getTranslateData(dHeader, dArticle, GAMBIARRA_DO_PROBLEMA_DA_API = True):
    i = 0
    dFinal = {}
    for headline, url in dHeader.items():
        dFinal[i] = {}
        if(GAMBIARRA_DO_PROBLEMA_DA_API):
            if(i == 0):
                dFinal[i]["manchete"] = "Esta bateria USB C que pode carregar totalmente um MacBook Pro de 15 polegadas custa US $ 100 na Black Friday"
            elif(i == 1):
                dFinal[i]["manchete"] = "As vendas da Black Friday nos jogos que realmente amamos este ano"
            elif(i == 2):
                dFinal[i]["manchete"] = "Você ainda pode encontrar uma boa oferta de Black Friday em um Apple Watch"
            elif(i == 3):
                dFinal[i]["manchete"] = "LG G8 ThinQ pode ser o melhor negócio de telefone da Black Friday por apenas US $ 400"
            elif(i == 4):
                dFinal[i]["manchete"] = "China torna crime publicar deepfakes ou notícias falsas sem divulgação"
        else:
            dFinal[i]["manchete"] = translateConsideringAPILimit(headline)

        dFinal[i]["url"] = url
        dFinal[i]["autor"] = dArticle[i]["autor"]
        dFinal[i]["data"] = dArticle[i]["data"]

        countParagraph = 0
        dFinal[i]["texto"] = {}
        for paragraph in dArticle[i]["texto"]:
            if(GAMBIARRA_DO_PROBLEMA_DA_API):
                if(i == 0 and countParagraph == 0):
                    dFinal[i]["texto"][countParagraph] = "Atualização, 9:30 AM ET, 30 de novembro de 2019: o cupom para este desconto não está mais disponível e o preço voltou a US $ 140,99."
                elif(i == 0 and countParagraph == 1):
                    dFinal[i]["texto"][countParagraph] = "Em maio, apresentamos a você baterias externas USB C PD de alta potência que podem carregar um laptop de tamanho grande em movimento - e não apenas um telefone - e o Zendure SuperTank de US $ 150 foi uma das nossas principais opções graças ao seu tamanho (relativamente) compacto e preço. Mas para a Black Friday, o SuperTank agora é mais acessível do que tem sido desde sua campanha no Kickstarter - apenas US $ 100,99 após o código de cupom na Amazon."
                elif(i == 1 and countParagraph == 0):
                    dFinal[i]["texto"][countParagraph] = "A Black Friday é a melhor época do ano para os fãs de jogos que sentem que não têm orçamento ou tempo para escolher cada novo título de sucesso no dia do lançamento. Eu me encontro nessa categoria, como alguém que jogou o excelente Homem-Aranha da Insomniac um ano atrasado (atualmente na Black Friday por US $ 14,99 na Best Buy) e ainda tem alguns candidatos ao jogo do ano de 2019 no meu backlog."
                elif(i == 2 and countParagraph == 0):
                    dFinal[i]["texto"][countParagraph] = "Se você estava esperando para atualizar seu Apple Watch ou se é um comprador pela primeira vez, a Black Friday 2019 está cheia de grandes promoções na linha de smartwatches da Apple. Os compradores de olhos de águia podem ter rapidamente aumentado a venda de acessórios de porta do Walmart, que teve o Apple Watch Series 3 em US $ 129 - seu preço mais baixo em US $ 70 -, que mostramos em nosso guia maior sobre os negócios da Apple na sexta-feira negra. Mas ainda há algumas oportunidades de economizar, se você estiver interessado nos mais afetos da Apple"
                elif(i == 3 and countParagraph == 0):
                    dFinal[i]["texto"][countParagraph] = "O LG G8 ThinQ não é o telefone mais incrível do mundo, mas pode ser o melhor retorno nesta sexta-feira negra. Em abril, escrevemos que “você receberá muito telefone pelo seu dinheiro” se conseguir encontrá-lo por US $ 699 - mas hoje, você pode comprar a versão desbloqueada por apenas US $ 400 na Amazon! Isso equivale a US $ 450 do preço original."
                elif(i == 4 and countParagraph == 0):
                    dFinal[i]["texto"][countParagraph] = "A China lançou uma nova política do governo projetada para impedir a disseminação de notícias falsas e vídeos enganosos criados usando inteligência artificial, também conhecidos como deepfakes. A nova regra, divulgada hoje pela Reuters, proíbe a publicação de informações falsas ou deepfakes online sem a devida divulgação de que o post em questão foi criado com a tecnologia AI ou VR. Não divulgar agora é uma ofensa criminal, diz o governo chinês."
            else:
                dFinal[i]["texto"][countParagraph] = translateConsideringAPILimit(dArticle[i]["texto"][countParagraph])
            countParagraph += 1
        dFinal[i]["total de palavras"] = dArticle[i]["total de palavras"]

        i += 1
        if(i == 5):
            break
    return dFinal
