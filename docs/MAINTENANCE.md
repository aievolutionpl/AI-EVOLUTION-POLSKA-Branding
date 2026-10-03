# Utrzymanie i instalacja

## Jedno źródło

Wiedzę edytuj w [COMPANY_BRAIN.md](../COMPANY_BRAIN.md). Skrypt generuje BRAND.md,
snapshot `agent/references/COMPANY_BRAIN.md` i sześć widoków w docs.
Obie pełne kopie są identyczne bajtowo. Widoki zawierają hash źródła,
wybrane sekcje oraz rekordy i ich pochodzenie. Nie zmieniaj ich ręcznie.

AGENTS.md opisuje pracę, nie ceny. `agent/AGENTS.md` jest kopią kompatybilną
tej samej instrukcji; utrzymuj oba pliki identycznie. Instrukcje i kod nie są
źródłem faktów o firmie. Po migracji stare integracje muszą pobrać nowy eksport.

## Aktualizacja danych

W źródle dopisz publiczny dowód i jego typ. W rekordzie wpisz rzeczywistą datę
potwierdzenia, status i zgodę na publikację. Dla danych zmiennych ustal datę
ponownego przeglądu. Nie wpisuj daty modyfikacji jako daty weryfikacji.
Sam wpis historyczny nie odblokowuje publikacji. Warunki i źródła potwierdza
właściciel lub odpowiedni dowód, nie walidator.

```bash
python3 scripts/brain.py build
python3 scripts/brain.py check
python3 -m unittest discover -s tests -v
```

`check` nie naprawia plików. Zwraca kod 1 przy błędach. Ostrzeżenia o brakach
zwracają kod 0, jeżeli rekord jest poprawnie zablokowany do publikacji.
Opcja `--today YYYY-MM-DD` służy powtarzalnym testom; nie używaj starej daty,
żeby ukrywać przedawnione dane. Domyślnie używana jest bieżąca data systemu.

## Codex

Uruchom w głównym katalogu repo. Root AGENTS.md kieruje do Company Brain.
Nie polegaj na samym pliku schowanym w `agent/`.
Sprawdź w sesji, czy agent odczytał oba dokumenty i podaje ich wersję.
Źródło instalacji, odczytane 2026-10-03:
[oficjalna dokumentacja AGENTS.md](https://developers.openai.com/codex/guides/agents-md/).
Nie wykonano testu instalacji w rzeczywistej sesji Codex.

## Claude Code

Z katalogu repo skopiuj kompletny skill do nowego katalogu osobistego.
Przykład dla powłoki POSIX; polecenie odmawia nadpisania istniejącej instalacji:

```bash
target="$HOME/.claude/skills/ai-evolution-polska-brand"
if [ -e "$target" ]; then
  printf '%s\n' 'Katalog już istnieje. Porównaj i zaktualizuj go świadomie.'
else
  mkdir -p "$target/references"
  cp agent/SKILL.md "$target/SKILL.md"
  cp agent/references/COMPANY_BRAIN.md "$target/references/COMPANY_BRAIN.md"
fi
```

Wywołaj skill w nowej sesji i wykonaj test kontekstu z README.
Nie kopiuj samego SKILL.md, bo odwołuje się do załączonego pliku wiedzy.
Źródło odczytane 2026-10-03:
[oficjalna dokumentacja skills](https://code.claude.com/docs/en/skills).
Nie wykonano instalacji w środowisku użytkownika.

## Hermes

Oddzielny katalog użytkownika to `~/.hermes/skills/`.
Użyj tego samego kompletnego pakietu, z odmiennym katalogiem docelowym:

```bash
target="$HOME/.hermes/skills/ai-evolution-polska-brand"
if [ -e "$target" ]; then
  printf '%s\n' 'Katalog już istnieje. Porównaj i zaktualizuj go świadomie.'
else
  mkdir -p "$target/references"
  cp agent/SKILL.md "$target/SKILL.md"
  cp agent/references/COMPANY_BRAIN.md "$target/references/COMPANY_BRAIN.md"
fi
```

Sprawdź widoczność skilla i odczyt snapshotu w używanej wersji / profilu Hermes.
Ścieżka niestandardowego profilu może być inna. Nie zakładaj automatycznej aktywacji.
Źródło odczytane 2026-10-03:
[oficjalny opis systemu skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills/).
Nie wykonano instalacji ani testu wykonania w Hermes.

## Ograniczenia kontroli

Walidator sprawdza strukturę, identyfikatory, statusy, metadane, lokalne
odwołania inline Markdown / HTML, ścieżki assetów i aktualność eksportów.
Nie jest pełnym parserem Markdown. Nie sprawdza dostępności zewnętrznych URL,
prawdziwości informacji, zgód, poprawności prawnej, renderu fontów i grafiki
ani zgodności odpowiedzi modelu z instrukcją. Nie jest skanerem sekretów.
Scenariusze agentowe wymagają osobnego wykonania i oceny.
