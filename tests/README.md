# Kontrola jakości

`python3 -m unittest discover -s tests -v` sprawdza kod generatora i walidatora
na danych syntetycznych oraz strukturę bieżącego źródła. Obejmuje duplikaty,
statusy, pochodzenie, daty, blokadę niepotwierdzonych cen, CTA, integralność
assetów, odwołania lokalne, deterministyczność i drift eksportów.
Nie wywołuje modelu, nie testuje ceny na stronie i nie wysyła wiadomości.

`python3 scripts/brain.py check` kontroluje pełny checkout repo. Porównuje
wygenerowane pliki, instrukcje kompatybilne oraz pliki assetów z hashami.
Ostrzeżenia o niepotwierdzonych danych są oczekiwane i nie oznaczają awarii CI.
Nie wolno ich usuwać przez automatyczne nadanie statusu CONFIRMED.

## Scenariusze zachowania agentów

[agent_scenarios.json](agent_scenarios.json) to zestaw zadań do przyszłej oceny.
Wszystkie mają NOT_RUN. Aby je ocenić, uruchom wskazany prompt w agencie
z wczytanym Company Brain i zbadaj wszystkie kryteria. Zapisz osobny publiczny,
bezpieczny raport: ID scenariusza, wersja / commit wiedzy, model i środowisko,
data, odpowiedź lub dozwolony fragment, oceniający i wynik PASS / FAIL / BLOCKED.
Brak uruchomienia to NOT_RUN, a brak dostępu do zależności to BLOCKED,
nie PASS. Zachowaj bazowy zestaw jako niezmieniony szablon testu.

Testy kodu nie dowodzą, że model zawsze zastosuje się do instrukcji.
Instalacje Codex, Claude Code i Hermes wymagają osobnych testów wczytania.
