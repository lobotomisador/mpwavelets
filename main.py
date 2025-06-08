import streamlit as st
import polars as pl
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
import os

def load_time_series(file_path):
    """Load time series data from a file using polars."""
    df = pl.read_csv(file_path)
    # Check if the file has a header line with parameters
    with open(file_path, 'r') as f:
        first_line = f.readline().strip()
    
    # Process header if it matches the expected format
    if first_line.startswith('N='):
        # Extract parameters from the header
        params = {}
        for param in first_line.split():
            if '=' in param:
                key, value = param.split('=')
                params[key] = value
        
        # Get the delta value for time spacing
        delta = float(params.get('Delta', 0.01))
        
        # Read the actual data, skipping the header
        df = pl.read_csv(file_path, skip_rows=1, has_header=False)
        
        # Create a time column with evenly spaced values
        num_rows = df.height
        time_values = [i * delta for i in range(num_rows)]
        
        # Add the time column as the first column
        df = df.with_columns(pl.Series("Time", time_values)).select(["Time", *df.columns])
    return df

def plot_time_series(df, column=None):
    """Create a time series plot using seaborn."""
    if df is None:
        return
    
    plt.figure(figsize=(12, 6))
    
    if column:
        sns.lineplot(data=df, x=df.columns[0], y=column)
    else:
        # If no column specified, plot all numeric columns
        numeric_cols = df.columns
        for col in numeric_cols:
            sns.lineplot(data=df, x=df.columns[0], y=col, label=col)
    
    plt.title("Time Series Visualization")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt

def main():
    st.title("Time Series Visualization")
    
    # Get list of files in the records directory
    records_dir = Path("records")
    if not records_dir.exists():
        st.error("Records directory not found. Please create a 'records' directory and add your time series files.")
        return
    
    files = list(records_dir.glob("*"))
    if not files:
        st.error("No files found in the records directory. Please add some time series data files.")
        return
    
    # File selection
    selected_file = st.selectbox(
        "Select a file to visualize",
        options=files,
        format_func=lambda x: x.name
    )
    
    if selected_file:
        # Load the selected file
        df = load_time_series(selected_file)
        print(df)
        st.write("### Data Preview")
        st.dataframe(df.head())
        
        # Column selection for plotting
        if len(df.columns) > 1:
            selected_column = st.selectbox(
                "Select column to plot",
                options=df.columns[1:],  # Skip the first column (time)
                index=0
            )
        else:
            selected_column = None 
        
        st.write("### Time Series Plot")
        fig = plot_time_series(df, selected_column)
        if fig:
            st.pyplot(fig)

if __name__ == "__main__":
    main()
