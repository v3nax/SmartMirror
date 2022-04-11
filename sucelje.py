from tkinter import *
from datetime import datetime as dt
import time
from turtle import bgcolor, width

class Sucelje():
    def __init__(self, root) -> None:
        root = root

        sati = dt.now().hour

        if sati >= 6 and sati <=20:
            self.boja = '#009999'
            self.ekran = '#63B4B8'
            self.slova ='white'
        else:
            self.boja = '#142850'
            self.ekran = '#27496D'
            self.slova ='#DADDFC'


    def promijeni_stil(self, naslov, geometrija):
        root.title(naslov)
        root.geometry(geometrija)
        root.configure(background=self.boja)

    def kreiraj_okvir(self, okvir, sirina, duzina, x, y):
        self.novi = Frame (okvir, width=sirina, height=duzina)
        self.novi.configure(background=self.ekran)
        self.novi.place(x=x, y=y)       

    def kreiraj_gumb(self, okvir, tekst, naredba, x, y):
        self.gumb = Button(okvir, text=str(tekst), command=naredba)
        self.gumb.configure(overrelief='groove', 
                bg=self.boja, 
                activebackground=self.boja,
                disabledforeground=self.boja, 
                foreground=self.slova, 
                relief='flat',
                activeforeground=self.slova)
        self.gumb.place(x=x, y=y)


root = Tk()
Sucelje(root).promijeni_stil('Smart Mirror', '300x400')

okvir = Sucelje(root).kreiraj_okvir(root, 200,200,10,10)

gumb1 = Sucelje(root).kreiraj_gumb(okvir, 'Gumb', print('Gumb'), 10, 10)

gumb2 = Sucelje(root).kreiraj_gumb(okvir, 'Gumbic', print('Gumbic'), 60, 10)

h = dt.now().hour
m = dt.now().minute
time = f'{h}:{m}'
print (time)

if h >= 6 and h <=20:
    boja = '#009999'
    ekran = '#63B4B8'
    slova ='white'
else:
    boja = '#142850'
    ekran = '#27496D'
    slova ='#DADDFC'


sat_str = StringVar(root, h)
sat = Spinbox(root, textvariable=sat_str, from_=0,to=23,wrap=True,width=3 ,state="readonly", 
                background=boja, 
                activebackground=boja,
                foreground=boja,
                buttonbackground=ekran,
                buttonuprelief='flat',
                buttondownrelief='flat',
                relief='flat')
sat.place(x=10,y=100)

min_str = StringVar(root,m)

min = Spinbox(root, textvariable=min_str, from_=0,to=59,wrap=True,width=3 ,state="readonly", format="%02.0f",
                background=boja, 
                activebackground=boja,
                foreground=boja,
                buttonbackground=ekran,
                buttonuprelief='flat',
                buttondownrelief='flat',
                relief='flat')
min.place(x=50,y=100)

from random import randint

lbl = Label(root, background=boja, foreground=slova, textvariable=randint(3, 9))

print(randint(18,23))


root.mainloop()