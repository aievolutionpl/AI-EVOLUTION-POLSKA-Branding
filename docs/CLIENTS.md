<!-- GENERATED: COMPANY_BRAIN.md | sha256:1ab182cd56d4f7bc68a252d2157e5867c4a0d7c31d5c29dbde88fff8c57f9240 -->
# CLIENTS | widok Company Brain

Nie edytuj ręcznie. Źródło: [COMPANY_BRAIN.md](../COMPANY_BRAIN.md).
Wygeneruj ponownie: `python3 scripts/brain.py build`.

<a id="audience"></a>
## 3. Odbiorcy i potrzeby

Poniższe opisy to robocze wskazówki komunikacyjne ze starej dokumentacji,
nie wyniki badania rynku ani automatyczne reguły kwalifikacji klienta.

| Odbiorca | Sytuacja / potrzeba | Obawa | Pierwszy krok i język |
|---|---|---|---|
| osoba zaczynająca | nie wie, do czego użyć AI | trudność i jakość odpowiedzi | jedno proste zadanie, bez żargonu |
| przedsiębiorca | powtarzalne zadania zajmują czas | koszt i utrata kontroli | wybierz jeden proces; pokaż korzyść i ograniczenia |
| marketer | potrzebuje spójnego contentu | generyczne wyniki | brief, przykład, korekta i kryteria jakości |
| programista / osoba budująca | szuka pomocy w pracy z kodem | błędy i bezpieczeństwo | konkretny workflow, testy i zakres uprawnień |
| zamawiający szkolenie firmowe | chce rozwoju umiejętności zespołu | dopasowanie i poufność | rozpoznaj zadania, poziom, skalę i wymagania |

Odbiorca darmowej treści, członek społeczności, kupujący kurs i zamawiający
szkolenie to różne role. Nie utożsamiaj liczby obserwujących z liczbą klientów.
Dobierz ścieżkę dopiero po rozpoznaniu potrzeby i sprawdzeniu statusu oferty.

Stare pliki wskazują przedsiębiorcę jako główny profil sprzedażowy, a osobę
początkującą jako domyślnego odbiorcę contentu. To mogą być dwa różne cele,
niekoniecznie sprzeczność. Zapisz cel konkretnego materiału w briefie.

Wykluczenia dotyczące ML/MLOps, dużych organizacji i osób zainteresowanych
certyfikatem wymagają decyzji właściciela (`DECISION-SCOPE`). Nie obiecuj
obsługi poza zakresem i nie odrzucaj automatycznie osoby tylko na podstawie
etykiety. Przy niejasnym dopasowaniu zbierz potrzeby i przekaż do kwalifikacji.

<a id="evidence"></a>
## 8. Dowody i twierdzenia marketingowe

Brak zatwierdzonych case studies w migrowanym repo. Nie zastępuj tego braku
fikcyjnym klientem, liczbą projektów ani oszczędnością czasu.
Wcześniejsze przykłady copy nie są źródłem wyników biznesowych.

Nowy dowód powinien zawierać: mierzoną rzecz, okres, metodę, punkt odniesienia,
źródło, ograniczenia, zatwierdzenie publikacji i treść dozwolonego twierdzenia.
Wynik testu nie jest gwarancją dla wszystkich. Anonimizacja nie pozwala
wymyślać wyników i nie usuwa automatycznie ryzyka identyfikacji klienta.

Zasada publikacji: wynik lub cena z `TO_CONFIRM`, `MISSING`, `CONFLICT`
lub `ARCHIVED` nie trafia do gotowego tekstu jako pewny fakt. `CONFIRMED`
nie wystarcza, gdy termin ważności minął albo zmienne dane trzeba ponownie
sprawdzić. Brak dowodu nie blokuje użytecznego przykładu bez liczbowej obietnicy.

Dane konkurencji ze starego `docs/STRATEGY.md` nie mają przypisanych
konkretnych źródeł do poszczególnych liczb. Nie przeniesiono ich do aktywnej
bazy porównań. Oryginał pozostaje w historii Git, wskazanej w źródle `SRC-STRATEGY`.
Nie publikuj rankingu ani porównania na podstawie samej historycznej tabeli.

## Statusy i pochodzenie danych

```json
{
  "records": [
    {
      "id": "CLAIM-RESULTS",
      "topic": "evidence",
      "kind": "evidence",
      "status": "MISSING",
      "value": null,
      "sources": [
        "SRC-CLIENTS"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false
    },
    {
      "id": "DECISION-SCOPE",
      "topic": "audience",
      "kind": "decision",
      "status": "TO_CONFIRM",
      "value": {
        "previous_exclusions": [
          "ML/MLOps",
          "korporacje 500+",
          "osoby szukające certyfikatu",
          "memy promptami"
        ],
        "action": "Nie rozszerzaj oferty i nie odrzucaj automatycznie; przekaż niejasne dopasowanie do właściciela."
      },
      "sources": [
        "SRC-STRATEGY",
        "SRC-CLIENTS"
      ],
      "verified_at": null,
      "review_after": null,
      "expires_at": null,
      "publication_allowed": false
    }
  ],
  "sources": [
    {
      "id": "SRC-STRATEGY",
      "kind": "repository_snapshot",
      "locator": "https://github.com/aievolutionpl/brand-brain/blob/63fcb0cd0ae1bd5e8aff7bc8d86905579931321e/docs/STRATEGY.md",
      "reviewed_at": "2026-10-03",
      "scope": "Dowód wcześniejszego zapisu, nie potwierdzenie bieżących danych."
    },
    {
      "id": "SRC-CLIENTS",
      "kind": "repository_snapshot",
      "locator": "https://github.com/aievolutionpl/brand-brain/blob/63fcb0cd0ae1bd5e8aff7bc8d86905579931321e/docs/CLIENTS.md",
      "reviewed_at": "2026-10-03",
      "scope": "Dowód wcześniejszego zapisu, nie potwierdzenie bieżących danych."
    }
  ]
}
```
