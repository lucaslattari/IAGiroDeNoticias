# coding: utf-8
from gtts import gTTS
from google.cloud import texttospeech
import os
import pydub
from pydub import AudioSegment
import librosa
import stringUtils as s

def changePitch(filename, steps):
    sound = AudioSegment.from_mp3(filename)
    sound.export("temp.wav", format="wav")

    y, sr = librosa.load("temp.wav", sr=16000) # y is a numpy array of the wav file, sr = sample rate
    y_shifted = librosa.effects.pitch_shift(y, sr, n_steps=steps)
    librosa.output.write_wav('temp.wav', y_shifted, sr)

    sound = AudioSegment.from_file("temp.wav")
    sound.export(filename, format="mp3")
    os.remove("temp.wav")

def saveMP3OfTextGoogle(speechText, mp3File):
    '''
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.types.SynthesisInput(text=speechText)
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='pt-br',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    print("ok")
    input()
    '''
    tts = gTTS(text=speechText, lang='pt-br', slow=False)
    tts.save(mp3File)

def saveMP3OfTextMicrosoft(speechText, mp3File):
    f = open("gpt2.vbs","w+")
    speechText = s.cleanSentence(speechText)
    speechText = speechText.replace("\"", "")
    speechText = speechText.replace("\'", "")
    f.writelines(["Const SAFT48kHz16BitStereo = 39\n",
        "Const SSFMCreateForWrite = 3\n",
        "Dim oFileStream, oVoice\n",
        "Set oFileStream = CreateObject(\"SAPI.SpFileStream\")\n",
        "oFileStream.Format.Type = SAFT48kHz16BitStereo\n",
        "oFileStream.Open \"" + os.getcwd() + "\\temp.wav\", SSFMCreateForWrite\n",
        "Set oVoice = CreateObject(\"SAPI.SpVoice\")\n",
        "Set oVoice.AudioOutputStream = oFileStream\n",
        "oVoice.Speak \"" + speechText + "\"\n",
        "oFileStream.Close"])
    f.close()

    os.system("gpt2.vbs")

    sound = AudioSegment.from_file("temp.wav")
    sound.export(mp3File, format="mp3")
    #os.remove("temp.wav")
    #os.remove("gpt2.vbs")

def speechNews(speech, filename, whoIsTalking):
    speech += "......"
    if whoIsTalking == "iasmim":
        saveMP3OfTextGoogle(speech, filename)
        #changePitch(filename, 2)
    else:
        saveMP3OfTextMicrosoft(speech, filename)
