
Autókölcsönző Rendszer 
===============================

Ez a projekt egy egyszerű autókölcsönző rendszer, amely lehetővé teszi személyautók és teherautók kezelését, bérlését és a bérlések nyilvántartását Python nyelven, objektum-orientált megközelítéssel.

Funkciók
--------
- Új autók hozzáadása a rendszerhez (személyautó vagy teherautó)
- Autók bérlése megadott időintervallumra
- Bérlések lemondása
- Összes bérlés kilistázása
- Jelenleg szabadon bérelhető autók listázása

Használt technológiák
----------------------
- datetime modul a dátumkezeléshez
- Absztrakt osztályok (abc modul) az autók típusainak egységes kezeléséhez

Futtatás
--------
A program futtatásához Python 3 szükséges.

1. Lépés: Klónozd a repót vagy másold le a kódot.

2. Lépés: Futtasd a programot terminálból vagy IDLE-ből:
    python autokolcsonzo.py

3. Lépés: Használat


A konzolban megjelenő menü alapján tudod kiválasztani a kívánt műveletet.

--- Autókölcsönző Menü ---
    1. Autó bérlése
    2. Bérlés lemondása
    3. Összes bérlés listázása
    4. Jelenleg bérelhető autók listázása
    0. Kilépés
        
Példák
------
- Bérlés: Add meg a rendszámot, kezdődátumot (pl. 2025-06-01) és a napok számát.
- Lemondás: Add meg a rendszámot és a bérlés kezdőnapját.

Példa autók
-----------
A program indításakor az alábbi autók kerülnek regisztrálásra:

- MDT-252 – Volvo V40 (Személyautó)
- LSK-211 – Ford Transit (Teherautó)
- KFE-201 – Suzuki Swift (Személyautó)
- LFG-444 – Mercedes-Benz Actros (Teherautó)

Ellenőrzések
------------
- Nem lehet múltbeli dátummal bérlést indítani
- Nem lehet ugyanarra az időszakra ugyanazt az autót kétszer lefoglalni
- A dátumformátumot a rendszer ellenőrzi (ÉÉÉÉ-HH-NN)

