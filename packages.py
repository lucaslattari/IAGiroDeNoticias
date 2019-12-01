import subprocess
import sys

INSTALL_PACKAGES = False

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

if(INSTALL_PACKAGES):
    install("beautifulsoup4")
    install("html5lib")
    install("pickle-mixin")
