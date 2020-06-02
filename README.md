# Gomoku
[Link do projektu na GitHub](https://github.com/pmasior/gomoku)

## Opis zadania:
* gra podobna do gry kółko i krzyżyk, w której celem jest ułożenie dokładnie pięciu kamieni swojego koloru w ciągłej linii na siatce o wielkości 15x15, ułożenie linii dłuższej niż pięć kamieni nie skutkuje wygraną
* po uruchomieniu wyświetlany jest krótki opis gry, po kliknięciu w dowolne miejsce rozpoczyna się runda
* okno w trakcie gry wyświetla aktualnego gracza, który wykonuje ruch w lewym górnym rogu oraz siatkę 15x15
* pierwszy ruch wykonuje człowiek (czarne kamienie), klikając w jedno z miejsc, w których przecina się linia pozioma z linią pionową +
* następnie ruch wykonuje komputer (wykorzystanie algorytmu alfa-beta do wyznaczenia ruchu komputera)
* po zakończeniu gry w górnej części okna, pojawia się informacja o wygranej określonego gracza lub remisie (jednocześnie plansza jest wyświetlana, co umożliwia zobaczenie, w jaki sposób nastąpił koniec gry)
* po kliknięciu w dowolne miejsce w obrębie okna pojawia się plansza podsumowująca, ile tur zostało wygranych przez człowieka, a ile przez komputer, kliknięcie w dowolne miejsce spowoduje rozpoczęcie nowej tury
* w trakcie wyświetlania ekranów wprowadzających lub podsumowujących rozgrywkę, kliknięcie przycisku X (na górnym pasku zawierającym nazwę programu) powoduje natychmiastowe zamknięcie gry
* w trakcie rozgrywki kliknięcie przycisku X spowoduje wyświetlenie informacji, ile tur zostało wygranych przez człowieka, a ile przez komputer, a kliknięcie w dowolne miejsce spowoduje rozpoczęcie nowej tury

## Testy:
1. ułożenie dokładnie 5 kamieni po jednej przekątnej \  - oczekiwana wygrana
    * sprawdzenie czy wygrana w `check_winning_diagonally1(`) - oczekiwanie zwrócenia `True`
    * sprawdzenie czy wygrana w `check_winning()` - oczekiwanie zwrócenia `True`
2. ułożenie dokładnie 5 kamieni po drugiej przekątnej /  - oczekiwana wygrana
    * sprawdzenie czy wygrana w `check_winning_diagonally2()` - oczekiwanie zwrócenia `True`
    * sprawdzenie czy wygrana w `check_winning(`) - oczekiwanie zwrócenia `True`
3. ułożenie dokładnie 6 kamieni w poziomie - oczekiwanie braku wygranej 
    * sprawdzenie czy brak wygranej w `check_winning_horizontally()` - oczekiwanie zwrócenia `False`
    * sprawdzenie czy brak wygranej w `check_winning()` - oczekiwanie zwrócenia `None`
    * sprawdzenie czy gra nie została zakończona w `test_if_gameover()` - oczekiwanie, że `self.winner is None`
4. ułożenie dokładnie 6 kamieni w pionie - oczekiwanie braku wygranej 
    * sprawdzenie czy brak wygranej w `check_winning_horizontally()` - oczekiwanie zwrócenia `False`
    * sprawdzenie czy brak wygranej w `check_winning()` - oczekiwanie zwrócenia `None`
    * sprawdzenie czy gra nie została zakończona w `test_if_gameover()` - oczekiwanie, że `self.winner is None`
5. zapełnienie planszy tak, że żaden gracz nie wygrał - spodziewany remis
    * sprawdzenie czy brak wygranej w `check_winning()` - oczekiwanie zwrócenia `None`
    * sprawdzenie czy remis w `check_draw()` - oczekiwanie zwrócenia `True`
6. zamiana gracza 
    * sprawdzenie czy gracz został poprawnie zmieniony z `COMPUTER` na `HUMAN` w `change_player()` - oczekiwanie, że `self.next_player is c.HUMAN`