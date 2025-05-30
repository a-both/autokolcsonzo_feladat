from abc import ABC, abstractmethod
from datetime import date, timedelta

class Felhasznalo:
    def __init__(self, nev):
        self.nev = nev

    def __str__(self):
        return self.nev

class Auto(ABC):
    def __init__(self, rendszam, tipus, berleti_dij):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def __str__(self):
        pass

class Szemelyauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, ajtok_szama):
        super().__init__(rendszam, tipus, berleti_dij)
        self.ajtok_szama = ajtok_szama

    def __str__(self):
        return f"Személyautó | Rendszám: {self.rendszam}, Típus: {self.tipus}, Díj: {self.berleti_dij} Ft/nap, Ajtók: {self.ajtok_szama}"

class Teherauto(Auto):
    def __init__(self, rendszam, tipus, berleti_dij, teherbiras):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def __str__(self):
        return f"Teherautó   | Rendszám: {self.rendszam}, Típus: {self.tipus}, Díj: {self.berleti_dij} Ft/nap, Teherbírás: {self.teherbiras} kg"

class Berles:
    def __init__(self, auto, kezdo_datum, leadasi_datum, felhasznalo): 
        self.auto = auto
        self.kezdo_datum = kezdo_datum
        self.leadasi_datum = leadasi_datum 
        self.felhasznalo = felhasznalo

    def napok_szama(self):
        return (self.leadasi_datum - self.kezdo_datum).days + 1 

    def osszeg_ar(self):
        return self.auto.berleti_dij * self.napok_szama()

    def __str__(self):
        return (f"Bérlő: {self.felhasznalo.nev} | Rendszám: {self.auto.rendszam} | "
                f"Időszak: {self.kezdo_datum} - {self.leadasi_datum} ({self.napok_szama()} nap) | " 
                f"Teljes ár: {self.osszeg_ar()} Ft")

class Autokolcsonzo:
    def __init__(self, nev):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadas(self, auto):
        self.autok.append(auto)

    def auto_berlese(self, rendszam, kezdo_datum, leadasi_datum, felhasznalo, silent_error=False): 
        if kezdo_datum < date.today():
            if not silent_error:
                print("Hiba: A kezdő dátum a múltban van. Kérlek, adj meg jövőbeli dátumot.")
            return False
        
        if leadasi_datum < kezdo_datum: 
            if not silent_error:
                print("Hiba: A leadási dátum nem lehet korábbi, mint a kezdő dátum.")
            return False

        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            if not silent_error:
                print(f"Hiba: A(z) {rendszam} rendszámú autó nem található.")
            return False

        current_date = kezdo_datum
        while current_date <= leadasi_datum:  
            if any(b.auto.rendszam == rendszam and b.kezdo_datum <= current_date <= b.leadasi_datum for b in self.berlesek): 
                if not silent_error:
                    print(f"Hiba: A(z) {rendszam} rendszámú autó már foglalt {current_date} napon!")
                return False
            current_date += timedelta(days=1)

        self.berlesek.append(Berles(auto, kezdo_datum, leadasi_datum, felhasznalo)) 
        print(f"Sikeres bérlés! Bérlő: {felhasznalo.nev}, Rendszám: {rendszam}, Időszak: {kezdo_datum} - {leadasi_datum} ({Berles(auto, kezdo_datum, leadasi_datum, felhasznalo).napok_szama()} nap), Teljes ár: {Berles(auto, kezdo_datum, leadasi_datum, felhasznalo).osszeg_ar()} Ft") 
        return True

    def berles_lemondasa(self, rendszam, kezdo_datum, leadasi_datum): 
        for b in self.berlesek:
            if b.auto.rendszam == rendszam and b.kezdo_datum == kezdo_datum and b.leadasi_datum == leadasi_datum: 
                self.berlesek.remove(b)
                print(f"A bérlés sikeresen le lett mondva: {rendszam} ({kezdo_datum} - {leadasi_datum})") 
                return True
        print(f"Hiba: Nincs ilyen bérlés a rendszerben ({rendszam} - {kezdo_datum} - {leadasi_datum})!")
        return False

    def berlesek_listazasa(self):
        if not self.berlesek:
            print("Jelenleg nincs aktív bérlés.")
        for b in self.berlesek:
            print(b)

    def autok_listazasa(self):
        if not self.autok:
            print("Nincsenek elérhető autók.") 
        else:
            print("\n--- Elérhető autók ---")
            for auto in self.autok:
                print(auto)
            print("----------------------")


def datum_bekerese_idopont():
    print("Add meg a bérlés KEZDŐ dátumát:")
    kezdo_datum = None
    while kezdo_datum is None:
        try:
            ev = int(input("Év (YYYY): "))
            honap = int(input("Hónap (MM): "))
            nap = int(input("Nap (DD): "))
            kezdo_datum = date(ev, honap, nap)
            if kezdo_datum < date.today():
                print("Hiba: A kezdő dátum a múltban van. Kérlek, adj meg jövőbeli dátumot.")
                kezdo_datum = None
        except ValueError:
            print("Hibás dátumformátum! Próbáld újra.")

    print("Add meg a bérlés LEADÁSI dátumát:")
    leadasi_datum = None 
    while leadasi_datum is None: 
        try:
            ev = int(input("Év (YYYY): "))
            honap = int(input("Hónap (MM): "))
            nap = int(input("Nap (DD): "))
            leadasi_datum = date(ev, honap, nap)
            if leadasi_datum < kezdo_datum: 
                print("Hiba: A leadási dátum nem lehet korábbi, mint a kezdő dátum. Próbáld újra.")
                leadasi_datum = None
        except ValueError:
            print("Hibás dátumformátum! Próbáld újra.")
            
    return kezdo_datum, leadasi_datum

def main():
    kolcsonzo = Autokolcsonzo("Autókölcsönző")

    kolcsonzo.auto_hozzaadas(Szemelyauto("ABC-123", "Opel Astra", 9000, 5))
    kolcsonzo.auto_hozzaadas(Szemelyauto("CBA-987", "Ford Focus", 8500, 4))
    kolcsonzo.auto_hozzaadas(Teherauto("QWE-456", "MAN TGL", 15000, 3500))

    print("--- Kezdeti bérlések ---")
    felhasznalo1 = Felhasznalo("Kiss Gábor")
    felhasznalo2 = Felhasznalo("Nagy Anna")
    felhasznalo3 = Felhasznalo("Kovács Péter")
    felhasznalo4 = Felhasznalo("Fehér Réka")

    kolcsonzo.auto_berlese("ABC-123", date(2025, 6, 1), date(2025, 6, 3), felhasznalo1, silent_error=True)
    kolcsonzo.auto_berlese("CBA-987", date(2025, 6, 2), date(2025, 6, 4), felhasznalo2, silent_error=True)
    kolcsonzo.auto_berlese("QWE-456", date(2025, 6, 1), date(2025, 6, 1), felhasznalo4, silent_error=True)
    kolcsonzo.auto_berlese("CBA-987", date(2025, 6, 5), date(2025, 6, 7), felhasznalo3, silent_error=True)
    
    kolcsonzo.auto_berlese("ABC-123", date(2024, 1, 1), date(2024, 1, 3), felhasznalo1, silent_error=True)
    kolcsonzo.auto_berlese("QWE-456", date(2025, 7, 10), date(2025, 7, 8), felhasznalo2, silent_error=True)
    kolcsonzo.auto_berlese("ABC-123", date(2025, 6, 2), date(2025, 6, 4), felhasznalo3, silent_error=True)
    print("-------------------------")

    while True:
        print("\n--- Autókölcsönző menü ---")
        print("1 - Autók listázása")
        print("2 - Autó bérlése")
        print("3 - Bérlés lemondása")
        print("4 - Bérlések listázása")
        print("0 - Kilépés")

        valasztas = input("Választás: ")

        if valasztas == "1":
            kolcsonzo.autok_listazasa()
        elif valasztas == "2":
            kolcsonzo.autok_listazasa()
            
            rendszam = input("Add meg a bérlendő autó rendszámát: ").upper()
            kezdo_datum, leadasi_datum = datum_bekerese_idopont() 
            
            if kezdo_datum and leadasi_datum: 
                berlo_neve = input("Kérlek add meg a nevedet (bérlő): ")
                uj_berlo = Felhasznalo(berlo_neve)
                kolcsonzo.auto_berlese(rendszam, kezdo_datum, leadasi_datum, uj_berlo) 
        elif valasztas == "3":
            rendszam = input("Add meg a lemondandó bérlés rendszámát: ").upper()
            kezdo_datum, leadasi_datum = datum_bekerese_idopont() 
            if kezdo_datum and leadasi_datum: 
                kolcsonzo.berles_lemondasa(rendszam, kezdo_datum, leadasi_datum) 
        elif valasztas == "4":
            kolcsonzo.berlesek_listazasa()
        elif valasztas == "0":
            print("Kilépés a rendszerből..")
            break
        else:
            print("Hibás választás, próbáld újra!")

if __name__ == "__main__":
    main()