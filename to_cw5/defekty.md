# Defekty aplikacji SklepTO

Testowana wersja: SklepTO 1.0, domyślna wersja studencka (`BUGI=true`).

## DEF-01 – Strona kontaktu ma pusty tytuł

- Wymaganie: REQ-UI-02
- Kroki: otworzyć `kontakt.php` i odczytać element `<title>`.
- Oczekiwany rezultat: `SklepTO – kontakt`.
- Rzeczywisty rezultat: tytuł jest pusty.
- Test: `test_page_has_descriptive_title[kontakt.php-...]`.

## DEF-02 – Obraz logo na stronie kontaktu nie ma tekstu alternatywnego

- Wymaganie: REQ-UI-03
- Kroki: otworzyć `kontakt.php` i sprawdzić atrybut `alt` obrazka.
- Oczekiwany rezultat: każdy obrazek ma niepusty atrybut `alt`.
- Rzeczywisty rezultat: obrazek `logo.svg` nie ma atrybutu `alt`.
- Test: `test_every_image_has_non_empty_alt_text`.

## DEF-03 – Pole e-mail na stronie kontaktu nie ma etykiety

- Wymaganie: REQ-UI-04
- Kroki: otworzyć `kontakt.php` i wyszukać `label[for="email"]`.
- Oczekiwany rezultat: widoczne pole e-mail ma powiązaną etykietę.
- Rzeczywisty rezultat: etykieta nie istnieje; użyto tylko placeholdera.
- Test: `test_contact_fields_have_associated_labels`.

## DEF-04 – Pole e-mail na stronie kontaktu ma niepoprawny typ

- Wymaganie: REQ-UI-05
- Kroki: otworzyć `kontakt.php` i odczytać typ pola `#email`.
- Oczekiwany rezultat: `type="email"`.
- Rzeczywisty rezultat: `type="text"`.
- Test: `test_contact_email_field_uses_email_type`.

## DEF-05 – Rejestracja akceptuje wielkie litery w loginie

- Wymaganie: REQ-REJ-02
- Kroki: zarejestrować poprawne konto z loginem `User123`.
- Oczekiwany rezultat: komunikat „Login musi mieć od 3 do 20 znaków (małe litery, cyfry, _).”
- Rzeczywisty rezultat: konto zostaje utworzone.
- Test: `test_uppercase_login_is_rejected`.

## DEF-06 – Rejestracja akceptuje wiek 100 lat

- Wymaganie: REQ-REJ-05
- Kroki: wysłać poprawny formularz rejestracji z wiekiem `100`.
- Oczekiwany rezultat: komunikat „Wiek musi być liczbą całkowitą z zakresu 18–99.”
- Rzeczywisty rezultat: konto zostaje utworzone.
- Test: `test_age_one_hundred_is_rejected`.

## DEF-07 – Poprawne logowanie nie zeruje licznika błędnych prób

- Wymaganie: REQ-LOG-02
- Kroki: raz podać błędne hasło dla `jan`, następnie zalogować się poprawnie i otworzyć panel Administracja.
- Oczekiwany rezultat: licznik nieudanych prób użytkownika `jan` wynosi `0`.
- Rzeczywisty rezultat: licznik nadal wynosi `1`.
- Test: `test_successful_login_resets_failed_attempt_counter`.

## DEF-08 – Karta i kod rabatowy naliczają 20% zamiast 15%

- Wymagania: REQ-KAL-03, REQ-KAL-08
- Kroki: obliczyć zamówienie 150 zł, zaznaczyć kartę, wpisać `student10`, wybrać kuriera.
- Oczekiwany rezultat: rabat `15%`, dostawa `0.00 zł`, do zapłaty `127.50 zł`.
- Rzeczywisty rezultat: rabat `20%`, dostawa `0.00 zł`, do zapłaty `120.00 zł`.
- Testy: `test_discount_combinations[...]`, `test_specification_calculator_example`.

## DEF-09 – Wysłane zamówienie można anulować

- Wymagania: REQ-ZAM-04, REQ-ZAM-05
- Kroki: zalogować się jako `jan` i sprawdzić akcje zamówienia #3 o statusie „Wysłane”.
- Oczekiwany rezultat: dostępna jest wyłącznie akcja „Potwierdź dostawę”.
- Rzeczywisty rezultat: aplikacja wyświetla również przycisk „Anuluj”.
- Test: `test_action_buttons_match_order_state[3-...]`.
