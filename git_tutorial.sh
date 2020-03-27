#!/bin/bash
echo "You should run gomoku.py file"
exit 1
echo "This file is executing"

git init  # inicjowanie nowego repozytorium

git status  # status plików (zmodyfikowane, śledzone, zatwierdzone)
git diff  # pokazuje dokładne zmiany między katalogiem roboczym a przechowalnią
git diff --staged  # pokazuje dokładne zmiany między przechowalnią a repozytorium
git log  # lista commitów
git log --oneline  # lista commitów (1 commit na linię)

git add .  # dodaj wszystkie pliki do przechowalni
git commit -m "Treść commita"  # wysłanie nowego commita
    # przeniosi pliki z przechowalni do repozytorium

git push -u origin develop  # aktualizacja do zdalnego repozytorium
    # o (lokalnej) nazwie origin na gałąź develop
git push  # aktualizacja zdalnego repozytorium

git fetch origin  # pobieranie ze zdalnego repozytorium o (lokalnej) nazwie origin

git branch develop  # stworzenie nowej gałęzi o nazwie develop
git checkout develop  # przełączenie na gałąź develop

git config user.email "pmasior@outlook.com"  # ustawianie maila do identyfikacji, kto wprowadza zmiany
git config user.name "pmasior"  # ustawianie nazwy użytkownika do identyfikacji, kto wprowadza zmiany
git remote add origin https://github.com/pmasior/gomoku.git  # dodanie repozytorium zdalnego
    # o lokalnej nazwie origin z adresu https://github.com/pmasior/gomoku.git
