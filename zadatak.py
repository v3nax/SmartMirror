'''
Zadatak:
Treba napraviti program kroz koji će se polaznici neke edukacijske ustanove evidentirati unutar
tečaja kojeg upišu. Svaki polaznik neka ima od podataka: ime, prezime, dob, bodove 
(kao neku brojčanu vrijednost od 0-100). Stvoriti klase polaznik i tečaj. 
Unutar klase tečaj napisati metodu za dodavanje polaznika i računanje prosječnog broja bodova  tečaja.
'''
import statistics

class Polaznik():
    def __init__(self, ime, prezime, dob, bodovi) -> None:
        self.ime = ime
        self.prezime = prezime
        self.dob = dob
        self.bodovi = bodovi
        self.polaznik = {}

         
    def polaznici_rijecnik(self):

        self.polaznik = {'Ime' : self.ime, 'Prezime' : self.prezime, 'Dob' :  self.dob, 'Bodovi' : self.bodovi}
        for k,v in self.polaznik.items():
            tekst = f'''{k}: {v}'''
            print(tekst)

polaznik1 = Polaznik('Hugo', 'Kant', '44', 98)
polaznik1.polaznici_rijecnik()
polaznik2 = Polaznik('NTO', 'DJ', '35', 72)
polaznik2.polaznici_rijecnik()

class Tecaj():
  
    def __init__(self) -> None:
        self.lista_bodova = []
        self.prosjek = 0 
        self.polaznik = {}

    def dodaj_polaznika(self, polaznik_ime, polaznik_prezime, bodovi):
        polaznik = polaznik_ime + ' ' + polaznik_prezime
        polaznici_tecaja = {polaznik : bodovi }
        for k,v in polaznici_tecaja.items():
            tekst = f'{k}: {v}'
        print(tekst)

    def izracunaj_projsek(self, bodovi):
        self.lista_bodova.append(bodovi)
        self.prosjek = statistics.mean(self.lista_bodova)
        print(f'Prosjek tečaja je {self.prosjek}')

tecaj = Tecaj()
tecaj.dodaj_polaznika(polaznik1.ime, polaznik1.prezime, polaznik1.bodovi)
tecaj.izracunaj_projsek(polaznik1.bodovi)

tecaj.dodaj_polaznika(polaznik2.ime, polaznik2.prezime, polaznik2.bodovi)
tecaj.izracunaj_projsek(polaznik2.bodovi)


        

