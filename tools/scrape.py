#scrape.py

import requests
from bs4 import BeautifulSoup
import os

#BirdVox-14SD
#url = 'https://zenodo.org/record/3667094#.YmgtEtrMK3A/'

#BirdVox-ANAFCC
url = "https://zenodo.org/record/3666782#.ZGt8qS-B3gs"
r = requests.get(url)

#print(r.content[:100])
soup = BeautifulSoup(r.content, 'html.parser')
files = soup.find_all('a', href=True)
names = []

links = soup.find_all('a')
i = 0


os.system("mkdir BirdVox-ANAFCC")
os.system("cd BirdVox-ANAFCC")

for link in links:
  if('.h5' in link.get('href', [])):
    i += 1
    print('Downloading file ', i)

    response = requests.get('http://zenodo.org' + link.get('href'))


    data = open(link.text.strip(), 'wb')
    data.write(response.content)
    data.close()
    print("Finished download ", i)

