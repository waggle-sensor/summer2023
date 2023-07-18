import os

for root, dirs, files in os.walk(".\images/patches/W083"):
    for file in files:   
        path = os.path.join(root, file)
        os.remove(path)