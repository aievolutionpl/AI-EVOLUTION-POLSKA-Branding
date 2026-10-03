# Wdrożenie szablonu Company Brain | 3.1.0

Źródło metody: `COMPANY_BRAIN_TEMPLATE.md` v1.0, przekazany przez właściciela
2026-10-03. SHA-256 oryginału:
`0d2ff05e72d0a92f316c2bb923fce98943731db7dc0497aa3e57eed792733578`.

Przejęto sposób organizacji kontekstu i opracowano treść dla AIEP.
Nie opublikowano oryginalnego szablonu ani prywatnego odnośnika Drive.
Szablon jest źródłem metody, nie potwierdzeniem danych biznesowych.

## Mapa wdrożenia

| Sekcje szablonu | Miejsce w Company Brain | Wdrożone rozwiązanie |
|---|---|---|
| 0, Quick Start | onboarding | START, research, konflikty, pięć pytań i ochrona kontekstu AIEP |
| 1–3 | identity + onboarding | szybki kontekst, dane formalne, lokalizacja bez domysłów |
| 4, 28 | channels + website | kontakt, adresy i stan sprawdzenia |
| 5 | offers + rejestr OFFER | jedna ewidencja warunków i kontrola karty oferty |
| 6 | audience + sales | potrzeby, kwalifikacja i obiekcje |
| 7–8 | identity + evidence | pozycjonowanie, dowody i odróżnienie ambicji od faktów |
| 9–10 | voice + visual | głos, przykłady i ochrona oryginalnych assetów |
| 11 | website | mapa stron, konwersja i testy przed publikacją |
| 12–14 | marketing + systems | kanały, content i stan wdrożenia narzędzi |
| 15–16 | sales | zapytania, trzy szkice wiadomości i obsługa po zakupie |
| 17 | evidence | opinie i wyniki ze źródłem; bez fikcyjnego social proof |
| 18–19 | seo | metoda porównania ofert i sześć hipotez fraz |
| 20–21 | marketing | filary contentu, trzy briefy i warunki uruchomienia reklam |
| 22–23 | planning | definicje KPI i robocze priorytety |
| 24 | systems + workflows | trzy scenariusze automatyzacji z kontrolą człowieka |
| 25–27 | governance + systems | uprawnienia, ryzyka, status systemu i dostęp |
| 29–30 | planning + open_questions | projekty robocze i pięć decyzji właściciela |
| 31–32 | sources + review_policy | pochodzenie, aktualność i raport CLI |
| 33–34 | governance + CHANGELOG | kontrola materiału i historia zmian |

Pełny kontekst: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).
Dokumenty tematyczne są teraz krótkimi indeksami do sekcji i rekordów,
nie kolejnymi kopiami faktów. `BRAND.md` i referencja skilla pozostają
pełnymi, generowanymi eksportami dla starszych integracji.

## Co jest propozycją, a nie działającym systemem

Nie uruchomiono kampanii, sekwencji wiadomości, monitoringu ani integracji CRM.
Nie testowano formularzy, koszyka, kont reklamowych ani danych analitycznych.
Statyczny odczyt strony zwrócił tylko komunikat JavaScript: PARTIAL, nie audyt.
Nie wykonano nowego badania konkurentów ani pomiaru SEO w narzędziu analitycznym.
Słowa kluczowe są hipotezami. Budżety, cele liczbowe, wyniki i SLA pozostają brakami.

Nie zmieniono wartości ani statusów 13 dotychczasowych rekordów biznesowych.
Rejestr zawiera teraz 30 rekordów. Logo, zdjęcia, baner i licencja są niezmienione.
Dopisanie nowego pola nie jest potwierdzeniem ceny, gwarancji ani integracji.

## Użycie i kontrola

```bash
python3 scripts/brain.py build
python3 -m unittest discover -s tests -v
python3 scripts/brain.py check
python3 scripts/brain.py report
```

`report` pokazuje luki i maksymalnie pięć pytań. Nie modyfikuje danych,
nie wykonuje researchu i nie uruchamia harmonogramu. Datę testową można
podać parametrem `--today 2026-10-03`.

Testy kodu sprawdzają strukturę i przykładowe metadane. Nie potwierdzają
prawdziwości opisów firmy ani zachowania modelu. Dodatkowe scenariusze
w [context_scenarios.json](../tests/context_scenarios.json) mają status `NOT_RUN`.
Łącznie z wcześniejszym zestawem przygotowano 18 scenariuszy odpowiedzi agentów.

Źródła metody i odczyty częściowe nie mogą potwierdzać faktów. Pomiary SEO
wymagają źródła, daty, regionu i narzędzia. Aktywny system wymaga potwierdzenia,
a kampania także oferty, budżetu i zatwierdzeń. Walidator nie jest systemem
kontroli dostępu i nie zastępuje zgody na działania w zewnętrznych narzędziach.
