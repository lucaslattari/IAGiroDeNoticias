import subprocess
import sys

INSTALL_PACKAGES = False

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

def upgrade(package):
    subprocess.call(['pip', "install", "--upgrade", package])

def installModule(package):
    install(package)
    upgrade(package)

def installTorch():
    subprocess.call(['pip3', "install", "torch==1.3.1", "torchvision===0.4.2", "-f", "https://download.pytorch.org/whl/torch_stable.html"])

if(INSTALL_PACKAGES):
    installModule("requests")
    installModule("beautifulsoup4")
    installModule("html5lib")
    installModule("pickle-mixin")
    installModule("translate")
    installModule("gTTS")
    installModule("tensorflow==1.15")
    installModule("tensorflow-gpu==1.15")
    installModule("gpt-2-simple")
    installModule("transformers")
    installModule("pypiwin32")
    installModule("pydub")
    installModule("scikit-learn")
    installTorch()
    install("librosa")
    install("opencv-python")
    install("mutagen")
