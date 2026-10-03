<!-- GENERATED: COMPANY_BRAIN.md | sha256:1ab182cd56d4f7bc68a252d2157e5867c4a0d7c31d5c29dbde88fff8c57f9240 -->
# AUDIENCE | widok Company Brain

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

## Statusy i pochodzenie danych

```json
{
  "records": [
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
