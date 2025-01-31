# Hiwi_Katarina
Climate Data Set 


## Installed Packages and Versions

This project uses the following key Python packages and their versions:

* aiohttp: 3.9.5
* anaconda-client: 1.11.0
* autopep8: 1.6.0
* bokeh: 2.4.3
* flask: 1.1.2
* jupyterlab: 3.4.4
* matplotlib: 3.9.4
* numpy: 1.24.4
* pandas: 1.4.4
* scikit-learn: 1.0.2
* scipy: 1.13.1
* seaborn: 0.11.2
* torch: 2.2.2
* torchvision: 0.17.2
* ultralytics: 8.3.56
  
For the full list of installed packages and versions, refer to the requirements.txt file or the detailed package output.
## Environment Setup Script  

This script generates the necessary files (`requirements.txt` and `env.yml`) to document and recreate the Python environment used in this project.  

### Features  
- Extracts installed **Conda** and **Pip** packages  
- Saves package lists to `requirements.txt`  
- Generates an `env.yml` file for easy environment recreation  

### Usage  

Run the script to generate the files:  
```bash
python generate_env_files.py
```

### Output Files  
1. **`requirements.txt`** – Lists all installed Conda and Pip packages  
2. **`env.yml`** – A Conda environment file for easy replication  

## Recreating the Environment

To create a new Conda environment using `env.yml`:  
```bash
conda env create -f env.yml
```

To install dependencies from `requirements.txt`:  
```bash
pip install -r requirements.txt
```

### Prerequisites  
Ensure you have **Conda** and **Pip** installed before running the script.


# **Project Overview**  

This repository contains two main modules:  

1. **Image Classification and Comparison (`clip_weapon_detection`)** – Uses **OpenAI's CLIP model** to detect weapons in images and compares results with **Roboflow's ground truth labels**.  
2. **Link Validation and Tweet Categorization (`update_automation`)** – Validates image links, replaces broken ones, logs deleted links, and categorizes tweets.  

---

## **FOLDER 1: Image Classification and Comparison - `clip_weapon_detection`**  

### **Overview**  
This module classifies images as **"weapon"** or **"not weapon"** using **OpenAI's CLIP model** and compares the results with **Roboflow's ground truth labels**.  

### **Features**  
✅ Loads and processes **Roboflow weapon classification results**  
✅ Uses **CLIP model** to classify images  
✅ Compares CLIP results with **Roboflow ground truth**  
✅ Computes **precision, recall, and F1-score** for multiple thresholds  
✅ Saves correctly classified **weapon images**  

### **Usage**  
Run the script to classify images and generate comparison statistics:  
```bash
python clip_weapon_detection.py
```

### **Input**  
- **`IMAGE_FOLDER`** → Directory containing images for classification  
- **`RESULTS_FILE`** → JSON file with Roboflow classification results  

### **Output**  
- **Matched weapon images** saved in **threshold-specific folders**  
- **`comparison_results.json`** → Accuracy statistics per threshold  

### **Customization**  
Modify the **thresholds** in the script to adjust classification sensitivity:  
```python
thresholds = [i * 0.1 for i in range(1, 10)]  # 0.1, 0.2, ..., 0.9
```

---

## **FOLDER 2: Link Validation and Tweet Categorization - `update_automation`**  

### **Overview**  
This module processes a **JSON file** containing **image links**, validates their accessibility, replaces broken links with alternatives, and categorizes tweets based on their content.  

### **Features**  
✅ **Validates image links** → Checks accessibility and replaces broken links  
✅ **Logs deleted links** → Stores broken links along with metadata  
✅ **Generates statistics** → Tracks deleted links per category over time  
✅ **Categorizes tweets** → Uses **NLTK** for content-based categorization  
✅ **Exports data to CSV** → Saves removed links in a structured format  

### **Methods**  

#### **1. Link Validation**  
- `validate_link(link)` → Checks if a given link is accessible.  
- `validate_links(alternatives)` → Returns a list of valid alternative links.  

#### **2. Processing and Logging**  
- `process_links(file_path, log_path)` → Processes and updates links, logs removed ones.  
- `export_deleted_links_to_csv(deleted_links, csv_path)` → Saves deleted links to a CSV file.  

#### **3. Tweet Categorization**  
- `categorize_tweet(tweet_context)` → Categorizes tweets based on keywords.  

### **Flow**  

#### **Dependencies:**  
Install required libraries:  
```bash
pip install requests nltk
```

#### **Run Scripts:**  
```bash
python update_automation.py
python tweet_categorization.py
```

### **Output Files**  
📂 `image_links.json` → Updated JSON with replaced links  
📂 `link_check.log` → Log file with deleted links and statistics  
📂 `deleted_links.csv` → CSV file containing details of removed links  

---

## **DEPENDENCIES**  
Ensure you have the necessary Python libraries installed:  
```bash
pip install torch transformers pillow tqdm requests nltk
```

Download required NLTK datasets:  
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```



## Violence Detection in Image Data Set - violence_detection

### Image Classification and Comparison - `clip_weapon_detection`
This module uses **OpenAI's CLIP model** to classify images as **weapon** or **not weapon**, then compares the results against **Roboflow's ground truth labels**.  

#### Functionality:
- Loads and processes weapon classification results from Roboflow  
- Runs CLIP model to classify images based on defined thresholds  
- Compares CLIP's predictions with Roboflow's ground truth  
- Calculates **precision, recall, and F1-score** for different thresholds  
- Saves correctly classified weapon images for analysis  

#### Usage: 
Run the script to classify images and generate comparison statistics:  
```bash
python clip_weapon_detection.py
```

#### Input: 
- **`IMAGE_FOLDER`** → Directory containing images for classification  
- **`RESULTS_FILE`** → JSON file with Roboflow classification results  

#### Output:  
- **Matched weapon images** saved in **threshold-specific folders**  
- **`comparison_results.json`** → Contains accuracy statistics per threshold  

#### Customization: 
Modify the **thresholds** in the script to adjust classification sensitivity:  
```python
thresholds = [i * 0.1 for i in range(1, 10)]  # 0.1, 0.2, ..., 0.9
```

---

### 2. Tweet Categorization - `tweet_categorization` 
A script that categorizes tweets into different topics using **NLTK-based keyword matching**.  

#### Functionality:
- Reads tweet text and categorizes it based on **predefined keywords**  
- Uses **NLTK tokenization** and **stopword removal** to improve accuracy  

#### Usage: 
Run the script to categorize a sample tweet:  
```bash
python tweet_categorization.py
```

#### Example:
```python
tweet = "Global temperatures are rising due to climate change."
category = categorize_tweet(tweet)
print(category)  # Output: "Klimawandel"
```

#### Customization:  
- Extend the `categories` dictionary in `categorize_tweet()` for additional topics.  

## DEPENDENCIES 
Ensure you have the necessary Python libraries installed:  
```bash
pip install torch transformers pillow tqdm nltk
```

Download required NLTK datasets:  
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```


