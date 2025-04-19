import pandas as pd, re, numpy as np, ace_tools as tools

CSV_PATH = "/mnt/data/todos_juntos.csv"
try:
    df_all = pd.read_csv(CSV_PATH, header=1, low_memory=False)
except:
    df_all = pd.read_csv(CSV_PATH, low_memory=False)

df_all['Year'] = df_all['PubYear'].astype(int)

# prepare searchable text
texts = (df_all['Title'].fillna('') + ' ' + df_all['Abstract'].fillna('')).str.lower()

disc_keywords = {
    'Física': ['physical oceanography', 'physical', 'physics', 'hydrodynamic', 'current',
               'circulation', 'wave', 'tide', 'tides', 'turbulence', 'flow', 'particle transport'],
    'Química': ['chemical', 'chemistry', 'geochemical', 'adsorption', 'leaching', 'reaction',
                'composition', 'oxidation', 'redox', 'degradation', 'aqueous chemistry'],
    'Biología': ['biological', 'biology', 'ecology', 'organism', 'fauna', 'flora', 'microbial',
                 'biofilm', 'toxicology', 'bioaccumulation', 'biota', 'ecotoxicology'],
    'Geología': ['geology', 'geological', 'geomorphology', 'sedimentology', 'sediment', 'stratigraphy',
                 'lithology', 'mineral', 'seafloor', 'geophysics']
}

marine_env_keywords = {
    'Superficie': ['surface', 'sea surface', 'upper ocean', 'epipelagic'],
    'Océano profundo': ['mesopelagic', 'bathyal', 'abyssal', 'pelagic',
                        'open ocean', 'offshore', 'deep sea', 'ocean interior'],
    'Playa / Costa': ['beach', 'shore', 'coast', 'coastal', 'intertidal', 'supratidal', 'harbour', 'port'],
    'Estuario / Laguna / Manglar': ['estuary', 'estuarine', 'mangrove', 'lagoon', 'delta'],
    'Sedimento / Béntico': ['sediment', 'seafloor', 'benthic', 'bottom', 'slope', 'continental shelf'],
    'General‑marino': ['marine', 'ocean', 'sea', 'oceanic']  # will filter later
}

# build base masks lazily
def build_mask(keys):
    pattern='|'.join(re.escape(k) for k in keys)
    return texts.str.contains(pattern, regex=True)

disc_masks={d:build_mask(kws) for d,kws in disc_keywords.items()}
env_masks_raw={e:build_mask(kws) for e,kws in marine_env_keywords.items()}

# Remove general-marine hits that already in specific env
spec_union = np.column_stack([env_masks_raw[e] for e in marine_env_keywords if e!='General‑marino']).any(axis=1)
env_masks_raw['General‑marino'] = env_masks_raw['General‑marino'] & (~spec_union)

environments=list(env_masks_raw.keys())
disciplines=list(disc_keywords.keys())

# Build tidy list
rows=[]
for year in sorted(df_all['Year'].unique()):
    idx_year = (df_all['Year']==year)
    for d in disciplines:
        for e in environments:
            count = int((idx_year & disc_masks[d] & env_masks_raw[e]).sum())
            if count>0:
                rows.append({'Year':year,'Disciplina':d,'Entorno':e,'Conteo':count})

tidy_df = pd.DataFrame(rows)

# Wide pivot: MultiIndex Year+Disciplina rows, Entorno columns
wide_df = tidy_df.pivot_table(index=['Year','Disciplina'], columns='Entorno', values='Conteo', aggfunc='sum').fillna(0).astype(int)
wide_df = wide_df.sort_index()

# display for copying
tools.display_dataframe_to_user("Tabla tidy (Year‑Disciplina‑Entorno‑Conteo)", tidy_df)
tools.display_dataframe_to_user("Tabla ancha (Year, Disciplina) × Entorno", wide_df)
