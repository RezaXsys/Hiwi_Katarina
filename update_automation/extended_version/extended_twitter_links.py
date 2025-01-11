import requests
import json
from collections import defaultdict
from datetime import datetime
import csv

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



    # Main
    process_links('image_links.json', 'link_check.log')