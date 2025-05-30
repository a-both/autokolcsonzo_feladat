# **Autókölcsönző Rendszer**

Ez a projekt egy egyszerű parancssori alapú autókölcsönző rendszert valósít meg Pythonban. Lehetőséget biztosít autók bérlésére egy adott időszakra, meglévő bérlések lemondására, és az aktuális bérlések áttekintésére. A rendszer induláskor előre betöltött adatokkal (autók és bérlések) indul, így azonnal kipróbálható.

---

## **Főbb Jellemzők**

* **Rugalmas Bérlés:** Autók bérlése meghatározott **kezdő és leadási dátummal**, a bérleti díj automatikus kiszámításával a napok száma alapján.
* **Intelligens Adatvalidáció:**
    * Ellenőrzi, hogy a megadott dátumok érvényesek és jövőbeliek-e.
    * Biztosítja, hogy a **leadási dátum** ne legyen korábbi, mint a kezdő dátum.
    * Ellenőrzi az autó **teljes időszakra vonatkozó foglaltságát**, elkerülve az ütközéseket.
    * Csak létező bérléseket enged lemondani.
* **Felhasználóbarát Interfész:**
    * Egyszerű, menüvezérelt parancssori felület.
    * Autó bérlésekor automatikusan listázza az elérhető autókat a könnyebb választás érdekében.
* **Előre Betöltött Adatok:** A program indításakor 3 autó és 4 bérlés kerül betöltésre, így nem szükséges manuálisan adatot rögzíteni a teszteléshez. A kezdeti adatok betöltése során felmerülő esetleges hibák (pl. múltbeli dátumok) nem jelennek meg a konzolon, így a rendszer indulása letisztult marad.

---

## **Fő Osztályok**

* **`Auto` (absztrakt osztály):** Alapvető autó attribútumokat (rendszám, típus, bérleti díj) definiál.
* **`Szemelyauto`:** Az `Auto` osztályból származik, specifikus személyautó attribútumokkal (pl. ajtók száma).
* **`Teherauto`:** Az `Auto` osztályból származik, specifikus teherautó attribútumokkal (pl. teherbírás).
* **`Felhasznalo`:** A bérlő adatait tárolja (név).
* **`Berles`:** Egy konkrét autóbérlést reprezentálja, tartalmazza az autót, a **kezdő dátumot, a leadási dátumot**, és a bérlőt. Kiszámolja a bérlés napjainak számát és a teljes árat.
* **`Autokolcsonzo`:** A fő logika, amely kezeli az autók és bérlések listáját, valamint a bérlési, lemondási és listázási műveleteket.

---

## **Futtatás**

1.  **Klonozd a repositoryt:**
    ```bash
    git clone [A_TE_REPOSITORY_URL-ed]
    cd [a_repo_mappaneve]
    ```

    (Cseréld ki az `[A_TE_REPOSITORY_URL-ed]` és `[a_repo_mappaneve]` részeket a saját adataiddal.)
2.  **Futtasd a fő szkriptet:**
    ```bash
    python a_programod_neve.py
    ```

    (Cseréld ki az `a_programod_neve.py` részt a fő Python fájlod nevére, ha az nem `main.py`.)

---

## **Használat**

A program indítása után egy menü fogad, ahonnan kiválaszthatod a kívánt műveletet:

1.  **Autók listázása:** Megjeleníti az összes elérhető autót.
2.  **Autó bérlése:** Lehetővé teszi egy autó bérlését kezdő és leadási dátum megadásával.
3.  **Bérlés lemondása:** Egy adott bérlés lemondása rendszám és dátumok alapján.
4.  **Bérlések listázása:** Kilistázza az összes aktív bérlést a bérlő nevével, az autóval, az időszakkal és a teljes árral.
5.  **Kilépés:** Bezárja az alkalmazást.
