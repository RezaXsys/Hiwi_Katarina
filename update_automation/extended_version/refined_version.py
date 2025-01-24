import requests
import json
from collections import defaultdict, Counter
from datetime import datetime
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# NLTK-Setup: Kann bei Bedarf erweitert werden 
nltk.download('punkt')
nltk.download('stopwords')

# ________________ Methoden ___________________________

#   Überprüft, ob ein Link gültig ist
def validate_link(link):
    try:
        response = requests.head(link, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

#   Überprüft Alternativlinks und gibt eine Liste der gültigen zurück
def validate_links(alternatives):
    return [link for link in alternatives if validate_link(link)]

#    Kategorisiert einen Tweet basierend auf Schlüsselwörtern

def categorize_tweet(tweet_context):
  
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(tweet_context.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Definierte Schlüsselwörter für Kategorien
    categories = {
        "Klimawandel": ["climate", "temperature", "global", "warming"],
        "Politik": ["politics", "government", "election", "policy"],
        "Technologie": ["technology", "innovation", "AI", "software"]
    }

    category_counts = Counter()
    for word in filtered_words:
        for category, keywords in categories.items():
            if word in keywords:
                category_counts[category] += 1

    # Wähle die häufigste Kategorie oder "Unknown"
    return category_counts.most_common(1)[0][0] if category_counts else "Unknown"


# ________________ Hauptfunktion ___________________________

def export_deleted_links_to_csv(deleted_links, csv_path):

    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['main', 'label', 'tweet', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for link in deleted_links:
            writer.writerow(link)

    print(f"CSV-Datei erstellt unter: {csv_path}")

#       Hauptfunktion zur Verarbeitung von Links, Erstellung von Logs und einer CSV-Datei

def process_links(file_path, log_path, csv_path):
    """
    Hauptfunktion zur Verarbeitung von Links, Erstellung von Logs und einer CSV-Datei.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)

    label_statistics = defaultdict(int)
    time_statistics = defaultdict(int)
    deleted_links = []
    updated_data = []
    replaced_count = 0
    invalid_count = 0

    for item in data:
        main_link = item['main']
        alternatives = item['alternatives']
        label = item.get('label', "Unknown")
        tweet_context = item.get('tweet', "Unknown")
        tweet_date = item.get('date', "Unknown")  # Erwartet ein Datum im Format YYYY-MM-DD

        if validate_link(main_link):
            updated_data.append(item)
            continue

        valid_alternatives = validate_links(alternatives)
        if valid_alternatives:
            item['main'] = valid_alternatives[0]
            updated_data.append(item)
            replaced_count += 1
        else:
            invalid_count += 1
            label_statistics[label] += 1
            if tweet_date != "Unknown":
                # Monat extrahieren
                month = datetime.strptime(tweet_date, "%Y-%m-%d").strftime("%Y-%m")
                time_statistics[month] += 1
            deleted_links.append({
                "main": main_link,
                "label": label,
                "tweet": tweet_context,
                "date": tweet_date
            })

    # JSON aktualisieren
    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)

    # Log-Datei schreiben
    with open(log_path, 'w') as log_file:
        log_file.write("Gelöschte Links und Statistik:\n")
        for link in deleted_links:
            log_file.write(f"Gelöscht: {link['main']} (Label: {link['label']}, Tweet: {link['tweet']}, Datum: {link['date']})\n")
        log_file.write("\nStatistik:\n")
        for label, count in label_statistics.items():
            log_file.write(f"{label}: {count} gelöschte Links\n")
        log_file.write("\nZeitliche Statistik:\n")
        for month, count in time_statistics.items():
            log_file.write(f"{month}: {count} gelöschte Links\n")

    # CSV-Datei exportieren
    export_deleted_links_to_csv(deleted_links, csv_path)

    print(f"Überprüfung abgeschlossen: {replaced_count} ersetzt, {invalid_count} ungültig.")


def main():
    
    input_file = 'image_links.json'
    log_file = 'link_check.log'
    csv_file = 'deleted_links.csv'

    # Links verarbeiten
    process_links(input_file, log_file, csv_file)

    # Beispiel für Kategorisierung eines Tweets
    tweet_context = "Discussion about global temperature rising due to climate change."
    category = categorize_tweet(tweet_context)
    print(f"Beispielkategorisierung: '{tweet_context}' -> Kategorie: {category}")


if __name__ == "__main__":
    main()