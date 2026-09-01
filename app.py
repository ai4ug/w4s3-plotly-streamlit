import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="Gapminder Analytics Explorer",
    layout="wide"
)

# Main Title and Overview
st.title("Gapminder Analytics Explorer")
st.caption("A comprehensive dashboard demonstrating advanced Streamlit capabilities: caching, sidebar layouts, dynamic KPIs, tabs, Plotly charts, and data export.")

# Cached Data Loading
@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

# Sidebar Controls
with st.sidebar:
    st.header("Filter Controls")
    
    year = st.slider(
        "Select Year",
        min_value=int(df["year"].min()),
        max_value=int(df["year"].max()),
        step=5,
        value=2007,
        key="year_slider"
    )
    
    all_continents = sorted(list(df["continent"].unique()))
    continents = st.multiselect(
        "Select Continents",
        options=all_continents,
        default=all_continents,
        key="continents_select"
    )
    
    st.divider()
    st.header("Visualization Settings")
    
    log_x = st.checkbox("Logarithmic Scale for GDP", value=True, key="log_x_toggle")
    max_bubble_size = st.slider("Max Bubble Size", min_value=20, max_value=100, value=60, step=5, key="bubble_size_slider")
    color_scheme = st.selectbox(
        "Color Metric",
        options=["continent", "lifeExp", "gdpPercap"],
        key="color_scheme_select"
    )

# Filter Data
filtered_df = df[(df["year"] == year) & (df["continent"].isin(continents))]

if filtered_df.empty:
    st.warning("No data found for the selected combination of year and continents.")
    st.stop()

# Top KPI Metric Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

avg_life = filtered_df["lifeExp"].mean()
total_pop = filtered_df["pop"].sum()
median_gdp = filtered_df["gdpPercap"].median()
country_count = len(filtered_df)

kpi1.metric(label="Countries Displayed", value=country_count)
kpi2.metric(label="Total Population", value=f"{total_pop:,.0f}")
kpi3.metric(label="Average Life Expectancy", value=f"{avg_life:.1f} yrs")
kpi4.metric(label="Median GDP per Capita", value=f"${median_gdp:,.0f}")

st.divider()

# Tabbed Interface
tab_overview, tab_distribution, tab_rankings, tab_compare, tab_data, tab_guide = st.tabs([
    "Global Overview",
    "Regional Distributions",
    "Rankings",
    "Multi-Country Trends",
    "Data & Export",
    "Streamlit Concepts Guide"
])

with tab_overview:
    st.subheader(f"Global Life Expectancy vs GDP per Capita ({year})")
    fig_scatter = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color=color_scheme,
        hover_name="country",
        log_x=log_x,
        size_max=max_bubble_size,
        labels={
            "gdpPercap": "GDP per Capita (USD)",
            "lifeExp": "Life Expectancy (Years)",
            "pop": "Population",
            "continent": "Continent"
        }
    )
    fig_scatter.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)

with tab_distribution:
    dist_col1, dist_col2 = st.columns(2)
    
    with dist_col1:
        st.subheader("Life Expectancy Distribution by Continent")
        fig_box = px.box(
            filtered_df,
            x="continent",
            y="lifeExp",
            color="continent",
            points="all",
            labels={"lifeExp": "Life Expectancy (Years)", "continent": "Continent"}
        )
        st.plotly_chart(fig_box, use_container_width=True)
        
    with dist_col2:
        st.subheader("GDP per Capita Distribution")
        fig_hist = px.histogram(
            filtered_df,
            x="gdpPercap",
            color="continent",
            nbins=30,
            log_x=log_x,
            labels={"gdpPercap": "GDP per Capita (USD)"}
        )
        st.plotly_chart(fig_hist, use_container_width=True)

with tab_rankings:
    rank_col1, rank_col2 = st.columns(2)
    
    with rank_col1:
        st.subheader("Top 10 Countries: Life Expectancy")
        top_life = filtered_df.nlargest(10, "lifeExp")[["country", "lifeExp", "continent"]]
        fig_top = px.bar(
            top_life,
            x="lifeExp",
            y="country",
            color="continent",
            orientation="h",
            labels={"lifeExp": "Life Expectancy (Years)", "country": "Country"}
        )
        fig_top.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_top, use_container_width=True)
        
    with rank_col2:
        st.subheader("Top 10 Countries: GDP per Capita")
        top_gdp = filtered_df.nlargest(10, "gdpPercap")[["country", "gdpPercap", "continent"]]
        fig_gdp = px.bar(
            top_gdp,
            x="gdpPercap",
            y="country",
            color="continent",
            orientation="h",
            labels={"gdpPercap": "GDP per Capita (USD)", "country": "Country"}
        )
        fig_gdp.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig_gdp, use_container_width=True)

with tab_compare:
    st.subheader("Historical Trend Comparison")
    selected_compare_countries = st.multiselect(
        "Select Countries to Compare Over Time",
        options=sorted(df["country"].unique()),
        default=["United States", "China", "India", "Germany", "Brazil"],
        key="compare_countries_multiselect"
    )
    
    if selected_compare_countries:
        compare_df = df[df["country"].isin(selected_compare_countries)]
        
        c_col1, c_col2 = st.columns(2)
        with c_col1:
            fig_trend_life = px.line(
                compare_df,
                x="year",
                y="lifeExp",
                color="country",
                markers=True,
                title="Life Expectancy (1952 to 2007)"
            )
            st.plotly_chart(fig_trend_life, use_container_width=True)
            
        with c_col2:
            fig_trend_gdp = px.line(
                compare_df,
                x="year",
                y="gdpPercap",
                color="country",
                markers=True,
                title="GDP per Capita (1952 to 2007)"
            )
            st.plotly_chart(fig_trend_gdp, use_container_width=True)

with tab_data:
    st.subheader("Filtered Dataset View")
    st.dataframe(
        filtered_df.sort_values("lifeExp", ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    with st.expander("Statistical Summary (describe)"):
        st.write(filtered_df[["lifeExp", "pop", "gdpPercap"]].describe())
    
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Filtered Data (CSV)",
        data=csv_bytes,
        file_name=f"gapminder_{year}_filtered.csv",
        mime="text/csv",
        key="download_gapminder_csv"
    )

with tab_guide:
    st.markdown("""
    ### Streamlit Core Concepts for Learners
    
    #### The Reactive Execution Model
    Streamlit executes scripts from top to bottom whenever an interactive input changes.
    
    #### Caching
    Using `@st.cache_data` avoids re-reading data or re-running heavy calculations on every interaction.
    
    #### Layout Primitives
    - `st.sidebar`: Collapsible side panel for user configuration.
    - `st.columns`: Horizontal column layout for side-by-side components.
    - `st.tabs`: Tabbed views for multi-page dashboard organization.
    - `st.expander`: Collapsible disclosure box for supplementary info.
    - `st.metric`: Display cards for high-level statistics and KPIs.
    
    #### Plotly Integration
    Streamlit natively displays interactive Plotly visualizations with `st.plotly_chart`.
    """)
