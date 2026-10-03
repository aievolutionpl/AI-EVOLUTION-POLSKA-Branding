<!-- GENERATED: COMPANY_BRAIN.md | sha256:1ab182cd56d4f7bc68a252d2157e5867c4a0d7c31d5c29dbde88fff8c57f9240 -->
# OFFER | widok Company Brain

Nie edytuj ręcznie. Źródło: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).
Wygeneruj ponownie: `python3 scripts/brain.py build`.

<a id="offers"></a>
## 2. Oferta i ceny

Jedyna edytowana ewidencja ofert znajduje się w rekordach `OFFER-*` poniżej.
Kwoty przeniesiono bez zmiany ze starego `docs/OFFER.md`. Nie sprawdzono ich
ponownie na stronie ani u właściciela. Status `TO_CONFIRM` nie oznacza wycofania
produktu: oznacza zakaz podawania tych warunków jako aktualnie zatwierdzonych.
Historyczną datę deklarowanej weryfikacji zachowano osobno od `verified_at`.

Dla każdej oferty potrzebne są: marka, odbiorca, problem, zakres, rezultat,
format, czas, wymagania, wyłączenia, cena, waluta, jednostka, netto/brutto,
źródło, data sprawdzenia, ważność i następny krok. `null` oznacza brak danych,
nie brak ograniczeń. Cena „od” nie jest ceną końcową. Nie przeliczaj jej
na osobę, godzinę lub grupę bez zatwierdzenia jednostki.

Gdy klient pyta o wycenę, a warunki nie są potwierdzone, przygotuj odpowiedź:
„Żeby dobrać zakres szkolenia, potrzebuję informacji o zespole, zadaniach
oraz oczekiwanym efekcie. Cenę i termin potwierdzimy po ustaleniu zakresu.”
To propozycja tekstu, nie wysłana wiadomość ani potwierdzenie dostępności.

Publiczne, zatwierdzone warunki można komunikować. Indywidualne wyceny,
negocjowane rabaty i umowy pozostają poza publicznym repo. Nie wyciągaj
cennika ze zdjęcia, z wcześniejszego posta ani z tabeli konkurencji.

## Statusy i pochodzenie danych

```json
{
  "records": [
    {
      "id": "OFFER-FREE",
      "topic": "offers",
      "kind": "offer",
      "status": "TO_CONFIRM",
      "value": {
        "name": "Darmowy kurs AI",
        "brand": "AI Evolution Polska",
        "audience": "osoba zaczynająca",
        "problem": null,
        "scope": null,
        "deliverable": null,
        "format": "kurs",
        "duration": null,
        "prerequisites": null,
        "exclusions": null,
        "price": 0,
        "regular_price": null,
        "currency": "PLN",
        "unit": "dostęp",
        "price_type": "fixed",
        "tax_basis": null,
        "availability": null,
        "next_step": "Potwierdź zakres i warunki z właścicielem.",
        "destination": null
      },
      "sources": [
        "SRC-OFFER"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false,
      "source_claimed_verified_at": "2026-09-30"
    },
    {
      "id": "OFFER-PRO",
      "topic": "offers",
      "kind": "offer",
      "status": "TO_CONFIRM",
      "value": {
        "name": "Kurs Premium (PRO)",
        "brand": "AI Evolution Polska",
        "audience": "do potwierdzenia",
        "problem": null,
        "scope": null,
        "deliverable": null,
        "format": "kurs",
        "duration": null,
        "prerequisites": null,
        "exclusions": null,
        "price": 1499,
        "regular_price": 1999,
        "currency": "PLN",
        "unit": null,
        "price_type": "promotional",
        "tax_basis": null,
        "availability": null,
        "next_step": "Potwierdź zakres i warunki z właścicielem.",
        "destination": null
      },
      "sources": [
        "SRC-OFFER"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false,
      "source_claimed_verified_at": "2026-09-30"
    },
    {
      "id": "OFFER-BUSINESS",
      "topic": "offers",
      "kind": "offer",
      "status": "TO_CONFIRM",
      "value": {
        "name": "Szkolenia dla firm",
        "brand": "AI Evolution Polska",
        "audience": "zespoły firmowe",
        "problem": null,
        "scope": null,
        "deliverable": null,
        "format": "szkolenie",
        "duration": null,
        "prerequisites": null,
        "exclusions": null,
        "price": 4999,
        "regular_price": null,
        "currency": "PLN",
        "unit": null,
        "price_type": "from",
        "tax_basis": null,
        "availability": null,
        "next_step": "Potwierdź zakres i warunki z właścicielem.",
        "destination": null
      },
      "sources": [
        "SRC-OFFER"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false,
      "source_claimed_verified_at": "2026-09-30"
    },
    {
      "id": "OFFER-WORKSHOPS",
      "topic": "offers",
      "kind": "offer",
      "status": "TO_CONFIRM",
      "value": {
        "name": "Warsztaty i prezentacje",
        "brand": "AI Evolution Polska",
        "audience": "do potwierdzenia",
        "problem": null,
        "scope": null,
        "deliverable": null,
        "format": "warsztat / prezentacja",
        "duration": null,
        "prerequisites": null,
        "exclusions": null,
        "price": 2499,
        "regular_price": null,
        "currency": "PLN",
        "unit": "osoba",
        "price_type": "from",
        "tax_basis": null,
        "availability": null,
        "next_step": "Potwierdź zakres i warunki z właścicielem.",
        "destination": null
      },
      "sources": [
        "SRC-OFFER"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false,
      "source_claimed_verified_at": "2026-09-30"
    },
    {
      "id": "CLAIM-FREE-ACCESS",
      "topic": "offers",
      "kind": "claim",
      "status": "TO_CONFIRM",
      "value": "Bez konta, bez karty, po polsku.",
      "sources": [
        "SRC-OFFER"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false
    }
  ],
  "sources": [
    {
      "id": "SRC-OFFER",
      "kind": "repository_snapshot",
      "locator": "https://github.com/aievolutionpl/brand-brain/blob/63fcb0cd0ae1bd5e8aff7bc8d86905579931321e/docs/OFFER.md",
      "reviewed_at": "2026-10-03",
      "scope": "Dowód wcześniejszego zapisu, nie potwierdzenie bieżących danych."
    }
  ]
}
```
