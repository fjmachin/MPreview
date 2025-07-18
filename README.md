# Marine Microplastics Review – Classification and Trend Analysis

This repository contains Python scripts used to classify and analyze scientific publications on **marine microplastics** published untill 2024. The current version is based on data retrieved from **Web of Science (WoS)** and **Scopus**, and supports a systematic review of disciplinary trends, environmental focus, and climate-related approaches in marine microplastics research.

---

## 📚 Overview

Publications were obtained from Web of Science and Scopus using keyword-based queries.

The analysis is structured in two main components:

- **General Classification**: Assigns each article to scientific disciplines (Physics, Chemistry, Biology, Geology), environments (e.g., surface, sediment, estuaries), and climate-related approaches (Diagnosis, Mitigation, Adaptation).
- **Deep Ocean Subset**: Focuses on publications related to the deep ocean, further categorizing them by ocean basin, maximum sampling depth, and vertical zone (mesopelagic, bathyal, etc.).

---

## 🧰 Repository Structure

marine-microplastics-review/
│
├── data/ # WoS/Scopus exports and intermediate files
│ ├── wos_marine_microplastic.txt
│ └── deep_ocean_records.txt
│
├── scripts/
│ ├── classify_articles.py # General classification script
│ └── deep_ocean_analysis.py # Specific deep ocean categorization
│
├── output/
│ └── deep_ocean_classified.csv
│
├── figures/
│ ├── discipline_deep_ocean.png
│ ├── depth_deep_ocean_legend.png
│ └── ...
│
└── README.md


---

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