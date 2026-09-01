import streamlit as st
import plotly.express as px

# Page Title and Introduction
st.title("Country Explorer Demo")
st.write("This is an introductory demo that shows Streamlit core flow:" \
"loading data, adding a widget, filtering data, and displaying a chart.")

# Load the dataset
df = px.data.gapminder()

# Interactive input widget
"""
When a user changes this dropdown streamlit reruns to display new country data
"""

country = st.selectbox(
    "Select a country",
    options=sorted(df["country"].unique()),
    index=sorted(df["country"].unique()).index("United States"),
    key="country_select"
)

# Filter data based on user selection
country_data = df[df["country"] == country]

# Display a simple metric
latest_year_data = country_data[country_data["year"] == 
                                country_data["year"].max()].iloc[0]

st.metric(
    label=f"Life expectancy in {country} ({int(latest_year_data['year'])})",
    value=f"{latest_year_data['lifeExp']:.1f} years"
)

# Display a plotly chart
fig = px.line(
    country_data,
    x="year",
    y="lifeExp",
    markers=True,
    title=f"Life expectancy trend: {country}"
)

fig.update_layout(
    xaxis_title="Year", yaxis_title="Life expectancy (years)"
)

st.plotly_chart(fig, use_container_width=True)

# Display a filtered data table
st.subheader("Underlying data")
st.dataframe(country_data)