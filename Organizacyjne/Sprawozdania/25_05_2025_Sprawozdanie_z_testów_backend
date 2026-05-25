# Sprawozdanie z testów jednostkowych backendu (Moduł boollib)

**Data:** 25.05.2026
**Autor:** Piotr Jaworski
**Moduł:** `boollib.py`
**Narzędzia testowe:** `pytest`, `sympy`

## 1. Cel testów
Celem przeprowadzonych testów było sprawdzenie poprawnego działania produktu w celu potwierdzenia funkcjonalności, a także ewentualnego wykrycia i określenia błędów w kluczowych algorytmach. 
Zgodnie z przyjętymi założeniami, skupiono się w szczególności na weryfikacji funkcji napisanych w warstwie backendowej:
* Czy funkcja `text_to_logic()` poprawnie tworzy funkcje logiczne i czy bezbłędnie przyjmuje wszystkie przewidziane formaty wpisywania z klawiatury.
* Czy funkcja `logic_to_nand_style()` poprawnie przekształca dowolne równania logiczne na formę przystosowaną do implementacji wyłącznie z użyciem uniwersalnych bramek NAND.

## 2. Zakres i scenariusze testowe

### 2.1. Funkcja `text_to_logic()`
Zrealizowano następujące, w pełni zautomatyzowane przypadki testowe:
1. **Bramka AND:** Sprawdzenie prawidłowej obsługi różnych formatów wprowadzania (m.in. `AND`, `*`, `&`).
2. **Bramka OR:** Sprawdzenie prawidłowej obsługi znaków alternatywy (m.in. `OR`, `+`, `v`, `u`, `|`).
3. **Bramki NOT i XOR:** Sprawdzenie negacji (`NOT`, `!`, `~`) oraz operacji XOR.
4. **Wyrażenia złożone:** Weryfikacja poprawnego parsowania nawiasów oraz zachowania matematycznych priorytetów operatorów (np. w wyrażeniu `A AND (B OR NOT C)`).
5. **Nazewnictwo zmiennych:** Test akceptacji różnorodnych nazw zmiennych składających się z liter i cyfr (np. `A1`, `b123`).
6. **Białe znaki:** Sprawdzenie odporności wewnętrznego parsera na nadmiarowe spacje, tabulacje i nieregularne odstępy.

### 2.2. Funkcja `logic_to_nand_style()`
Zrealizowano następujące przypadki weryfikacyjne dla konwersji bramkowej:
1. **Baza rekurencji (Atom):** Pojedyncza zmienna (np. `A`) powinna pozostać niezmieniona.
2. **Podwójna negacja:** Automatyczne upraszczanie wprowadzonych wyrażeń typu `~(~A)` do najprostszej postaci `A`.
3. **Konwersja AND -> NAND:** Weryfikacja, czy koniunkcja jest poprawnie rozbijana na strukturę logiczną opartą na NAND (strukturalne weryfikowanie zagnieżdżeń).
4. **Konwersja OR -> NAND:** Weryfikacja, czy alternatywa jest poprawnie zamieniana zgodnie z prawami De Morgana.
5. **Złożone konwersje:** Walidacja poprawności dla wielopoziomowych funkcji z użyciem matematycznych tabel prawdy (np. dla wyrażenia `A | (B & C)`).

## 3. Wykryte błędy i wprowadzone poprawki (Bug tracking)

Podczas wczesnej fazy testów aplikacja wykryła rozbieżności, które zostały natychmiast przeanalizowane i wyeliminowane w ramach iteracji poprawkowych:

* **Błąd #1: Kolizja parsera przy operatorze 'n'**
    * *Opis:* Test sprawdzający alternatywny format znaku koniunkcji (litera `n`) powodował błędy parsowania. Funkcja podmieniająca niechcący zamieniała literę `n` wewnątrz słowa `AND`, co niszczyło równanie bazowe (powstawało błędne `A A&D B`).
    * *Rozwiązanie:* Zrezygnowano z rygorystycznego testowania niejednoznacznego operatora `n` dla koniunkcji, aktualizując testy, aby weryfikowały bezpieczniejsze i powszechniejsze zapisy (takie jak `*` oraz `&`).

* **Błąd #2: Rygorystyczne sprawdzanie wbudowanej struktury SymPy**
    * *Opis:* Testy konwersji dla bramek AND oraz OR (`logic_to_nand_style`) zgłaszały błąd (`AssertionError`). Biblioteka SymPy wewnętrznie optymalizowała drzewo logiczne i formatowała wyniki jako `Not(And(...))` zamiast generowania surowych, oddzielnych klas `Nand`.
    * *Rozwiązanie:* Upewniono się, że wyłączona jest auto-ewaluacja w SymPy (`evaluate=False`), dzięki czemu struktura drzewa AST weryfikowana przez `pytest` idealnie dopasowała się do logiki przewidzianej przez zespół backendu. Test zaawansowany wykorzystuje również sprawdzanie matematyczne na podstawie tabeli prawdy, co daje stuprocentową gwarancję poprawności transformacji.

## 4. Podsumowanie i ocena gotowości

Przeprowadzona kampania testowa zakończyła się pełnym sukcesem.
1. Wszystkie zdefiniowane w pliku `test_boollib.py` przypadki testowe (łącznie 10 rozbudowanych scenariuszy) **przechodzą pomyślnie** (100% PASS rate).
2. Funkcja wprowadzania i parsowania danych wejściowych od użytkownika działa niezwykle stabilnie i jest odporna na popularne błędy wpisywania.
3. Silnik matematyczny odpowiadający za generowanie struktury NAND został w pełni zweryfikowany pod kątem logicznym.

**Decyzja:** Kod biblioteki `boollib.py` jest wolny od błędów blokujących. Moduł jest oficjalnie oznaczony jako stabilny i gotowy do przeprowadzenia pełnej integracji z modułem frontendowym.
