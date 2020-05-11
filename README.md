# Gomoku
[Link do projektu na GitHub](https://github.com/pmasior/gomoku)

## Opis zadania:
* gra podobna do gry kółko i krzyżyk, w której celem jest ułożenie dokładnie pięciu kamieni swojego koloru w ciągłej linii na siatce o wielkości 15x15
* po uruchomieniu wyświetlany jest krótki opis gry, po kliknięciu w dowolne miejsce rozpoczyna się runda
* okno w trakcie gry wyświetla aktualnego gracza, który wykonuje ruch w lewym górnym rogu oraz siatkę 15x15
* pierwszy ruch wykonuje człowiek (czarne kamienie), klikając w jedno z miejsc, w których przecina się linia pozioma z linią pionową +
* następnie ruch wykonuje komputer (wykorzystanie algorytmu alfa-beta do wyznaczenia ruchu komputera)
* po zakończeniu gry w górnej części okna, pojawia się informacja o wygranej określonego gracza lub remisie (jednocześnie plansza jest wyświetlana, co umożliwia zobaczenie, w jaki sposób nastąpił koniec gry)
* po kliknięciu w dowolne miejsce w obrębie okna pojawia się plansza podsumowująca, ile tur zostało wygranych przez człowieka, a ile przez komputer, kliknięcie w dowolne miejsce spowoduje rozpoczęcie nowej tury
* w trakcie wyświetlania ekranów wprowadzających lub podsumowujących rozgrywkę, kliknięcie przycisku X (na górnym pasku zawierającym nazwę programu) powoduje natychmiastowe zamknięcie gry
* w trakcie rozgrywki kliknięcie przycisku X spowoduje wyświetlenie informacji, ile tur zostało wygranych przez człowieka, a ile przez komputer, a kliknięcie w dowolne miejsce spowoduje rozpoczęcie nowej tury

## Testy:
1. wykonanie dwóch przykładowych ruchów przez każdego z graczy
2. sprawdzenie czy ruch zostanie wykonany, gdy kliknięcie nastąpi poza obszarem planszy - oczekiwany brak ruchu i brak zmiany gracza, który wykonuje ruch
3. sprawdzenie czy poprawnie jest wykrywany remis, czyli gdy wszystkie pola na planszy są zajęte
4. sprawdzenie czy po wygranej gracza poprawnie jest ustawiany licznik wygranych
5. sprawdzenie czy wygrana, gdy będzie umieszczone więcej niż 5 kamieni w linii - oczekiwana kontynuacja gry
6. sprawdzenie czy wygrana, gdy gracz ułoży dokładnie 5 kamieni w poziomie - oczekiwana wygrana
7. sprawdzenie czy wygrana, gdy gracz ułoży dokładnie 5 kamieni w pionie - oczekiwana wygrana
8. sprawdzenie czy wygrana, gdy gracz ułoży dokładnie 5 kamieni po jednej przekątnej \  - oczekiwana wygrana
9. sprawdzenie czy wygrana, gdy gracz ułoży dokładnie 5 kamieni po drugiej przekątnej /  - oczekiwana wygrana
