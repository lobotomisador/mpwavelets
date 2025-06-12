import numpy as np
from scipy import stats
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os   
from pathlib import Path
from src.utils import find_files, find_folders
from statsmodels.stats.diagnostic import het_breuschpagan
import statsmodels.api as sm

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

slope, intercept, r_value, p_value, std_err = stats.linregress(df_melted['SaRatio'], df_melted['DMF'])

# Create regression line
x_reg = np.linspace(df_melted['SaRatio'].min(), df_melted['SaRatio'].max(), 100)
y_reg = slope * x_reg + intercept


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

fig.add_trace(go.Scatter(
    x=x_reg,
    y=y_reg,
    mode='lines',
    name=f'Regression (y = {slope:.3f}x + {intercept:.3f})',
    line=dict(color='red', width=2)
))

st.plotly_chart(fig, use_container_width=True)

# Display regression statistics
st.write("Regression Statistics:")
st.write(f"Slope: {slope:.3f}")
st.write(f"Intercept: {intercept:.3f}")
st.write(f"R-squared: {r_value**2:.3f}")
st.write(f"P-value: {p_value:.3e}")

# Calculate residuals
predicted = slope * df_melted['SaRatio'] + intercept
residuals = df_melted['DMF'] - predicted

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

# Test for constant variance using Breusch-Pagan test

# Prepare data for the test
X = sm.add_constant(df_melted['SaRatio'])
model = sm.OLS(df_melted['DMF'], X).fit()
residuals = model.resid
fitted_values = model.fittedvalues

# Perform Breusch-Pagan test
bp_test = het_breuschpagan(residuals, X)
# het_breuschpagan returns 4 values: test statistic, p-value, f-statistic, and f-pvalue
bp_statistic, bp_pvalue, _, _ = bp_test

st.write("Breusch-Pagan Test for Heteroscedasticity:")
st.write(f"Test Statistic: {bp_statistic:.3f}")
st.write(f"P-value: {bp_pvalue:.3e}")

# Interpret the results
if bp_pvalue < 0.05:
    st.write("The test suggests there is heteroscedasticity (non-constant variance) in the residuals.")
else:
    st.write("The test suggests the residuals have constant variance (homoscedasticity).")


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

# Perform Shapiro-Wilk test
shapiro_test = stats.shapiro(residuals)
shapiro_statistic, shapiro_pvalue = shapiro_test

st.write("Shapiro-Wilk Test for Normality (α = 0.005):")
st.write(f"Test Statistic: {shapiro_statistic:.3f}")
st.write(f"P-value: {shapiro_pvalue:.3e}")

# Interpret the results
if shapiro_pvalue < 0.005:
    st.write("The test suggests the residuals are not normally distributed (reject H0 at α = 0.005).")
else:
    st.write("The test suggests the residuals are normally distributed (fail to reject H0 at α = 0.005).")

