from asyncio.windows_events import NULL
import requests
from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import datetime
from PIL import Image, ImageTk
from tkcalendar import Calendar, DateEntry
import sqlite3
from random import randint
import time

#####################################################
#############   DOHVACANJE PROGNOZE   ###############

url = 'https://meteo.hr/podaci.php?section=podaci_vrijeme&param=hrvatska1_n'
response = requests.get(url)
stranica = BeautifulSoup(response.text, 'html.parser')
tablica = stranica.find_all('tr')
    
prognoza_hr = []
rijecnik_prognoza_hr = {}

for t in tablica:
    tekst = t.get_text()
    red = tekst.split('\n')
    for i in red:
        if i == ' '*32:
            red.remove(i)
    if len(red) == 13:
        prognoza_hr.append(red)

for p in prognoza_hr:
    p[11] = p[11].strip()
    rijecnik_prognoza_hr[p[1]] = p[:]

################################################
#############   SUCELJE TKINTER  ###############

r = Tk()

###   Style: boje   ###
lista_gumba = []
sati = datetime.datetime.now().hour

if sati > 6 and sati < 19:
    boja = '#009999'
    ekran = '#63B4B8'
    slova ='white'
else:
    boja = '#142850'
    ekran = '#27496D'
    slova ='#DADDFC'

###   Okvir aplikacije   ### 

r.title("Smart Mirror")
r.geometry('350x520')
r.resizable(width=False, height=False)
r.configure(background=boja)


def promjena_boje():
    if sati > 7 and sati < 19:
        boja = '#009999'
    else:
        boja = '#142850'
    r.configure(background=boja)
    r.after(1000, promjena_boje)
promjena_boje()

################################################
##########        ZAGLAVLJE      ###############


okvir = Frame (r, border=1)
okvir.grid(column=0, row=0, columnspan=3)

gradovi = StringVar()
gradovi.set('Zagreb-Maksimir')

###   Izbor grada   ###

for k,values in rijecnik_prognoza_hr.items():
    values = rijecnik_prognoza_hr.get('Zagreb-Maksimir')
    grad = values[1]
    vjetar = values[3]

#############   SET HOME EKRAN  ###############

prikaz_temperature = ttk.Label(   r, 
                            text='No image!', 
                            font = ('Sans','8'), 
                            foreground=slova, 
                            justify=RIGHT, 
                            background=boja)
prikaz_temperature.place(x=230, y=90)

if rijecnik_prognoza_hr.get('Zagreb-Maksimir'):
    tekst_home = f'{round(float(values[6]))}°C\n彡{values[3]}'
    
     
prikaz_temperature.configure(text=tekst_home, font = ('Sans','12','bold'))


#############   PRIKAZ TEMPERATURE PO GRADOVIMA   ###############

prognoza_ispis = ttk.Label( r, 
                    text='', 
                    font = ('Sans','8'), 
                    foreground=slova, 
                    justify=LEFT, 
                    background=boja )


prikaz_slike = ttk.Label(  r, 
                            text='No image!', 
                            font = ('Sans','8'), 
                            foreground=slova, 
                            justify=CENTER, 
                            background=boja)
prikaz_slike.place(x=170, y=75)
prikaz_slike.configure(text='', image='')

values = rijecnik_prognoza_hr.get('Zagreb-Maksimir')

if values[11] == 'kiša' or values[11] == 'slaba kiša':
    sl = ImageTk.PhotoImage(Image.open("fotke\kisa.png"))

elif values[11] == 'susnježica':
    sl = Image.open("fotke\snow_s_rain.png")

elif values[11] == 'zrnat snijeg' or values[11] == 'slab snijeg' or values[11] == 'jak snijeg':
    sl = Image.open("fotke\snow.png")

elif values[11] == 'magla':
    sl = Image.open("fotke\\fog.png")

elif values[11] == 'umjereno oblačno' or values[11] == 'pretežno oblačno':
    sl = Image.open("fotke\partly_cloudy.png")

elif values[11] == 'potpuno oblačno':
    sl = Image.open("fotke\cloudy.png")

elif values[11] == 'pretežno vedro' or values[11] == 'vedro':
    sl = Image.open("fotke\sunny.png")

else:
    sl = Image.open("fotke\partly_cloudy.png")
        
slika1 = ImageTk.PhotoImage(sl.resize((50, 50), Image.ANTIALIAS))
prikaz_temperature.configure(image=slika1,compound=LEFT)
        

def prikazi_prognozu_hr(event):
    set_option = gradovi.get()
    global slika2

    if set_option in rijecnik_prognoza_hr.keys():
        values = (rijecnik_prognoza_hr.get(set_option))
        ispis =f'''Postaja: {values[1]}
Vjetar smjer: {values[3]}
Vjetar brzina (m/s): {values[4]}
Temperatura zraka (°C): {values[6]}	
Relativna vlažnost (%): {values[7]}	
Tlak zraka (hPa): {values[8]}
Stanje vremena: {values[11]}'''

    prognoza_ispis.configure(text=ispis, wraplength=160)
    prognoza_ispis.place(y=25,x=20)
    values = (rijecnik_prognoza_hr.get(set_option))

    if set_option in rijecnik_prognoza_hr.keys():
        if values[11] == 'kiša' or values[11] == 'slaba kiša':
            sl = ImageTk.PhotoImage(Image.open("fotke\kisa.png"))

        elif values[11] == 'susnježica':
            sl = Image.open("fotke\snow_s_rain.png")

        elif values[11] == 'zrnat snijeg' or values[11] == 'slab snijeg' or values[11] == 'jak snijeg':
            sl = Image.open("fotke\snow.png")

        elif values[11] == 'magla':
            sl = Image.open("fotke\\fog.png")

        elif values[11] == 'umjereno oblačno' or values[11] == 'pretežno oblačno':
            sl = Image.open("fotke\partly_cloudy.png")

        elif values[11] == 'potpuno oblačno':
            sl = Image.open("fotke\cloudy.png")

        elif values[11] == 'pretežno vedro' or values[11] == 'vedro':
            sl = Image.open("fotke\sunny.png")

        else:
            sl = Image.open("fotke\partly_cloudy.png")
        
        slika2 = ImageTk.PhotoImage(sl.resize((35, 35), Image.ANTIALIAS))
        

        if set_option == 'Zagreb-Maksimir':
            prikaz_slike.configure(image='')

        else:
            prikaz_slike.configure(image=slika2)


prikazi_prognozu_hr(values)

izbor_grada = OptionMenu(  okvir, 
                        gradovi, 
                        *rijecnik_prognoza_hr, 
                        command=prikazi_prognozu_hr)
izbor_grada.configure(  bg=boja, 
                        width=45, 
                        activebackground=slova, 
                        foreground=slova, 
                        relief='flat',
                        border=0, 
                        highlightthickness=0, 
                        activeforeground=boja)
izbor_grada.grid(column=0, row=0, ipadx=20)


prikaz_vremena = ttk.Label( r, 
                            font = ('Sans','10','bold'), 
                            foreground=slova, 
                            justify=RIGHT, 
                            background=boja)
prikaz_vremena.place(x=220, y=25)


#############   SET DATUM I VRIJEME   ###############

def clock():
    now = datetime.datetime.now()
        
    trenutno = now.strftime(f"{grad}\n%d. %m. %Y\n%H:%M:%S\n")

    datum_vrijeme = f'{trenutno}'
    prikaz_vremena.configure(text=datum_vrijeme)
    
    r.after(1000, clock)
clock()

sada=datetime.datetime.now()


#############   PORUKA DOBRODOSLICE   ###############

jutro_img = ImageTk.PhotoImage(Image.open("fotke\\jutro.png").resize((35, 35), Image.ANTIALIAS))
dan_img = ImageTk.PhotoImage(Image.open("fotke\\dan.png").resize((35, 35), Image.ANTIALIAS))
noc_img = ImageTk.PhotoImage(Image.open("fotke\\noc.png").resize((35, 35), Image.ANTIALIAS))

dobrodoslica = ttk.Label(   r, 
                            background=boja, 
                            foreground=slova, 
                            text='',
                            image='',
                            compound=LEFT, 
                            justify=CENTER, 
                            font=('Gulim','11','bold'))

def ispisi_dobrodoslicu():
    if sati <= 8 and sati >= 6:
        dobrodoslica.configure(text='Dobro jutro', image=jutro_img)
    elif sati > 8 and sati <= 18:
        dobrodoslica.configure(text='Pozdrav', image=dan_img)
    else:
        dobrodoslica.configure(text='Ugodnu vecer', image=noc_img)
    dobrodoslica.place(x=20, y=140)
    r.after(1000, ispisi_dobrodoslicu)
ispisi_dobrodoslicu()


#############   TERMOMETAR   #############

if sati > 7 and sati < 19:
    thermo_img = ImageTk.PhotoImage(Image.open("fotke\sensor_icon.png").resize((20, 20), Image.ANTIALIAS))
else:
    thermo_img = ImageTk.PhotoImage(Image.open("fotke\sensor_icon_noc.png").resize((20, 20), Image.ANTIALIAS))

lbl_ocitanje = ttk.Label(   r, 
                            background=boja, 
                            foreground=slova,
                            image=thermo_img, 
                            text='', 
                            justify=CENTER,
                            compound=LEFT, 
                            font=('Gulim','8'))

def pokazi_ocitanje():

    for values in rijecnik_prognoza_hr.values():
        values = rijecnik_prognoza_hr.get('Zagreb-Maksimir')
        try:
            tlak = float(values[8]) - 2
        except:
            if values[8] == '-':
                tlak = 0.0
            else:
                tlak = values[8].strip('*')
        tlak = round(tlak, 1)
        
        
        if int(values[7]) > 50:
            vlaga = int(values[7]) - 10
        else:
            vlaga = values[7]

        if sati < 5:
            temp = 18
        else:
            temp = 22
            
    tekst = f'''{temp}°C  {vlaga}%  {tlak}hPa'''
    lbl_ocitanje.configure(text=tekst)
    lbl_ocitanje.place(x=190, y=145)

    datum = datetime.date.today().strftime('%d. %m. %y.')     
    vrijeme = datetime.datetime.now().strftime('%H:%M')

    database_name = 'vrijeme.db'

    con = sqlite3.connect(database_name)
    cur = con.cursor()

    # try:
    #     cur.execute(f'''INSERT INTO Promjene (datum, vrijeme, temperatura, vlaznost, tlak)
    #                 VALUES ("{datum}", "{vrijeme}", {temp}, {vlaga}, {tlak}) ''')
    #     print(f'Unesena je promjena u bazu: {datum}, {vrijeme}, {temp}, {vlaga}, {tlak}.')
            
    # except sqlite3.Error as error:
    #     print(f"ERROR - Dogodila se greska prilikom pokusaja spajanja na {database_name}:", error)

    try:
        cur.execute(''' SELECT datum, vrijeme, temperatura, vlaznost, tlak 
                        LAST_VALUE FROM Promjene 
                        ORDER BY datum DESC, vrijeme DESC''')
        data = cur.fetchone()

        # print(data[3], vlaga, data [4], tlak)
        # print(data[3] != int(vlaga) or data[4] != tlak)
        try:
            if data[3] != int(vlaga) or data[4] != tlak:
                cur.execute(f'''INSERT INTO Promjene (datum, vrijeme, temperatura, vlaznost, tlak)
                                VALUES ("{datum}", "{vrijeme}", {temp}, {vlaga}, {tlak}) ''')
                print(f'Unesena je promjena u bazu: {datum}, {vrijeme}, {temp}, {vlaga}, {tlak}.')
            
        except sqlite3.Error as error:
            print(f"ERROR - Dogodila se greska prilikom pokusaja spajanja na {database_name}:", error)

    except sqlite3.Error as error:
        print(f"ERROR - Dogodila se greska prilikom pokusaja spajanja na {database_name}:", error)

    con.commit()
    r.after(1000, pokazi_ocitanje)
            
pokazi_ocitanje()

########################################
#############   PODNOZJE   #############

#############   IZBORNIK   #############

def prikazi_izbornik():
    srednji_ekran.grid(row=4,column=0, columnspan=3)
    srednji_ekran.place(x=20, y=180)
    izlaz.configure(state=NORMAL)
    izbornik.configure(state=DISABLED)
    zatvori_kalendar()
    notifikacija.place_forget()
    notifikacija2.place_forget()
    
def izadi_iz_izbornika():
    srednji_ekran.grid_forget()
    srednji_ekran.place_forget()
    izlaz.configure(state=DISABLED)
    izbornik.configure(state=NORMAL)
    zatvori_kalendar()
    gumb_za_povratak.place_forget()
    notifikacija.place(x=20,y=200)
    notifikacija2.place(x=20, y=220)


dno = Frame (r, background=boja)
dno.place(y=480, x=20)

izbornik = Button(  dno, 
                    text='Izbornik', 
                    overrelief='groove', 
                    command=prikazi_izbornik)
izbornik.grid(column=0,row=5)

izlaz = Button(  dno, 
                text='Izlaz', 
                overrelief='groove', 
                command=izadi_iz_izbornika,
                state=DISABLED)
izlaz.grid(column=3,row=5, padx=220)



###############################################
#############   SREDNJI EKRAN   ###############

srednji_ekran = Frame(r, background=ekran, width=310, height=300)

############   NOTIFIKACIJE   ##############

notifikacija = ttk.Label(   r, 
                            text='',
                            image='',
                            compound=RIGHT, 
                            justify=CENTER,
                            background=boja, 
                            foreground=slova, 
                            font=('Verdana','8','bold'))

notifikacija2 = ttk.Label(   r, 
                            text='', 
                            background=boja, 
                            foreground=slova, 
                            font=('Verdana','8'),
                            wraplength=150)


if sati >= 6 and sati <= 19:
    kisobran = ImageTk.PhotoImage(Image.open("fotke\\umbrella.png").resize((20, 20), Image.ANTIALIAS))
else:
    kisobran = ImageTk.PhotoImage(Image.open("fotke\\umbrella_night.png").resize((20, 20), Image.ANTIALIAS))


def pokazi_notifikaciju():
    for values in rijecnik_prognoza_hr.values():
        #print(values)
        values = rijecnik_prognoza_hr.get('Zagreb-Maksimir')
        if values[11] == 'kiša' or values[11] == 'slaba kiša':
            notifikacija.configure(text='Ne zaboravi kisobran.', image=kisobran)
        elif round(float(values[6])) <= 0 or values[11] == 'slab snijeg':
            notifikacija.configure(text='Odmrznuti auto.')
        elif values[11] == 'jak snijeg':
            notifikacija.configure(text='Pripremi se na jaki snijeg.')
        elif values[11] == 'potpuno oblačno':
            notifikacija.configure(text='Moguca kisa, ponesi kisobran.', image=kisobran)
        else:
            notifikacija.configure(text='Iskoristi dan!')

        notifikacija.place(x=20, y=200)

pokazi_notifikaciju()

def pokazi_notifikaciju2():
    notifikacija2.place(x=20, y=220)

    for values in rijecnik_prognoza_hr.values():
        #print(values)
        values = rijecnik_prognoza_hr.get('Zagreb-Maksimir')
        if round(float(values[6])) <= 0:
            notifikacija2.configure(text='Smrzavanje! Obuci kapu, sal i rukavice.')
        elif round(float(values[6])) > 0 and round(float(values[6])) <= 12 :
            notifikacija2.configure(text='Vani je zima, obuci zimsku jaknu!')
        elif round(float(values[6])) > 12 and round(float(values[6])) <= 22 :
            notifikacija2.configure(text='Vani je bas proljetno vrijeme, uzmi laganu jaknu.')
        elif round(float(values[6])) > 22:
            notifikacija2.configure(text='Vrijeme je za kratke rukave.')
        else:
            notifikacija2.configure(text='nisam dobar programer!')

pokazi_notifikaciju2()



#############   KALENDAR   ###############

tekst_kalendara= StringVar()
cal = Calendar( srednji_ekran,     
                selectmode = 'day',
                year = sada.year, 
                month = sada.month,
                day = sada.day,
                background=boja,
                foreground=slova,
                bordercolor=boja,
                headersbackground=ekran,
                headersforeground=boja,
                selectbackground=slova,
                selectforeground=boja,
                normalbackground=ekran,
                normalforeground=slova,
                weekendbackground=ekran,
                weekendforeground=slova,
                otherbackground=boja,
                otherforeground=slova,
                othermonthforeground=ekran,
                othermonthbackground=boja,
                othermonthweforeground=ekran,
                othermonthwebackground=boja,
                tooltipforeground=boja,
                relief='flat')


kalendar_gumb = Button(  
    srednji_ekran, 
    text='Kalendar', 
    command= lambda: prikazi_kalendar())
kalendar_gumb.place(x=10, y=265)

zatvori = Button(  
    srednji_ekran, 
    text='Zatvori', 
    command= lambda: zatvori_kalendar())

prikaz_dana = Button(  
    srednji_ekran, 
    text='Prikazi', 
    command= lambda: prikazi_dan(cal.get_date()))

gumb_za_povratak = Button(  
    srednji_ekran, 
    text='Povratak', 
    command= lambda: prikazi_kalendar())

dnevna_lista = Listbox (srednji_ekran, background=boja,foreground=slova, listvariable='', relief="flat",selectbackground=slova, selectforeground=boja)
ispis_dogadaja = Label (srednji_ekran, text ='', background=ekran, foreground=slova, justify='left', wraplength=120)

def odabir_dnevne_liste(selected):
    database_name = 'event.db'
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    for i in dnevna_lista.curselection():
        selected = dnevna_lista.get(i)
        print(selected)
        
    with con:
        try:
            cur.execute(f'''SELECT * FROM Planer
                            WHERE naslov=? 
                            ORDER BY vrijeme ASC''', (selected[1],))
            data = cur.fetchall()
            #print(data)
            for d in data:
                if d[3] != 'DA':
                    dogadaj = f'\n{d[2]} - {d[4]}\n\n{d[5]}'
                else:
                    dogadaj = f'\nCijeli dan - {d[4]}\n\n{d[5]}'
            ispis_dogadaja.configure(text=dogadaj)
        except:
            ispis_dogadaja.configure(text='\nLista je prazna!')
        
    con.commit()
    

    # database_name = 'event.db'
    # con = sqlite3.connect(database_name)
    # cur = con.cursor()
    # selected = dnevna_lista.get(ACTIVE)
    # #dtm = cal.get_date()
    # # print(selected)
        
    # with con:
    #     try:
    #         cur.execute(f'''SELECT * FROM Planer WHERE
    #                         vrijeme = ? AND
    #                         naslov = ? 
    #                         ORDER BY vrijeme ASC''', (selected[0], selected[1],))
    #         data = cur.fetchall()
    #         print(data)
    #         for d in data:
    #             print(d[3] != 'DA')
    #             print(d[3], 'DA')
    #             if d[3] != 'DA':
    #                 dogadaj = f'\n{d[2]} - {d[4]}\n\n{d[5]}'
    #             else:
    #                 dogadaj = f'\nCijeli dan - {d[4]}\n\n{d[5]}'
    #         ispis_dogadaja.configure(text=dogadaj)
    #     except:
    #         ispis_dogadaja.configure(text='\nLista je prazna!')
        
    # con.commit()

dnevna_lista.bind('<<ListboxSelect>>', odabir_dnevne_liste)

def prikazi_kalendar():
    cal.place(x=10, y=30)
    kalendar_gumb.place_forget()
    zatvori.place(x=10, y=265)
    gumb_za_povratak.place_forget()
    obveze.configure(text='Kalendar', font=('Sans','10','bold'))
    prikaz_dana.place(x=10, y=220)
    gumb_spremi_event.place_forget()
    zaboravi_dodavanje_eventa()
    zaboravi_sve()
    gumb_dodaj_event.place(x=60, y=220)
    cal.selection_set(datetime.datetime.today().date())
    notifikacija.place_forget()
    notifikacija2.place_forget()

def zatvori_kalendar():
    kalendar_gumb.place(x=10, y=265)
    cal.place_forget()
    zatvori.place_forget()
    prikazivanje_obveza()
    kalendar_gumb.configure(text='Kalendar')
    prikaz_dana.place_forget()
    gumb_dodaj_event.place_forget()
    gumb_brisi_event.place_forget()
    zaboravi_dodavanje_eventa()
    zaboravi_sve()


def prikazi_dan(selected):
    zatvori_kalendar()
    kalendar_gumb.place_forget()
    obveze.configure(text=f'Dnevni planer: {cal.get_date()}', font=('Sans','10','bold'))
    gumb_za_povratak.place(x=10, y=265)
    gumb_dodaj_event.place(x=70, y=265)
    gumb_brisi_event.place(x=115, y=265)
    
    database_name = 'event.db'

    con = sqlite3.connect(database_name)
    cur = con.cursor()
    selected = cal.get_date()

    with con:
        cur.execute(f'''SELECT vrijeme, naslov FROM Planer 
                        WHERE datum = ? 
                        ORDER BY vrijeme ASC, naslov ASC''', (selected,))
        data = cur.fetchall()
        print(data)
        for d in data: 
            dnevna_lista.insert(END, d)

    con.commit()
    dnevna_lista.place(x=10, y=50)
    ispis_dogadaja.place(x=150, y=30)


##############   GLASNOCA   ##############

var = IntVar()
razina_glasnoce = var.set(32)
zvuk = f'Zvuk: {var.get()}%'
lbl_glasnoca = Label (srednji_ekran, background=ekran, foreground=slova, text=zvuk)


def ispis_stanja_glasnoce(event):
    lbl_glasnoca.place(x= 240, y= 240)

def obrisi_ispis_stanja_glsn(event):
    lbl_glasnoca.place_forget()


def regulacija_glasnoce(event):
    zvuk = f'Zvuk: {var.get()}%'
    lbl_glasnoca.configure(text=zvuk)
   
def prikazivanje_glasnoce():
    klizac.place(x=260, y=30)
    ispis.place(x=280, y=240)
    gumb_glasnoca.place_forget()
    gumb_zatvori_glasnocu.place(x=250, y=265)

gumb_glasnoca = Button(  
    srednji_ekran, 
    text='Glasnoca', 
    command= prikazivanje_glasnoce)
gumb_glasnoca.place(x=240, y=265)
gumb_glasnoca.bind('<Enter>', ispis_stanja_glasnoce)
gumb_glasnoca.bind('<Leave>', obrisi_ispis_stanja_glsn)


gumb_zatvori_glasnocu = Button(  
    srednji_ekran, 
    text='Zatvori', 
    command= lambda: zatvori_glasnocu())

klizac = Scale( srednji_ekran, 
                length=200, 
                width=10, 
                showvalue=False,
                from_=100, to=0,
                tickinterval=25,
                orient=VERTICAL, 
                highlightbackground=ekran,
                variable=var,
                background=ekran,
                foreground=slova,
                highlightcolor=boja,
                troughcolor=boja,
                sliderrelief='flat',
                activebackground=ekran,
                command=regulacija_glasnoce)

ispis = Entry(  srednji_ekran, 
                width=3, 
                state=DISABLED,
                textvariable=var, 
                justify=CENTER, 
                disabledforeground=slova,
                disabledbackground=boja,
                background=boja,
                foreground=slova,
                relief='flat')


def zatvori_glasnocu():
    gumb_zatvori_glasnocu.place_forget()
    gumb_glasnoca.place(x=240, y=265)
    klizac.place_forget()
    ispis.place_forget()


##########     DODAVANJE EVENTA    #############

gumb_dodaj_event = Button(  
    srednji_ekran, 
    text='Dodaj', 
    command= lambda: dodavanje_eventa())

def brisanje_eventa():
    database_name = 'event.db'
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    selected = dnevna_lista.get(ACTIVE)
    dtm = cal.get_date()
    # print(selected)
    # print(dtm)

    with con:
        try:
            cur.execute(f'''DELETE FROM Planer WHERE 
                            datum = ? AND
                            vrijeme = ? AND
                            naslov = ?''', (dtm, selected[0], selected[1],))
            tekst = '\nUspjesno ste obrisali dogadaj.'
            dnevna_lista.delete(ACTIVE)
        except:
            tekst = '\nZa brisanje molimo odaberite dogadaj.'

    con.commit()
    
    ispis_dogadaja.configure(text=tekst)
    


gumb_brisi_event = Button(  
    srednji_ekran, 
    text='Brisi', 
    command= brisanje_eventa)

gumb_spremi_event = Button(  
    srednji_ekran, 
    text='Spremi', 
    command= lambda: spremanje_eventa())

label_dogadaj_naslov = Label (
    srednji_ekran, 
    relief=FLAT, 
    background=ekran, 
    foreground=slova,
    text='Naslov')

entri_dogadaj_naslov = Entry(
    srednji_ekran, 
    relief=FLAT, 
    background=boja, 
    foreground=slova,
    width=27)

label_dogadaj = Label (
    srednji_ekran, 
    relief=FLAT, 
    background=ekran, 
    foreground=slova,
    text='Dogadaj'
)
entri_dogadaj = Text(
    srednji_ekran, 
    relief=FLAT, 
    background=boja, 
    foreground=slova,
    width=20,
    height=5)

minute = datetime.datetime.now().minute

label_vrijeme = Label (
    srednji_ekran, 
    relief=FLAT, 
    background=ekran, 
    foreground=slova,
    text='Vrijeme'
)

sat_str = StringVar(srednji_ekran, sati)
min_str = StringVar(srednji_ekran, minute)

sat = Spinbox(srednji_ekran, textvariable=sat_str, from_=0,to=23,wrap=True,width=3 ,state="readonly", format="%02.0f",
                background=boja,
                foreground=slova,
                selectbackground=ekran,
                activebackground=boja,
                insertbackground=boja, 
                disabledbackground=boja,
                disabledforeground=boja,
                buttonbackground=ekran,
                buttonuprelief='flat',
                buttondownrelief='flat',
                relief='flat')

min = Spinbox(srednji_ekran, 
                textvariable=min_str, 
                from_=0,to=59,
                wrap=True,
                width=3,
                state="readonly", 
                format="%02.0f",
                background=boja,
                activebackground=boja,
                insertbackground=boja,
                selectbackground=ekran, 
                foreground=slova,
                disabledbackground=boja,
                disabledforeground=boja,
                buttonbackground=ekran,
                buttonuprelief='flat',
                buttondownrelief='flat',
                relief='flat')

cal_entry = DateEntry(
    srednji_ekran,
    selectmode='day',
    day = sada.day,
    month = sada.month,
    year = sada.year,
    background=boja,
    foreground=slova,
    bordercolor=boja,
    headersbackground=ekran,
    headersforeground=boja,
    selectbackground=slova,
    selectforeground=boja,
    normalbackground=ekran,
    normalforeground=slova,
    weekendbackground=ekran,
    weekendforeground=slova,
    otherbackground=boja,
    otherforeground=slova,
    othermonthforeground=ekran,
    othermonthbackground=boja,
    othermonthweforeground=ekran,
    othermonthwebackground=boja,
    tooltipforeground=boja,
    relief='flat')

def odaberi_cijeli_dan():
    #print(ck_var.get())
    if ck_var.get() != 'DA':
        sat.configure(state=NORMAL, textvariable=sat_str)
        min.configure(state=NORMAL, textvariable=min_str)

    else:
        var_s = StringVar(r)
        var_m = StringVar(r)
        var_s.set('00')
        var_m.set('00')
        sat.configure(state=DISABLED, textvariable=var_s)
        min.configure(state=DISABLED, textvariable=var_m)


ck_var = StringVar()

cijeli_dan = Checkbutton(
    srednji_ekran,
    text= 'Cijeli dan',
    background=ekran,
    foreground=slova,
    variable= ck_var,
    state = NORMAL,
    onvalue='DA',
    offvalue='NE',
    activebackground=ekran,
    activeforeground=boja,
    selectcolor=boja,
    command=odaberi_cijeli_dan)
cijeli_dan.deselect()

odaberi_cijeli_dan()

def dodavanje_eventa():
    zatvori_kalendar()
    kalendar_gumb.place_forget()
    obveze.configure(text=f'Stvori novi dogadaj: ', font=('Sans','10','bold'))
    cal_entry.place(x=150, y=10)
    cal_entry.set_date(cal.get_date())
    cijeli_dan.place(x=10, y=165)
    prikaz_dana.place(x=10, y=265)
    prikaz_dana.configure(text='Povratak')
    gumb_za_povratak.place_forget()
    gumb_spremi_event.place(x=70, y=265)
    entri_dogadaj_naslov.place(x=70, y=44)
    label_dogadaj_naslov.place(x=10, y=40)
    label_dogadaj.place(x=10, y=70)
    entri_dogadaj.place(x=70, y=73)
    label_vrijeme.place(x=10, y= 200)
    sat.place(x=70,y=200)
    min.place(x=110,y=200)
    ispis_dogadaja.place_forget()

def zaboravi_sve():
    gumb_dodaj_event.place_forget()
    gumb_brisi_event.place_forget()
    entri_dogadaj.place_forget()
    label_dogadaj_naslov.place_forget()
    entri_dogadaj_naslov.place_forget()
    label_dogadaj.place_forget()
    entri_dogadaj.place_forget()
    label_vrijeme.place_forget()
    sat.place_forget()
    min.place_forget()
    ispis_dogadaja.place_forget()
    dnevna_lista.place_forget()
    dnevna_lista.delete(0, END)
    gumb_za_povratak.place_forget()
    kalendar_gumb.configure(text='Kalendar')
    ispis_dogadaja.configure(text='')
    entri_dogadaj_naslov.delete(0, 'end')
    entri_dogadaj.delete('1.0', 'end')
    notifikacija.place_forget()
    notifikacija2.place_forget()
    cal_entry.place_forget()
    cijeli_dan.place_forget()

def zaboravi_dodavanje_eventa():
    gumb_spremi_event.place_forget()
    prikaz_dana.configure(text='Pokazi')
    zaboravi_sve()

def spremanje_eventa():
    gumb_dodaj_event.place(x=70, y=265)
    gumb_brisi_event.place(x=115, y=265)
    
    odabir = cal_entry.get_date().strftime('%d. %m. %Y.')

    database_name = 'event.db'

    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    cur.execute(''' SELECT naslov
                    FROM Planer 
                    WHERE datum = ?''', (odabir,))
    data = cur.fetchall()
    print(data)
    for d in data:
        d = d
    with con:
        try:
            if entri_dogadaj_naslov.get() != d[0] and len(ck_var.get()) != 0 and len(entri_dogadaj_naslov.get()) != 0:
                cur.execute(f'''INSERT INTO Planer (datum, vrijeme, dan, naslov, dogadaj)
                            VALUES ("{odabir}", "{sat.get()}:{min.get()}", "{ck_var.get()}", "{entri_dogadaj_naslov.get()}", "{entri_dogadaj.get("1.0",END)}") ''')
                ispis_dogadaja.configure(text='Uspjesno ste pohranili dogadaj.')
                ispis_dogadaja.place(x=150, y=30)
            else:
                if len(entri_dogadaj_naslov.get()) == 0:
                    ispis_dogadaja.configure(justify = LEFT, text='Unesite naslov.', wraplength=240)
                elif entri_dogadaj_naslov.get() == d[0]:
                    ispis_dogadaja.configure(justify = LEFT, text=f'Naslov "{entri_dogadaj_naslov.get()}" vec postoji, unesite novi naslov.', wraplength=240)
                    entri_dogadaj_naslov.delete(0, END)
                    entri_dogadaj_naslov.focus()
                else:
                    ispis_dogadaja.configure(justify = LEFT, text=f'Odaberite vrijeme.', wraplength=240)
                    
                ispis_dogadaja.place(x=10, y=225)
                gumb_brisi_event.place_forget()
                return zaboravi_sve, dodavanje_eventa

        except sqlite3.Error as error:
            print("ERROR - Dogodila se greska prilikom pokusaja spajanja na SQLite:", error)
    con.commit()

    zaboravi_dodavanje_eventa()
    zaboravi_sve()
    prikazi_dan(cal_entry.get_date())
    ispis_dogadaja.configure(text='\nUspjesno ste pohranili dogadaj.', wraplength=130)
    ispis_dogadaja.place(x=150, y=30)

#############   ISPIS PLANOVA ZA DANAS   ###############

obveze = ttk.Label(srednji_ekran, text='Danas nemas planova!', foreground=slova, background=ekran, font=('Sans','9'))
obveze.place(x=10, y=10)
def prikazivanje_obveza():
    database_name = 'event.db'

    con = sqlite3.connect(database_name)
    cur = con.cursor()
    cur.execute(''' SELECT datum, naslov, vrijeme, dan, dogadaj FROM Planer ORDER BY vrijeme ASC, naslov ASC''')
    lst_data = []
    data = cur.fetchall()
    for d in data:
        datum_str = d[0]
        datum = datetime.datetime.strptime(datum_str,'%d. %m. %Y.')
        vrijeme_str= d[2]
        vrijeme = datetime.datetime.strptime(vrijeme_str, '%H:%M')
        cal.calevent_create(datum.date(), d[1])
        #print(datetime.datetime.today().date() != datum.date() and datetime.datetime.today().hour >= vrijeme.hour)
 
        if datetime.datetime.today().date() == datum.date():
            if d[3] != 'DA' and datetime.datetime.today().hour <= vrijeme.hour:
                obveze_poruka = f'{d[2]} - {d[1]}:\n{d[4]}'
                lst_data.append(obveze_poruka)
                tekst = "\n".join(lst_data)
                obveze.configure(text=f'DANAS:\n\n{tekst}', wraplength=250, font=('Sans','9'))
            elif d[3] == 'DA':
                obveze_poruka = f'Cijeli dan - {d[1]}:\n{d[4]}'
                lst_data.append(obveze_poruka)
                tekst = "\n".join(lst_data)
                obveze.configure(text=f'DANAS:\n\n{tekst}', wraplength=250, font=('Sans','9'))

            else:
                obveze.configure(text='Danas nemas planove.', font=('Sans','9'))
    con.commit()

################   STIL GUMBA   ###################

lista_gumba = [gumb_brisi_event, gumb_spremi_event, izbornik, izlaz, kalendar_gumb,zatvori, prikaz_dana, gumb_za_povratak, gumb_glasnoca, gumb_zatvori_glasnocu, gumb_dodaj_event]

def style_button_configure(gumb):
    gumb.configure(
                overrelief='groove', 
                bg=boja, 
                activebackground=boja,
                disabledforeground=boja, 
                foreground=slova, 
                relief='flat',
                activeforeground=slova)

for i in lista_gumba:
    style_button_configure(i)

#####################################################
#############   POKRETANJE PROGRAMA   ###############

r.mainloop()

