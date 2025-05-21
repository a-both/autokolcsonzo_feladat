from abc import ABC, abstractmethod
from datetime import date, timedelta

class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij_naponta = berleti_dij_naponta

    @abstractmethod
    def ar_szamolasa(self, napok_szama: int) -> float:
        pass

    def __str__(self):
        return f"Rendszám: {self.rendszam}, Típus: {self.tipus}, Napi díj: {self.berleti_dij_naponta:.2f} Ft"

class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float, utas_szam: int):
        super().__init__(rendszam, tipus, berleti_dij_naponta)
        self.utas_szam = utas_szam

    def ar_szamolasa(self, napok_szama: int) -> float:
        return self.berleti_dij_naponta * napok_szama

    def __str__(self):
        return f"{super().__str__()}, Utasok száma: {self.utas_szam}"

class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij_naponta: float, teherbiras_kg: float):
        super().__init__(rendszam, tipus, berleti_dij_naponta)
        self.teherbiras_kg = teherbiras_kg

    def ar_szamolasa(self, napok_szama: int) -> float:
        return self.berleti_dij_naponta * napok_szama

    def __str__(self):
        return f"{super().__str__()}, Teherbírás: {self.teherbiras_kg} kg"

class Berles:
    def __init__(self, auto: Auto, kezdeti_datum: date, napok_szama: int):
        self.auto = auto
        self.kezdeti_datum = kezdeti_datum
        self.veg_datum = kezdeti_datum + timedelta(days=napok_szama - 1)
        self.napok_szama = napok_szama
        self.ar = auto.ar_szamolasa(napok_szama)

    def __str__(self):
        return (f"Bérelt autó: {self.auto.rendszam} ({self.auto.tipus}), "
                f"Kezdés: {self.kezdeti_datum}, Befejezés: {self.veg_datum}, "
                f"Napok száma: {self.napok_szama}, Ár: {self.ar:.2f} Ft")

class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok = []
        self.berlesek = []

    def auto_hozzaadasa(self, auto: Auto):
        self.autok.append(auto)

    def berles_hozzaadasa(self, berles: Berles):
        self.berlesek.append(berles)

    def auto_berlese(self, rendszam: str, kezdeti_datum_str: str, napok_szama: int) -> tuple[bool, str]:
        try:
            kezdeti_datum = date.fromisoformat(kezdeti_datum_str)
            if kezdeti_datum < date.today():
                return False, "A bérlés dátuma nem lehet múltbeli."
        except ValueError:
            return False, "Érvénytelen dátum formátum. Használja az ÉÉÉÉ-HH-NN formátumot."

        valasztott_auto = None
        for auto in self.autok:
            if auto.rendszam == rendszam:
                valasztott_auto = auto
                break

        if not valasztott_auto:
            return False, "Nincs ilyen rendszámú autó a kölcsönzőben."

        uj_berles_veg_datum = kezdeti_datum + timedelta(days=napok_szama - 1)

        for berles in self.berlesek:
            if (berles.auto.rendszam == rendszam and
                max(berles.kezdeti_datum, kezdeti_datum) <= min(berles.veg_datum, uj_berles_veg_datum)):
                return False, f"Az autó már foglalt {berles.kezdeti_datum}-tól {berles.veg_datum}-ig."

        uj_berles = Berles(valasztott_auto, kezdeti_datum, napok_szama)
        self.berlesek.append(uj_berles)
        return True, f"Az autó sikeresen bérelve. Ár: {uj_berles.ar:.2f} Ft"

    def berles_lemondasa(self, rendszam: str, kezdeti_datum_str: str) -> tuple[bool, str]:
        try:
            kezdeti_datum = date.fromisoformat(kezdeti_datum_str)
        except ValueError:
            return False, "Érvénytelen dátum formátum. Használja az ÉÉÉÉ-HH-NN formátumot."

        for i, berles in enumerate(self.berlesek):
            if berles.auto.rendszam == rendszam and berles.kezdeti_datum == kezdeti_datum:
                del self.berlesek[i]
                return True, "A bérlés sikeresen lemondva."
        return False, "Nincs ilyen bérlés a rendszerben (ellenőrizze a rendszámot és a kezdeti dátumot)."

    def berlesek_listazasa(self):
        if not self.berlesek:
            print("Nincsenek aktuális bérlések.")
            return

        print("\n--- Aktuális bérlések ---")
        
        rendezett_berlesek = sorted(self.berlesek, key=lambda b: (b.auto.rendszam, b.kezdeti_datum))
        for i, berles in enumerate(rendezett_berlesek):
            print(f"{i+1}. {berles}")
        print("-------------------------\n")

    def berelheto_autok_listazasa(self):
        berelheto_autok = []
        most = date.today()

        for auto in self.autok:
            foglalt_e = False
            for berles in self.berlesek:
                if (berles.auto.rendszam == auto.rendszam and
                    berles.kezdeti_datum <= most <= berles.veg_datum):
                    foglalt_e = True
                    break
            if not foglalt_e:
                berelheto_autok.append(auto)
        
        if not berelheto_autok:
            print("Jelenleg nincs azonnal bérelhető autó.")
            return
        
        print("\n--- Jelenleg bérelhető autók ---")
        for i, auto in enumerate(berelheto_autok):
            print(f"{i+1}. {auto}")
        print("--------------------------------\n")


if __name__ == "__main__":
    kolcsonzo = Autokolcsonzo("Autókölcsönző")

    kolcsonzo.auto_hozzaadasa(Szemelyauto("MDT-252", "Volvo V40", 8000, 5))
    kolcsonzo.auto_hozzaadasa(Teherauto("LSK-211", "Ford Transit", 15000, 1500))
    kolcsonzo.auto_hozzaadasa(Szemelyauto("KFE-201", "Suzuki Swift", 6000, 5))
    kolcsonzo.auto_hozzaadasa(Teherauto("LFG-444", "Mercedes-Benz Actros ", 20000, 3000))

    today = date.today()

    
    kolcsonzo.berles_hozzaadasa(Berles(kolcsonzo.autok[0], today, 3)) 
    kolcsonzo.berles_hozzaadasa(Berles(kolcsonzo.autok[1], today, 2)) 
    kolcsonzo.berles_hozzaadasa(Berles(kolcsonzo.autok[2], today + timedelta(days=5), 4)) 
    kolcsonzo.berles_hozzaadasa(Berles(kolcsonzo.autok[0], today + timedelta(days=10), 2)) 

    while True:
        print("\n--- Autókölcsönző Menü ---")
        print("1. Autó bérlése")
        print("2. Bérlés lemondása")
        print("3. Összes bérlés listázása")
        print("4. Jelenleg bérelhető autók listázása") 
        print("0. Kilépés")

        valasztas = input("Válasszon menüpontot: ")

        if valasztas == '1':
            rendszam = input("Adja meg a bérelni kívánt autó rendszámát: ").upper()
            kezdeti_datum_str = input("Adja meg a bérlés kezdeti dátumát (ÉÉÉÉ-HH-NN formátumban, pl. 2025-06-01): ")
            try:
                napok_szama = int(input("Adja meg a bérlés napjainak számát: "))
                if napok_szama <= 0:
                    print("A napok száma pozitív egész szám kell legyen.")
                    continue
            except ValueError:
                print("Érvénytelen napok száma. Kérjük, egész számot adjon meg.")
                continue

            siker, uzenet = kolcsonzo.auto_berlese(rendszam, kezdeti_datum_str, napok_szama)
            print(uzenet)

        elif valasztas == '2':
            rendszam = input("Adja meg a lemondani kívánt bérlés autójának rendszámát: ").upper()
            kezdeti_datum_str = input("Adja meg a lemondani kívánt bérlés kezdeti dátumát (ÉÉÉÉ-HH-NN): ")

            siker, uzenet = kolcsonzo.berles_lemondasa(rendszam, kezdeti_datum_str)
            print(uzenet)

        elif valasztas == '3':
            kolcsonzo.berlesek_listazasa() 

        elif valasztas == '4': 
            kolcsonzo.berelheto_autok_listazasa()

        elif valasztas == '0':
            print("Viszontlátásra!")
            break
        else:
            print("Érvénytelen választás. Kérjük, próbálja újra.")