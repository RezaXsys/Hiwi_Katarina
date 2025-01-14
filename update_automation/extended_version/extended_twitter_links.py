import requests
import json
from collections import defaultdict
from datetime import datetime
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


# Überprüft, ob ein Link gültig ist 
def validate_link(link):
    try: 
        response = requests.head(link, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False 
    

# Überprüft die Alternativen und gibt eine Liste der gültigen zurück 
def validate_links(alternatives):
    valid_links = []
    for link in alternatives:
        if validate_link(link):
            valid_links.append(link)
    return valid_links

# Hauptfunktion zur Verarbeitung der Links. Speichter Labels und Themen von Tweets, wenn Links geköscht werden 
# Statistik- und Label-Sammlung 
#   - Zählt die Anzahl gelöschter Links pro Label 
#   - Speichert die Details von gelöschten Links 
#   - Speichter die aktualisierten Links 

def process_links(file_path, log_path):

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
        label = item.get('label', "Unknown") # TODO Warum Unknown 
        tweet_context = item.get('tweet', "Unknown")

        if validate_link(main_link): # Überprüfung des Hauptlinks 
            updated_data.append(item)
            continue 

        valid_alternatives = validate_links(alternatives) # Wird ausgeführt, wenn Hauptlink ungültig ist 
        if valid_alternatives:
            item['main'] = valid_alternatives[0]
            updated_data.append(item)
            replaced_count += 1
        else:
            invalid_count += 1
            label_statistics[label] += 1
            deleted_links.append({
                "main": main_link,
                "label": label,
                "tweet": tweet_context
            })

    # in image_links schreiben 
    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)
    # log datei schreiben 
    with open(log_path, 'w') as log_file:
        log_file.write("Gelöschte Links und Statistik:\n")
        for link in deleted_links:
            log_file.write(f"Gelöscht: {link['main']} (Label: {link['label']}, Tweet: {link['tweet']})\n")
        log_file.write("\nStatistik:\n")
        for label, count in label_statistics.items():
            log_file.write(f"{label}: {count} gelöscht Links\n")

    print(f"Überprüfung abgeschlossen: {replaced_count} ersetzt, {invalid_count} ungültig.")
    print("Statistik geschrieben.")



def process_links_with_time_stats(file_path, log_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Statistik- und Zeitdaten
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

    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)

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

    print(f"Überprüfung abgeschlossen: {replaced_count} ersetzt, {invalid_count} ungültig.")

def export_deleted_links_to_csv(deleted_links, csv_path):
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['main', 'label', 'tweet', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for link in deleted_links:
            writer.writerow(link)

    print(f"CSV-Datei erstellt unter: {csv_path}")


nltk.download('punkt')
nltk.download('stopwords')

def categorize_tweet(tweet_context):
    """
    Kategorisiert einen Tweet basierend auf Schlüsselwörtern.
    """
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


# Main
process_links('image_links.json', 'link_check.log')
export_deleted_links_to_csv(deleted_links, 'deleted_links.csv')
tweet_context = "Discussion about global temperature rising due to climate change."
print(categorize_tweet(tweet_context))  # Gibt "Klimawandel" zurück
label = item.get('label', categorize_tweet(tweet_context))