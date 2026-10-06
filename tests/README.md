# Kontrola jakości

`python3 -m unittest discover -s tests -v` sprawdza kod generatora i walidatora
na danych syntetycznych oraz strukturę bieżącego źródła. Obejmuje duplikaty,
statusy, pochodzenie, daty, blokadę niepotwierdzonych cen, CTA, integralność
assetów, odwołania lokalne, powtarzalność i zgodność eksportów.
Nie wywołuje modelu, nie testuje ceny na stronie i nie wysyła wiadomości.

Wersja 3.1 dodaje testy źródeł metody i odczytu częściowego, hipotez SEO,
pomiarów, statusu systemów, kampanii, KPI, raportu oraz pięciu pytań.
Test regresji kontroluje hash 13 wcześniejszych rekordów biznesowych;
zachowanie tych rekordów nie oznacza potwierdzenia ich aktualności.

`python3 scripts/brain.py check` kontroluje pełny checkout repo. Porównuje
wygenerowane pliki, instrukcje kompatybilne oraz pliki assetów z hashami.
Ostrzeżenia o niepotwierdzonych danych są oczekiwane i nie oznaczają awarii CI.
Nie wolno ich usuwać przez automatyczne nadanie statusu CONFIRMED.

`python3 scripts/brain.py report` pokazuje braki offline. Nie przeprowadza
pomiarów marketingowych ani nie aktualizuje faktów. Test raportu sprawdza
powtarzalność i brak zmian wejściowych danych, nie skuteczność biznesową.

## Scenariusze zachowania agentów

[agent_scenarios.json](agent_scenarios.json) zawiera 11 zadań z wersji 3.0.
[context_scenarios.json](context_scenarios.json) dodaje 7 zadań rozszerzenia.
Łącznie 18 scenariuszy, wszystkie NOT_RUN. Test struktury zestawu nie jest
wykonaniem odpowiedzi modeli.

Aby je ocenić, uruchom prompt w agencie z wczytanym Company Brain i zbadaj
wszystkie kryteria. Zapisz osobny publiczny, bezpieczny raport: ID scenariusza,
wersja / commit wiedzy, model i środowisko, data, odpowiedź lub dozwolony
fragment, oceniający i wynik PASS / FAIL / BLOCKED. Brak uruchomienia to NOT_RUN,
a brak dostępu do zależności to BLOCKED, nie PASS.
Zachowaj bazowe zestawy jako niezmienione szablony testów.

Testy kodu nie dowodzą, że model zawsze zastosuje się do instrukcji.
Instalacje Codex, Claude Code i Hermes wymagają osobnych testów wczytania.
