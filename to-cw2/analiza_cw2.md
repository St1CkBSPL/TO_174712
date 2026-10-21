# Analiza EP i AWB

Testy zaprojektowano wyłącznie na podstawie `SPECYFIKACJA.md`. Przyjęta
precyzja to: 1 punkt procentowy, 1 minuta, 1 znak hasła i 1 pełny rok.

## 1. `grade_from_percent`

### Klasy równoważności (EP)

| Klasa | Opis | Rodzaj | Wartość | Oczekiwany |
| --- | --- | --- | --- | --- |
| OC-K1 | 0–50 | poprawna | `25` | `2.0` |
| OC-K2 | 51–60 | poprawna | `55` | `3.0` |
| OC-K3 | 61–70 | poprawna | `65` | `3.5` |
| OC-K4 | 71–80 | poprawna | `75` | `4.0` |
| OC-K5 | 81–90 | poprawna | `85` | `4.5` |
| OC-K6 | 91–100 | poprawna | `95` | `5.0` |
| OC-N1 | mniej niż 0 | niepoprawna wartość | `-10` | `ValueError` |
| OC-N2 | więcej niż 100 | niepoprawna wartość | `110` | `ValueError` |
| OC-N3 | `float` | niepoprawny typ | `50.0` | `TypeError` |
| OC-N4 | `str` | niepoprawny typ | `"50"` | `TypeError` |
| OC-N5 | `NoneType` | niepoprawny typ | `None` | `TypeError` |
| OC-N6 | `bool` (jest podtypem `int`, ale specyfikacja go wyklucza) | niepoprawny typ | `True` | `TypeError` |

### Wartości brzegowe (AWB)

| Granica | 2p | 3p – dodatkowo | Oczekiwane |
| --- | --- | --- | --- |
| początek dziedziny 0 | `-1`, `0` | `1` | `ValueError`, `2.0`, `2.0` |
| 50 / 51 | `50`, `51` | `49`, `52` | `2.0`, `3.0`, `2.0`, `3.0` |
| 60 / 61 | `60`, `61` | `59`, `62` | `3.0`, `3.5`, `3.0`, `3.5` |
| 70 / 71 | `70`, `71` | `69`, `72` | `3.5`, `4.0`, `3.5`, `4.0` |
| 80 / 81 | `80`, `81` | `79`, `82` | `4.0`, `4.5`, `4.0`, `4.5` |
| 90 / 91 | `90`, `91` | `89`, `92` | `4.5`, `5.0`, `4.5`, `5.0` |
| koniec dziedziny 100 | `100`, `101` | `99` | `5.0`, `ValueError`, `5.0` |

Pokrycie: AWB 2p – 14/14 elementów; AWB 3p – dodatkowe 12/12,
łącznie 26/26.

## 2. `parking_fee`

### Klasy równoważności (EP)

| Klasa | Opis | Rodzaj | Wartość | Oczekiwany |
| --- | --- | --- | --- | --- |
| PK-K1 | 0–15 min, klasa wyjścia 0 zł | poprawna | `10` | `0.0` |
| PK-K2 | 16–60 min, klasa wyjścia 5 zł | poprawna | `30` | `5.0` |
| PK-K3 | 61–120 min, klasa wyjścia 10 zł | poprawna | `90` | `10.0` |
| PK-K4 | 121–180 min, klasa wyjścia 15 zł | poprawna | `150` | `15.0` |
| PK-K5 | 181–1440 min, klasa wyjścia 20 zł | poprawna | `600` | `20.0` |
| PK-N1 | mniej niż 0 | niepoprawna wartość | `-10` | `ValueError` |
| PK-N2 | więcej niż 1440 | niepoprawna wartość | `1500` | `ValueError` |
| PK-N3 | `float` | niepoprawny typ | `60.0` | `TypeError` |
| PK-N4 | `str` | niepoprawny typ | `"60"` | `TypeError` |
| PK-N5 | `NoneType` | niepoprawny typ | `None` | `TypeError` |
| PK-N6 | `bool` | niepoprawny typ | `True` | `TypeError` |

### Wartości brzegowe (AWB)

| Granica | 2p | 3p – dodatkowo | Oczekiwane |
| --- | --- | --- | --- |
| początek dziedziny 0 | `-1`, `0` | `1` | `ValueError`, `0.0`, `0.0` |
| 15 / 16 | `15`, `16` | `14`, `17` | `0.0`, `5.0`, `0.0`, `5.0` |
| 60 / 61 | `60`, `61` | `59`, `62` | `5.0`, `10.0`, `5.0`, `10.0` |
| 120 / 121 | `120`, `121` | `119`, `122` | `10.0`, `15.0`, `10.0`, `15.0` |
| 180 / 181 | `180`, `181` | `179`, `182` | `15.0`, `20.0`, `15.0`, `20.0` |
| koniec dziedziny 1440 | `1440`, `1441` | `1439` | `20.0`, `ValueError`, `20.0` |

Pokrycie: AWB 2p – 12/12 elementów; AWB 3p – dodatkowe 10/10,
łącznie 22/22.

## 3. `validate_password`

### Klasy równoważności (EP)

| Klasa | Opis | Rodzaj | Wartość | Oczekiwany |
| --- | --- | --- | --- | --- |
| HS-K1 | 8–20 znaków, litera i cyfra | poprawna | `"abc12345"` | `True` |
| HS-K2 | dozwolone znaki specjalne | poprawna | `"abc123#!"` | `True` |
| HS-K3 | dozwolona spacja | poprawna | `"abc 1234"` | `True` |
| HS-K4 | dozwolone polskie litery | poprawna | `"żółć1234"` | `True` |
| HS-N1 | brak litery | niepoprawna wartość | `"12345678"` | `False` |
| HS-N2 | brak cyfry | niepoprawna wartość | `"abcdefgh"` | `False` |
| HS-N3 | mniej niż 8 znaków | niepoprawna wartość | `"a1a1a1a"` | `False` |
| HS-N4 | więcej niż 20 znaków | niepoprawna wartość | `"a1a1a1a1a1a1a1a1a1a1a"` | `False` |
| HS-N5 | `NoneType` | niepoprawny typ | `None` | `TypeError` |
| HS-N6 | liczba | niepoprawny typ | `12345678` | `TypeError` |
| HS-N7 | kolekcja | niepoprawny typ | `["haslo123"]` | `TypeError` |

### Wartości brzegowe długości (AWB)

| Granica | 2p | 3p – dodatkowo | Oczekiwane |
| --- | --- | --- | --- |
| 7 / 8 znaków | `7`, `8` | `6`, `9` | `False`, `True`, `False`, `True` |
| 20 / 21 znaków | `20`, `21` | `19`, `22` | `True`, `False`, `True`, `False` |

Wartości generuje `password_of_length`, więc każda poza długością spełnia
warunek obecności litery i cyfry. Pokrycie: AWB 2p – 4/4 elementy; AWB 3p –
dodatkowe 4/4, łącznie 8/8.

Hasło długości 20 z polskimi literami, np. `Zażółć12345678901234`, powinno
zwrócić `True`: polskie litery spełniają HS-3, a długość 20 należy do zakresu.

Minimalny zestaw Each Choice dla cech „litera obecna/nieobecna” i „cyfra
obecna/nieobecna”, przy poprawnej długości, ma 3 testy:

1. `"a1aaaaaa"` – litera i cyfra obecne → `True`;
2. `"12345678"` – brak litery → `False`;
3. `"abcdefgh"` – brak cyfry → `False`.

## 4. `ticket_price`

### Klasy równoważności (EP)

| Klasa | Opis | Rodzaj | Wartość | Oczekiwany |
| --- | --- | --- | --- | --- |
| BL-K1 | 0–6, bilet bezpłatny | poprawna | `3` | `0.0` |
| BL-K2 | 7–18, ulgowy dziecięcy | poprawna | `12` | `10.0` |
| BL-K3 | 19–64, normalny | poprawna | `40` | `20.0` |
| BL-K4 | 65–120, ulgowy seniorski | poprawna | `70` | `10.0` |
| BL-N1 | mniej niż 0 | niepoprawna wartość | `-10` | `ValueError` |
| BL-N2 | więcej niż 120 | niepoprawna wartość | `130` | `ValueError` |
| BL-N3 | `float` | niepoprawny typ | `18.0` | `TypeError` |
| BL-N4 | `str` | niepoprawny typ | `"18"` | `TypeError` |
| BL-N5 | `NoneType` | niepoprawny typ | `None` | `TypeError` |
| BL-N6 | `bool` | niepoprawny typ | `True` | `TypeError` |

### Wartości brzegowe (AWB)

| Granica | 2p | 3p – dodatkowo | Oczekiwane |
| --- | --- | --- | --- |
| początek dziedziny 0 | `-1`, `0` | `1` | `ValueError`, `0.0`, `0.0` |
| 6 / 7 | `6`, `7` | `5`, `8` | `0.0`, `10.0`, `0.0`, `10.0` |
| 18 / 19 | `18`, `19` | `17`, `20` | `10.0`, `20.0`, `10.0`, `20.0` |
| 64 / 65 | `64`, `65` | `63`, `66` | `20.0`, `10.0`, `20.0`, `10.0` |
| koniec dziedziny 120 | `120`, `121` | `119` | `10.0`, `ValueError`, `10.0` |

Pokrycie: AWB 2p – 10/10 elementów; AWB 3p – dodatkowe 8/8,
łącznie 18/18.

## Podsumowanie pokrycia

- EP: wszystkie zidentyfikowane klasy wejść i wyjść są reprezentowane.
- AWB 2p: 40/40 elementów (100%).
- AWB 3p: 34/34 elementy dodatkowe (100%), łącznie z 2p: 74/74 (100%).

# Defekty

Pierwsze uruchomienie dało `9 failed, 117 passed`. Polecenie
`python -m pytest --lf -q` ponownie uruchomiło te same 9 porażek. Po analizie
zgrupowano je w 5 defektów. Przypadki wykrywające defekty mają ścisłe znaczniki
`xfail`, więc nie ukrywają nieoczekiwanej naprawy (`strict=True`).

## DEF-01 – `grade_from_percent` akceptuje niedozwolone typy

| Pole | Treść |
| --- | --- |
| Wymaganie | OC-4 |
| Kroki | Wywołać kolejno `grade_from_percent(50.0)`, `grade_from_percent("50")`, `grade_from_percent(True)`. |
| Oczekiwany | Każde wywołanie zgłasza `TypeError`. |
| Rzeczywisty | Żadne z wywołań nie zgłasza `TypeError`. |
| Test | `test_ep_wrong_type[float/string/bool]` |
| Technika | EP; AWB wartości całkowitych nie wykryłaby tego defektu. |
| Ważność | wysoka – naruszenie kontraktu typów i niejawna konwersja danych |

## DEF-02 – dla 90% zwracana jest ocena 5.0 zamiast 4.5

| Pole | Treść |
| --- | --- |
| Wymaganie | OC-2 |
| Kroki | Wywołać `grade_from_percent(90)`. |
| Oczekiwany / rzeczywisty | `4.5` / `5.0` |
| Test | `test_bva_2p[good-plus-upper]` |
| Technika | AWB 2p; wybrane wartości EP i dodatkowe AWB 3p nie wykryły defektu. |
| Ważność | wysoka – zawyżona ocena końcowa |

## DEF-03 – minuta postoju kosztuje 5 zł zamiast 0 zł

| Pole | Treść |
| --- | --- |
| Wymaganie | PK-2 |
| Kroki | Wywołać `parking_fee(1)`. |
| Oczekiwany / rzeczywisty | `0.0` / `5.0` |
| Test | `test_bva_3p_extra[min-inside]` |
| Technika | AWB 3p; wartość typowa EP oraz punkty AWB 2p tej klasy przechodzą. |
| Ważność | wysoka – naliczenie opłaty za bezpłatny postój |

## DEF-04 – dozwolone znaki specjalne i spacje unieważniają hasło

| Pole | Treść |
| --- | --- |
| Wymaganie | HS-4 |
| Kroki | Wywołać `validate_password("abc123#!")` oraz `validate_password("abc 1234")`. |
| Oczekiwany / rzeczywisty | `True` / `False` dla obu haseł |
| Test | `test_ep_valid[special-characters/space]` |
| Technika | EP; AWB długości nie wykryłaby defektu składu. |
| Ważność | średnia – odrzucenie haseł dozwolonych przez wymagania |

## DEF-05 – wiek 119 i 120 lat jest błędnie poza dziedziną

| Pole | Treść |
| --- | --- |
| Wymaganie | BL-1, BL-2 |
| Kroki | Wywołać `ticket_price(119)` i `ticket_price(120)`. |
| Oczekiwany | `10.0` dla obu wartości. |
| Rzeczywisty | `ValueError` dla obu wartości. |
| Test | `test_bva_3p_extra[max-inside]`, `test_bva_2p[max]` |
| Technika | AWB 2p i AWB 3p; typowa wartość EP dla seniora przechodzi. |
| Ważność | wysoka – poprawne dane wejściowe są odrzucane |
