import pygame
import sys
import json
import shutil
import os
from random import shuffle, choice
import time
from pygame.locals import *
import tkinter
from tkinter import filedialog


pygame.init()
pygame.font.init()
gameIcon = pygame.image.load('assets/flag.ico')
pygame.display.set_icon(gameIcon)
pygame.display.set_caption('MemoQuiz')
screen = pygame.display.set_mode((1490, 750), pygame.RESIZABLE)

buttonFont = pygame.font.SysFont('impact', 80)
sButtonFont = pygame.font.SysFont('impact', 30)
buttonTxt = buttonFont.render('New Game', True, (255, 255, 255))
sButtonTxt = sButtonFont.render('Save & Play', True, (255, 255, 255))
shButtonTxt = sButtonFont.render('Play', True, (255, 255, 255))
gbButtonTxt = sButtonFont.render('Do nothing', True, (255, 255, 255))
dButtonTxt = sButtonFont.render('Delete', True, (255, 255, 255))

buttonImg = pygame.image.load("assets/button.png")
selectedButton = pygame.image.load("assets/selected button.png")
box = pygame.image.load("assets/box.png")
emptyBox = pygame.image.load("assets/empty box.png")
selectedBox = pygame.image.load("assets/selected box.png")
previousButton = pygame.image.load("assets/previous.png")
nextButton = pygame.image.load("assets/next.png")
delButton = pygame.image.load("assets/delete.png")
editButton = pygame.image.load("assets/edit.png")
playButton = pygame.image.load("assets/play.png")
plusButton = pygame.image.load("assets/plus.png")
sedit = pygame.image.load("assets/sedit.png")
sdelete = pygame.image.load("assets/sdelete.png")
splay = pygame.image.load("assets/splay.png")
bbox = pygame.image.load("assets/bbox.png")
wbox = pygame.image.load("assets/wbox.png")
back = pygame.image.load("assets/back.gif")

lastDir = os.path.expanduser('~/Documents/')
lastDirSound = os.path.expanduser('~/Documents/')
n = 0

menu = True
newGame = False
game = False
delmenu = False

def browse_image(path):
    main_win = tkinter.Tk()
    main_win.withdraw()
    main_win.overrideredirect(True)
    main_win.geometry('0x0+0+0')
    main_win.lift()
    main_win.focus_force()
    filename = filedialog.askopenfilename(initialdir=path,
                                          title="Select an IMAGE",
                                          filetypes=(("images", "*.png*"),
                                                     (" ", "*.*")))
    main_win.destroy()

    if filename[-4:] == ".PNG" or filename[-4:] == ".png":
        with open("data/handler.json", "r") as f:
            data = json.load(f)
        dirname = ""
        temp = ""
        for char in filename:
            temp += char
            if char == "/":
                dirname += temp
                temp = ""
        data["ipics"] += 1
        shutil.copyfile(filename, os.getcwd() + "\\data\\pics\\" + str(data["ipics"])+".png")
        with open("data/handler.json", "w") as f:
            json.dump(data, f)
        return str(data["ipics"])+".png", dirname
    else:
        return "", path


def browse_sound(path):
    main_win = tkinter.Tk()
    main_win.withdraw()
    main_win.overrideredirect(True)
    main_win.geometry('0x0+0+0')
    main_win.lift()
    main_win.focus_force()
    filename = filedialog.askopenfilename(initialdir=path,
                                          title="Select a SOUND",
                                          filetypes=(("sound", "*.mp3*"),
                                                     (" ", "*.*")))
    main_win.destroy()

    if filename[-4:] == ".mp3":
        with open("data/handler.json", "r") as f:
            data = json.load(f)
        dirname = ""
        temp = ""
        for char in filename:
            temp += char
            if char == "/":
                dirname += temp
                temp = ""
        data["isound"] += 1
        shutil.copyfile(filename, os.getcwd() + "\\data\\sound\\" + str(data["isound"])+".mp3")
        with open("data/handler.json", "w") as f:
            json.dump(data, f)
        return str(data["isound"])+".mp3", dirname
    else:
        return "0.mp3", path


with open("data/handler.json", "r") as f:
    data = json.load(f)

for game in range(len(data["games"])):
    for i in range(len(data["games"][game][0])):
        if data["games"][game][0][i] != "":
            exist = False
            for root, dirs, files in os.walk('data/pics/'):
                for file in files:
                    if data["games"][game][0][i] == file:
                        exist = True
            if not(exist):
                data["games"][game][0][i] = "0.png"
for game in range(len(data["games"])):
    for i in range(len(data["games"][game][1])):
        if data["games"][game][0][i] != "":
            exist = False
            for root, dirs, files in os.walk('data/sound/'):
                for file in files:
                    if data["games"][game][1][i] == file:
                        exist = True
            if not(exist):
                data["games"][game][1][i] = "0.mp3"

if data["games"] == []:
    data["isound"] = 0
    data["ipics"] = 0
    
with open("data/handler.json", "w") as f:
    json.dump(data, f)

for root, dirs, files in os.walk('data/pics/'):
    for file in files:
        try:
            if int(file[:-4]) > data["ipics"]:
                os.remove(os.path.join(root, file))
        except:
            os.remove(os.path.join(root, file))
for root, dirs, files in os.walk('data/sound/'):
    for file in files:
        try:
            if int(file[:-4]) > data["isound"]:
                os.remove(os.path.join(root, file))
        except:
            os.remove(os.path.join(root, file))

for root, dirs, files in os.walk('data/pics/'):
    for file in files:
        if file != "0.png":
            exist = False
            for game in data["games"]:
                for image in game[0]:
                    if image == file:
                        exist = True
            if not(exist):
                os.remove(os.path.join(root, file))
for root, dirs, files in os.walk('data/sound/'):
    for file in files:
        if file != "0.mp3":
            exist = False
            for game in data["games"]:
                for sound in game[1]:
                    if sound == file:
                        exist = True
            if not(exist):
                os.remove(os.path.join(root, file))

while True:
    while menu:
        pygame.time.delay(100)
        screen.fill((60, 60, 85))
        width, height = screen.get_size()
        mx, my = pygame.mouse.get_pos()
        area = -1
        action = 0
        with open("data/handler.json", "r") as f:
            data = json.load(f)

        if (width / 2 - 550 * width / 1490 / 2 < mx < width / 2 + 550 * width / 1490 / 2 and
                height / 4 - 100 * width / 1490 / 2 < my < height / 4 + 100 * width / 1490 / 2):
            screen.blit(pygame.transform.scale(selectedButton, (int(550 * width / 1490),
                                                                int(100 * width / 1490))),
                        (int(width / 2 - 550 * width / 1490 / 2), int(height / 4 - 100 * width / 1490 / 2)))
        else:
            screen.blit(pygame.transform.scale(buttonImg, (int(550 * width / 1490),
                                                           int(100 * width / 1490))),
                        (int(width / 2 - 550 * width / 1490 / 2), int(height / 4 - 100 * width / 1490 / 2)))

        screen.blit(pygame.transform.scale(buttonTxt, (int(buttonTxt.get_width() * width / 1490),
                                                       int(buttonTxt.get_height() * width / 1490))),
                    (int(width / 2 - buttonTxt.get_width() * width / 1490 / 2),
                     int(height / 4 - buttonTxt.get_height() * width / 1490 / 2)))

        if n<len(data["games"]):
            if (width * 3 / 14 - 300 * width / 1490 / 2 < mx < width * 3 / 14 + 300 * width / 1490 / 2 and
                    height / 1.45 - 300 * width / 1490 / 2 < my < height / 1.45 + 300 * width / 1490 / 2):
                screen.blit(pygame.transform.scale(selectedBox, (int(300 * width / 1490),
                                                                 int(300 * width / 1490))),
                            (int(width * 3 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
                area = 0
            else:
                screen.blit(pygame.transform.scale(box, (int(300 * width / 1490),
                                                         int(300 * width / 1490))),
                            (int(width * 3 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
            i = 0
            while i<12 and data["games"][n][0][i] == '':
                i+=1
            tempImg = pygame.image.load("data/pics/" + data["games"][n][0][i])
            tempImg = pygame.transform.scale(tempImg,
                                             (int(tempImg.get_width() * 150 * width / 1490 / tempImg.get_height()),
                                              int(150 * width / 1490)))
            if tempImg.get_width() > 200 * width / 1490:
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(200 * width / 1490),
                                                  int(tempImg.get_height() * 200 * width / 1490 / tempImg.get_width())))
            screen.blit(tempImg,(int(width * 3 / 14 -tempImg.get_width()/2),
                                 int(height / 1.45 - 50 * width / 1490 -tempImg.get_height()/2)))

            title = sButtonFont.render(data["games"][n][2], True, (255, 255, 255))
            screen.blit(pygame.transform.scale(title, (int(title.get_width() * width / 1490),
                                                       int(title.get_height() * width / 1490))),
                        (int(width * 3 / 14 - title.get_width()/2),
                         int(height / 1.45 + 45 * width / 1490 - title.get_height()/2)))

            if (width * 3 / 14 - 75 * width / 1490 - 50 * width / 2980 < mx < width * 3 / 14 - 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 1
                screen.blit(pygame.transform.scale(sdelete, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 3 / 14 - 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(delButton, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 3 / 14 - 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 3 / 14 - 50 * width / 2980 < mx < width * 3 / 14 + 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                screen.blit(pygame.transform.scale(splay, (int(50 * width / 1490),
                                                           int(50 * width / 1490))),
                            (int(width * 3 / 14 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(playButton, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 3 / 14 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 3 / 14 + 75 * width / 1490 - 50 * width / 2980 < mx < width * 3 / 14 + 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 2
                screen.blit(pygame.transform.scale(sedit, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 3 / 14 + 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(editButton, (int(50 * width / 1490),
                                                           int(50 * width / 1490))),
                            (int(width * 3 / 14 + 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))

        else:
            screen.blit(pygame.transform.scale(emptyBox, (int(300 * width / 1490),
                                                          int(300 * width / 1490))),
                       (int(width * 3 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))

        if n+1<len(data["games"]):
            if (width * 7 / 14 - 300 * width / 1490 / 2 < mx < width * 7 / 14 + 300 * width / 1490 / 2 and
                    height / 1.45 - 300 * width / 1490 / 2 < my < height / 1.45 + 300 * width / 1490 / 2):
                screen.blit(pygame.transform.scale(selectedBox, (int(300 * width / 1490),
                                                                 int(300 * width / 1490))),
                            (int(width * 7 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
                area = 1
            else:
                screen.blit(pygame.transform.scale(box, (int(300 * width / 1490),
                                                         int(300 * width / 1490))),
                            (int(width * 7 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
            i = 0
            while 1 < 12 and data["games"][n+1][0][i] == '':
                i += 1
            tempImg = pygame.image.load("data/pics/" + data["games"][n+1][0][i])
            tempImg = pygame.transform.scale(tempImg,
                                             (int(tempImg.get_width() * 150 * width / 1490 / tempImg.get_height()),
                                              int(150 * width / 1490)))

            title = sButtonFont.render(data["games"][n+1][2], True, (255, 255, 255))
            screen.blit(pygame.transform.scale(title, (int(title.get_width() * width / 1490),
                                                       int(title.get_height() * width / 1490))),
                        (int(width * 7 / 14 - title.get_width() / 2),
                         int(height / 1.45 + 45 * width / 1490 - title.get_height() / 2)))

            if tempImg.get_width() > 200 * width / 1490:
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(200 * width / 1490),
                                                  int(tempImg.get_height() * 200 * width / 1490 / tempImg.get_width())))
            screen.blit(tempImg, (int(width * 7 / 14 - tempImg.get_width() / 2),
                                  int(height / 1.45 - 50 * width / 1490 - tempImg.get_height() / 2)))
            if (width * 7 / 14 - 75 * width / 1490 - 50 * width / 2980 < mx < width * 7 / 14 - 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 1
                screen.blit(pygame.transform.scale(sdelete, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 7 / 14 - 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(delButton, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 7 / 14 - 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 7 / 14 - 50 * width / 2980 < mx < width * 7 / 14 + 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                screen.blit(pygame.transform.scale(splay, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 7 / 14 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(playButton, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 7 / 14 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 7 / 14 + 75 * width / 1490 - 50 * width / 2980 < mx < width * 7 / 14 + 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 2
                screen.blit(pygame.transform.scale(sedit, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 7 / 14 + 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(editButton, (int(50 * width / 1490),
                                                           int(50 * width / 1490))),
                            (int(width * 7 / 14 + 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(emptyBox, (int(300 * width / 1490),
                                                          int(300 * width / 1490))),
                       (int(width * 7 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))

        if n + 2 < len(data["games"]):
            if (width * 11 / 14 - 300 * width / 1490 / 2 < mx < width * 11 / 14 + 300 * width / 1490 / 2 and
                    height / 1.45 - 300 * width / 1490 / 2 < my < height / 1.45 + 300 * width / 1490 / 2):
                screen.blit(pygame.transform.scale(selectedBox, (int(300 * width / 1490),
                                                                 int(300 * width / 1490))),
                            (int(width * 11 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
                area = 2
            else:
                screen.blit(pygame.transform.scale(box, (int(300 * width / 1490),
                                                         int(300 * width / 1490))),
                            (int(width * 11 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))
            i = 0
            while 1 < 12 and data["games"][n+2][0][i] == '':
                i += 1
            tempImg = pygame.image.load("data/pics/" + data["games"][n+2][0][i])
            tempImg = pygame.transform.scale(tempImg,
                                             (int(tempImg.get_width() * 150 * width / 1490 / tempImg.get_height()),
                                              int(150 * width / 1490)))

            title = sButtonFont.render(data["games"][n + 2][2], True, (255, 255, 255))
            screen.blit(pygame.transform.scale(title, (int(title.get_width() * width / 1490),
                                                       int(title.get_height() * width / 1490))),
                        (int(width * 11 / 14 - title.get_width() / 2),
                         int(height / 1.45 + 45 * width / 1490 - title.get_height() / 2)))

            if tempImg.get_width() > 200 * width / 1490:
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(200 * width / 1490),
                                                  int(tempImg.get_height() * 200 * width / 1490 / tempImg.get_width())))
            screen.blit(tempImg, (int(width * 11 / 14 - tempImg.get_width() / 2),
                                  int(height / 1.45 - 50 * width / 1490 - tempImg.get_height() / 2)))
            if (width * 11 / 14 - 75 * width / 1490 - 50 * width / 2980 < mx < width * 11 / 14 - 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 1
                screen.blit(pygame.transform.scale(sdelete, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 11 / 14 - 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(delButton, (int(50 * width / 1490),
                                                               int(50 * width / 1490))),
                            (int(width * 11 / 14 - 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 11 / 14 - 50 * width / 2980 < mx < width * 11 / 14 + 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                screen.blit(pygame.transform.scale(splay, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 11 / 14 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(playButton, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 11 / 14 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            if (width * 11 / 14 + 75 * width / 1490 - 50 * width / 2980 < mx < width * 11 / 14 + 75 * width / 1490+ 50 * width / 2980 and
                    height / 1.45 + 100 * width / 1490 - 50 * width / 2980 < my < height / 1.45 + 100 * width / 1490+ 50 * width / 2980):
                action = 2
                screen.blit(pygame.transform.scale(sedit, (int(50 * width / 1490),
                                                                int(50 * width / 1490))),
                            (int(width * 11 / 14 + 75 * width / 1490 - 50 * width / 2980),
                             int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
            else:
                screen.blit(pygame.transform.scale(editButton, (int(50 * width / 1490),
                                                           int(50 * width / 1490))),
                            (int(width * 11 / 14 + 75 * width / 1490 - 50 * width / 2980),
                            int(height / 1.45 + 100 * width / 1490 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(emptyBox, (int(300 * width / 1490),
                                                          int(300 * width / 1490))),
                        (int(width * 11 / 14 - 300 * width / 1490 / 2), int(height / 1.45 - 300 * width / 1490 / 2)))

        if (width / 14 - 75 * width / 1490 / 2 < mx < width / 14 + 75 * width / 1490 / 2 and
                height / 1.45 - 300 * width / 1490 / 2 < my < height / 1.45 + 300 * width / 1490 / 2):
            area = -2
            pygame.draw.rect(screen, (70, 70, 95), (int(width / 14 - 75 * width / 1490 / 2),
                                                    int(height / 1.45 - 300 * width / 1490 / 2),
                                                    int(75 * width / 1490),
                                                    int(300 * width / 1490)))
        elif (width * 13 / 14 - 75 * width / 1490 / 2 < mx < width * 13 / 14 + 75 * width / 1490 / 2 and
              height / 1.45 - 300 * width / 1490 / 2 < my < height / 1.45 + 300 * width / 1490 / 2):
            area = -3
            pygame.draw.rect(screen, (70, 70, 95), (int(width * 13 / 14 - 75 * width / 1490 / 2),
                                                    int(height / 1.45 - 300 * width / 1490 / 2),
                                                    int(75 * width / 1490),
                                                    int(300 * width / 1490)))

        screen.blit(pygame.transform.scale(nextButton, (int(100 * width / 1490),
                                                        int(100 * width / 1490))),
                    (int(width * 13 / 14 - 100 * width / 1490 / 2), int(height / 1.45 - 100 * width / 1490 / 2)))

        screen.blit(pygame.transform.scale(previousButton, (int(100 * width / 1490),
                                                            int(100 * width / 1490))),
                    (int(width / 14 - 100 * width / 1490 / 2), int(height / 1.45 - 100 * width / 1490 / 2)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if (width / 2 - 550 * width / 1490 / 2 < mx < width / 2 + 550 * width / 1490 / 2 and
                        height / 4 - 100 * width / 1490 / 2 < my < height / 4 + 100 * width / 1490 / 2):
                    newGame = True
                    menu = False
                    k = -1
                    imgList = ['', '', '', '', '', '', '', '', '', '', '', '']
                    soundList = ['', '', '', '', '', '', '', '', '', '', '', '']
                    name = ' '
                    screen.fill((60, 60, 85))
                    pygame.display.update()
                elif area >= 0:
                    if action == 2:
                        with open("data/handler.json", "r") as f:
                            data = json.load(f)
                        newGame = True
                        menu = False
                        k = n+area
                        imgList = data["games"][k][0]
                        soundList = data["games"][k][1]
                        name = data["games"][k][2]
                        screen.fill((60, 60, 85))
                        pygame.display.update()
                    elif action == 0:
                        game = True
                        menu = False
                        k = n+area
                        imgList = data["games"][k][0]
                        soundList = data["games"][k][1]
                        name = data["games"][k][1]
                        screen.fill((60, 60, 85))
                        pygame.display.update()
                    elif action == 1:
                        delmenu = True
                        menu = False
                        k = n + area
                        imgList = data["games"][k][0]
                        soundList = data["games"][k][1]
                        screen.fill((60, 60, 85))
                        pygame.display.update()
                elif area == -2:
                    if n > 2:
                        n -= 3
                elif area == -3:
                    with open("data/handler.json", "r") as f:
                        data = json.load(f)
                    if n+3 < len(data["games"]):
                        n += 3

        pygame.display.update()

    while newGame:
        pygame.time.delay(50)
        screen.fill((60, 60, 85))
        width, height = screen.get_size()
        mx, my = pygame.mouse.get_pos()
        j = 0
        area = -1

        for i in range(12):
            j = i // 4
            if imgList[i] == '':
                screen.blit(pygame.transform.scale(emptyBox, (int(304 * width / 1490),
                                                              int(188 * width / 1490))),
                            (int(width * (3 + (i % 4) * 10.8) / 49), int(height * (4 + j * 11) / 40)))
            else:
                tempImg = pygame.image.load("data/pics/" + imgList[i])
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(tempImg.get_width()*188 * width / 1490 / tempImg.get_height()),
                                                  int(188 * width / 1490)))
                if tempImg.get_width() > 304 * width / 1490:
                    tempImg = pygame.transform.scale(tempImg,
                                                     (int(304 * width / 1490),
                                                      int(tempImg.get_height()*304 * width / 1490/tempImg.get_width())))

                screen.blit(pygame.transform.scale(wbox, (int(314 * width / 1490),
                                                          int(198 * width / 1490))),
                            (int(width * (3 + (i % 4) * 10.8) / 49-10 * width / 2980), int(height * (4 + j * 11) / 40-10* width / 2980)))

                screen.blit(tempImg,
                            (int(width * (3 + (i % 4) * 10.8) / 49+304 * width / 2980-tempImg.get_width()/2),
                             int(height * (4 + j * 11) / 40+188 * width / 2980-tempImg.get_height()/2)))

            if (width * (3 + (i % 4) * 10.8) / 49 < mx < width * (3 + (i % 4) * 10.8) / 49 + 304 * width / 1490 and
                    height * (4 + j * 11) / 40 < my < height * (4 + j * 11) / 40 + 188 * width / 1490):
                area = i
                screen.blit(pygame.transform.scale(plusButton, (int(150 * width / 1490),
                                                                int(150 * width / 1490))),
                            (int(width * (3 + (i % 4) * 10.8) / 49 + 154 * width / 2980),
                             int(height * (4 + j * 11) / 40 + 38 * width / 2980)))

        if (width / 2 - 300 * width / 2980 < mx < width / 2 + 300 * width / 2980 and
                height * 46.5 / 49 - 50 * width / 2980 < my < height * 46.5 / 49 + 50 * width / 2980):
            area = -2
            screen.blit(pygame.transform.scale(selectedButton, (int(300 * width / 1490),
                                                                int(50 * width / 1490))),
                        (int(width / 2 - 300 * width / 2980),
                         int(height * 46.5 / 49 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(buttonImg, (int(300 * width / 1490),
                                                           int(50 * width / 1490))),
                        (int(width / 2 - 300 * width / 2980),
                         int(height*46.5 / 49 - 50 * width / 2980)))

        screen.blit(pygame.transform.scale(sButtonTxt, (int(sButtonTxt.get_width() * width / 1490),
                                                        int(sButtonTxt.get_height() * width / 1490))),
                    (int(width / 2 - sButtonTxt.get_width() * width / 2980),
                     int(height*46.5 / 49 - sButtonTxt.get_height() * width / 2980)))

        if (width / 28 - 50 * width / 2980 < mx < width / 28 + 50 * width / 2980 and
                height*2.5 / 49 - 50 * width / 2980 < my < height*2.5 / 49 + 40 * width / 2980):
            area = -3
            pygame.draw.rect(screen, (70, 70, 95), (int(width / 28 - 50 * width / 2980),
                                                    int(height*2.5 / 49 - 50 * width / 2980),
                                                    int(50 * width / 1490),
                                                    int(50 * width / 1490)))

        screen.blit(pygame.transform.scale(previousButton, (int(50 * width / 1490),
                                                            int(50 * width / 1490))),
                    (int(width / 28 - 50 * width / 1490 / 2), int(height*2.5 / 49 - 50 * width / 1490 / 2)))

        title = sButtonFont.render(name, True, (255, 255, 255))
        pygame.draw.rect(screen, (70, 70, 95), (int(width / 2 - (title.get_width()+30) * width / 2980),
                                                int(height / 20 - (title.get_height()+10) * width / 2980),
                                               (int(title.get_width()+30) * width / 1490),
                                                int((title.get_height()+10) * width / 1490)))
        screen.blit(pygame.transform.scale(title, (int(title.get_width() * width / 1490),
                                                   int(title.get_height() * width / 1490))),
                    (int(width / 2 - title.get_width() * width / 2980),
                     int(height / 20 - title.get_height() * width / 2980)))
        if (width / 2 - (title.get_width()+30) * width / 2980 < mx < width / 2 + (title.get_width()+30) * width / 2980 and
                height / 20 - (title.get_height()+10) * width / 2980 < my < height / 20 + (title.get_height()+10) * width / 2980):
            area = -4

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if area >= 0:
                    imgList[area], lastDir = browse_image(lastDir)
                    if imgList[area] != '':
                        soundList[area], lastDirSound = browse_sound(lastDirSound)
                elif area == -2 and imgList != ["", "", "", "", "", "", "", "", "", "", "", ""]:
                    if k == -1:
                        with open("data/handler.json", "r") as f:
                            data = json.load(f)
                        data["games"].append([imgList, soundList, name])
                        with open("data/handler.json", "w") as f:
                            json.dump(data, f)
                        game = True
                        newGame = False
                    else:
                        data["games"][k][0] = imgList
                        data["games"][k][1] = soundList
                        data["games"][k][2] = name
                        with open("data/handler.json", "w") as f:
                            json.dump(data, f)
                        game = True
                        newGame = False


                elif area == -3:
                    menu = True
                    newGame = False
                elif area == -4:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 11:
                    name += event.unicode
        pygame.display.update()

    hidden = -1
    while game:
        pygame.time.delay(50)
        screen.fill((60, 60, 85))
        width, height = screen.get_size()
        mx, my = pygame.mouse.get_pos()
        area = -1


        if (width / 2 - 300 * width / 2980 < mx < width / 2 + 300 * width / 2980 and
                height * 46.5 / 49 - 50 * width / 2980 < my < height * 46.5 / 49 + 50 * width / 2980):
            area = -2
            screen.blit(pygame.transform.scale(selectedButton, (int(300 * width / 1490),
                                                                int(50 * width / 1490))),
                        (int(width / 2 - 300 * width / 2980),
                         int(height * 46.5 / 49 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(buttonImg, (int(300 * width / 1490),
                                                           int(50 * width / 1490))),
                        (int(width / 2 - 300 * width / 2980),
                         int(height*46.5 / 49 - 50 * width / 2980)))

        screen.blit(pygame.transform.scale(shButtonTxt, (int(shButtonTxt.get_width() * width / 1490),
                                                         int(shButtonTxt.get_height() * width / 1490))),
                    (int(width / 2 - shButtonTxt.get_width() * width / 2980),
                     int(height*46.5 / 49 - shButtonTxt.get_height() * width / 2980)))

        for i in range(12):
            j = i // 4
            if imgList[i] != '':
                tempImg = pygame.image.load("data/pics/" + imgList[i])
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(tempImg.get_width()*188 * width / 1490 / tempImg.get_height()),
                                                  int(188 * width / 1490)))
                if tempImg.get_width() > 304 * width / 1490:
                    tempImg = pygame.transform.scale(tempImg,
                                                     (int(304 * width / 1490),
                                                      int(tempImg.get_height()*304 * width / 1490/tempImg.get_width())))

                screen.blit(pygame.transform.scale(wbox, (int(314 * width / 1490),
                                                          int(198 * width / 1490))),
                            (int(width * (3 + (i % 4) * 10.8) / 49-10 * width / 2980), int(height * (4 + j * 11) / 40-10* width / 2980)))

                screen.blit(tempImg,
                            (int(width * (3 + (i % 4) * 10.8) / 49+304 * width / 2980-tempImg.get_width()/2),
                             int(height * (4 + j * 11) / 40+188 * width / 2980-tempImg.get_height()/2)))

            if (width * (3 + (i % 4) * 10.8) / 49 < mx < width * (3 + (i % 4) * 10.8) / 49 + 304 * width / 1490 and
                    height * (4 + j * 11) / 40 < my < height * (4 + j * 11) / 40 + 188 * width / 1490):
                area = i

        if (width / 28 - 50 * width / 2980 < mx < width / 28 + 50 * width / 2980 and
                height*2.5 / 49 - 50 * width / 2980 < my < height*2.5 / 49 + 40 * width / 2980):
            area = -3
            pygame.draw.rect(screen, (70, 70, 95), (int(width / 28 - 50 * width / 2980),
                                                    int(height*2.5 / 49 - 50 * width / 2980),
                                                    int(50 * width / 1490),
                                                    int(50 * width / 1490)))

        screen.blit(pygame.transform.scale(previousButton, (int(50 * width / 1490),
                                                            int(50 * width / 1490))),
                    (int(width / 28 - 50 * width / 1490 / 2), int(height*2.5 / 49 - 50 * width / 1490 / 2)))


        if hidden != -1:
            j = hidden // 4
            screen.blit(pygame.transform.scale(bbox, (int(314 * width / 1490),
                                                      int(198 * width / 1490))),
                        (int(width * (3 + (hidden % 4) * 10.8) / 49 - 10 * width / 2980),
                         int(height * (4 + j * 11) / 40 - 10 * width / 2980)))
            screen.blit(pygame.transform.scale(back, (int(198 * width / 1490),
                                                      int(198 * width / 1490))),
                        (int(width * (3 + (hidden % 4) * 10.8) / 49 - (10 - 314 + 198) * width / 2980),
                         int(height * (4 + j * 11) / 40 - 10 * width / 2980)))


        for event in pygame.event.get():
            if event.type == QUIT:
                sys.tracebacklimit = 0
                pygame.mixer.music.stop()
                pygame.mixer.quit()
                pygame.quit()
                sys.exit(1)


            elif event.type == MOUSEBUTTONDOWN:
                if area >= 0:
                    pygame.mixer.music.stop()
                    if area == hidden :
                        hidden = -1
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("data/sound/"+soundList[area])
                    pygame.mixer.music.play()
                elif area == -2:
                    pygame.mixer.music.stop()

                    for i in range(12):
                        j = i // 4
                        if imgList[i] != '':
                            screen.blit(pygame.transform.scale(bbox, (int(314 * width / 1490),
                                                                      int(198 * width / 1490))),
                                        (int(width * (3 + (i % 4) * 10.8) / 49 - 10 * width / 2980),
                                         int(height * (4 + j * 11) / 40 - 10 * width / 2980)))
                            screen.blit(pygame.transform.scale(back, (int(198 * width / 1490),
                                                                      int(198 * width / 1490))),
                                        (int(width * (3 + (i % 4) * 10.8) / 49 - (10-314+198) * width / 2980),
                                         int(height * (4 + j * 11) / 40 - 10 * width / 2980)))
                    pygame.display.update()
                    time.sleep(1)
                    index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                    shuffle(index)
                    tempImgList = imgList.copy()
                    tempSoundList = soundList.copy()
                    for i in range(12):
                        imgList[i] = tempImgList[index[i]]
                        soundList[i] = tempSoundList[index[i]]
                    rList = []
                    for i in range(12):
                        if imgList[i] != '':
                            rList.append(i)
                    hidden = choice(rList)


                elif area == -3:
                    pygame.mixer.music.stop()
                    menu = True
                    game = False

        pygame.display.update()

    while delmenu:
        pygame.time.delay(100)
        screen.fill((60, 60, 85))
        width, height = screen.get_size()
        mx, my = pygame.mouse.get_pos()
        area = -1

        for i in range(12):
            j = i // 4
            if imgList[i] != '':
                tempImg = pygame.image.load("data/pics/" + imgList[i])
                tempImg = pygame.transform.scale(tempImg,
                                                 (int(tempImg.get_width()*188 * width / 1490 / tempImg.get_height()),
                                                  int(188 * width / 1490)))
                if tempImg.get_width() > 304 * width / 1490:
                    tempImg = pygame.transform.scale(tempImg,
                                                     (int(304 * width / 1490),
                                                      int(tempImg.get_height()*304 * width / 1490/tempImg.get_width())))

                screen.blit(pygame.transform.scale(wbox, (int(314 * width / 1490),
                                                          int(198 * width / 1490))),
                            (int(width * (3 + (i % 4) * 10.8) / 49-10 * width / 2980), int(height * (4 + j * 11) / 40-10* width / 2980)))

                screen.blit(tempImg,
                            (int(width * (3 + (i % 4) * 10.8) / 49+304 * width / 2980-tempImg.get_width()/2),
                             int(height * (4 + j * 11) / 40+188 * width / 2980-tempImg.get_height()/2)))

        if (width *2/6 - 300 * width / 2980 < mx < width*2/6  + 300 * width / 2980 and
                height * 46.5 / 49 - 50 * width / 2980 < my < height * 46.5 / 49 + 50 * width / 2980):
            area = 2
            screen.blit(pygame.transform.scale(selectedButton, (int(300 * width / 1490),
                                                                int(50 * width / 1490))),
                        (int(width*2/6 - 300 * width / 2980),
                         int(height * 46.5 / 49 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(buttonImg, (int(300 * width / 1490),
                                                           int(50 * width / 1490))),
                        (int(width*2/6 - 300 * width / 2980),
                         int(height * 46.5 / 49 - 50 * width / 2980)))

        screen.blit(pygame.transform.scale(dButtonTxt, (int(dButtonTxt.get_width() * width / 1490),
                                                        int(dButtonTxt.get_height() * width / 1490))),
                    (int(width * 2 / 6 - dButtonTxt.get_width() * width / 2980),
                     int(height * 46.5 / 49 - dButtonTxt.get_height() * width / 2980)))

        if (width*4/6 - 300 * width / 2980 < mx < width *4/6  + 300 * width / 2980 and
                height * 46.5 / 49 - 50 * width / 2980 < my < height * 46.5 / 49 + 50 * width / 2980):
            area = 1
            screen.blit(pygame.transform.scale(selectedButton, (int(300 * width / 1490),
                                                                int(50 * width / 1490))),
                        (int(width*4/6 - 300 * width / 2980),
                         int(height * 46.5 / 49 - 50 * width / 2980)))
        else:
            screen.blit(pygame.transform.scale(buttonImg, (int(300 * width / 1490),
                                                           int(50 * width / 1490))),
                        (int(width*4/6 - 300 * width / 2980),
                         int(height*46.5 / 49 - 50 * width / 2980)))

        screen.blit(pygame.transform.scale(gbButtonTxt, (int(gbButtonTxt.get_width() * width / 1490),
                                                         int(gbButtonTxt.get_height() * width / 1490))),
                    (int(width *4/ 6 - gbButtonTxt.get_width() * width / 2980),
                     int(height * 46.5 / 49 - gbButtonTxt.get_height() * width / 2980)))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if area == 1:
                    menu = True
                    delmenu = False
                elif area == 2:
                    with open("data/handler.json", "r") as f:
                        data = json.load(f)
                    data["games"].pop(k)
                    menu = True
                    delmenu = False
                    with open("data/handler.json", "w") as f:
                        json.dump(data, f)
        pygame.display.update()
