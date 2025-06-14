import numpy as np
from scipy import stats
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os   
from pathlib import Path
from src.utils import find_files, find_folders, create_melted_df
from statsmodels.stats.diagnostic import het_breuschpagan
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

RESULTS_DIR = Path("results/")
RECORDS_DIR = Path("records/")
SA_RATIOS_DIR = RESULTS_DIR / "saratios"
DMF_DIR = RESULTS_DIR / "dmfs"


PERIOD_CUTOFF = 5.0

dmf_files = find_files(DMF_DIR, only_csv=True)
saratios_by_ab = find_folders(SA_RATIOS_DIR)

def get_regression_results(x, y):
    # Center data around (1,1) for forced regression through (1,1)
    x_centered = x - 1
    y_centered = y - 1

    # Fit regression through origin (since data is centered)
    slope, _, r_value, p_value, std_err = stats.linregress(x_centered, y_centered)
    intercept = 1 - slope  # This ensures the line passes through (1,1)
    return slope

def compute_rmse(x, y, slope):
    intercept = 1 - slope  # Ensures line passes through (1,1)
    y_pred = slope * x + intercept
    rmse = np.sqrt(np.mean((y - y_pred) ** 2))
    return rmse


median_rmse_by_ab = {}
rmse_by_ab = {}
for ab_folder in saratios_by_ab:
    saratios_dir = SA_RATIOS_DIR / ab_folder
    saratios_files = find_files(saratios_dir, only_csv=True)
    rmse_by_damping = {}
    for damping in saratios_files:
        if '0.05' in damping:
            continue
        saratio = pd.read_csv(saratios_dir / damping, index_col=0)
        dmf = pd.read_csv(DMF_DIR / damping, index_col=0)
        saratio = saratio[saratio.index <= PERIOD_CUTOFF]
        dmf = dmf[dmf.index <= PERIOD_CUTOFF]
        df_melted = create_melted_df(saratio, dmf, damping)
        xs = df_melted['SaRatio']
        ys = df_melted['DMF']
        slope = get_regression_results(xs, ys)
        rmse = compute_rmse(xs, ys, slope)
        rmse_by_damping[damping] = rmse
    # median_rmse_by_ab[ab_folder] = np.median(list(rmse_by_damping.values()))
    rmse_by_ab[ab_folder] = rmse_by_damping.values()


TOP_ITEMS = 8
median_rmse = {label: np.median(list(values)) for label, values in rmse_by_ab.items()}
top_8_labels = sorted(median_rmse.items(), key=lambda x: x[1])[:TOP_ITEMS]
top_8_labels = [label for label, _ in top_8_labels]

fig = go.Figure()

for label in top_8_labels:
    values = rmse_by_ab[label]
    fig.add_trace(go.Box(
        y=list(values),
        name=label,
        width=0.5
    ))

fig.update_layout(
    title='RMSE Distribution by AB Combination',
    yaxis_title='RMSE across damping',
    showlegend=False,
    boxmode='group',
    height=600,
    width=1000,
    xaxis=dict(
        tickangle=45
    ),
    boxgap=0.2,
    boxgroupgap=0.2
)

fig.write_image('rmse_boxplot.pdf', format='pdf', scale=2)

