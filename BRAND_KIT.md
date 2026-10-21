# AI Evolution Polska | Brand Kit

Gotowe assety i zasady dla zespołu i agentów. Wiedza o firmie: [COMPANY_BRAIN.md](COMPANY_BRAIN.md).
System wizualny: Brand System 2026 v2 „Ścieżka Ewolucji” ([podgląd](brand/brand-system-2026.html), [zrzut](brand/brand-system-2026.jpg)).

## Co gdzie leży

| Potrzebujesz | Plik / folder |
|---|---|
| Logo (PNG, przezroczyste) | [brand/logo/ai-evolution-polska-logo.png](brand/logo/ai-evolution-polska-logo.png) |
| Logo pixelowe 128 / 256 / 512 / 1024 px | [assets/pixel-education-series/04-brand/logo-pixel-512.png](assets/pixel-education-series/04-brand/logo-pixel-512.png) (też 128/256/1024) |
| Kolory i fonty do kodu (CSS) | [brand/tokens/aiep-tokens.css](brand/tokens/aiep-tokens.css) |
| Kolory i fonty jako dane (JSON, HEX + HSL) | [brand/tokens/aiep-tokens.json](brand/tokens/aiep-tokens.json) |
| Postacie pixelowe (zespół, JARVIS, AIROBOT) | [assets/pixel-education-series/02-characters/](assets/pixel-education-series/08-preview/team-overview.png) · np. [chris_master.png](assets/pixel-education-series/02-characters/chris/chris_master.png) |
| Karty postaci (przód, 3/4, profil, tył) | [assets/pixel-education-series/03-reference-sheets/](assets/pixel-education-series/03-reference-sheets/airobot_turnaround.png) |
| Robot AIROBOT (maskotka, referencje) | [AIROBOT_MASTER_FRONT.png](assets/pixel-education-series/00-references/robot/AIROBOT_MASTER_FRONT.png) · [turnaround](assets/pixel-education-series/00-references/robot/AIROBOT_TURNAROUND_DETAILS.png) |
| Tła pixel (biuro, sala, laboratorium; 16:9 i 9:16) | [assets/pixel-education-series/05-backgrounds/](assets/pixel-education-series/05-backgrounds/office_landscape.png) |
| Rekwizyty PNG (laptop, tablica, serwer…) | [assets/pixel-education-series/06-props/](assets/pixel-education-series/06-props/atlas.png) |
| Animacje (sprite sheety + JSON, klatki, MP4, GIF) | [assets/pixel-education-series/07-animation/](assets/pixel-education-series/07-animation/airobot-wave-spritesheet.json) · [test MP4](assets/pixel-education-series/07-animation/test-landscape.mp4) |
| Instrukcja animacji pixel dla agenta | [assets/pixel-education-series/AGENT_GUIDE.md](assets/pixel-education-series/AGENT_GUIDE.md) |
| Szablon karuzeli Instagram 1080×1350 | [templates/instagram-carousel/](templates/instagram-carousel/README.md) |
| Baner repo, merch, zdjęcia referencyjne | [brand/cover.jpg](brand/cover.jpg), [merch](brand/logo/ai-evolution-polska-merch.png), [brand/photos/](brand/photos/README.md) |

## Kolory w skrócie

Void `#08070E` (tło) · Graphite `#12111C` (karty) · Bone `#F2EFE8` (tekst, jasne tło) · Mist `#9E9AB8` (pomocniczy)
Violet `#7B5CFF` (marka) · Blue `#3D8BFF` (dane) · Magenta `#E04A9A` (energia) · **Amber `#FFB23E` tylko CTA i cena**
Aurora: `linear-gradient(115deg, #3D8BFF, #7B5CFF 48%, #E04A9A)`, najwyżej ok. 15% kadru.

## Fonty

Bricolage Grotesque (nagłówki 700/800) · Instrument Serif Italic (1 słowo akcentu) · Geist (tekst) · Geist Mono (etykiety).
Wszystkie z Google Fonts, z pełnymi polskimi znakami. Link: w [aiep-tokens.css](brand/tokens/aiep-tokens.css).

## Postacie

| ID | Kto | Uwagi |
|---|---|---|
| `chris` | Chris, CEO & Founder | nie myl z Mattem |
| `matt` | Matt, Co-Founder | odrębna fryzura i twarz |
| `marcin` | Marcin, trener | dłuższe falowane włosy, okulary, krótka broda |
| `ivvan` | Ivvan, DevOps | bardzo krótkie włosy, krótki zarost |
| `jarek` | Jarek | pełna broda, złoty zegarek |
| `jarvis` | JARVIS, agent AI | humanoid, bez anteny i nadruku |
| `airobot` | AIROBOT, maskotka | fioletowa antena, cyjanowe oczy, pełne logo |

Każda postać: `<id>_master.png` (zbliżenia), `<id>_sprite.png` (mały bohater), `<id>_pixel4x.png`, `<id>_portrait.png` (avatar).
Skaluj nearest-neighbor, nie odbijaj postaci w poziomie (odwraca logo).

## Zasady

- Logo zawsze z oryginalnego pliku. Bez przerysowywania przez AI i bez deformacji.
- Bez czystej czerni `#000`, czystej bieli `#FFF` i limonki `#B6FF00` (marka AI Evolution Labs).
- Teksty po polsku, na „Ty”, bez em dash (—). Pisz „kontent”, nie „content”.
- Ceny, liczby i terminy tylko z COMPANY_BRAIN.md. Nie obiecuj dofinansowania ani wyników.
- Nie publikuj w imieniu firmy bez zgody właściciela.
