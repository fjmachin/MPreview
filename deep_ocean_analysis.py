# deep_ocean_analysis.py
import re, os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# 1. Paths
# ----------------------------------------------------------
deep_wos = r'C:\Users\Usuario\Dropbox\Universidad\Investigacion\MicroPlastic\Review\Datos\WoS\deep_ocean_records.txt'
out_csv  = r'C:\Users\Usuario\Dropbox\Universidad\Investigacion\MicroPlastic\Review\Datos\WoS\deep_ocean_classified.csv'
fig_dir  = r'C:\Users\Usuario\Dropbox\Universidad\Investigacion\MicroPlastic\Review\Figuras'
os.makedirs(fig_dir, exist_ok=True)

# ----------------------------------------------------------
# 2. Dictionaries (disciplines + climate approaches)
# ----------------------------------------------------------
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

oceans = {
    'North_Atlantic':  ['north atlantic', 'n. atlantic', 'atlantic gyre'],
    'South_Atlantic':  ['south atlantic', 's. atlantic'],
    'North_Pacific':   ['north pacific', 'n. pacific', 'kuroshio'],
    'South_Pacific':   ['south pacific', 's. pacific'],
    'Indian':          ['indian ocean', 'arabian sea', 'bay of bengal'],
    'Southern':        ['southern ocean', 'antarctic ocean', 'weddell sea', 'ross sea'],
    'Arctic':          ['arctic ocean', 'barents sea', 'kara sea', 'beaufort'],
    'Mediterranean':   ['mediterranean', 'aegean', 'adriatic', 'tyrrhenian'],
    'Caribbean':       ['caribbean', 'gulf of mexico', 'sargasso'],
    'Baltic':          ['baltic sea']
}

def build_regex(stems):
    return re.compile(r'\b(' + '|'.join(re.escape(s)+r'\w*' for s in stems) + r')\b', re.I)

disc_rgx  = {k: build_regex(v) for k,v in disciplines.items()}
cli_rgx   = {k: build_regex(v) for k,v in climate.items()}
ocean_rgx = {k: build_regex(v) for k,v in oceans.items()}

re_depth_num = re.compile(r'(\d{2,4})(?:\s*[-–]\s*\d{2,4})?\s*(m|meters?)', re.I)
depth_kw = {
    'Mesopelagic': build_regex(['mesopelag']),
    'Bathyal': build_regex(['bathyal']),
    'Abyssal': build_regex(['abyss']),
    'Hadal': build_regex(['hadal'])
}

rows = []
for rec in open(deep_wos, encoding='utf-8').read().split('\nER'):
    flat = re.sub(r'\n {2,}', ' ', rec)
    yearm = re.search(r'\nPY\s+(\d{4})', flat)
    if not yearm: continue
    year = int(yearm.group(1))

    text = ' '.join(re.findall(r'\n(?:TI|AB|DE|ID)\s+([^\n]+)', flat)).lower()
    if not text: continue

    disc = next((k for k, rg in disc_rgx.items() if rg.search(text)), 'Unclassified')
    cli = next((k for k, rg in cli_rgx.items() if rg.search(text)), 'Unclassified')
    ocean = next((k for k, rg in ocean_rgx.items() if rg.search(text)), 'Unclassified')

    nums = [int(n) for n,_ in re_depth_num.findall(text)]
    prof_max = max(nums) if nums else None

    prof_cat = 'Unknown'
    if prof_max:
        if prof_max < 1000: prof_cat = 'Mesopelagic'
        elif prof_max < 4000: prof_cat = 'Bathyal'
        elif prof_max < 6000: prof_cat = 'Abyssal'
        else: prof_cat = 'Hadal'
    if prof_cat == 'Unknown':
        for cat, rg in depth_kw.items():
            if rg.search(text):
                prof_cat = cat
                break

    rows.append({'Year': year, 'Discipline': disc, 'Climate': cli,
                 'Ocean': ocean, 'ProfMax_m': prof_max, 'ProfCat': prof_cat})

df = pd.DataFrame(rows).sort_values('Year')
df.to_csv(out_csv, index=False, encoding='utf-8')
print(f'CSV saved: {out_csv}   ({len(df)} records)')

depth_legend = {
    'Mesopelagic': 'Mesopelagic (0–1 km)',
    'Bathyal': 'Bathyal (1–4 km)',
    'Abyssal': 'Abyssal (4–6 km)',
    'Hadal': 'Hadal (>6 km)',
    'Unknown': 'Unknown'
}

disc_colors = {
    'Physics': '#1f77b4',
    'Chemistry': '#ff7f0e',
    'Biology': '#2ca02c',
    'Geology': '#d62728',
    'Unclassified': '#8c564b'
}

def stacked_area(df, col, fname, title=None):
    pivot = (df
             .pivot_table(index='Year', columns=col, aggfunc='size', fill_value=0)
             .loc[:, lambda x: x.sum() > 0]
             .sort_index())

    series = [pivot[c] for c in pivot.columns]
    if col == 'Discipline':
        colour_list = [disc_colors.get(c, '#999999') for c in pivot.columns]
    else:
        colour_list = None

    plt.figure(figsize=(8, 5))
    plt.stackplot(pivot.index, series, labels=pivot.columns, colors=colour_list, alpha=.85)
    plt.xlim(2003, 2024)
    plt.xticks(range(2003, 2025, 2))
    plt.xlabel('Year')
    plt.ylabel('Articles')
    if title:
        plt.title(title)
    plt.legend(loc='upper left')
    plt.grid(alpha=.4)
    plt.tight_layout()
    plt.savefig(os.path.join(fig_dir, fname), dpi=300)
    plt.close()

# Timeline
timeline = df['Year'].value_counts().sort_index()
plt.figure(figsize=(8,4))
plt.plot(timeline.index, timeline.values, marker='o')
plt.xlim(2003,2024); plt.xticks(range(2003,2025,2))
plt.ylabel('Articles'); plt.grid(alpha=.4); plt.tight_layout()
plt.savefig(os.path.join(fig_dir,'timeline_deep_ocean.png'), dpi=300); plt.close()

# Stacked area plots
stacked_area(df, 'Discipline', 'discipline_deep_ocean.png')
stacked_area(df, 'Climate', 'climate_deep_ocean.png')
stacked_area(df, 'ProfCat', 'depth_deep_ocean.png')

# Depth legend version
pivot = df.pivot_table(index='Year', columns='ProfCat', aggfunc='size', fill_value=0)\
          .loc[:, lambda x: x.sum()>0].sort_index()
plt.figure(figsize=(8,5))
plt.stackplot(pivot.index, [pivot[c] for c in pivot.columns],
              labels=[depth_legend.get(c,c) for c in pivot.columns], alpha=.85)
plt.xlim(2003,2024); plt.xticks(range(2003,2025,2))
plt.xlabel('Year'); plt.ylabel('Articles')
plt.legend(loc='upper left'); plt.grid(alpha=.4)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir,'depth_deep_ocean_legend.png'), dpi=300); plt.close()

# Ocean basin
stacked_area(df, 'Ocean', 'ocean_deep_ocean.png')

print('Figures saved in:', fig_dir)
