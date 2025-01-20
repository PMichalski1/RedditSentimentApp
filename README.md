
Reddit sentiment, emotion and keyword analysis
1. Charakterystyka oprogramowania 
a. Nazwa skrócona  
Reddit SEK analysis
b. Nazwa pełna
Reddit Sentiment, Emotion and Keyword analysis app
c. Krótki opis ze wskazaniem celów 
  Aplikacja pozwala na połączenie z API reddit'a w celu pobrania danych dla wpisanych słów kluczowych. Pobrane dane są wykorzystywane w celu zbadania analizy sentymentu prostą metodą TextBlob, wskazując liczbę komentarzy/postów pozytywnych, negatywnych oraz neutrolanych, analizę sentymentu modelem distilBERT (na pozytywne/negatywne), analizę emocji modelem distilBERT (na 6 klas- joy, angry, fear, love, surprise, sadness), zliczanie najczęściej występujących słów kluczowych (keyword analysis) wraz z wizualizacją wyników powyższych metod.
2. Prawa autorskie. 
a. Autorzy
Piotr Michalski
b. Warunki licencyjne do oprogramowania wytworzonego przez grupę
GNU General Public License v3.0

`3. Specyfikacja wymagań`
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

`4. a. Architektura systemu/oprogramowania `

| **Nazwa**       | **Przeznaczenie**                                      | **Nr wersji**     |
|-----------------|--------------------------------------------------------|-------------------|
| **Python**      | Środowisko uruchomieniowe do aplikacji                 | 3.9               |
| **textblob**    | Analiza tekstu i przetwarzanie języka naturalnego      | 0.18.0.post0      |
| **transformers**| Przetwarzanie języka naturalnego, modele NLP           | 4.47.0            |
| **matplotlib**  | Tworzenie wykresów i wizualizacja danych               | 3.8.1             |
| **praw**        | Interakcja z API Reddita                               | 7.8.1             |
| **pandas**      | Analiza danych w formacie tabelarycznym                 | 2.1.2             |
| **nltk**        | Natural Language Toolkit, przetwarzanie tekstów        | 3.8.1             |
| **wordcloud**   | Generowanie chmur słów                                 | 1.9.3             |
| **tensorflow**  | Tworzenie i trenowanie modeli uczenia maszynowego      | 2.18.0            |
| **tf_keras**    | Interfejs do pracy z Keras w TensorFlow                 | 2.18.0            |
| **os**          | Praca z systemem operacyjnym                            | -                 |
| **csv**         | Praca z plikami CSV                                    | -                 |
| **glob**        | Praca z plikami w systemie                             | -                 |
| **collections** | Praca z kontenerami i strukturami danych               | -                 |
| **re**          | Obsługa wyrażeń regularnych                            | -                 |
| **BytesIO**     | Obsługa danych binarnych w pamięci                     | -                 |
| **tkinter**     | Interfejs graficzny (GUI)                              | -                 |


`b. Architektura uruchomieniowa `
| **Nazwa**                   | **Przeznaczenie**                                      | **Nr wersji**     |
|-----------------------------|--------------------------------------------------------|-------------------|
| **Edytor kodu (np. Visual Studio Code)** | Włączenie aplikacji                              | -                 |
| **Przeglądarka internetowa** | Założenie konta Reddit, pobranie kluczy dostępu        | -                 |
| **Środowisko systemowe**     | System operacyjny, na którym aplikacja będzie działać  | Windows           |

`5. Testy`
| **Nr testu** | **Opis**                                              | **Kroki testowe**                                                                                             | **Oczekiwany wynik**                                                                                       | **Wynik** |
|--------------|-------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|-----------|
| T01          | Pobieranie danych                                     | 1. Uruchom aplikację 2. Wpisz temat do pobrania danych 3. Kliknij „Fetch reddit data”                          | Dane powinny zostać pobrane i zapisane w pliku CSV.                                                           | Działa        |
| T02          | Załadowanie danych dla jednego produktu              | 1. Uruchom aplikację 2. Załaduj dane dla jednego produktu                                                     | Aplikacja powinna umożliwia załadowanie danych dla jednego produktu.                                        | Działa        |
| T03          | Załadowanie danych dla dwóch produktów jednocześnie   | 1. Uruchom aplikację 2. Załaduj dane dla dwóch produktów jednocześnie                                          | Aplikacja powinna umożliwia załadowanie danych dla dwóch produktów jednocześnie.                            | Działa        |
| T04          | Wykonanie analizy TextBlob dla jednego produktu      | 1. Uruchom aplikację 2. Załaduj dane dla jednego produktu 3. Kliknij 'TextBlob Analysis' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy TextBlob dla jednego produktu w okienku tekstowym oraz wykres obok.       | Działa        |
| T05          | Wykonanie analizy TextBlob dla dwóch produktów       | 1. Uruchom aplikację 2. Załaduj dane dla dwóch produktów jednocześnie 3. Kliknij 'TextBlob Analysis' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy TextBlob dla dwóch produktów jednocześnie w okienku tekstowym oraz dwa wykresy obok. | Działa        |
| T06          | Wykonanie analizy Bert Sentiment dla jednego produktu | 1. Uruchom aplikację 2. Załaduj dane dla jednego produktu 3. Kliknij 'Bert Sentiment' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Bert Sentiment dla jednego produktu w okienku tekstowym oraz wykres obok. | Działa        |
| T07          | Wykonanie analizy Bert Sentiment dla dwóch produktów | 1. Uruchom aplikację 2. Załaduj dane dla dwóch produktów jednocześnie 3. Kliknij 'Bert Sentiment' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Bert Sentiment dla dwóch produktów jednocześnie w okienku tekstowym oraz dwa wykresy obok. | Działa        |
| T08          | Wykonanie analizy Bert Emotion dla jednego produktu  | 1. Uruchom aplikację 2. Załaduj dane dla jednego produktu 3. Kliknij 'Bert Emotion' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Bert Emotion dla jednego produktu w okienku tekstowym oraz wykres obok.  | Działa        |
| T09          | Wykonanie analizy Bert Emotion dla dwóch produktów   | 1. Uruchom aplikację 2. Załaduj dane dla dwóch produktów jednocześnie 3. Kliknij 'Bert Emotion' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Bert Emotion dla dwóch produktów jednocześnie w okienku tekstowym oraz dwa wykresy obok. | Działa        |
| T10          | Wykonanie analizy Keyword Analysis dla jednego produktu | 1. Uruchom aplikację 2. Załaduj dane dla jednego produktu 3. Kliknij 'Keyword analysis' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Keyword Analysis dla jednego produktu w okienku tekstowym oraz wykres obok. | Działa        |
| T11          | Wykonanie analizy Keyword Analysis dla dwóch produktów | 1. Uruchom aplikację 2. Załaduj dane dla dwóch produktów jednocześnie 3. Kliknij 'Keyword analysis' 4. Kliknij 'Perform Analysis' | Aplikacja wyświetli wyniki analizy Keyword Analysis dla dwóch produktów jednocześnie w okienku tekstowym oraz dwa wykresy obok. | Działa        |
