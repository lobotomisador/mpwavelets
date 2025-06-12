import streamlit as st
import os
from pathlib import Path
from src.utils import find_folders

RESULTS_DIR = Path("results/")
RECORDS_DIR = Path("records/")
SA_RATIOS_DIR = RESULTS_DIR / "saratios"


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

# Main content area
st.title("MP Wavelets Analysis Dashboard")

if selected_folder and selected_folder != "No folders found":
    st.write(f"Selected folder: {selected_folder}")
    # Add your analysis content here based on the selected folder
else:
    st.info("Please add some AB combination folders to get started.")
