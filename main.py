import numpy as np
from scipy import stats
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from src.utils import find_files, find_folders
from statsmodels.stats.diagnostic import het_breuschpagan
import statsmodels.api as sm
from statsmodels.stats.stattools import durbin_watson

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

# Add period cutoff slider
st.sidebar.markdown("---")  # Add a separator
st.sidebar.subheader("Period Filter")
period_cutoff = st.sidebar.slider(
    "Period Cutoff (s)",
    min_value=1.0,
    max_value=10.0,
    value=5.0,
    step=0.1,
    disabled=not selected_folder
)

# Add toggle buttons in sidebar
st.sidebar.markdown("---")  # Add a separator
st.sidebar.subheader("Plot Controls")
show_residuals = st.sidebar.checkbox("Show Residuals Plot", value=True)
show_qq = st.sidebar.checkbox("Show Q-Q Plot", value=True)

saratio = pd.read_csv(saratios_dir / selected_damping, index_col=0)
dmf = pd.read_csv(DMF_DIR / selected_damping, index_col=0)

# Filter data based on period cutoff
saratio = saratio[saratio.index <= period_cutoff]
dmf = dmf[dmf.index <= period_cutoff]

df_melted = saratio.reset_index().melt(id_vars=['index'], var_name='Case', value_name='SaRatio')
df_melted = df_melted.rename(columns={'index': 'T'})

dmf_melted = dmf.reset_index().melt(id_vars=['index'], var_name='Case', value_name='DMF')
dmf_melted = dmf_melted.rename(columns={'index': 'T'})
df_melted['DMF'] = dmf_melted['DMF']

# damping_str = selected_damping.split('_')[1][:-4]
# if float(damping_str) > 0.05:
#     df_melted['DMF'] = df_melted['DMF'] * 100

# Center data around (1,1) for forced regression through (1,1)
x_centered = df_melted['SaRatio'] - 1
y_centered = df_melted['DMF'] - 1


# Fit regression through origin (since data is centered)
slope, _, r_value, p_value, std_err = stats.linregress(x_centered, y_centered)
intercept = 1 - slope  # This ensures the line passes through (1,1)

# Create regression line
x_reg = np.linspace(df_melted['SaRatio'].min(), df_melted['SaRatio'].max(), 100)
y_reg = slope * x_reg + intercept

fig = px.scatter(df_melted, 
                 x='SaRatio', 
                 y='DMF',
                 color='T',
                 color_continuous_scale='viridis',
                 opacity=0.6,
                 title='SaRatio vs DMF Colored by Period (Regression through (1,1))')

fig.update_layout(
    showlegend=True,
    plot_bgcolor='white',
)

# Add point (1,1) to the plot
fig.add_trace(go.Scatter(
    x=[1],
    y=[1],
    mode='markers',
    marker=dict(
        color='red',
        size=10,
        symbol='star'
    ),
    name='Reference Point (1,1)'
))

fig.add_trace(go.Scatter(
    x=x_reg,
    y=y_reg,
    mode='lines',
    name=f'Regression (y = {slope:.3f}x + {intercept:.3f})',
    line=dict(color='red', width=2)
))

st.plotly_chart(fig, use_container_width=True)

# Calculate residuals and perform tests
predicted = slope * df_melted['SaRatio'] + intercept
residuals = df_melted['DMF'] - predicted

# Prepare data for Breusch-Pagan test
X = sm.add_constant(df_melted['SaRatio'])
model = sm.OLS(df_melted['DMF'], X).fit()
residuals = model.resid

# Perform tests
bp_test = het_breuschpagan(residuals, X)
bp_statistic, bp_pvalue, _, _ = bp_test

# Perform Shapiro-Wilk test
shapiro_test = stats.shapiro(residuals)
shapiro_statistic, shapiro_pvalue = shapiro_test

# Perform Durbin-Watson test for autocorrelation
dw_statistic = durbin_watson(residuals)
# Durbin-Watson test interpretation:
# DW ≈ 2: No autocorrelation
# DW < 1.5: Positive autocorrelation
# DW > 2.5: Negative autocorrelation
dw_result = "✅ No Autocorrelation" if 1.5 <= dw_statistic <= 2.5 else "❌ Autocorrelation Present"

# Create a summary table for test results
st.markdown("### Statistical Test Results")

# Define test results
test_results = {
    "Test": [
        "Breusch-Pagan (Heteroscedasticity)",
        "Shapiro-Wilk (Normality)",
        "Durbin-Watson (Autocorrelation)"
    ],
    "Statistic": [
        f"{bp_statistic:.3f}",
        f"{shapiro_statistic:.3f}",
        f"{dw_statistic:.3f}"
    ],
    "P-value": [
        f"{bp_pvalue:.2e}",
        f"{shapiro_pvalue:.2e}",
        "N/A"  # Durbin-Watson doesn't have a p-value
    ],
    "α": ["0.005", "0.005", "N/A"],
    "Result": [
        "✅ Homoscedastic" if bp_pvalue >= 0.005 else "❌ Heteroscedastic",
        "✅ Normal" if shapiro_pvalue >= 0.005 else "❌ Non-normal",
        dw_result
    ]
}

# Create DataFrame and display as table
df_results = pd.DataFrame(test_results)
st.dataframe(
    df_results,
    hide_index=True,
    use_container_width=True,
    column_config={
        "Test": st.column_config.TextColumn("Test", width="medium"),
        "Statistic": st.column_config.NumberColumn("Statistic", format="%.3f"),
        "P-value": st.column_config.TextColumn("P-value"),
        "α": st.column_config.TextColumn("Significance Level"),
        "Result": st.column_config.TextColumn("Result", width="medium")
    }
)

# Only show residuals plot if enabled
if show_residuals:
    # Create residual plot
    fig_residuals = go.Figure()
    fig_residuals.add_trace(go.Scatter(
        x=df_melted['SaRatio'],
        y=residuals,
        mode='markers',
        marker=dict(
            color=df_melted['T'],
            colorscale='viridis',
            opacity=0.3
        ),
        name='Residuals'
    ))

    # Add horizontal line at y=0
    fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")

    fig_residuals.update_layout(
        title='Residual Plot',
        xaxis_title='SaRatio',
        yaxis_title='Residuals',
        showlegend=True,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig_residuals, use_container_width=True)

# Only show QQ plot if enabled
if show_qq:
    # Create QQ plot
    fig_qq = go.Figure()

    # Calculate theoretical quantiles
    theoretical_quantiles = np.sort(stats.norm.ppf(np.linspace(0.01, 0.99, len(residuals))))
    sample_quantiles = np.sort(residuals)

    # Add QQ plot
    fig_qq.add_trace(go.Scatter(
        x=theoretical_quantiles,
        y=sample_quantiles,
        mode='markers',
        marker=dict(
            color='blue',
            opacity=0.5
        ),
        name='QQ Plot'
    ))

    # Add diagonal line
    min_val = min(theoretical_quantiles.min(), sample_quantiles.min())
    max_val = max(theoretical_quantiles.max(), sample_quantiles.max())
    fig_qq.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode='lines',
        line=dict(color='red', dash='dash'),
        name='Normal Line'
    ))

    fig_qq.update_layout(
        title='Q-Q Plot for Residuals',
        xaxis_title='Theoretical Quantiles',
        yaxis_title='Sample Quantiles',
        showlegend=True,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig_qq, use_container_width=True)

