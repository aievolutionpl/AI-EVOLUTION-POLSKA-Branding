# Szablon karuzeli Instagram (Brand System 2026 v2)

8 slajdów 1080×1350 w stylu „Ścieżka Ewolucji”. Przykład: kampania Kursu PRO ([podgląd](example/kurs-pro-contact-sheet.jpg), [opis posta](example/kurs-pro-caption.md)).

## Layouty

Każdy slajd to `<section class="slide ...">` z `data-step`:

| Klasa | Do czego |
|---|---|
| `l-cover` | okładka z hakiem |
| `l-list` | problem w 3 punktach |
| `l-pillars` | 3 filary w kartach |
| `l-modules` | numerowana lista (moduły, kroki) |
| `l-number` | jedna wielka liczba |
| `l-check` | checklista „dla kogo” |
| `l-offer` | cena i CTA (tryb Bone) |

Pasek postępu „ścieżka ewolucji” i numeracja w stopce generują się same z `data-step`.

## Jak zrobić nową karuzelę

1. Skopiuj `carousel.html`, podmień teksty. Jedno słowo nagłówka w `<span class="it au">`.
2. Wyrenderuj (Python 3.10+, `pip install playwright`, Google Chrome):

```bash
python templates/instagram-carousel/render.py slides templates/instagram-carousel/carousel.html out
```

3. Sprawdź każdy PNG: polskie znaki, obcięcia, Amber tylko na CTA lub cenie.

Fonty ładują się z Google Fonts, więc render potrzebuje internetu. Logo jest brane z `brand/logo/`.
