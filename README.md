# boolutil
Tool for help with logic gates and functions

Wszechstronne narzędzie do projektowania układów na bramkach logicznych i przerzutnikach. Projekt łączy intuicyjny interfejs przeglądarkowy z potężnym silnikiem matematycznym w Pythonie, umożliwiając łatwą analizę, upraszczanie i transformację funkcji logicznych.

## Zespół Projektowy

Projekt realizowany w ramach metodyki SCRUM.

* **Frontend:** Maciej Karolak, Jan Habdas
* **Backend:** Wiktor Gwoździewicz, Piotr Jaworski

##  Główne funkcjonalności

* **Wprowadzanie wyrażeń z klawiatury:** Inteligentny parser obsługujący popularne operatory logiczne (AND, OR, NOT, XOR) w wielu formatach notacyjnych (np. `*`, `+`, `!`, `~`, `&`, `|`).
* **Interaktywne tabele prawdy:** Dynamiczny generator tabeli prawdy (obsługa od 1 do 5 zmiennych). Posiada innowacyjny system wprowadzania stanów za pomocą cyklicznych przycisków (`0` -> `1` -> `-` jako stan nieokreślony "don't care").
* **Upraszczanie funkcji logicznych:** Automatyczna redukcja wprowadzonych równań do najprostszej postaci minimalnej.
* **Konwersja na bramki NAND:** Transformacja równań logicznych do postaci możliwej do zaimplementowania wyłącznie za pomocą uniwersalnych bramek NAND.

##  Założenia i status projektu

Obecna wersja aplikacji skupia się na dostarczeniu stabilnego fundamentu operacyjnego:
- [x] Backend wykrywający zmienne i formatujący wyrażenia.
- [x] Logika upraszczania funkcji oraz konwersji do postaci NAND.
- [x] Interfejs użytkownika z generatorem tabel prawdy.
- [x] Integracja API pomiędzy warstwą Frontend a Backend.
- [ ] Renderowanie graficznych schematów bramek (planowane w przyszłych wydaniach).

##  Technologie

* **Frontend:** Czysty JavaScript (Vanilla JS), HTML5, CSS3.
* **Backend:** Python 3, FastAPI (obsługa REST API), Pydantic (walidacja danych).
* **Silnik logiczny:** SymPy (biblioteka do obliczeń symbolicznych).

## Usprawnienia

Silnik bez problemu interpretuje różne konwencje zapisu. Równania:
* `A AND B`
* `A * B`
* `A n B`
Zostaną zinterpretowane tak samo jako koniunkcja logiczna.
