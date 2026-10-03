<div align="center">
<img src="brand/cover.jpg" alt="AI Evolution Polska | Company Brain: wiedza i zasady pracy dla agentów" width="100%">

# AI Evolution Polska | Company Brain

Publiczna wiedza o firmie, procedury pracy i kontrola jakości dla agentów AI.
</div>

## Zacznij tutaj

**[COMPANY_BRAIN.md](COMPANY_BRAIN.md)** to jedyne edytowane źródło wiedzy firmy.
Opisuje markę, ofertę, odbiorców, komunikację, branding, procesy i granice działania.
Wersja struktury: **3.0.0**. [Historia zmian](CHANGELOG.md).

Nie wszystko jest potwierdzone. Historyczne warunki ofert zachowano bez zmiany
kwot, ale wymagają aktualnej weryfikacji. Brakujący dowód nie jest zastępowany
obietnicą. Przeczytaj [audyt i decyzje właściciela](docs/AUDIT.md).

## Podłącz do pracy

Sklonuj repo i uruchom agenta w jego katalogu. Poleć mu przeczytać
[AGENTS.md](AGENTS.md) oraz Company Brain. Samo klonowanie nie wczytuje wiedzy.

```bash
git clone https://github.com/aievolutionpl/brand-brain.git
cd brand-brain
```

Test kontekstu: „Podaj wersję Company Brain, trzy zasady dotyczące mojego zadania
oraz jedną rzecz wymagającą potwierdzenia. Nie traktuj cen historycznych jako aktualnych.”

Do ręcznego załącznika wystarczy COMPANY_BRAIN.md. `BRAND.md` pozostaje pełnym,
identycznym eksportem dla starszych integracji. [Instrukcje Codex / Claude / Hermes](docs/MAINTENANCE.md)
opisują oddzielnie sposób podłączenia i ograniczenia pakietu.

## Mapa repo

| Plik / katalog | Rola |
|---|---|
| [COMPANY_BRAIN.md](COMPANY_BRAIN.md) | wiedza, procedury, rejestr źródeł i statusów |
| [AGENTS.md](AGENTS.md) | instrukcja pracy w całym repo |
| [BRAND.md](BRAND.md) | generowany, samodzielny eksport kompatybilny |
| [agent/SKILL.md](agent/SKILL.md) | skill z dołączonym snapshotem wiedzy |
| [docs/OFFER.md](docs/OFFER.md) | generowany widok oferty, nie drugi cennik |
| [docs/VOICE.md](docs/VOICE.md) | generowany widok komunikacji i CTA |
| [docs/AUDIENCE.md](docs/AUDIENCE.md) | generowany widok odbiorców |
| [docs/CLIENTS.md](docs/CLIENTS.md) | generowany widok kwalifikacji i dowodów |
| [docs/STRATEGY.md](docs/STRATEGY.md) | generowany widok zakresu i kierunków |
| [docs/TOOLS.md](docs/TOOLS.md) | tematy narzędziowe, bez fikcyjnych integracji |
| [tests/README.md](tests/README.md) | testy struktury i scenariusze agentowe |
| `brand/` | oryginalne, niezmienione materiały marki |

## Aktualizacja i sprawdzenie

Python 3.10+ i standardowa biblioteka. Bez zależności, płatnych usług i kluczy API.

```bash
python3 scripts/brain.py build
python3 scripts/brain.py check
python3 -m unittest discover -s tests -v
```

Edytuj COMPANY_BRAIN.md, a potem przebuduj eksporty. CI wykonuje kontrolę,
nie nadpisuje ani nie zatwierdza danych biznesowych. Ostrzeżenia o niepotwierdzonych
rekordach są jawne; błędna struktura lub nieaktualny eksport powodują błąd testu.

## Dane i licencja

Repo jest publiczne. Nie umieszczaj tu prywatnych danych, umów i sekretów.
Zasady wykorzystania określa niezmieniona [LICENSE.md](LICENSE.md).
Tekst lub symbol na istniejącym banerze nie zastępuje postanowień licencji.
