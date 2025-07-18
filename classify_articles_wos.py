# classify_articles.py
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

# 1) Read and parse WoS tag-based file 'savedrecs.txt'
savedrecs = r'C:\Users\Usuario\Dropbox\Universidad\Investigacion\MicroPlastic\Review\Datos\WoS\wos_marine_microplastic.txt' 
with open(savedrecs, encoding='utf-8') as f:
    raw = f.read()

records = raw.split('\nER')
years, texts = [], []

for rec in records:
    # 1) Join continuation lines
    rec_flat = re.sub(r'\n {2,}', ' ', rec)

    # 2) Extract year
    m = re.search(r'\nPY\s+(\d{4})', rec_flat)
    if not (m and int(m.group(1)) <= 2024):
        continue
    year = int(m.group(1))

    # 3) Extract title, abstract, and keywords
    core = re.findall(r'\n(?:TI|AB|DE|ID)\s+([^\n]+)', rec_flat)
    if not core:
        continue

    years.append(year)
    texts.append(' '.join(core).lower())

df = pd.DataFrame({'year': years, 'text': texts})
years_range = range(df['year'].min(), 2025)

# 2) Keyword dictionaries
disciplines = {
    'Physics': [
        "physic", "physical oceanography",
        "hydrodynam", "current", "circulat", "advection",
        "wave", "tide", "tidal", "turbulenc", "mixing",
        "eddy", "dispersion", "flow", "particle transport",
        "modeling", "numerical model", "lagrangian", "drifter"
    ],
    'Chemistry': [
        "chem", "geochem", "aqueous chemistry",
        "adsorpt", "absorp", "partition", "sorption",
        "leach", "desorb", "react", "oxid", "redox",
        "photochem", "hydroly", "degrad", "weathering",
        "composition", "polymer analys", "spectroscop",
        "chromatograph", "isotope"
    ],
    'Biology': [
        "biolog", "ecolog", "organism", "species", "fauna", "flora",
        "plankton", "zooplankton", "phytoplankton",
        "microb", "bacteri", "fung", "alga",
        "biofilm", "biofouling", "ingestion", "uptake",
        "toxicol", "ecotoxicol", "bioaccumul", "biomagnificat",
        "immune", "metabol", "physiolog", "genotoxic", "endocrine"
    ],
    'Geology': [
        "geolog", "geomorph", "sediment", "sedimentolog", "stratigraph",
        "litholog", "mineral", "core", "grain size", "facies",
        "seafloor", "bottom", "benthic", "continental shelf",
        "deltaic", "estuarine sediment", "marsh", "mudflat",
        "provenance", "deposition", "erosion", "transport pathway"
    ]
}

environments = {
    'Surface': [
        "surface", "sea surface", "upper ocean", "epipelagic",
        "neuston", "slick", "sea-slick", "driftline"
    ],
    'Deep ocean': [
        "mesopelag", "bathyal", "abyss", "hadal",
        "pelagic", "open ocean", "offshore", "blue water",
        "deep sea", "ocean interior", "water column", "midwater"
    ],
    'Beach/Coast': [
        "beach", "beachface", "shore", "coast", "coastal",
        "intertidal", "supratidal", "swash zone",
        "harbour", "harbor", "port", "marina", "dock",
        "seawall", "breakwater", "surf zone"
    ],
    'Estuary/Lagoon/Mangrove': [
        "estuar", "mangrov", "lagoon", "delta", "tidal creek",
        "back-barrier", "salt marsh", "manglar", "ria"
    ],
    'Sediment/Benthic': [
        "sediment", "seafloor", "sea floor", "benthic", "benthos",
        "bottom", "continental shelf", "shelf break",
        "slope", "canyon", "mud", "sand bed", "pore water"
    ],
    'General marine': [
        "marine", "ocean", "oceanic", "sea", "seawater",
        "seas", "ocean-wide"
    ]
}

climate = {
    'Diagnosis': [
        "quantif", "quantitativ", "monitor", "surveil", "observat",
        "mapp", "spatial distribut", "temporal distribut",
        "flux", "loading", "budget", "mass balance",
        "characte", "fingerprint", "profil",
        "survey", "sampling", "methodolog", "analyt", "spectroscop",
        "exposur", "risk assess", "hazard", "vulnerab",
        "transport", "dispersion", "drift", "pathway", "accumulat",
        "toxicit", "ecotox", "bioavailab", "bioaccum", "genotoxic",
        "numerical model", "hindcast", "data assimil"
    ],
    'Mitigation': [
        "prevent", "source control", "reduce", "reduction",
        "ban", "phase-out", "single-use", "producer responsib",
        "wastewater treatment", "filter", "nanofiltrat",
        "membrane", "biofilter", "capture device", "separator",
        "cleanup", "removal", "trawl-clean", "litter trap", "beach clean",
        "ocean clean", "vacuum", "skimmer",
        "biodegrad", "photo-degrad", "oxo-degrad", "enzymatic degrad",
        "compostab", "bioplastic",
        "recycl", "upcycl", "valoris", "circular econom",
        "policy", "regulat", "legislat", "directive", "framework",
        "waste manag", "extended producer", "stewardship",
        "eco-label", "tax", "subsid", "incentiv"
    ],
    'Adaptation': [
        "resilienc", "adaptive", "adaptation strateg", "coping strateg",
        "risk manag", "contingen", "preparedness", "early warning",
        "green infrastructure", "nature-based", "seagrass restor",
        "wetland restor", "living shorelin",
        "governance", "stakeholder", "co-manag", "community-based",
        "citizen scienc", "participatory", "public awareness",
        "policy respons", "national plan", "regulat adapt", "mainstreaming",
        "financ", "funding", "investment plan"
    ]
}

# 3) Keyword flagging function
def assign_flags(texts, category_dict):
    flags = pd.DataFrame(False, index=range(len(texts)), columns=category_dict.keys())
    for cat, stems in category_dict.items():
        pat = r'\b(' + '|'.join(re.escape(stem) + r'\w*' for stem in stems) + r')\b'
        regex = re.compile(pat)
        flags[cat] = [bool(regex.search(t)) for t in texts]
    return flags

flags_disc = assign_flags(df['text'], disciplines)
flags_env = assign_flags(df['text'], environments)
flags_cli = assign_flags(df['text'], climate)

# 4) Yearly counts and percentages
def count_by_year(df, flags, years_range):
    counts = pd.DataFrame(0, index=years_range, columns=flags.columns, dtype=int)
    for year in years_range:
        mask = df['year'] == year
        counts.loc[year] = flags[mask].sum().values
    totals = counts.sum(axis=1)
    pct = counts.div(totals, axis=0).fillna(0) * 100
    return counts, pct

c_disc, p_disc = count_by_year(df, flags_disc, years_range)
c_env,  p_env  = count_by_year(df, flags_env,  years_range)
c_cli,  p_cli  = count_by_year(df, flags_cli,  years_range)

# Prepare figure directory
figdir = r'C:\Users\Usuario\Dropbox\Universidad\Investigacion\MicroPlastic\Review\Figuras'
os.makedirs(figdir, exist_ok=True)

# 5) Plotting
def plot_category(counts, pct, title):
    fname = title.replace(' ','_')
    
    # a) Count (log or linear)
    plt.figure(figsize=(8,5))
    for col in counts.columns:
        plt.plot(counts.index, counts[col], marker='o', label=col)
    plt.xlim(2003, 2024)
    plt.xticks(range(2003, 2025, 2))
    plt.xlabel('Year'); plt.ylabel('Articles')
    plt.legend(loc='upper left')
    plt.grid(True, which='both', ls='--')
    plt.savefig(os.path.join(figdir, f'{fname}_count.png'), bbox_inches='tight')
    plt.show()
    
    # b) Annual fraction (stacked area)
    plt.figure(figsize=(8,5))
    frac = pct.div(100)
    series = [frac[col] for col in frac.columns]
    plt.stackplot(frac.index, series, labels=frac.columns, alpha=0.8)
    plt.xlim(2003, 2024)
    plt.xticks(range(2003, 2025, 2))
    plt.ylim(0,1)
    plt.xlabel('Year'); plt.ylabel('Annual fraction')
    plt.legend(loc='upper left')
    plt.grid(True, ls='--', alpha=0.5)
    plt.savefig(os.path.join(figdir, f'{fname}_fraction.png'), bbox_inches='tight')
    plt.show()

# Run plots
plot_category(c_disc, p_disc, 'Discipline')
plot_category(c_env,  p_env,  'Environment')
plot_category(c_cli,  p_cli,  'Climate_Approach')
