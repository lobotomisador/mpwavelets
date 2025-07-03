import numpy as np
from scipy import stats
from scipy.stats import boxcox, gaussian_kde
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from src.utils import find_files, find_folders
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
import statsmodels.api as sm

from plotly.subplots import make_subplots

RESULTS_DIR = Path("results/")
RECORDS_DIR = Path("records/")
SA_RATIOS_DIR = RESULTS_DIR / "saratios"
SA_RATIOS_CONSTANT_DIR = RESULTS_DIR / "saratios_constant"
DMF_DIR = RESULTS_DIR / "dmfs"


st.set_page_config(
    page_title="MP Wavelets Analysis",
    page_icon="📊",
    layout="wide"
)

st.sidebar.title("Settings")

directory_option = st.sidebar.selectbox(
    "Select Directory",
    options=["saratios", "saratios_constant"],
    help="Choose between regular saratios and saratios_constant directories"
)

if directory_option == "saratios":
    base_dir = SA_RATIOS_DIR
else:
    base_dir = SA_RATIOS_CONSTANT_DIR

folders = find_folders(base_dir)

ab_index = folders.index('a=0.020_b=2.100')


selected_folder = st.sidebar.selectbox(
    "Select AB Combination",
    options=folders if folders else ["No folders found"],
    disabled=not folders,
    index=ab_index
)

saratios_dir = base_dir / selected_folder

selected_damping = st.sidebar.selectbox(
    "Select Damping",
    options=find_files(DMF_DIR, only_csv=True),
    disabled=not selected_folder
)

st.sidebar.markdown("---")
st.sidebar.subheader("Period Filter")
period_cutoff = st.sidebar.slider(
    "Period Cutoff (s)",
    min_value=1.0,
    max_value=10.0,
    value=3.0,
    step=0.1,
    disabled=not selected_folder
)

st.sidebar.markdown("---")
st.sidebar.subheader("Options")
force_through_origin = st.sidebar.checkbox("Force fit through (1,1)", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("Plot Controls")
show_residuals = st.sidebar.checkbox("Show Residuals Plot", value=False)

saratio = pd.read_csv(saratios_dir / 'pulses_0.05.csv', index_col=0)
saratio.index = pd.to_numeric(saratio.index, errors='coerce')
dmf = pd.read_csv(DMF_DIR / selected_damping, index_col=0)
dmf.index = pd.to_numeric(dmf.index, errors='coerce')

saratio = saratio[saratio.index <= period_cutoff]
dmf = dmf[dmf.index <= period_cutoff]

df_melted = saratio.reset_index().melt(id_vars=['index'], var_name='Case', value_name='SaRatio')
df_melted = df_melted.rename(columns={'index': 'T'})

dmf_melted = dmf.reset_index().melt(id_vars=['index'], var_name='Case', value_name='DMF')
dmf_melted = dmf_melted.rename(columns={'index': 'T'})
df_melted['DMF'] = dmf_melted['DMF']


# x_centered = df_melted['SaRatio'] - 1
# y_centered = df_melted['DMF'] - 1
x_centered = df_melted['SaRatio']
y_centered = df_melted['DMF']

if force_through_origin:
    x_shifted = x_centered - 1
    y_shifted = y_centered - 1
    X = sm.add_constant(x_shifted, has_constant='add')
    model = sm.OLS(y_shifted, X).fit()
    slope = model.params[1]
    intercept = 1 - slope
else:
    X = sm.add_constant(x_centered)
    model = sm.OLS(y_centered, X).fit()
    slope, intercept = model.params[1], model.params[0]

y_pred = slope * x_centered + intercept

x_reg = np.linspace(df_melted['SaRatio'].min(), df_melted['SaRatio'].max(), 100)
y_reg = slope * x_reg + intercept

fig = px.scatter(df_melted, 
                 x='SaRatio', 
                 y=y_centered,
                 color='T',
                 color_continuous_scale='viridis',
                 opacity=0.6,
                 title='SaRatio vs DMF (Ordinary Least Squares Regression)')

fig.update_layout(
    showlegend=True,
    plot_bgcolor='white',
)

fig.add_trace(go.Scatter(
    x=[1],
    y=[1],
    mode='markers',
    marker=dict(
        color='red',
        size=10,
        symbol='star'
    ),
))

fig.add_trace(go.Scatter(
    x=x_reg,
    y=y_reg,
    mode='lines',
    line=dict(color='red', width=2)
))
st.plotly_chart(fig, use_container_width=True)

predicted = slope * df_melted['SaRatio'] + intercept
residuals = y_centered - predicted

X = sm.add_constant(df_melted['SaRatio'])
bp_test = het_breuschpagan(residuals, X, robust=True)
bp_statistic, bp_pvalue, _, _ = bp_test

white_test = het_white(residuals, X)
white_statistic, white_pvalue, _, _ = white_test

st.write(f'Regression parameters (y = {slope:.3f}x + {intercept:.3f})')
st.markdown("### Statistical Test Results")
test_results = {
    "Test": [
        "Breusch-Pagan (Heteroscedasticity)",
        "White (Heteroscedasticity)"
    ],
    "Statistic": [
        f"{bp_statistic:.3f}",
        f"{white_statistic:.3f}"
    ],
    "P-value": [
        f"{bp_pvalue:.2e}",
        f"{white_pvalue:.2e}"
    ],
    "α": ["0.005", "0.005"],
    "Result": [
        "✅ Homoscedastic" if bp_pvalue >= 0.005 else "❌ Heteroscedastic",
        "✅ Homoscedastic" if white_pvalue >= 0.005 else "❌ Heteroscedastic"
    ]
}

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

if show_residuals:
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

    fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")

    fig_residuals.update_layout(
        title='Residual Plot',
        xaxis_title='SaRatio',
        yaxis_title='Residuals',
        showlegend=True,
        plot_bgcolor='white'
    )

    st.plotly_chart(fig_residuals, use_container_width=True)

np.random.seed(42)

n_cols = 66
random_cols = np.random.choice(saratio.columns, size=n_cols, replace=False)

fig = make_subplots(rows=22, cols=3, 
                    subplot_titles=random_cols,
                    vertical_spacing=0.02,
                    horizontal_spacing=0.1)


for idx, col in enumerate(random_cols):
    row = idx // 3 + 1
    col_num = idx % 3 + 1
    
    xs = saratio.index
    ratios = saratio[col].values
    dmfs = dmf[col].values
    
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=dmfs,
            mode='lines',
            marker=dict(color='black', opacity=0.5, size=8),
            name=f'DMF {col}',
            showlegend=False
        ),
        row=row, col=col_num
    )
    
    y_reg = slope * ratios + intercept
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=y_reg,
            mode='lines',
            line=dict(color='red', width=2),
            name=f'predictor {col}',
            showlegend=False
        ),
        row=row, col=col_num
    )

fig.update_layout(
    title='SaRatio vs DMF for Random Columns',
    height=4400,
    width=1200,
    plot_bgcolor='white',
    showlegend=False
)

for i in range(1, 23):
    for j in range(1, 4):
        fig.update_xaxes(title_text='T/Tp', row=i, col=j)
        fig.update_yaxes(title_text='DMF', row=i, col=j)

st.plotly_chart(fig, use_container_width=True)