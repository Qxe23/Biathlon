## 🏔️ Biathlon Data Pipeline

This repository contains a **complete data pipeline to extract, clean, and engineer features from Biathlon World Cup results** using the `biathlonresults` API.  
The project is designed for **data science research, machine learning modeling, and performance analysis**.

---

# 📌 Project Overview
The goal of this project is to:
- Extract official biathlon race results from the IBU API
- Clean and standardize raw data
- Engineer advanced features (shooting accuracy, ski time, range time, etc.)
- Produce a ML-ready dataset for further analysis (performance prediction, fatigue modeling, injury risk, etc.)

This pipeline follows **data engineering best practices** (ETL separation, modular functions, reproducibility).

---

# 📂 Project Structure
```
biathlon-data-pipeline/
│
├── extract.py           # API extraction (raw data)
├── clean.py             # Data cleaning & feature engineering
├── requirements.txt
├── README.md
│
└── data/
    ├── raw/              # Raw API exports (CSV)
    └── processed/         # Cleaned datasets
```

---

# ⚙️ Installation

## 1️⃣ Clone the repository
```bash
git clone https://github.com/<your-username>/biathlon-data-pipeline.git
cd biathlon-data-pipeline
```

## 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- pandas
- tqdm
- biathlonresults

---

# 🚀 Usage

## 🧩 Step 1 — Extract Raw Data
```bash
python extract.py --season 2425 --out data/raw/all_races_2425.csv
```
This downloads all World Cup races for the selected season.

---

## 🧹 Step 2 — Clean & Engineer Features
```bash
python clean.py
```
This will generate:
```
data/processed/all_races_2425_cleaned.csv
```

---

# 🧠 Feature Engineering
The cleaning pipeline creates the following advanced variables:

### ⏱️ Time Features (converted to seconds)
- TotalTime_seconds
- Behind_seconds
- TotalTime_ski_seconds
- TotalTime_range_seconds
- TotalTime_shooting_seconds

### 🎯 Shooting Features
- prone_shooting1 / prone_shooting2
- standing_shooting1 / standing_shooting2
- prone_shooting (total)
- standing_shooting (total)

### 📊 Accuracy Metrics
- accuracy_prone
- accuracy_standing
- accuracy_total

### 🏁 Metadata
- race_name (Sprint, Pursuit, Individual, MassStart)
- compet_name (World Cup / World Championship)
- Season, Event, RaceDate, Gender

---

# 🧪 Data Cleaning Steps
The pipeline:
- Removes DNF / DNS / DSQ / LAP athletes
- Converts time strings (mm:ss, hh:mm:ss) to numeric seconds
- Parses shooting patterns depending on race format
- Computes shooting accuracy metrics
- Adds competition metadata

---

# 📈 Potential Applications
This dataset can be used for:
- Performance modeling (ranking prediction)
- Fatigue and workload analysis
- Injury risk modeling
- Athlete profiling & clustering
- Sports analytics research

---

# ⚠️ Notes & Limitations
- Relay races are excluded
- Some analytics fields may be missing depending on API availability
- Shooting parsing assumes standard IBU formats

---

# 📌 Future Improvements
Planned upgrades:
- Vectorized shooting parsing (speed improvement)
- Parquet storage instead of CSV
- Multi-season batch pipeline
- Snakemake/Makefile automation
- ML feature pipeline (X, y generation)
- Unit tests and logging

---

# 👤 Author
**Quentin Blanchet**  
IMT Atlantique — Data Science Engineering  

---

# ⭐ If you use this project
Feel free to star the repo or contact me for collaboration!

