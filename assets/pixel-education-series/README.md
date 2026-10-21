# AI Evolution Polska — Pixel Animation Pack
Wersja 1.0 · wybrany styl 03 — 32-BIT DETAIL · 2026-10-21

## Otwórz najpierw
- [Wszystkie postacie](08-preview/team-overview.png)
- [Test animacji 16:9](07-animation/test-landscape.mp4)
- [Test animacji 9:16](07-animation/test-portrait.mp4)
- [Test jako GIF](07-animation/test-landscape.gif)
- [Porównanie twarzy ze zdjęciami](08-preview/likeness-check.png)
- [Instrukcja dla agenta](AGENT_GUIDE.md)
- [Manifest plików](manifest.json)

## Zawartość
- 7 postaci: Chris, Matt, Marcin, Ivvan, Jarek, JARVIS i oficjalny AIROBOT.
- Dla każdej: transparentny master PNG, native sprite, render pikseli 4× i portret.
- 7 kart referencyjnych: przód, 3/4 z gestem prowadzącego, profil i tył.
- 6 teł: nocne biuro, jasna sala szkoleniowa, laboratorium AI; każde w 1920×1080 i 1080×1920.
- 12 osobnych rekwizytów PNG: laptop, tablica, biurko, krzesło, serwer, książki, roślina, mikrofon, dymek, dokument, koło zębate, workflow.
- Oryginalne logo i warianty pixelowe szerokości 128, 256, 512 i 1024 px.
- Dwa 6-sekundowe MP4, GIF, 24 klatki PNG AIROBOTA, 24 klatki Chrisa, sprite sheety z JSON i prosty rig AIROBOTA.
- Zdjęcia źródłowe, niezmienione referencje maskotki, 21 promptów i źródłowe wygenerowane grafiki.

## Pliki postaci
W 02-characters/<id>/:
- <id>_master.png: największa czytelność twarzy i nadruku; ludzie/JARVIS 1024×1536, AIROBOT 1024×1024.
- <id>_sprite.png: 256×384; AIROBOT 256×256. Skalować nearest-neighbor.
- <id>_pixel4x.png: powiększenie native sprite'a 4×.
- <id>_portrait.png: transparentny portret 512×512.

JARVIS jest humanoidem ze strony. AIROBOT to przesłana maskotka. JARVIS zachowuje brak nadruku zgodnie ze źródłem.

## Twarze i logo
Twarze opracowano osobno z rzeczywistych zdjęć jako stylizowaną interpretację. Porównanie kontrolne: 08-preview/likeness-check.png.
Na masterach pięciu osób i AIROBOTA napisy zastąpiono grafiką z oryginalnego logo. Warianty pixelowe też pochodzą z tego źródła.

Pełny napis na bardzo małej koszulce traci czytelność. Do filmu zalecany jest master i wysokość człowieka około 720 px lub większa. Przy mniejszej postaci użyj osobnego logo w kadrze. Małych sprite'ów nie skaluj filtrem rozmywającym.

## Karty i animacja
Karty utrzymują wygląd przy nowych generowaniach. Profil, tył i części niewidoczne na zdjęciu są opracowanym uzupełnieniem. Karty nie są klatkami jednego ruchu.
Test to animacja wycinankowa 2D, bez lektora i synchronizacji ust. AIROBOT porusza ręką, mruga i przechyla głowę; Chris ma subtelny ruch głowy. To baza do rozbudowy gestów, scen i pełnego rigowania.

## Odtworzenie
Wymagania: Python 3.10+, Pillow, numpy, FFmpeg/FFprobe w PATH. Font: lokalny Consolas w Windows; na innym systemie zmień ścieżki fontów w skryptach.

    python source/build_pack.py
    python source/render_preview.py
    python source/finalize_pack.py

Skrypty są offline: nie wywołują modeli ani API. Grafiki wygenerowano wbudowanym image_gen. Prompty: source/prompts/. Oryginalne wyniki: source/generated/.

## Źródła
Zdjęcia: https://www.aievolutionpolska.pl/ — pobrane 2026-10-21; adresy: 00-references/sources.json.
Branding: https://github.com/aievolutionpl/AI-EVOLUTION-POLSKA-Branding — Brand System 2026 v2.
AIROBOT: dwa załączniki użytkownika i oficjalne niezmienione referencje maskotki.
Sprawdzone narzędzie do dalszej ręcznej animacji: https://github.com/Orama-Interactive/Pixelorama — timeline, onion skinning, PNG/APNG/GIF/wideo i sprite sheety. Paczka działa bez jego instalacji.

Kontrola plików: quality-report.json. Parametry animacji: 07-animation/verification.json.
