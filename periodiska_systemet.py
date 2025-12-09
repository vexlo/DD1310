import tkinter as tk
import os
import random
import urllib.request

class Atom:
    """Klass som definerar vad en atom är."""
    def __init__(self, atombeteckning, atomnamn, atomvikt, atomnummer, rad, kolumn):
        self.atomnamn = atomnamn
        self.atomvikt = atomvikt
        self.atomnummer = atomnummer
        self.atombeteckning = atombeteckning
        self.kolumn = kolumn
        self.rad = rad

    def __str__(self):
        return f"{self.atomnummer}: {self.atomnamn} {self.atomvikt}: {self.atombeteckning}" 
        # För att definera hur atom klassen ska representeras i text.

class Periodiska_systemet:
    """Klassen som all väsentlig kod ligger i. Gör koden mer modulär än att ha allt i funktioner.
       Upplägget av klassen är följande: Globala, text och GUI metoder. 
    """
    def __init__(self):
        self.atomer = {} # Dict för att göra filinläsning enklare.

        self.RADER = 10 # Rader i periodiska systemet
        self.KOLUMNER = 18 # Kolumner i periodiska systemet
        self.tomt_system = [[" " for _ in range(self.KOLUMNER)] for _ in range(self.RADER)]

    def läsa_in_atomer_från_fil(self,filnamn):
        """Läser in atomer från en egen skapad fil, 'atom_sammanfogad.txt'"""
        with open(filnamn, "r", encoding="UTF-8") as f: #UTF för att tillåta svenska bokstäver
            for rad in f:
                delar = rad.strip().split()  #Ta bort radbrytning och dela upp raden i delar
                if len(delar) < 6: # Kontrollera om det finns tillräckligt mycket på varje rad
                    continue

                #Plockar ut värden från listan i delar
                atombeteckning = delar[0]
                atomnamn = delar[1]
                atomvikt = float(delar[2])
                atomnummer = int(delar[3])
                atomrad = int(delar[4])
                atomkolumn = int(delar[-1])

                #Skapar ett Atom-objekt
                self.atomer[atomnummer] = Atom(atombeteckning,atomnamn,atomvikt,atomnummer,atomrad,atomkolumn)

    def lista_atomer(self):
        """Lista ut alla atomer i ordning (båda för gui och text)"""
        resultat = []
        for atomnummer in sorted(self.atomer.keys()): #Sorterar en lista av nycklarna i dictonaryn
            atom = self.atomer[atomnummer] #Tar fram själva Atom-objet

            #Sträng med atomens data
            rad = f"{atom.atomnummer}: {atom.atombeteckning} {atom.atomnamn} {atom.atomvikt} {atom.rad} {atom.kolumn}"
            resultat.append(rad) #lägger till strängen i resultatlistan
        return resultat

    def slumpa_atom(self):
        """Slumpar fram atomer från nycklarna i en dictionary."""
         #från random modulen slumpar man från en lista av nycklar i dict atomer
        nyckel = random.choice(list(self.atomer.keys()))
        return self.atomer[nyckel] #Skickar tillbaka den slumpade atomens nyckel eller atomnummer

    def användare_gissar(self, sak_att_gissa, inmatad_datatyp, slumpad_atom):
        """Användaren gissar i text versionen. Med parametrarna sak_att_gissa vilket är vilket attribut
           och inmatad_datatyp vilket är vilken typ av svar som förväntas.
        """
        #slumpad_atom = self.slumpa_atom() #Slumpar atom från metod slumpa atom
        #getattr är en inbyggd funktion som innebär att hämta attributen 'sak_att_gissa'
        #från objektet eftersom att göra slumpad_atom.sak_att_gissa inte fungerar.
        #Hittades från ett google sök
        korrekt_attribut = getattr(slumpad_atom, sak_att_gissa)

        if sak_att_gissa == "atomnamn":
            användar_input = inmatad_datatyp(input(f"Vilket {sak_att_gissa} har: {slumpad_atom.atomnummer}: "))
        else:
            användar_input = inmatad_datatyp(input(f"Vilket {sak_att_gissa} har: {slumpad_atom.atomnamn}: "))

        #isinstance är en inbyggd funktion för att kontrollera vad för typ objektet är.
        if isinstance(användar_input, str) and isinstance(korrekt_attribut, str):
            return användar_input.lower() == korrekt_attribut.lower() #skickar tillbaka en bolean
        else:
            return användar_input == korrekt_attribut

    def träna_text(self, beskrivning, funktion, datatyp, försök_max=3):
        """Metoden är till för att låta användaren träna på något.
           Den existerar endast för att inte kodupprepa.
        """
        försök = 1
        atom_att_gissa = self.slumpa_atom() if "atom" in beskrivning.lower() else None

        while försök <= försök_max:
            #korrekt är funktionen som ges som parameter och sedan beskrivning är
            #vad som ska tränas på. Sedan gör atom slumpningen här så att sammma atom
            #kvarstår att gissa på.
            try:
                if atom_att_gissa:
                    korrekt = funktion(beskrivning, datatyp, atom_att_gissa)
                else:
                    korrekt = funktion(beskrivning,datatyp)
            except (ValueError,IndexError):
                print("Ange giltig input.")
                continue
            if korrekt:
                print("Korrekt.")
                break
            else:
                print(f"Fel, försök: {försök}")
                försök += 1
        self.meny() #sedan återgå till menyn efter alla försök

    def placera_atom(self, atom):
        """Låter användaren placera in atomer i ett tomt periodisk system."""
        #Hämtar korrekt rad och kolumn
        korrekt_rad = atom.rad
        korrekt_kolumn = atom.kolumn

        print(f"Placera atomen {atom.atomnamn} ({atom.atombeteckning}) i periodiska systemet.")

        while True:
            try:
                #Fråga användaren efter rad och kolumn
                användar_rad = int(input(f"Vilken rad (1-{self.RADER})?: "))
                användar_kolumn = int(input(f"Vilken kolumn (1-{self.KOLUMNER})?: "))

                print(f"{korrekt_kolumn} {användar_kolumn}")
                print(f"{korrekt_rad} {användar_rad}")

                #Kontrollera om användaren placerade atomen korrekt
                if användar_rad == korrekt_rad and användar_kolumn == korrekt_kolumn:
                    self.tomt_system[korrekt_rad-1][korrekt_kolumn-1] = atom.atombeteckning
                    print("Rätt plats!")
                    break
                else:
                    print("Fel plats, försök igen.")
            except ValueError:
                print("Mata in giltigt tal.")

    def träna_periodiska_systemet(self):
        """Kallar in metoden placera_atom och visa_periodiskt_system.
           Sedan när varje atom är placerad så skickas ett meddelande till konsolen.
        """

        #En lista med alla atomer skapas sedan blandas ordningen slumpmässigt.
        alla_atomer = list(self.atomer.values())
        random.shuffle(alla_atomer)

        for atom in alla_atomer: #Loopar igenom varenda atom
            #Visar nuvarande periodiskt system
            self.visa_periodiskt_system()
            #kallar metoden för att placera in i systemet med slumpade atomen
            self.placera_atom(atom)

        print("Du har fyllt periodiska systemet korrekt!")

    def visa_periodiskt_system(self):
        """Ritar upp ett periodiskt system."""
        print("\nPeriodiska systemet (tomt):")
        #For loop för varje rad i variablen tomt_system uppbygt från RADER och KOLUMNER
        for rad in self.tomt_system:
            print(" | ".join(rad)) #Skriver upp varje rad snyggt formaterad
        print("\n")

    def gissa_atom_text(self,max_försök=2):
        """Metod för att låta användaren gissa mellan 3 atomer utifrån beteckning."""

        #Slumpar tre atomer
        slumpade_atomer = [self.slumpa_atom(), self.slumpa_atom(),self.slumpa_atom()]
        #väljer en av atomerna som rätt svar
        rätt_atom = random.choice(slumpade_atomer)
        print(f"Vilken atomvikt har: {rätt_atom.atomnamn}\n1. {slumpade_atomer[0].atomvikt}\n2. {slumpade_atomer[1].atomvikt}\n3. {slumpade_atomer[2].atomvikt}")
        försök = 1

        #Loopar tills rätt svar eller max antal försök nås
        while försök <= max_försök:
            användarsvar = input("Vad är din gissning? ")
            try:
                #Kontrollera om användaren angav 1,2,3 och om de är rätt
                if slumpade_atomer[int(användarsvar)-1] == rätt_atom:
                    print("Korrekt!")
                    break
                else:
                    print(f"Fel, försök: {försök}.")
                    försök += 1
            except (ValueError,IndexError): #Fångar upp ogiltiga input
                print("Felaktigt värde, mata in siffra.")


    def användare_gissar_gui(self, sak_att_gissa):
        """Förbereder en gissningsfråga för GUI för en given atom."""
        atom = self.slumpa_atom()

        #Får ut rätt attribut från Atom objektet
        korrekt_attribut = getattr(atom, sak_att_gissa)

        #Bestäm datatyp och fråga beroende på vilken attribut som ska gissa på
        if sak_att_gissa == "atomnummer":
            datatyp = int
            fråga = f"Vilket {sak_att_gissa} har {atom.atomnamn}?"
        elif sak_att_gissa == "atomvikt":
            datatyp = float
            fråga = f"Vilken {sak_att_gissa} har {atom.atomnamn}?"
        else:
            datatyp = str
            if sak_att_gissa == "atomnamn":
                #Om användaren tränar på atomnamn används atomnummer som ledtråd.
                fråga = f"Vilket {sak_att_gissa} har atomnummer {atom.atomnummer}?"
            else:
                fråga = f"Vilket {sak_att_gissa} har {atom.atomnamn}?"

        #Skicka tillbaka all relevant info som GUI behöver för att visa och kontrollera svar
        return {"atom": atom, "fråga": fråga, "korrekt": korrekt_attribut, "datatyp": datatyp}

    def gissa_atom_gui(self):
        """Förbereder en gui version av att gissa atom."""
        #Slumpar tre olika atomer
        slumpade_atomer = [self.slumpa_atom(), self.slumpa_atom(), self.slumpa_atom()]
        #Väljer en av dom som rätt
        rätt_atom = random.choice(slumpade_atomer)

        #Returnerar både rätt och alla alternativ till GUI
        return {"rätt_atom": rätt_atom, "alternativ": slumpade_atomer}

    def träna_gui(self, beskrivning, funktion, datatyp, försök_max=3):
        """Träningsfunktion för gui-version."""
        resultat = []
        försök = 1 

        while försök <= försök_max:
            #Om datatyp är None eller False kommer den inte skicka en datatyp till en funktion som inte har det
            korrekt = funktion(beskrivning, datatyp) if datatyp else funktion()
            if korrekt:
                resultat.append({"försök": försök, "status": "Korrekt"})
                break
            else:
                resultat.append({"försök": försök, "status": "Fel"})
                försök += 1
        return resultat


    def meny(self):
        """Huvudmenyn för text versionen av programmet."""

        #Ritar upp en meny enligt instruktionerna
        print("-"*14 + " Meny " + "-"*15)
        print(
            "1. Visa alla atomer\n"
            "2. Träna på atomnummer\n"
            "3. Träna på atombeteckningar\n"
            "4. Träna på atomnamn\n"
            "5. Träna på atomvikter\n"
            "6. Gissa på 3 atomer\n"
            "7. Träna på kollumn och rad\n"
            "8. Sluta"
        )
        print("-"*35)

        #Användarens input
        användar_input = input("Vad vill du göra?: ")

        #match/case istället för if/elif
        match användar_input:
            case "1":
                #Visar alla atomer, gjort så här så att metoden även fungerar för gui
                for rad in self.lista_atomer():
                    print(rad)
                self.meny()
            case "2":
                #Träna på atomnummer
                self.träna_text("atomnummer", self.användare_gissar, int)
            case "3":
                #Träna på atombeteckning
                self.träna_text("atombeteckning", self.användare_gissar, str)
            case "4":
                #Träna på atomnamn
                self.träna_text("atomnamn", self.användare_gissar, str)
            case "5":
                #Träna på atomvikt
                self.träna_text("atomvikt", self.användare_gissar, float)
            case "6":
                #Gissa rätt utav 3 alternativ
                self.gissa_atom_text()
                self.meny()
            case "7":
                #Träna på att placera atomer i ett periodiskt system
                self.träna_periodiska_systemet()
                self.meny()
            case "8":
                #Avsluta programmet
                print("Hejdå!")
                quit()
            case _:
                #Ogiltig input visar menyn igen.
                print("Välj giltig siffra.")
                self.meny()





def kolla_om_fil_finns(fil,filnamn,url_att_ladda_ner):

    while not os.path.isfile(filnamn):
        print("Fil med atomer hittas inte. Filen laddas ner.")
        urllib.request.urlretrieve(url_att_ladda_ner, fil)
        continue


def main():
    """Huvudfunktionen av programmet."""
    #Här pågrund av cirkulär importering, ingen aning varför det fungerar
    #men det fungerar bara om den ligger här och inte längst upp.
    from periodiska_systemet_gui import GUI

    #Filplats handlar om att hitta den absoluta vägen som python skripten körs i
    #os.path.join sätter ihop filplats och filnamnet 
    #tex C:\dadad\dadadff\ + asf.txt blir till C:\dadad\dadadff\asf.txt
    fil_plats = os.path.dirname(os.path.abspath(__file__))
    FIL = "atom_sammanfogad.txt"
    filnamn = os.path.join(fil_plats, FIL)


    #Skapar ett system objekt av klassen Periodiska_systemet sen kallar en metod därifrån
    systemet = Periodiska_systemet()
    systemet.läsa_in_atomer_från_fil(filnamn)

    #För att ge användaren ett val till gui eller text
    text_eller_gui = input("Gui (1) eller text (2): ")
    #Endast 1 eller 2 kommer göra något.
    while text_eller_gui not in ("1","2"):
        text_eller_gui = input("1 eller 2: ")

    match text_eller_gui:
        case "1":
            #Skapar huvudfönstret
            grund = tk.Tk()
            #Skapar instans av GUI från modulen GUI
            GUI(grund, systemet)
            #Gör att fönstret reagerar på användarens handlingar
            grund.mainloop()
        case "2":
            #Kallar på huvudmenyn
            systemet.meny()

#Så att andra py skripter inte kör igång main funktionen utan körs bara om den här koden körs
#som huvud.
if __name__ == "__main__":
    main()
