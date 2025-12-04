"""Modul som innehåller kod för grafiskt användargränssnitt."""
import tkinter as tk
from tkinter import messagebox

class GUI:
    """GUI för periodiska systemet huvudfil."""
    def __init__(self, huvud, system):
        self.huvud = huvud # Självaste root fönstret
        self.system = system #Där all logik ligger kommer vara periodiska systemet i huuvdfilen
        self.huvud.title("Periodiska systemet") #Titel på fönster
        self.huvud.geometry("800x600") #Storlek på fönster

        #Default värden ifall något går fel.
        self.atom = "Väte"
        self.fråga = "Vilken atomnummer har Väte?"
        self.korrekt = 1
        self.datatyp = int
        self.försök = 1
        self.max_försök = 3
        self.sak_att_gissa = 0

        #Väljer en slumpad atom
        self.aktuell_atom = self.system.slumpa_atom()

        self.feedback = 0
        self.grid_frame = 0
        self.början = 0

        self.huvudmeny() #startar huvudmenyn

    def huvudmeny(self):
        """Skapar huvudmenyn för gui."""
        self.töm() #Tömmer allt på skärmen

        #Skapar titeln för menyn
        tk.Label(self.huvud,text="Meny", font=("Arial",26)).pack(pady=25)

        #Lista med knappar, lambda för att kalla funktion med paramterar som knapp
        knappar = [
            ("Visa alla atomer", self.visa_atomer),
            ("Träna på atomnummer (3 försök)", lambda: self.börja_träning("atomnummer")),
            ("Träna på atombeteckning (3 försök)", lambda: self.börja_träning("atombeteckning")),
            ("Träna på atomnamn (3 försök)", lambda: self.börja_träning("atomnamn")),
            ("Träna på atomvikt (3 försök)", lambda: self.börja_träning("atomvikt")),
            ("Gissa atom (3 alternativ)", self.gissa_atom_gui),
            ("Periodiska systemet-pussel", self.start_pussel),
            ("Avsluta", self.huvud.quit)
        ]

        #Skapa och "packa" varje knapp i fönstret skapar knappar utifrån listan
        for text,cmd in knappar:
            tk.Button(self.huvud,text=text,width=30,height=2,command=cmd).pack(pady=5)

    def töm(self):
        """Tar bort allt från huvudfönstret."""
        for fönster in self.huvud.winfo_children():
            fönster.destroy()

    def visa_atomer(self):
        """Visar alla atomer i textfält."""
        self.töm()
        #Skapa rubrik
        tk.Label(self.huvud,text="Alla atomer", font=("Arial",20)).pack(pady=10)

        #Skapar ett textfält där alla atomer visas
        t = tk.Text(self.huvud,width=60,height=22)
        t.pack()

        #Hämta alla atomer från systemet och lägg till i ett textfält.
        for rad in self.system.lista_atomer():
            t.insert(tk.END, rad + "\n")

        #Skapar knapp som går tillbaka till huvudmenyn (kallar funktionen)
        tk.Button(self.huvud,text="Tillbaka",command=self.huvudmeny).pack(pady=20)

    def börja_träning(self, sak_att_gissa):
        """Börjar träningsmomentet för ett attribut, tar emot användarens gissning."""
        self.töm()

        #Hämtar slumpad atom och frågedata från systemet
        frågdata = self.system.användare_gissar_gui(sak_att_gissa)

        #Spara informationen som instansvariablar
        self.atom = frågdata["atom"]
        self.fråga = frågdata["fråga"]
        self.korrekt = frågdata["korrekt"]
        self.datatyp = frågdata["datatyp"]
        self.sak_att_gissa = sak_att_gissa

        #Skapa rubrik
        tk.Label(self.huvud,text=f"Träna på {sak_att_gissa}",font=("Arial",20)).pack(pady=10)
        #Visar frågan
        tk.Label(self.huvud,text=self.fråga,font=("Arial",16)).pack(pady=15)

        #Skapa inmatningfält
        self.början = tk.Entry(self.huvud, font=("Arial",16))
        self.början.pack(pady=10)

        #Skapa knapp för att ta emot användarens gissning
        tk.Button(self.huvud,text="Gissa",command=self.kolla_träning).pack(pady=5)
        #Knapp för tillbaka till menyn
        tk.Button(self.huvud,text="Tillbaka",command=self.huvudmeny).pack(pady=5)

        #Skapa en liten text under knapparna om det är rätt eller fel
        self.feedback = tk.Label(self.huvud,text="",font=("Arial",14))
        self.feedback.pack(pady=20)

    def kolla_träning(self):
        """Kontrollerar användarens gissning i träningsmomentet."""
        #Hämtar inmatning från Entry från metod börja_träning
        svar = self.början.get()

        #Försök konvertera svaret till rätt datatyp
        try:
            svar = self.datatyp(svar)
        except ValueError:
            self.feedback.config(text="Felaktigt värde.")
            return

        #Kolla om svaret är korrekt
        if svar == self.korrekt:
            self.feedback.config(text="Korrekt!")
            #Vänta en stund och starta om träningen med en ny slumpad atom
            self.huvud.after(1200, lambda: self.börja_träning(self.sak_att_gissa))
            return

        #Om svaret är fel
        self.feedback.config(text=f"Fel! {self.försök}/3")
        self.försök += 1

        #Om användaren har nått max antal försök
        if self.försök > self.max_försök:
            self.feedback.config(text=f"Slut på försök. Rätt svar var: {self.korrekt}")
            #Vänta 2 sekunder och starta om med ny slumpad atom
            self.huvud.after(2000, lambda: self.börja_träning(self.sak_att_gissa))

    def gissa_atom_gui(self):
        """Visar en gui fråga gui fråga där användaren ska gissa rätt bland tre alternativ."""
        self.töm()

        #Hämta slumpade atomer och rätt atom från systemet
        data = self.system.gissa_atom_gui()
        rätt_atom = data["rätt_atom"]   
        alternativen = data["alternativ"]

        #Visa frågan som rubrik
        tk.Label(self.huvud,text=f"Vilken atom är {rätt_atom.atombeteckning}?",font=("Arial",20)).pack(pady=20)

        #Skapa knappar för varje alternativ
        for i, atom in enumerate(alternativen):
            #Lambda för att inte den ska köras direkt utan istället när knappen trycks
            tk.Button(self.huvud,text=f"{i+1}. {atom.atomnamn}", width=25,command=lambda a=atom:self.kolla_3val(a,rätt_atom)).pack(pady=5)

        #Feedback (rätt/fel)
        self.feedback = tk.Label(self.huvud,text="",font=("Arial",15))
        self.feedback.pack(pady=15)

        #Knapp för att gå tillbaka
        tk.Button(self.huvud,text="Tillbaka",command=self.huvudmeny).pack(pady=5)

    def kolla_3val(self,gissad,korrekt):
        """Kontrollerar användarens gissning när det är 3 alternativ."""
        #Kollar om gissningen är korrekt
        if gissad == korrekt:
            #Uppdatera feedback med korrekt som meddelande
            self.feedback.config(text="Korrekt!")
        else:
            #Om fel säga vad som var rätt
            self.feedback.config(text=f"Fel! Rätt svar: {korrekt.atomnamn}")

    def start_pussel(self):
        """Startar gui versionen av periodiska systemet spelet"""
        self.töm()

        #Titel 
        tk.Label(self.huvud,text="Periodiska Systemet-pussel",font=("Arial",20)).pack(pady=15)


        #Skapa en ram för knapparna som ska representera periodiska systemet
        tk.Label(self.huvud,text=f"Placera atom: {self.aktuell_atom.atomnamn} ({self.aktuell_atom.atombeteckning})",font=("Arial", 16)).pack(pady=5)
        self.grid_frame = tk.Frame(self.huvud)
        self.grid_frame.pack(pady=15)

        #Skapa ett 10x18 rutnät
        for r in range(1, 11):
            for k in range(1, 19):
                #Lambda används för att knappen ska fungera som den ska
                btn = tk.Button(self.grid_frame, text=f"{r},{k}",
                                width=4, height=2,
                                command=lambda rr=r, cc=k: self.kolla_pussel(rr, cc))
                #Placera knappen i rutnätet
                btn.grid(row=r, column=k) 

        #Tillbaka knapp
        tk.Button(self.huvud, text="Tillbaka", command=self.huvudmeny).pack(pady=20)

    def kolla_pussel(self, rad, kolumn):
        """Kontrollerar om användaren har placerat den aktuella atomen på rätt plats."""
        rätt_r = self.aktuell_atom.rad
        rätt_k = self.aktuell_atom.kolumn

        #Om användaren klickade rätt
        if rad == rätt_r and kolumn == rätt_k:
            #Visa informationsruta med korrektmeddelande med  messagebox
            messagebox.showinfo("Rätt!", f"Korrekt! {self.aktuell_atom.atomnamn} ligger i rad {rätt_r}, kolumn {rätt_k}.")
            #Starta pusslet igen med en ny atom
            self.start_pussel()
        else:
            #Visar felmeddelande och sen rätt plats
            messagebox.showerror("Fel", f"Fel plats!\nRätt var rad {rätt_r}, kolumn {rätt_k}.")