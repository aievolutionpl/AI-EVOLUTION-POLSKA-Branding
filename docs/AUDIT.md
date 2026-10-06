# Audyt migracji Company Brain 3.0.0

Przegląd: 2026-10-03. Podstawa: commit
`63fcb0cd0ae1bd5e8aff7bc8d86905579931321e`, bez założenia, że zapis w repo
potwierdza bieżącą ofertę. [Snapshot źródłowy](https://github.com/aievolutionpl/brand-brain/tree/63fcb0cd0ae1bd5e8aff7bc8d86905579931321e).
Przeczytano README, BRAND, instrukcje agentów, sześć dokumentów docs i licencję.
Spis i hashe assetów sprawdzono w drzewie Git. Nie wykonano nowego audytu
wizualnego zdjęć ani testu glifów w plikach fontów.

## Zmiany

| Problem w źródle | Wdrożona zmiana |
|---|---|
| cennik w czterech ręcznie utrzymywanych plikach | pojedyncze rekordy w Company Brain; generowane eksporty |
| publiczne ceny i równoczesny zakaz cenników | rozdzielenie oferty publicznej od indywidualnych wycen |
| daty deklarowane bez konkretnych dowodów | oddzielone reviewed_at, verified_at i źródłowa data historyczna |
| liczbowe przykłady copy przypominające wyniki firmy | przykłady bez obietnic; brak case studies jawnie oznaczony |
| dane konkurencji bez odnośników przy poszczególnych liczbach | poza aktywną bazą; oryginał zachowany w historii Git |
| każda domena spoza marki blokowana | oddzielone CTA marki i źródła researchu |
| jeden CTA z niepotwierdzoną wysyłką pliku | rekord CTA z brakiem assetu i weryfikacji dostarczenia |
| instrukcje tylko w agent/ | root AGENTS.md i kompatybilna kopia |
| kopiowanie samego skilla z odsyłaczami do niedostępnych plików | pełny snapshot w references, osobne instrukcje instalacji |
| kategoryczne stwierdzenia o rodzinach fontów | wymóg sprawdzenia konkretnego pliku, bez zmiany palety fontów |
| kontrola obcięć tylko kodem | kontrola wymiarów oraz ocena wizualna |
| różne numery wersji | wersja struktury w rejestrze; eksporty pochodzą z tego samego pliku |

## Nierozstrzygnięte

Kwot, strategii ani licencji nie zastąpiono nowymi decyzjami. Zachowano
historyczne ceny z oznaczeniem TO_CONFIRM. Brak aktualnego potwierdzenia
nie oznacza zmiany ceny ani wycofania produktu.

Otwarte decyzje: warunki ofert, rozdzielenie AIEP / Labs, kwalifikacja odbiorców,
aktualne kanały i CTA, dowody wyników oraz interpretacja opisu licencji.
Pełny rejestr i pięć pytań znajdują się w
[Company Brain](../COMPANY_BRAIN.md#governance).

LICENSE.md i wszystkie istniejące pliki graficzne pozostają bez zmian.
Baner nie jest dowodem statusu licencji, dat ani wyników firmy.
Nie dołączono prywatnych danych, materiałów klientów i historii rozmów.

## Kontrola wykonania

Automatyczne testy dotyczą generatora i walidatora. Polecenia oraz zakres:
[utrzymanie](MAINTENANCE.md) i [testy](../tests/README.md).
Testy scenariuszy zachowania agentów pozostają NOT_RUN do wykonania w danym
modelu i środowisku. Plik scenariuszy nie jest raportem udanych odpowiedzi.
Wynik CI należy odczytać przy konkretnym commicie, nie z tego dokumentu.
