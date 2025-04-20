import pandas as pd
import re
import numpy as np
import ace_tools as tools

# ---------- 1. Load data (same as before) ----------
CSV_PATH = "/todos_juntos.csv"
try:
    df = pd.read_csv(CSV_PATH, header=1, low_memory=False)
except:
    df = pd.read_csv(CSV_PATH, low_memory=False)

# Ensure Year column
df['Year'] = df['PubYear'].astype(int)

# Prepare searchable text
texts = (df['Title'].fillna('') + ' ' + df['Abstract'].fillna('')).str.lower()

# ---------- 2. Define keyword groups for climate-style categorization ----------
climate_keywords = {
    'Diagnosis': [
        'quantify', 'monitoring', 'distribution', 'assessment', 'survey',
        'characterization', 'exposure', 'transport', 'accumulation',
        'toxicity', 'ecotoxicology'
    ],
    'Mitigation': [
        'reduction', 'prevention', 'cleanup', 'biodegradation', 'degradable',
        'recycling', 'policy', 'ban', 'legislation', 'filter', 'waste management'
    ],
    'Adaptation': [
        'resilience', 'adaptive management', 'policy response', 'response strategy',
        'governance', 'preparedness', 'infrastructure', 'risk management'
    ]
}

# ---------- 3. Classify each article into one or more categories ----------
def classify_climate(text):
    categories = []
    for cat, words in climate_keywords.items():
        pattern = r'\b(' + '|'.join(re.escape(w) for w in words) + r')\b'
        if re.search(pattern, text):
            categories.append(cat)
    return categories

df['ClimateCategory'] = texts.apply(classify_climate)

# Explode to one row per article-category
df_exploded = df.explode('ClimateCategory')
df_exploded = df_exploded.dropna(subset=['ClimateCategory'])

# ---------- 4. Annual counts by Climate Category ----------
annual_counts = (
    df_exploded
    .groupby(['Year', 'ClimateCategory'])
    .size()
    .reset_index(name='Count')
    .pivot(index='Year', columns='ClimateCategory', values='Count')
    .fillna(0)
    .astype(int)
    .sort_index()
)

# Display the table for copying
tools.display_dataframe_to_user("Annual Counts by Climate-style Category", annual_counts)

# Save CSV if needed
annual_counts.to_csv("annual_climate_category_counts.csv", index=True)
