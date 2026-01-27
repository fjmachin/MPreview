# Marine Microplastics Review – Classification and Trend Analysis

This repository contains Python scripts used to classify and analyze scientific publications on **marine microplastics** published untill 2024. The current version is based on data retrieved from **Web of Science (WoS)**, and supports a systematic review of disciplinary trends, environmental focus, and climate-related approaches in marine microplastics research.

---

## 📚 Overview

Publications were obtained from Web of Science and Scopus using keyword-based queries.

The analysis is structured in two main components:

- **General Classification**: Assigns each article to scientific disciplines (Physics, Chemistry, Biology, Geology), environments (e.g., surface, sediment, estuaries), and climate-related approaches (Diagnosis, Mitigation, Adaptation).
- **Deep Ocean Subset**: Focuses on publications related to the deep ocean, further categorizing them by ocean basin, maximum sampling depth, and vertical zone (mesopelagic, bathyal, etc.).

---

## 🧰 Repository Structure

This repository contains the core scripts and datasets used in the bibliometric analysis:

MPreview/
│
├── classify_articles_wos.py # Main script to parse WoS export and classify articles
├── deep_ocean_analysis.py # Script for deep-ocean subset analysis and figure generation
├── doi_list_classified.csv # Public dataset: DOIs, year, and classification flags
├── LICENSE # License file (MIT)
├── README.md # Project documentation
└── README.md.bak # Backup of previous README version

Each script is self-contained and fully documented to ensure reproducibility.  
All figures and tables presented in the manuscript can be generated directly from these scripts and the data provided.

### 🗂️ File Summary

| File | Description |
|------|-------------|
| `classify_articles_wos.py` | Parses Web of Science export files, extracts metadata (year, DOI, journal, etc.), and classifies articles by discipline, environment, and climate-inspired approach. |
| `deep_ocean_analysis.py` | Performs secondary analysis on the classified dataset, generates summary tables and visualizations (e.g., Figures 9–11). |
| `doi_list_classified.csv` | Public dataset listing DOIs, publication years, bibliographic metadata, and classification flags (discipline, environment, and climate approach). |
| `LICENSE` | Open-source license (MIT). |
| `README.md` | Project documentation. |
| `README.md.bak` | Backup of a previous version of the README. |

## ⚙️ How to Use

1. **Install requirements**

```bash
pip install pandas matplotlib

2. **Place your WoS/Scopus export files in the data/ folder with the expected names:**

    wos_marine_microplastic.txt for the general classification.

    deep_ocean_records.txt for deep ocean articles.

3. **Run the classification scripts**

python scripts/classify_articles.py
python scripts/deep_ocean_analysis.py

Output figures and tables will be saved in the figures/ and output/ folders, respectively.
👥 Authors

This repository was developed by Francisco Machín in support of a systematic literature review on marine microplastics research.
📄 License

This project is licensed under the MIT License.

---

## 🔍 Data Availability and Reproducibility

The bibliographic dataset analyzed in this study originates from **Web of Science (WoS)** searches performed in July 2025.  
Because Web of Science content is subject to license restrictions, the original text exports (including abstracts and detailed metadata) **cannot be redistributed**.  

However, this repository provides:
- The **classification scripts** (`classify_articles_wos.py`, `deep_ocean_analysis.py`) for full methodological transparency.
- The **derived datasets**, including  
  - `classified_articles.csv` (internal working file, not redistributed publicly)  
  - `doi_list_classified.csv` (public dataset listing DOIs, publication years, and classification tags by discipline, environment, and climate approach)  

These files allow the complete reconstruction of the dataset by any user with institutional access to Web of Science or Scopus.

For records without DOIs, additional bibliographic metadata (journal, volume, issue, and pages) are included to ensure traceability without reproducing copyrighted content.

---

## 📘 Citation

If you use these data or scripts, please cite:

> Machín F. et al. (2026). *Structural Biases in Marine Microplastics Research: The Underrepresentation of Deep Ocean and Full Water Column Studies.*  
> **Environmental Research Letters**, 21 023003. https://doi.org/10.1088/1748-9326/ae3849 
> Repository: https://github.com/fjmachin/MPreview
