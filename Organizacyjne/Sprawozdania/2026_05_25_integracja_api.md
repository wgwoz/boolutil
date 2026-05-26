# Sprawozdanie — Integracja warstwy frontendowej z API backendu
**Data:** 25.05.2026
**Autor:** Maciej Karolak

## Opis zadania:
Zrealizowano pełną integrację interaktywnej tabeli prawdy z serwerem deweloperskim FastAPI (gałąź `Backend-W`).

## Zakres prac i rozwiązane problemy:
* **Mapowanie struktury danych:** Zaimplementowano funkcję w JavaScript agregującą stany przycisków (`1` oraz `-`) do formatu oczekiwanego przez endpoint `/expression/nand` (podział na mintermy i dont-cares).
* **Usunięcie błędu CORS / Preflight:** Zidentyfikowano i usunięto krytyczny błąd w pliku `api.py` związany z podwójną inicjalizacją instancji `FastAPI()`, która unieważniała reguły middleware CORS. Dodano poprawną konfigurację dla zapytań wstępnych `OPTIONS`.
* **Weryfikacja systemu:** Połączenie zostało pomyślnie przetestowane lokalnie — serwer poprawnie zwraca zminimalizowane wyrażenia logiczne oraz ich formę NAND, które są wyświetlane w interfejsie.

## Status:
Zadanie ukończone. Kod zintegrowany na gałęzi roboczej.