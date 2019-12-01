import subprocess
import sys

INSTALL_PACKAGES = True

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def upgrade(package):
    subprocess.call(['pip', "install", "--upgrade", package])

def installModule(package):
    install(package)
    upgrade(package)

if(INSTALL_PACKAGES):
    '''
    installModule("beautifulsoup4")
    installModule("html5lib")
    installModule("pickle-mixin")
    installModule("translate")
    installModule("gTTS")
    '''
    #installModule("tensorflow")
    #installModule("gpt2-client")
    pass
