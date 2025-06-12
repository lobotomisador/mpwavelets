import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
from src.utils import find_files, find_folders

RESULTS_DIR = Path("results/")
RECORDS_DIR = Path("records/")
SA_RATIOS_DIR = RESULTS_DIR / "saratios"
DMF_DIR = RESULTS_DIR / "dmfs"


# Set page config
st.set_page_config(
    page_title="MP Wavelets Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar
st.sidebar.title("Settings")

# Get ab_combinations folders
# You can modify this path to point to where your ab_combinations folders are located
# Get list of folders for dropdown
folders = find_folders(SA_RATIOS_DIR)

# Dropdown in sidebar
selected_folder = st.sidebar.selectbox(
    "Select AB Combination",
    options=folders if folders else ["No folders found"],
    disabled=not folders
)

saratios_dir = SA_RATIOS_DIR / selected_folder

selected_damping = st.sidebar.selectbox(
    "Select Damping",
    options=find_files(saratios_dir, only_csv=True),
    disabled=not selected_folder
)

saratio = pd.read_csv(saratios_dir / selected_damping, index_col=0)
dmf = pd.read_csv(DMF_DIR / selected_damping, index_col=0)

df_melted = saratio.reset_index().melt(id_vars=['index'], var_name='Case', value_name='SaRatio')
df_melted = df_melted.rename(columns={'index': 'T'})

dmf_melted = dmf.reset_index().melt(id_vars=['index'], var_name='Case', value_name='DMF')
dmf_melted = dmf_melted.rename(columns={'index': 'T'})
df_melted['DMF'] = dmf_melted['DMF']
df_melted

fig = px.scatter(df_melted, 
                 x='SaRatio', 
                 y='DMF',
                 color='T',
                 color_continuous_scale='viridis',
                 opacity=0.6,
                 title='SaRatio vs DMF Colored by Period')

fig.update_layout(
    showlegend=True,
    plot_bgcolor='white',
)

st.plotly_chart(fig, use_container_width=True)



if selected_folder and selected_folder != "No folders found":
    st.write(f"Selected folder: {selected_folder}")
    # Add your analysis content here based on the selected folder
else:
    st.info("Please add some AB combination folders to get started.")
