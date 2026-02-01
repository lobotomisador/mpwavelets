# MP Wavelets Dashboard

This dashboard provides interactive analysis tools for exploring the statistical relationship between the DMF and SdRatio.

The dashboard displays linear fits across DMF-SdRatio space with statistical test results and residual plots. The dashboard also shows the fit for each wavelet in the training set.

## Features

- **Interactive Data Exploration**: Select different AB parameter combinations and damping levels
- **Regression Analysis**: Perform linear regression with options to force through origin or use weighted least squares
- **Statistical Testing**: Automated heteroscedasticity tests (Breusch-Pagan and White tests)
- **Visualization**: Multiple Plotly-based visualizations including scatter plots, residual plots, and wavelet comparisons
- **Period Filtering**: Filter data by period range for focused analysis

## Quickstart

```bash
uv sync
```

Once dependencies are installed:

```bash
source .venv/bin/activate
make
```

## Usage

1. **Select Directory**: Choose between `saratios` or `saratios_constant` directories
2. **Select AB Combination**: Choose the parameter combination (e.g., `a=0.020_b=2.100`)
3. **Select Damping**: Choose the damping level from available CSV files
4. **Adjust Period Range**: Use the slider to filter data by period range (default: 0.1-3.0 seconds)
5. **Configure Regression Options**:
   - Force fit through (1,1): Constrain regression to pass through the point (1,1)
   - Use Weighted Least Squares: Apply KDE-based weights to regression
6. **View Results**: The dashboard displays:
   - Scatter plot of SaRatio vs DMF with regression line
   - Statistical test results for heteroscedasticity
   - Residual plots
   - Comparison plots for multiple wavelets
   - Grid visualizations for different damping levels

## Deployment

The application is configured for deployment on Fly.io. To deploy:

1. Install Fly CLI: https://fly.io/docs/getting-started/installing-flyctl/
2. Deploy:

```bash
fly deploy
```

Configuration is managed in `fly.toml`.

## Live Demo

The application is deployed at: https://mpwavelets.fly.dev/

## License

MIT License - see [LICENSE](LICENSE) file for details.
