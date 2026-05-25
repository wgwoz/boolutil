========================================================================
DOKUMENTACJA TECHNICZNA: STRUKTURA I DZIAŁANIE CZĘŚCI FRONTENDOWEJ
========================================================================

1. OPIS OGÓLNY MODUŁU
------------------------------------------------------------------------
Niniejszy moduł stanowi warstwę prezentacji (front-end) aplikacji webowej 
dedykowanej analizie oraz minimalizacji funkcji logicznych. 

Głównym celem modułu jest zebranie danych wejściowych od użytkownika i 
przygotowanie ich do wysyłki w formacie akceptowalnym przez warstwę 
backendową. Użytkownik ma do dyspozycji dwie niezależne metody 
definiowania funkcji logicznej:
  A. Wpisanie formuły tekstowej z klawiatury.
  B. Wygenerowanie i interaktywne uzupełnienie tabeli prawdy.

2. STOS TECHNOLOGICZNY (TECHNOLOGY STACK)
------------------------------------------------------------------------
* Język programowania: JavaScript (wersja ES6+)
* Podejście architektoniczne: Vanilla JS (czysty kod, brak zewnętrznych 
  frameworków typu React, Vue czy Angular).
* Renderowanie interfejsu: Dynamiczne manipulowanie strukturą DOM 
  (Document Object Model) z poziomu kodu JavaScript.
* Stylizowanie: Stylowanie wbudowane bezpośrednio w obiekty JS 
  (In-line styling) w celu zachowania autonomii pliku skryptu.

3. ARCHITEKTURA I STRUKTURA PLIKÓW
------------------------------------------------------------------------
Moduł został zaprojektowany tak, aby zminimalizować narzut strukturalny. 
W środowisku produkcyjnym i deweloperskim frontend składa się z dwóch 
kluczowych plików umieszczonych w katalogu frontendowym:

  frontend/
  ├── index.html   - Główny plik osadzający warstwę aplikacji.
  └── app.js       - Główny plik wykonywalny zawierający logikę i interfejs.

4. SZCZEGÓŁOWY OPIS FUNKCJONALNOŚCI (DZIAŁANIE)
------------------------------------------------------------------------

SEKCJA 1: Wprowadzanie tekstowe funkcji
* Komponenty: Pole tekstowe typu 'text' (input) z placeholderem oraz 
  przycisk akcji (button) "Wyślij funkcję".
* Działanie: Umożliwia użytkownikowi wpisanie jawnej postaci funkcji 
  logicznej (np. przy użyciu operatorów AND, OR, NOT). Sekcja ta stanowi 
  punkt wejścia pod parser tekstu, który w kolejnych etapach rozwoju 
  projektu może automatycznie mapować tekst na stany tabeli.

SEKCJA 2: Interaktywny Generator Tabeli Prawdy
* Komponenty: Selektor liczby zmiennych (input typu 'number' obsługujący 
  wartości w zakresie 1-5), przycisk "Generuj tabelę" oraz kontener dynamiczny.
* Algorytm generowania wierszy: Liczba wierszy w tabeli jest ściśle 
  zależna od wprowadzonej liczby zmiennych (n) i wynosi dokładnie 2^n 
  (kombinacji dwójkowych).
* Przekształcenie binarne: Iteracja pętli generującej wiersze konwertuje 
  indeks pętli na postać binarną za pomocą metody `.toString(2)`. Brakujące 
  bity są automatycznie dopełniane zerami z lewej strony za pomocą 
  funkcji `.padStart(ileZmiennych, '0')`, gwarantując pełną reprezentację 
  wszystkich stanów wejściowych (od X1 do Xn).

SEKCJA 3: Trójstanowa kolumna wynikowa (0 / 1 / -)
* Działanie: Zamiast statycznych wartości, w kolumnie "Wynik (Y)" każdy 
  wiersz posiada dedykowany przycisk oznaczony domyślnie jako '0'.
* Logika cykliczna: Do przycisków przypisano detektor zdarzeń kliknięcia 
  (EventListener), który przełącza stan przycisku w pętli zamkniętej:
  -> Jeśli aktualna wartość to '0' -> zmień na '1'
  -> Jeśli aktualna wartość to '1' -> zmień na '-' (stan nieokreślony / don't care)
  -> Jeśli aktualna wartość to '-' -> powróć do '0'
* Zastosowanie: Obsługa stanu nieokreślonego '-' jest kluczowa w zadaniach 
  minimalizacji układów cyfrowych (np. tablice Karnaugh), pozwalając na 
  optymalizację struktur logicznych na etapie backendowym.

5. INTEGRACJA I TRANSMISJA DANYCH (INTERFEJS API)
------------------------------------------------------------------------
Moduł posiada w pełni zaimplementowaną logikę agregacji danych przed 
wysyłką do API backendu. 

Po kliknięciu przycisku "Wyślij wyniki z tabeli":
1. Program uruchamia selektor `.querySelectorAll('.wynik-btn')`, pobierając 
   referencje do wszystkich przycisków stanów wynikowych w tabeli.
2. Wartości tekstowe ('0', '1', '-') są sekwencyjnie przepisywane do 
   płaskiej tablicy indeksowanej (`zebraneWyniki`).
3. Kolejność elementów w tablicy idealnie odpowiada naturalnemu porządkowi 
   kombinacji binarnych wierszy tabeli.

Format przesyłanego pakietu danych (Payload):
Dane są przygotowane w postaci tablicy łańcuchów znaków (String). Przykład 
struktury danych dla 2 zmiennych wejściowych (4 kombinacje):

  [ "0", "1", "-", "1" ]

W aktualnej wersji deweloperskiej przygotowana paczka danych jest 
wyprowadzana na konsolę programistyczną przeglądarki (klawisz F12 -> sekcja 
Console) w celach diagnostycznych, a użytkownik jest informowany o 
sukcesie operacji komunikatem systemowym alert().
========================================================================