# Gapminder Streamlit Dashboards

Teaching applications demonstrating Streamlit from fundamental concepts to full dashboards using the Gapminder dataset.

## Application Structure

### 1. Introductory Basics (`mini_app.py`)
Designed as a first demo for students:
- Loads the dataset.
- Adds a single country dropdown (`st.selectbox`).
- Filters the dataframe reactively.
- Displays a simple KPI metric card (`st.metric`).
- Renders a clean Plotly line chart (`st.plotly_chart`).
- Displays the filtered tabular data (`st.dataframe`).

### 2. Full Analytics Dashboard (`app.py`)
Demonstrates the full range of Streamlit production patterns:
- Performance optimization using `@st.cache_data`.
- Collapsible sidebar controls for multi-faceted data slicing and visual formatting.
- Multi-column layout with 4 dynamic KPI summary metric cards.
- Tabbed interface (`st.tabs`):
  - Global Overview: Interactive bubble scatter plot.
  - Regional Distributions: Box plots and distribution histograms.
  - Rankings: Top 10 rankings by life expectancy and GDP.
  - Multi-Country Trends: Historical time series comparisons.
  - Data & Export: Data table, summary statistics expander, and CSV download button.
  - Streamlit Concepts Guide: In-app curriculum notes on execution flow, caching, and layout components.

## Setup Instructions

1. Open this folder in VS Code.
2. Open the integrated terminal (`Ctrl+` ` or `Cmd+` `).
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the apps:
   - For the introductory demo:
     ```bash
     streamlit run mini_app.py
     ```
   - For the complete dashboard:
     ```bash
     streamlit run app.py
     ```
5. A browser tab will open automatically at http://localhost:8501.