import subprocess
import sys

required_libraries = [
    "textblob", 
    "transformers", 
    "tkinter", 
    "matplotlib", 
    "praw", 
    "pandas", 
    "nltk", 
    "wordcloud", 
    #"Pillow",
    "tensorflow",
    #"torch",
    "tf_keras"

]

def install_missing_libraries():
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            print(f"Biblioteka '{lib}' nie jest zainstalowana. Instalowanie...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"Biblioteka '{lib}' została zainstalowana.")
            
install_missing_libraries()

import os
import csv
from textblob import TextBlob
from transformers import pipeline, AutoTokenizer
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import praw
import glob
import pandas as pd
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re
from wordcloud import WordCloud
from io import BytesIO
from PIL import ImageTk, Image
from keys_reddit import client_id, client_secret, user_agent  # Import kluczy do API Reddit

try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')
#nltk.download('punkt')

def fetch_reddit_data(product_name,  technology, max_comments, max_comments_per_post=None):
    

    # Sprawdzamy, czy plik z danymi już istnieje
    output_csv = f'Data\\{product_name}_{max_comments}.csv'
    if os.path.exists(output_csv):
        # Jeśli dane zostały już pobrane, wyświetl komunikat w oknie aplikacji
        results_text.insert(tk.END, f"Data for {product_name} already fetched and saved in '{output_csv}'.\n")
        return output_csv  # Zwracamy nazwę pliku bez ponownego pobierania danych
    
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    subreddit = reddit.subreddit('all')  # Szukaj we wszystkich subredditch

    # Dostosowanie max_comments_per_post na podstawie liczby postów
    if max_comments >= 5000:
        max_comments_per_post = 150
    elif max_comments >= 2500 and max_comments < 5000:
        max_comments_per_post = 100
    elif max_comments >= 1500 and max_comments < 2500:
        max_comments_per_post = 75
    elif max_comments >= 1000 and max_comments < 1500:
        max_comments_per_post = 50
    elif max_comments >= 500 and max_comments < 1000:
        max_comments_per_post = 35
    elif max_comments >= 250 and max_comments < 500:
        max_comments_per_post = 20
    elif max_comments >= 100 and max_comments < 250:
        max_comments_per_post = 12
    else:
        max_comments_per_post = 10

    # Obliczamy liczbę postów na podstawie max_comments i max_comments_per_post
    max_posts = max_comments // max_comments_per_post if max_comments is not None else 10  # Przykładowa wartość domyślna to 10 postów

    with open(output_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Post Title', 'Post URL', 'Comment Author', 'Comment Body', 'Comment Score'])

        total_comment_count = 0  # Licznik pobranych komentarzy

        for post in subreddit.search(product_name, limit=max_posts):  # Wyszukiwanie w Reddit
            if total_comment_count >= max_comments:  # Jeśli pobrano już max_comments komentarzy, przerwij
                break

            post.comments.replace_more(limit=0)

            # Zbiór do przechowywania unikalnych użytkowników
            seen_users = set()

            comment_count = 0  # Licznik komentarzy w danym poście
            for comment in post.comments.list():
                if total_comment_count >= max_comments:  # Jeśli osiągnięto łączny limit, przerwij
                    break
                if comment_count >= max_comments_per_post:  # Limit komentarzy na post
                    break

                # Sprawdzamy, czy użytkownik już skomentował
                if comment.author in seen_users:
                    continue  # Jeśli tak, pomijamy ten komentarz

                # Dodajemy autora do zbioru
                seen_users.add(comment.author)

                writer.writerow([post.title, post.url, comment.author, comment.body, comment.score])
                comment_count += 1
                total_comment_count += 1  # Zwiększenie liczby pobranych komentarzyselect_csv_for_analysis

    return output_csv

def refresh_csv_list():
    """Odświeża listę plików CSV w obu Comboboxach."""
    csv_files = glob.glob("Data\\*.csv")  # Szuka wszystkich plików CSV w katalogu
    csv_var_1.set("")  # Resetuje wybór w pierwszym Comboboxie
    csv_var_2.set("")  # Resetuje wybór w drugim Comboboxie
    csv_dropdown['values'] = csv_files  # Aktualizuje wartości w pierwszym Comboboxie
    csv_dropdown_2['values'] = csv_files  # Aktualizuje wartości w drugim Comboboxie
    
    if csv_files:
        print("CSV list updated.")
    else:
        print("No CSV files found.")

def get_product_name_from_csv(csv_file):
    # Wyciągnij nazwę pliku z pełnej ścieżki
    file_name = os.path.basename(csv_file)  # np. 'phonea_100.csv'
    
    # Usuń rozszerzenie .csv z nazwy pliku
    product_name = os.path.splitext(file_name)[0]  # np. 'phonea_100'
    
    return product_name

def update_checkboxes():
    selected_option = analysis_var.get()
    if selected_option == "TextBlob":
        textblob_var.set(True)
        bert_sentiment_var.set(False)
        bert_emotion_var.set(False)
        keyword_var.set(False)
    elif selected_option == "BERT Sentiment":
        textblob_var.set(False)
        bert_sentiment_var.set(True)
        bert_emotion_var.set(False)
        keyword_var.set(False)

    elif selected_option == "Emotion Analysis":
        textblob_var.set(False)
        bert_sentiment_var.set(False)
        bert_emotion_var.set(True)
        keyword_var.set(False)
    
    elif selected_option == "Keyword Analysis":
        textblob_var.set(False)
        bert_sentiment_var.set(False)
        bert_emotion_var.set(False)
        keyword_var.set(True)

def sentiment_analysis_textblob(input_csv, max_comments=None):
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    total_comments = 0

    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            comment_body = row['Comment Body']
            total_comments += 1

            if max_comments and total_comments > max_comments:
                break

            blob = TextBlob(comment_body)
            sentiment = blob.sentiment.polarity

            if sentiment > 0.1:
                positive_count += 1
            elif sentiment < -0.1:
                negative_count += 1
            else:
                neutral_count += 1

    return positive_count, negative_count, neutral_count, total_comments

def sentiment_analysis_bert(input_csv, max_comments=None):
    # Załaduj tokenizer do modelu BERT
    tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
    sentiment_pipeline = pipeline("sentiment-analysis", model='distilbert-base-uncased-finetuned-sst-2-english', tokenizer=tokenizer)

    positive_count = 0
    negative_count = 0
    total_comments = 0

    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            comment_body = row['Comment Body']
            total_comments += 1

            if max_comments and total_comments > max_comments:
                break

            # Tokenizacja i przycinanie tekstu do 512 tokenów
            tokens = tokenizer.encode(comment_body, truncation=True, max_length=512, padding=False)

            # Konwertujemy tokeny z powrotem na tekst
            truncated_comment = tokenizer.decode(tokens, skip_special_tokens=True)

            result = sentiment_pipeline(truncated_comment)[0]
            label = result['label']

            if label == 'POSITIVE':
                positive_count += 1
            elif label == 'NEGATIVE':
                negative_count += 1

    return positive_count, negative_count, total_comments

def emotion_analysis_distilbert(input_csv, max_comments=None):
    # Załaduj tokenizer do modelu DistilBERT
    tokenizer = AutoTokenizer.from_pretrained('bhadresh-savani/distilbert-base-uncased-emotion')
    emotion_pipeline = pipeline('sentiment-analysis', model='bhadresh-savani/distilbert-base-uncased-emotion', tokenizer=tokenizer)

    emotion_counts = {}
    total_comments = 0

    with open(input_csv, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            comment_body = row['Comment Body']
            total_comments += 1

            if max_comments and total_comments > max_comments:
                break

            # Tokenizacja i przycinanie tekstu do 512 tokenów
            tokens = tokenizer.encode(comment_body, truncation=True, max_length=512, padding=False)

            # Konwertujemy tokeny z powrotem na tekst
            truncated_comment = tokenizer.decode(tokens, skip_special_tokens=True)

            # Analiza emocji
            emotion_scores = emotion_pipeline(truncated_comment)[0]  # Teraz wynik to słownik

            # Jeśli wynik jest słownikiem, otrzymujemy dominującą emocję
            if isinstance(emotion_scores, dict):
                dominant_emotion = emotion_scores['label']
            else:
                # Jeśli wynik jest listą, wybieramy ten z najwyższym wynikiem
                dominant_emotion = max(emotion_scores, key=lambda x: x['score'])['label']

            if dominant_emotion in emotion_counts:
                emotion_counts[dominant_emotion] += 1
            else:
                emotion_counts[dominant_emotion] = 1

    return emotion_counts, total_comments

def keyword_analysis(input_csv, max_comments=None):
    # Otwieramy plik CSV i zbieramy teksty z tytułów postów oraz komentarzy
    all_texts = []  # Lista, do której będą dodawane teksty postów i komentarzy
    total_comments = 0  # Licznik przetworzonych komentarzy

    with open(input_csv, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Pomijamy nagłówek

        for row in reader:
            post_title = row[0]  # Tytuł posta
            comment_body = row[3]  # Treść komentarza

            # Jeśli istnieje limit komentarzy i osiągnięto go, przerywamy
            if max_comments and total_comments >= max_comments:
                break

            # Dodajemy tytuł postu oraz komentarz do listy tekstów (przekształcone na małe litery)
            all_texts.append(post_title.lower())
            all_texts.append(comment_body.lower())

            total_comments += 1  # Zwiększamy licznik przetworzonych komentarzy

    # Jeśli nie przetworzono żadnych komentarzy
    if total_comments == 0:
        results_text.insert(tk.END, "No comments found to analyze.\n")
        return

    # Analiza słów kluczowych
    all_text = ' '.join(all_texts)

    # Usuwanie znaków specjalnych i liczb
    all_text = re.sub(r'[^a-zA-Z\s]', '', all_text)

    # Usuwanie stop słów (domyślnie angielskich, ale można dostosować do innych języków)
    stop_words = set(stopwords.words('english'))  # Można zmienić język, np. 'polish' w przypadku polskich postów
    filtered_words = [word for word in all_text.split() if word not in stop_words]

    # Liczenie częstotliwości słów
    word_counts = Counter(filtered_words)

    # Wybieramy top 10 najczęściej występujących słów
    top_words = word_counts.most_common(15)
    return top_words, total_comments
    
def plot_results(frame, analysis_results_1, analysis_results_2, analysis_type, product_1, product_2):
    # Usuń poprzednie wykresy
    for widget in frame.winfo_children():
        widget.destroy()

    emotion_order = ['joy', 'anger', 'fear', 'sadness', 'love', 'surprise']

    # Tworzymy wykres dla produktu 1
    fig_1 = Figure(figsize=(5, 4), dpi=100)
    ax_1 = fig_1.add_subplot(111)

    if analysis_type == "TextBlob":
        labels = ['Positive', 'Negative', 'Neutral']
        counts_1 = analysis_results_1[:3]
        ax_1.bar(labels, counts_1, color=['green', 'red', 'blue'])
    elif analysis_type == "Sentiment":
        labels = ['Positive', 'Negative']
        counts_1 = analysis_results_1[:2]
        ax_1.bar(labels, counts_1, color=['green', 'red'])
    elif analysis_type == "Emotion":
        labels_1 = emotion_order
        counts_1 = [analysis_results_1.get(label, 0) for label in labels_1]
        ax_1.bar(labels_1, counts_1)
    elif analysis_type == "Keyword":
        wordcloud_1 = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(analysis_results_1)
        fig_1 = plt.figure(figsize=(5, 4))
        plt.imshow(wordcloud_1, interpolation="bilinear")
        plt.axis("off")
        buf = BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        img = Image.open(buf)
        img = ImageTk.PhotoImage(img)
        label = tk.Label(frame, image=img)
        label.image = img
        label.pack()
        plt.close(fig_1)

    ax_1.set_title(f'{analysis_type.capitalize()} Analysis for {product_1}')
    ax_1.set_xlabel('Category')
    ax_1.set_ylabel('Counts')

    if analysis_type != "Keyword":
        canvas_1 = FigureCanvasTkAgg(fig_1, master=frame)
        canvas_1.draw()
        canvas_1.get_tk_widget().pack()

    # Jeśli analiza jest tylko dla jednego produktu, nie tworzymy wykresu dla produktu 2
    if analysis_results_2 is not None:
        # Tworzymy wykres dla produktu 2
        fig_2 = Figure(figsize=(5, 4), dpi=100)
        ax_2 = fig_2.add_subplot(111)

        if analysis_type == "TextBlob":
            counts_2 = analysis_results_2[:3]
            ax_2.bar(labels, counts_2, color=['green', 'red', 'blue'])
        elif analysis_type == "Sentiment":
            counts_2 = analysis_results_2[:2]
            ax_2.bar(labels, counts_2, color=['green', 'red'])
        elif analysis_type == "Emotion":
            labels_2 = emotion_order
            counts_2 = [analysis_results_2.get(label, 0) for label in labels_2]
            ax_2.bar(labels_2, counts_2)
        elif analysis_type == "Keyword":
            wordcloud_2 = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(analysis_results_2)
            fig_2 = plt.figure(figsize=(5, 4))
            plt.imshow(wordcloud_2, interpolation="bilinear")
            plt.axis("off")
            buf = BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            img = Image.open(buf)
            img = ImageTk.PhotoImage(img)
            label = tk.Label(frame, image=img)
            label.image = img
            label.pack()
            plt.close(fig_2)

        ax_2.set_title(f'{analysis_type.capitalize()} Analysis for {product_2}')
        ax_2.set_xlabel('Category')
        ax_2.set_ylabel('Counts')

        if analysis_type != "Keyword":
            canvas_2 = FigureCanvasTkAgg(fig_2, master=frame)
            canvas_2.draw()
            canvas_2.get_tk_widget().pack()

def perform_analysis():
    results_text.delete("1.0", tk.END)
    
    # Get selected CSV file paths from the Comboboxes
    selected_csv_1 = csv_var_1.get()
    selected_csv_2 = csv_var_2.get()
    
    # Check if both CSV files are selected
    if not selected_csv_1 and not selected_csv_2:
        results_text.insert(tk.END, "Please select CSV file for any product first.\n")
        return

    # Get product names from selected CSV files
    selected_product_1 = get_product_name_from_csv(selected_csv_1) if selected_csv_1 else None
    selected_product_2 = get_product_name_from_csv(selected_csv_2) if selected_csv_2 else None
    
    # If any product name is None, stop the analysis
    if not selected_product_1:
        return

    scoring_1 = 0
    scoring_2 = 0

    good_emotions = {'joy', 'love', 'surprise'}
    bad_emotions = {'anger', 'fear', 'sadness'}

    # Perform the analysis for the selected products
    max_comments_input = max_comments_var.get()
    max_comments = None if max_comments_input == "max" else int(max_comments_input)

    # Analyze for product 1
    if selected_csv_1:
        if textblob_var.get():
            tb_results_1 = sentiment_analysis_textblob(selected_csv_1, max_comments)
            total_comments_1 = sum(tb_results_1)
            positive_percentage_1 = (tb_results_1[0] / total_comments_1) * 200 if total_comments_1 > 0 else 0
            negative_percentage_1 = (tb_results_1[1] / total_comments_1) * 200 if total_comments_1 > 0 else 0
            neutral_percentage_1 = (tb_results_1[2] / total_comments_1) * 200 if total_comments_1 > 0 else 0
            scoring_1 += tb_results_1[0] - tb_results_1[1]

            results_text.insert(tk.END, f"Product 1 (TextBlob Analysis):\n")
            results_text.insert(tk.END, f"Positive: {tb_results_1[0]} ({positive_percentage_1:.2f}%)\n")
            results_text.insert(tk.END, f"Negative: {tb_results_1[1]} ({negative_percentage_1:.2f}%)\n")
            results_text.insert(tk.END, f"Neutral: {tb_results_1[2]} ({neutral_percentage_1:.2f}%)\n")
            results_text.insert(tk.END, f"\n\n")

        if bert_sentiment_var.get():
            bert_results_1 = sentiment_analysis_bert(selected_csv_1, max_comments)
            total_comments_1_bert = sum(bert_results_1)
            positive_percentage_1_bert = (bert_results_1[0] / total_comments_1_bert) * 200 if total_comments_1_bert > 0 else 0
            negative_percentage_1_bert = (bert_results_1[1] / total_comments_1_bert) * 200 if total_comments_1_bert > 0 else 0
            scoring_1 += bert_results_1[0] - bert_results_1[1]

            results_text.insert(tk.END, f"Product 1 (BERT Sentiment Analysis):\n")
            results_text.insert(tk.END, f"Positive: {bert_results_1[0]} ({positive_percentage_1_bert:.2f}%)\n")
            results_text.insert(tk.END, f"Negative: {bert_results_1[1]} ({negative_percentage_1_bert:.2f}%)\n")
            results_text.insert(tk.END, f"\n\n")

        if bert_emotion_var.get():
            emotion_counts_1, total_comments_1 = emotion_analysis_distilbert(selected_csv_1, max_comments)
            emotion_percentages_1 = {emotion: (count / total_comments_1) * 100 for emotion, count in emotion_counts_1.items()}
             # Calculate emotion-based scoring for product 1
            for emotion, count in emotion_counts_1.items():
                if emotion in good_emotions:
                    scoring_1 += count
                elif emotion in bad_emotions:
                    scoring_1 -= count

            results_text.insert(tk.END, "Product 1 (Emotion Analysis):\n")
            for emotion, count in emotion_counts_1.items():
                results_text.insert(tk.END, f"{emotion}: {count} ({emotion_percentages_1[emotion]:.2f}%)\n")
            results_text.insert(tk.END, f"\nTotal Comments Analyzed for Product 1: {total_comments_1}\n")
            results_text.insert(tk.END, f"\n\n")

        if keyword_var.get():
            top_words_1, total_comments_1 = keyword_analysis(selected_csv_1, max_comments)
            results_text.insert(tk.END, f"Top 15 most frequent words comments for Product 1:\n")
            for word, count in top_words_1:
                results_text.insert(tk.END, f"{word}: {count}\n")
            results_text.insert(tk.END, f"\n")

    # Analyze for product 2 (only if the second CSV is selected)
    if selected_csv_2:
        if textblob_var.get():
            tb_results_2 = sentiment_analysis_textblob(selected_csv_2, max_comments)
            total_comments_2 = sum(tb_results_2)
            positive_percentage_2 = (tb_results_2[0] / total_comments_2) * 200 if total_comments_2 > 0 else 0
            negative_percentage_2 = (tb_results_2[1] / total_comments_2) * 200 if total_comments_2 > 0 else 0
            neutral_percentage_2 = (tb_results_2[2] / total_comments_2) * 200 if total_comments_2 > 0 else 0
            scoring_2 += tb_results_2[0] - tb_results_2[1]

            results_text.insert(tk.END, f"Product 2 (TextBlob Analysis):\n")
            results_text.insert(tk.END, f"Positive: {tb_results_2[0]} ({positive_percentage_2:.2f}%)\n")
            results_text.insert(tk.END, f"Negative: {tb_results_2[1]} ({negative_percentage_2:.2f}%)\n")
            results_text.insert(tk.END, f"Neutral: {tb_results_2[2]} ({neutral_percentage_2:.2f}%)\n")
            results_text.insert(tk.END, f"\n\n")

        if bert_sentiment_var.get():
            bert_results_2 = sentiment_analysis_bert(selected_csv_2, max_comments)
            total_comments_2_bert = sum(bert_results_2)
            positive_percentage_2_bert = (bert_results_2[0] / total_comments_2_bert) * 200 if total_comments_2_bert > 0 else 0
            negative_percentage_2_bert = (bert_results_2[1] / total_comments_2_bert) * 200 if total_comments_2_bert > 0 else 0
            scoring_2 += bert_results_2[0] - bert_results_2[1]

            results_text.insert(tk.END, f"Product 2 (BERT Sentiment Analysis):\n")
            results_text.insert(tk.END, f"Positive: {bert_results_2[0]} ({positive_percentage_2_bert:.2f}%)\n")
            results_text.insert(tk.END, f"Negative: {bert_results_2[1]} ({negative_percentage_2_bert:.2f}%)\n")
            results_text.insert(tk.END, f"\n\n")

        if bert_emotion_var.get():
            emotion_counts_2, total_comments_2 = emotion_analysis_distilbert(selected_csv_2, max_comments)
            emotion_percentages_2 = {emotion: (count / total_comments_2) * 100 for emotion, count in emotion_counts_2.items()}
            # Calculate emotion-based scoring for product 2
            for emotion, count in emotion_counts_2.items():
                if emotion in good_emotions:
                    scoring_2 += count
                elif emotion in bad_emotions:
                    scoring_2 -= count
            results_text.insert(tk.END, "Product 2 (Emotion Analysis):\n")
            for emotion, count in emotion_counts_2.items():
                results_text.insert(tk.END, f"{emotion}: {count} ({emotion_percentages_2[emotion]:.2f}%)\n")
            results_text.insert(tk.END, f"\nTotal Comments Analyzed for Product 2: {total_comments_2}\n")
            results_text.insert(tk.END, f"\n\n")

        if keyword_var.get():
            top_words_2, total_comments_2 = keyword_analysis(selected_csv_2, max_comments)
            results_text.insert(tk.END, f"Top 15 most frequent words comments for Product 2:\n")
            for word, count in top_words_2:
                results_text.insert(tk.END, f"{word}: {count}\n")
            results_text.insert(tk.END, f"\n")

    if not keyword_var.get():
        results_text.insert(tk.END, f"Scoring Results:\n")
        results_text.insert(tk.END, f"Product 1 Scoring: {scoring_1}\n")
        if selected_csv_2:
            results_text.insert(tk.END, f"Product 2 Scoring: {scoring_2}\n")
            if scoring_1 > scoring_2:
                results_text.insert(tk.END, f"Product 1 is better based on scoring.\n")
            elif scoring_1 < scoring_2:
                results_text.insert(tk.END, f"Product 2 is better based on scoring.\n")
            else:
                results_text.insert(tk.END, f"Both products have the same scoring.\n")
        else:
            results_text.insert(tk.END, f"Scoring only available for Product 1.\n")



    if textblob_var.get():
        if selected_csv_2:
            plot_results(plot_frame, tb_results_1, tb_results_2, "TextBlob", "Product 1", "Product 2")
        else:
            plot_results(plot_frame, tb_results_1, None, "TextBlob", "Product 1", "Product 2")
            
    if bert_sentiment_var.get():
        if selected_csv_2:
            plot_results(plot_frame, bert_results_1, bert_results_2, "Sentiment", "Product 1", "Product 2")
        else:
            plot_results(plot_frame, bert_results_1, None, "Sentiment", "Product 1", "Product 2")

    if bert_emotion_var.get():
        if selected_csv_2:
            plot_results(plot_frame, emotion_counts_1, emotion_counts_2, "Emotion", "Product 1", "Product 2")
        else:
            plot_results(plot_frame, emotion_counts_1, None, "Emotion", "Product 1", "Product 2")

    if keyword_var.get():
        if selected_csv_2:
            keyword_data_1 = dict(top_words_1)
            keyword_data_2 = dict(top_words_2)
            plot_results(plot_frame, keyword_data_1, keyword_data_2, "Keyword", "Product 1", "Product 2")
        else:
            keyword_data_1 = dict(top_words_1)
            plot_results(plot_frame, keyword_data_1, None, "Keyword", "Product 1", "Product 2")

def fetch_and_analyze():
    product_name = product_name_entry.get()
    max_comments_input = max_comments_var.get()
    max_comments = None if max_comments_input == "max" else int(max_comments_input)

    if not product_name:
        results_text.insert(tk.END, "Please enter a product name.\n")
        return

    results_text.insert(tk.END, f"Fetching Reddit data for '{product_name}'...\n")
    try:
        global input_csv
        input_csv = fetch_reddit_data(product_name, "all", max_comments)  # Usunięcie `technology`

        results_text.insert(tk.END, f"Data fetched successfully and saved to '{input_csv}'.\n")
    except Exception as e:
        results_text.insert(tk.END, f"Error fetching data: {e}\n")


# GUI setup
root = tk.Tk()
root.title("Reddit Data Fetcher and Analyzer")
root.geometry("1200x800")

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Left frame
left_frame = tk.Frame(main_frame)
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=1, pady=1)

# Right frame
right_frame = tk.Frame(main_frame)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=1, pady=1)




# Checkboxes
textblob_var = tk.BooleanVar(value=True)
bert_sentiment_var = tk.BooleanVar(value=False)
bert_emotion_var = tk.BooleanVar(value=False)
keyword_var = tk.BooleanVar(value=False)



analysis_var = tk.StringVar(value="TextBlob")  # Domyślnie wybrana opcja

tk.Radiobutton(left_frame, text="TextBlob Analysis", variable=analysis_var, value="TextBlob", command=update_checkboxes).pack(anchor='w')
tk.Radiobutton(left_frame, text="BERT Sentiment Analysis", variable=analysis_var, value="BERT Sentiment", command=update_checkboxes).pack(anchor='w')
tk.Radiobutton(left_frame, text="Emotion Analysis (DistilBERT)", variable=analysis_var, value="Emotion Analysis", command=update_checkboxes).pack(anchor='w')
tk.Radiobutton(left_frame, text="Keyword Analysis", variable=analysis_var, value="Keyword Analysis", command=update_checkboxes).pack(anchor='w')

# Create a frame to hold the two product entry widgets side by side
product_frame = tk.Frame(left_frame)
product_frame.pack(pady=5)

# Create separate variables for each Combobox
csv_var_1 = tk.StringVar()  # For the first Combobox
csv_var_2 = tk.StringVar()  # For the second Combobox

# Combobox for choosing CSV file (under product 1)
tk.Label(product_frame, text="Choose product (1)").grid(row=2, column=0, pady=5)
csv_dropdown = ttk.Combobox(product_frame, textvariable=csv_var_1, width=30)
csv_dropdown.grid(row=3, column=0, padx=5, pady=5)


# Combobox for choosing CSV file (under product 2)
tk.Label(product_frame, text="Choose product (2):").grid(row=2, column=1, pady=5)
csv_dropdown_2 = ttk.Combobox(product_frame, textvariable=csv_var_2, width=30)
csv_dropdown_2.grid(row=3, column=1, padx=5, pady=5)

tk.Button(left_frame, text="Refresh CSV List", command=refresh_csv_list).pack(pady=5)
refresh_csv_list()  # Wywołanie funkcji po załadowaniu GUI

# Analysis button
tk.Button(left_frame, text="Perform Analysis", command=perform_analysis).pack(pady=10)

# Results text area
results_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=50, height=20)
results_text.pack(pady=10)

# Plot frame
plot_frame = tk.Frame(right_frame)
plot_frame.pack(fill=tk.BOTH, expand=True)

# Product name input
tk.Label(left_frame, text="Enter product name:").pack()
product_name_entry = tk.Entry(left_frame, width=30)
product_name_entry.pack(pady=5)
product_name_entry.insert(0, "")

# Max comments selection
tk.Label(left_frame, text="Max Comments:").pack()
max_comments_var = tk.StringVar(value="100")
max_comments_dropdown = ttk.Combobox(left_frame, textvariable=max_comments_var, values=["100", "1000", "5000", "10000"])
max_comments_dropdown.pack(pady=5)

# Fetch data button
tk.Button(left_frame, text="Fetch Reddit Data", command=fetch_and_analyze).pack(pady=10)


# Start the application
root.mainloop()

# TUTAJ TEST #