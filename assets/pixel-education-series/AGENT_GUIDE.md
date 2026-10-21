# Instrukcja dla agenta
Cel: edukacyjne filmy AI Evolution Polska w zatwierdzonym stylu 03 — 32-BIT DETAIL.

## Start
1. Wczytaj manifest.json i scenariusz filmu.
2. Zdjęcia i oryginalne referencje w 00-references/ określają tożsamość. Nie zastępuj ich wygenerowanym wariantem jako nowym źródłem prawdy.
3. Identyfikatory: chris, matt, marcin, ivvan, jarek, jarvis, airobot.
4. Wybierz format i tło. Pionowe sceny komponowano osobno, nie są cropem poziomych.
5. text_safe_box_normalized to sugerowany obszar treści. Sprawdź granice tablicy i nakładanie się warstw w docelowym renderze.

## Pliki i skalowanie
- Master: zbliżenia, twarz, czytelne logo.
- Native sprite: mocniejszy raster, mały bohater.
- Pixel4x: gotowe powiększenie native sprite'a 4×.
- Portret: avatar lub panel rozmowy.
- Karta: referencja nowych gestów i widoków, nie sekwencja ruchu.
- Rekwizyty: samodzielne warstwy z alfa; atlas zachowano dodatkowo.
- Skaluj nearest-neighbor, preferuj całkowite mnożniki native sprite'a.
- Master zachowuje więcej szczegółów; nie jest ścisłym rastrem 4 px.
- Początek współrzędnych: lewy górny róg. Pivot: dolny środek sylwetki; dokładne wartości są w manifeście.
- Nie odbijaj całej postaci poziomo: odwraca to litery nadruku i asymetryczne cechy.
- Małe sprite'y przesuwaj w pełnych pikselach, bez subpikselowego rozmycia.
- Dobierz kontrast czarnego stroju ze sceną. Dostępne są jasne i ciemne tła.
- Zostaw miejsce na napisy i interfejs platformy, szczególnie dolne ok. 18% pionowego kadru.

## Logo i podobieństwo
- Źródło: 04-brand/logo-original.png.
- Warianty 128/256 px są natywne; 512/1024 px to powiększenia 4×.
- Mastery pięciu ludzi i AIROBOTA mają nałożony oryginalny znak.
- Dla czytelności pełnego nadruku zalecana wysokość człowieka około 720 px lub większa.
- Przy mniejszej postaci dodaj osobne logo. Pełnego napisu nie da się czytać przy dowolnie małej skali.
- Marcin: falowane dłuższe włosy, okulary i krótka broda. Jarek: pełna broda i złoty zegarek. Ivvan: bardzo krótkie włosy i krótki zarost.
- Chris i Matt mają odrębne fryzury i twarze. Nie używaj jednego awatara jako tożsamości obu.
- AIROBOT: szeroka głowa, jeden fioletowy punkt anteny, cyanowe oczy i uśmiech, fioletowe pierścienie, pełne logo.
- JARVIS: wysoki humanoid, owalna głowa, małe białe oczy, bez anteny i nadruku.

## Ruch
- 07-animation/airobot-wave-spritesheet.json: 24 klatki, 12 fps, pętla 2 s.
- 07-animation/chris-idle-spritesheet.json: 24 klatki, 12 fps, pętla 2 s.
- Klatki RGBA: 07-animation/frames/airobot/ i 07-animation/frames/chris/.
- Warstwy i pivoty robota: 07-animation/rig/airobot/.
- test-landscape.mp4 i test-portrait.mp4: gotowe kompozycje po 6 s.
- Do własnego filmu używaj klatek PNG. MP4 ma wkomponowane tło.
- To test wycinankowy, bez pełnego rigowania twarzy, lip-syncu i cyklu chodu.
- Karty mają osobno opracowane widoki. Odtwarzanie ich jako klatek spowoduje skoki.

## Kontrola
Sprawdź sylwetkę, antenę i stopy, podobieństwo twarzy, nadruk w docelowej skali, granice planszy i ostrość pikseli. Obejrzyj początek, środek i koniec filmu. Nie zasłaniaj twarzy napisami. Raport: quality-report.json.
