Reddit sentiment, emotion and keyword analysis
1. Charakterystyka oprogramowania 
a. Nazwa skrócona  
Reddit SEK 
b. Nazwa pełna
Reddit Sentiment, Emotion and Keyword analysis app
c. Krótki opis ze wskazaniem celów 
Jeden dwa akapity
  Aplikacja pozwala na połączenie z API reddit'a w celu pobrania danych dla wpisanych słów kluczowych. Pobrane dane są wykorzystywane w celu zbadania analizy sentymentu prostą metodą TextBlob, wskazując liczbę komentarzy/postów pozytywnych, negatywnych oraz neutrolanych, analizę sentymentu modelem distilBERT (na pozytywne/negatywne), analizę emocji modelem distilBERT (na 6 klas- joy, angry, fear, love, surprise, sadness), zliczanie najczęściej występujących słów kluczowych (keyword analysis) wraz z wizualizacją wyników powyższych metod.
3. Prawa autorskie. 
a. Autorzy
Piotr Michalski
b. Warunki licencyjne do oprogramowania wytworzonego przez grupę
GNU General Public License v3.0

5. Specyfikacja wymagań
| Identyfikator | Nazwa                                      | Opis                                                                                      | Priorytet | Kategoria        |
|---------------|--------------------------------------------|-------------------------------------------------------------------------------------------|-----------|------------------|
| W01           | Pobieranie danych                          | Aplikacja umożliwia pobranie danych na wybrane tematy.                                      | 1         | Funkcjonalne     |
| W02           | Analiza danych                             | Użytkownik może przeprowadzić podstawowe analizy danych w interfejsie aplikacji.           | 1         | Funkcjonalne     |
| W03           | Zapisywanie wyników                        | Wyniki analizy są zapisywane w formie csv.                                                 | 1         | Funkcjonalne     |
| W05           | Intuicyjny interfejs                       | Aplikacja posiada prosty i intuicyjny interfejs użytkownika (GUI).                         | 1         | Pozafunkcjonalne |
| W06           | Wydajność                                  | Aplikacja działa sprawnie z dużą ilością danych.                                           | 1         | Pozafunkcjonalne |
| W07           | Bezpieczeństwo API                         | Dane pobierane przez bezpieczne połączenie z API Reddita.                                  | 1         | Pozafunkcjonalne |
| W08           | Wyświetlanie statystyk                     | Aplikacja wyświetla podsumowania w formie wykresów.                                        | 1         | Funkcjonalne     |
| W09           | Skalowalność                               | Aplikacja może być rozszerzana o nowe funkcje bez konieczności dużych zmian w kodzie.      | 2         | Pozafunkcjonalne |
| W10           | Instrukcja instalacji                      | Aplikacja posiada instrukcję instalacji i konfiguracji.                                    | 2         | Pozafunkcjonalne |
| W11           | Pobieranie bibliotek                       | Aplikacja sama pobiera potrzebne biblioteki do działania.                                  | 2         | Pozafunkcjonalne |
| W12           | Zabezpieczenie pobierania                  | Aplikacja nie pobierze danych, gdy identyczne już są pobrane.                              | 2         | Pozafunkcjonalne |
| W13           | Porównanie produktów                       | Aplikacja umożliwia wyświetlanie wyników dwóch produktów jednocześnie.                    | 1         | Funkcjonalne     |
| W14           | Wyświetlanie scoringu                      | Aplikacja wyświetla scoring dla porównania dwóch produktów, wskazując lepszy.             | 2         | Funkcjonalne     |
| W15           | Wyniki jednego produktu                    | Aplikacja umożliwia wyświetlanie wyników dla jednego produktu.                            | 1         | Funkcjonalne     |
| W16           | Wybór ilości komentarzy                    | Aplikacja pozwala na wybór liczby pobranych komentarzy użytkowników reddita.              | 3         | Funkcjonalne     |
| W17           | Automatyczne dostosowywanie liczby pobieranych komentarzy | Aplikacja, w zależności od liczby wybranych komentarzy, ustawia limity pobrania odpowiedzi z pojedynczego posta w celu uzyskania reprezentatywnych wyników. | 3         | Pozafunkcjonalne |



7. Architektura systemu/oprogramowania 
a. Architektura rozwoju - stos technologiczny w postaci wykazu 
składającego się z: nazwy, przeznaczenia, numeru wersji  
Narzędzie programistyczne i technologie informatyczne wykorzystywane 
podczas rozwoju oprogramowania 
b. Architektura uruchomieniowa - stos technologiczny w postaci wykazu 
składającego się z: nazwy, przeznaczenia, numeru wersji 
Narzędzie programistyczne i technologie informatyczne wymagane podczas 
wykonywania oprogramowania lub systemu w środowisku docelowym

8. Testy 
a. Scenariusze testów 
b. Sprawozdanie z wykonania scenariuszy testów
