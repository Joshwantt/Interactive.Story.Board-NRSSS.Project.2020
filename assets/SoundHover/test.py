import json
import os

##Find errors between filesystem and json file
##Replace test.json in this directory with the current narrative.json

with open('test.json', 'r') as file:
    data = file.read()

l = data.split("\n")

titles = []
tidyTitles = []

hover = []
tidyHover = []

for f in l:
    if ("sound_narration" in f):
        titles.append(f)

for e in titles:
    temp =  e.split('"')
    tidyTitles.append(temp[3])

for f in l:
    if ("sound_hover" in f):
        hover.append(f)

for e in hover:
    temp =  e.split('"')
    tidyHover.append(temp[3])

d = os.listdir()

for eff in tidyTitles:
    if eff not in d:
        print(eff+"\n")

for ef in tidyHover:
    if ef not in d:
        print(ef+"\n")
        



