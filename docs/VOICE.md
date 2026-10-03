<!-- GENERATED: COMPANY_BRAIN.md | sha256:1ab182cd56d4f7bc68a252d2157e5867c4a0d7c31d5c29dbde88fff8c57f9240 -->
# VOICE | widok Company Brain

Nie edytuj ręcznie. Źródło: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).
Wygeneruj ponownie: `python3 scripts/brain.py build`.

<a id="voice"></a>
## 5. Głos marki i content

Przyjazny, rzeczowy praktyk. Po polsku, proste zdania, krótkie akapity,
konkretne zastosowania. Używaj „ty” i „twoje”, bez sztucznego hype'u.
Poziom techniczny dopasuj do odbiorcy, nie ukrywaj istotnych ograniczeń.

Jeden post = jeden temat. Konstrukcja: obserwacja lub problem → przykład
→ zastosowanie → ograniczenie, gdy istotne → naturalny następny krok.
Nie zaczynaj zawsze pytaniem i nie kończ każdego materiału tą samą frazą.
Emotikony tylko wtedy, gdy pomagają. Nie pisz „testowaliśmy”, „nasz klient”
ani „zaoszczędziliśmy”, jeśli brak zatwierdzonego dowodu.

Nie używaj: korporacyjnych frazesów, em dash, słowa „realnie”,
„game changer”, „rewolucyjne rozwiązanie”, „w dzisiejszych czasach”.
Liczby w dobrym copy też wymagają źródła. Nie zastępuj ogólnego sloganu
konkretną, ale wymyśloną oszczędnością czasu.

Propozycje redakcyjne, nie archiwum zatwierdzonych wypowiedzi właściciela:

| Nie tak | Lepiej |
|---|---|
| „Ten tool zmieni wszystko” | „Ten workflow porządkuje brief przed generowaniem treści” |
| „Gwarantujemy oszczędność godzin” | „Porównaj czas tego zadania przed i po wdrożeniu” |
| „Przetestowaliśmy nowy model” bez testu | „Producent opisuje tę funkcję; nie sprawdziliśmy jej w tym zadaniu” |
| „Napisz hasło, wyślemy plik” bez materiału | „Zapisz przykład i wykorzystaj go przy kolejnym briefie” |

W treści edukacyjnej podaj narzędzie, kroki lub przykład oraz warunki użycia.
Przy newsach oddziel fakt, deklarację producenta, opinię i przewidywanie.
Nie udawaj doświadczenia tylko po to, żeby post brzmiał bardziej osobiście.

<a id="channels"></a>
## 4. Kanały, ścieżka klienta i CTA

Oficjalne domeny wskazane w dotychczasowym repo: `aievolutionpolska.pl`
(strona marki), `ai-evolution.online` (ścieżka edukacyjna) i `aievolutionlabs.io`
(osobna marka usługowa). Przed publikacją sprawdź konkretny adres docelowy.
Nie zastępuj ich podobnie brzmiącą domeną. Nie potwierdzono tutaj działania
formularzy, dostępności kursu ani aktualnych warunków dostępu.

Koncepcja ścieżki: użyteczna treść → materiał edukacyjny → społeczność lub
newsletter → kurs / rozpoznanie potrzeby szkolenia. To opis planowanej
komunikacji, nie potwierdzenie wdrożonego lejka i wszystkich integracji.
Nazwy społeczności, aktywne zaproszenia i formularz newslettera wymagają
uzupełnienia w `CHANNEL-COMMUNITY`. Nie zgaduj identyfikatorów i linków.

Bezpieczne CTA w szkicu: „Zapisz ten przykład do następnego zadania” albo
„Który etap tego procesu zajmuje ci najwięcej czasu?”. To propozycje tekstu.
CTA z linkiem wymaga sprawdzonego adresu. CTA obiecujące plik, konsultację
lub automatyczną wiadomość wymaga potwierdzonego materiału i dostarczenia.
`CTA-ARGON` jest niepotwierdzone, więc nie obiecuj wysłania checklisty.

Domeny marki służą kierowaniu klientów. Dokumentacja producenta, publikacje
badawcze i oficjalne komunikaty mogą być zewnętrznymi źródłami researchu.
Nie blokuj cytowania takiego źródła regułą „tylko trzy domeny”.

## Statusy i pochodzenie danych

```json
{
  "records": [
    {
      "id": "CTA-ARGON",
      "topic": "channels",
      "kind": "cta",
      "status": "TO_CONFIRM",
      "value": {
        "keyword": "ARGON",
        "promised_asset": "checklista wdrożenia AI",
        "asset_path": null,
        "delivery_verified": false
      },
      "sources": [
        "SRC-VOICE"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false
    },
    {
      "id": "CHANNEL-COMMUNITY",
      "topic": "channels",
      "kind": "channel",
      "status": "TO_CONFIRM",
      "value": {
        "historical_name": "AI Poland (Facebook)",
        "current_name": null,
        "community_url": null,
        "newsletter_url": null
      },
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
    },
    {
      "id": "SRC-VOICE",
      "kind": "repository_snapshot",
      "locator": "https://github.com/aievolutionpl/brand-brain/blob/63fcb0cd0ae1bd5e8aff7bc8d86905579931321e/docs/VOICE.md",
      "reviewed_at": "2026-10-03",
      "scope": "Dowód wcześniejszego zapisu, nie potwierdzenie bieżących danych."
    }
  ]
}
```
