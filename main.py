import numpy as np
from scipy import stats
from scipy.stats import boxcox, gaussian_kde
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from src.utils import find_files, find_folders, create_melted_df
from statsmodels.stats.diagnostic import het_breuschpagan, het_white
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib as mpl

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
period_range = st.sidebar.slider(
    "Period Range (s)",
    min_value=0.1,
    max_value=10.0,
    value=(0.1, 3.0),
    step=0.1,
    disabled=not selected_folder
)

st.sidebar.markdown("---")
st.sidebar.subheader("Options")
force_through_origin = st.sidebar.checkbox("Force fit through (1,1)", value=False)
use_weighted_ls = st.sidebar.checkbox("Use Weighted Least Squares (KDE weights)", value=False)

st.sidebar.markdown("---")
st.sidebar.subheader("Plot Controls")
show_residuals = st.sidebar.checkbox("Show Residuals Plot", value=True)

saratio = pd.read_csv(saratios_dir / 'pulses_0.05.csv', index_col=0)
saratio.index = pd.to_numeric(saratio.index, errors='coerce')
dmf = pd.read_csv(DMF_DIR / selected_damping, index_col=0)
dmf.index = pd.to_numeric(dmf.index, errors='coerce')

period_min, period_max = period_range
saratio = saratio[(saratio.index >= period_min) & (saratio.index <= period_max)]
dmf = dmf[(dmf.index >= period_min) & (dmf.index <= period_max)]

df_melted = create_melted_df(saratio, dmf, selected_damping)

x_centered = df_melted['SaRatio']
y_centered = df_melted['DMF']

if use_weighted_ls:
    kde = gaussian_kde(np.column_stack([x_centered, y_centered]).T, bw_method='silverman')
    points = np.column_stack([x_centered, y_centered])
    densities = kde(points.T)
    weights = 1.0 / (densities + 1e-10)
    weights = weights / np.sum(weights) * len(weights)

if force_through_origin:
    x_shifted = x_centered - 1
    y_shifted = y_centered - 1
    X = sm.add_constant(x_shifted, has_constant='add')
    if use_weighted_ls:
        model = sm.WLS(y_shifted, X, weights=weights).fit()
    else:
        model = sm.OLS(y_shifted, X).fit()
    slope = model.params[1]
    intercept = 1 - slope
else:
    X = sm.add_constant(x_centered)
    if use_weighted_ls:
        model = sm.WLS(y_centered, X, weights=weights).fit()
    else:
        model = sm.OLS(y_centered, X).fit()
    slope, intercept = model.params[1], model.params[0]

y_pred = slope * x_centered + intercept

x_reg = np.linspace(df_melted['SaRatio'].min() - 0.2, df_melted['SaRatio'].max() + 0.2, 100)
y_reg = slope * x_reg + intercept

X_reg = sm.add_constant(x_reg)
prediction = model.get_prediction(X_reg)
prediction_summary = prediction.summary_frame(alpha=0.005)
lower = prediction_summary['obs_ci_lower']
upper = prediction_summary['obs_ci_upper']

fig = go.Figure()


sampled_indices = np.random.choice(len(df_melted), size=len(df_melted)//2, replace=False)
fig.add_trace(go.Scattergl(
    x=df_melted['SaRatio'].iloc[sampled_indices],
    y=y_centered.iloc[sampled_indices],
    mode='markers',
    marker=dict(
        color=df_melted['T'].iloc[sampled_indices],
        colorscale='viridis',
        opacity=0.8,
        size=4,
        showscale=True,
        colorbar=dict(title='T')
    ),
    name='Data Points'
))

fig.update_layout(
    title='SdRatio vs DMF',
    xaxis_title='SdRatio',
    yaxis_title='DMF',
    showlegend=True,
    plot_bgcolor='white',
)

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
    line=dict(color='red', width=2),
    name='Regression Line'
))

st.plotly_chart(fig, use_container_width=True)


predicted = slope * df_melted['SaRatio'] + intercept
residuals = y_centered - predicted

if use_weighted_ls:
    weighted_residuals = residuals * np.sqrt(weights)
else:
    weighted_residuals = residuals

X = sm.add_constant(df_melted['SaRatio'])
bp_test = het_breuschpagan(weighted_residuals, X, robust=True)
bp_statistic, bp_pvalue, _, _ = bp_test

white_test = het_white(weighted_residuals, X)
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
    fig_residuals.add_trace(go.Scattergl(
        x=df_melted['SaRatio'].iloc[sampled_indices],
        y=weighted_residuals.iloc[sampled_indices],
        mode='markers',
        marker=dict(
            color=df_melted['T'].iloc[sampled_indices],
            colorscale='viridis',
            opacity=0.8,
            size=4,
            showscale=True,
            colorbar=dict(title='T')
        ),
        name='Residuals'
    ))

    fig_residuals.add_hline(y=0, line_dash="dash", line_color="red")

    fig_residuals.update_layout(
        title='Residual Plot',
        xaxis_title='SdRatio',
        yaxis_title='Residuals',
        showlegend=True,
        plot_bgcolor='white'
    )

    # Professional export for PDF using Plotly
    fig_residuals_pdf = go.Figure()
    fig_residuals_pdf.add_trace(go.Scattergl(
        x=df_melted['SaRatio'].iloc[sampled_indices],
        y=weighted_residuals.iloc[sampled_indices],
        mode='markers',
        marker=dict(
            color=df_melted['T'].iloc[sampled_indices],
            colorscale='plasma',
            opacity=1.0,
            size=4,
            showscale=True,
            colorbar=dict(title='T', thickness=18, len=0.8, x=1.02, y=0.5, yanchor='middle')
        ),
        name='Residuals'
    ))
    fig_residuals_pdf.add_hline(y=0, line_dash="dash", line_color="gray", line_width=2)
    fig_residuals_pdf.update_layout(
        xaxis_title='SdRatio',
        yaxis_title='Residuals',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=40, r=40, t=10, b=80),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            linecolor='black',
            linewidth=2,
            mirror=True,
            zeroline=False,
            title_font=dict(size=20),
            title_standoff=40,
            ticks='inside',
            ticklen=12,
            tickwidth=2,
            tickcolor='black',
            tickson='boundaries',
            range=[1, 4],
            dtick=0.5
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            gridwidth=1,
            linecolor='black',
            linewidth=2,
            mirror=True,
            zeroline=False,
            title_font=dict(size=20),
            title_standoff=40,
            ticks='inside',
            ticklen=12,
            tickwidth=2,
            tickcolor='black',
            tickson='boundaries',
            range=[-0.15, 0.15],
            dtick=0.05
        )
    )
    # fig_residuals_pdf.write_image("residuals_plot.pdf")

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
        go.Scattergl(
            x=xs,
            y=dmfs,
            mode='lines',
            marker=dict(color='black', opacity=0.5, size=4),
            name=f'DMF {col}',
            showlegend=False
        ),
        row=row, col=col_num
    )
    
    y_reg = slope * ratios + intercept
    fig.add_trace(
        go.Scattergl(
            x=xs,
            y=y_reg,
            mode='lines',
            marker=dict(color='red', size=3),
            name=f'predictor {col}',
            showlegend=False
        ),
        row=row, col=col_num
    )

fig.update_layout(
    title='SdRatio model vs DMF for all wavelets',
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

# Select only the specified damping levels for the 2x2 grid
selected_dampings = ['pulses_0.02.csv', 'pulses_0.04.csv', 'pulses_0.08.csv', 'pulses_0.2.csv']

fig_grid = make_subplots(rows=2, cols=2, horizontal_spacing=0.08, vertical_spacing=0.10, 
    subplot_titles=[f'$\\xi={d.replace("pulses_", "").replace(".csv", "")}$' for d in selected_dampings])

for i, damping_file in enumerate(selected_dampings):
    dmf_grid = pd.read_csv(DMF_DIR / damping_file, index_col=0)
    dmf_grid.index = pd.to_numeric(dmf_grid.index, errors='coerce')
    saratio_grid = pd.read_csv(saratios_dir / 'pulses_0.05.csv', index_col=0)
    saratio_grid.index = pd.to_numeric(saratio_grid.index, errors='coerce')
    period_min, period_max = period_range
    saratio_grid = saratio_grid[(saratio_grid.index >= period_min) & (saratio_grid.index <= period_max)]
    dmf_grid = dmf_grid[(dmf_grid.index >= period_min) & (dmf_grid.index <= period_max)]
    df_melted_grid = create_melted_df(saratio_grid, dmf_grid, damping_file)
    x = df_melted_grid['SaRatio']
    y = df_melted_grid['DMF']
    X = sm.add_constant(x)
    model_grid = sm.OLS(y, X).fit()
    slope_grid, intercept_grid = model_grid.params[1], model_grid.params[0]
    x_reg_grid = np.linspace(x.min()-0.5, x.max()+0.5, 100)
    y_reg_grid = slope_grid * x_reg_grid + intercept_grid
    sampled_indices_grid = np.random.choice(len(df_melted_grid), size=len(df_melted_grid)//10, replace=False)
    row = i // 2 + 1
    col = i % 2 + 1
    fig_grid.add_trace(
        go.Scattergl(
            x=x.iloc[sampled_indices_grid],
            y=y.iloc[sampled_indices_grid],
            mode='markers',
            marker=dict(
                color=df_melted_grid['T'].iloc[sampled_indices_grid],
                colorscale='plasma',
                opacity=0.5,
                size=2,
                showscale=(col==2),
                colorbar=dict(title='T', thickness=14, len=0.7, x=1.05, y=0.5, yanchor='middle') if col==2 else None
            ),
            name='Data Points',
            showlegend=False
        ), row=row, col=col
    )
    fig_grid.add_trace(
        go.Scatter(
            x=x_reg_grid,
            y=y_reg_grid,
            mode='lines',
            line=dict(color='red', width=2),
            name='Regression Line',
            showlegend=False
        ), row=row, col=col
    )
    fig_grid.add_trace(
        go.Scatter(
            x=[1],
            y=[1],
            mode='markers',
            marker=dict(color='red', size=12, symbol='star'),
            name='(1,1)',
            showlegend=False
        ), row=row, col=col
    )

fig_grid.update_layout(
    height=1200, width=1200,
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(l=50, r=40, t=40, b=80),
    showlegend=False,
)
for i in range(1, 3):
    for j in range(1, 3):
        show_x_title = (i == 2)
        show_y_title = (j == 1)
        fig_grid.update_xaxes(
            range=[0.5, 4.5], dtick=0.5, showgrid=True, gridcolor='lightgray', gridwidth=1,
            linecolor='black', linewidth=1, mirror=True, zeroline=False,
            title_font=dict(size=18), title_standoff=30, ticks='inside', ticklen=10, tickwidth=2, tickcolor='black', tickson='boundaries',
            tickfont=dict(size=12),
            title_text='$S_R$' if show_x_title else '',
            row=i, col=j
        )
        fig_grid.update_yaxes(
            range=[0.7, 1.2], dtick=0.1, showgrid=True, gridcolor='lightgray', gridwidth=1,
            linecolor='black', linewidth=1, mirror=True, zeroline=False,
            title_font=dict(size=18), title_standoff=30, ticks='inside', ticklen=10, tickwidth=2, tickcolor='black', tickson='boundaries',
            tickfont=dict(size=12),
            title_text='DMF' if show_y_title else '',
            row=i, col=j
        )


# fig_grid.write_image('scatter_grid.pdf')

random_cols_grid = np.random.choice(saratio.columns, size=16, replace=False)
fig_wavelet_grid = make_subplots(rows=4, cols=4, 
    subplot_titles=[str(col) for col in random_cols_grid],
    horizontal_spacing=0.06, vertical_spacing=0.10)

for idx, col in enumerate(random_cols_grid):
    row = idx // 4 + 1
    col_num = idx % 4 + 1
    xs = saratio.index
    ratios = saratio[col].values
    dmfs = dmf[col].values
    show_legend = (row == 1 and col_num == 1)
    fig_wavelet_grid.add_trace(
        go.Scattergl(
            x=xs,
            y=dmfs,
            mode='lines',
            line=dict(color='black', width=1),
            name='Exact',
            showlegend=show_legend
        ), row=row, col=col_num
    )
    y_reg = slope * ratios + intercept
    fig_wavelet_grid.add_trace(
        go.Scattergl(
            x=xs,
            y=y_reg,
            mode='lines',
            line=dict(color='red', width=1),
            name='Prediction',
            showlegend=show_legend
        ), row=row, col=col_num
    )

fig_wavelet_grid.update_layout(
    height=1800, width=1800,
    plot_bgcolor='white', paper_bgcolor='white',
    margin=dict(l=40, r=40, t=40, b=60),
    showlegend=True,
)
for i in range(1, 5):
    for j in range(1, 5):
        show_x_title = (i == 4)
        show_y_title = (j == 1)
        fig_wavelet_grid.update_xaxes(
            range=[0, 3], dtick=0.5, showgrid=True, gridcolor='lightgray', gridwidth=1,
            linecolor='black', linewidth=1, mirror=True, zeroline=False,
            title_font=dict(size=14), title_standoff=20, ticks='inside', ticklen=8, tickwidth=1.5, tickcolor='black', tickson='boundaries',
            tickfont=dict(size=10),
            title_text='$T/T_p$' if show_x_title else '',
            row=i, col=j
        )
        fig_wavelet_grid.update_yaxes(
            range=[0.9, 1.6], dtick=0.1, showgrid=True, gridcolor='lightgray', gridwidth=1,
            linecolor='black', linewidth=1, mirror=True, zeroline=False,
            title_font=dict(size=14), title_standoff=20, ticks='inside', ticklen=8, tickwidth=1.5, tickcolor='black', tickson='boundaries',
            tickfont=dict(size=10),
            title_text='DMF' if show_y_title else '',
            row=i, col=j
        )
# fig_wavelet_grid.write_image('sdratio_model_vs_dmf_grid.pdf')