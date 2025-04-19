# Marine Microplastics Review – Classification and Trend Analysis (2016–2024)

This repository contains the Python scripts used to classify and analyze scientific publications on **marine microplastics** published between **2016 and 2024**. The analysis supports a systematic literature review focused on identifying disciplinary patterns and spatial domains in marine microplastics research.

---

## 🔍 Overview

Articles were retrieved from the [Dimensions](https://www.dimensions.ai/) database using the search terms:

microplastic* AND marin*


Due to export limitations on the Dimensions platform (2,500 records per export), the data were downloaded **year by year** and combined into a single CSV containing **6,870 articles**, each with metadata including:

- Publication ID  
- DOI  
- Title  
- Abstract  
- Source title  
- Year of publication  
- Authors  

---


---

## ⚙️ How to Use

1. **Clone the repository** and install requirements (only pandas and matplotlib):

```bash
git clone https://github.com/yourusername/marine-microplastics-review.git
cd marine-microplastics-review
pip install pandas matplotlib

2. Place your Dimensions CSV export in the data/ folder with the name all_articles_2016_2024.csv.

3. Run the classification script:
python scripts/classify_articles.py

Output will be saved in the output/ folder.

👥 Authors and Credits

This repository was developed by Francisco Machín, in support of a review article on marine microplastics research.

📄 License

This project is licensed under the MIT License.
