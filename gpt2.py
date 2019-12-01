from gpt2_client import GPT2Client

def loadGPT2Model(modelSize = "xl"):
    if(modelSize.lower() == "simple"):
        gpt2 = GPT2Client('117M')
    elif(modelSize.lower() == "medium"):
        gpt2 = GPT2Client('345M')
    elif(modelSize.lower() == "large"):
        gpt2 = GPT2Client('774M')
    else:
        gpt2 = GPT2Client('1558M')
    gpt2.load_model(force_download=False)

    return gpt2

def generateText(model):
    model.generate_batch_from_prompts("teste")    
