

import streamlit as st
import pandas as pd
import plotly.express as px
import re

# ===== DARK THEME SETUP =====
# Add this CSS at the top of your dark theme section
st.markdown("""
<style>
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.stPlotlyChart, .stDataFrame, .stMetric {
    animation: fadeIn 0.5s ease-out;
}

/* Smooth transitions for tabs */
.stTabs [role="tabpanel"] {
    transition: all 0.3s ease;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
:root {
    --primary: #08e8de;
    --secondary: #a777e3;
}

.stApp {
    background-color: #0e1117 !important;
    color: #ffffff !important;
}

.stSidebar {
    background-color: #1a1d24 !important;
    border-right: 1px solid #2a2e36;
}

.stDataFrame {
    background-color: #1a1d24 !important;
    color: white !important;
}

.stMetric {
    background-color: #1a1d24 !important;
    border: 1px solid #2a2e36;
}

h1, h2, h3 {
    color: var(--primary) !important;
    text-shadow: 0 0 8px var(--primary);
}

.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: black !important;
    font-weight: bold;
    border: none;
}

.stSelectbox, .stMultiselect, .stSlider {
    background-color: #1a1d24 !important;
}

/* Plotly dark theme */
.js-plotly-plot .plotly, .js-plotly-plot .plotly .modebar {
    background-color: #1a1d24 !important;
}
</style>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_data():
    try:
        df = pd.read_excel("Mobiles Dataset (2025).xlsx")
    except:
        df = pd.read_csv("Mobiles Dataset (2025).csv", encoding='ISO-8859-1')

    df.columns = df.columns.str.strip()

    def clean_price(price_str):
        if isinstance(price_str, str):
            cleaned = re.sub(r'[^\d.]', '', price_str)
            return float(cleaned) if cleaned else None
        return price_str

    price_columns = [
        'Launched Price (Pakistan)', 'Launched Price (India)',
        'Launched Price (China)', 'Launched Price (USA)', 'Launched Price (Dubai)'
    ]

    for col in price_columns:
        if col in df.columns:
            df[col] = df[col].apply(clean_price)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Numeric conversion for units
    numeric_conversions = {
        'Mobile Weight': ('g', 1),
        'RAM': ('GB', 1),
        'Battery Capacity': ('mAh', 1),
        'Screen Size': ('inches', 1)
    }

    for col, (unit, multiplier) in numeric_conversions.items():
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(unit, '', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce') * multiplier

    df = df.dropna(subset=['Launched Price (USA)'])

    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ===== SIDEBAR FILTERS =====
st.sidebar.header("Filter Options")

selected_brands = st.sidebar.multiselect(
    "Select Brands",
    options=sorted(df['Company Name'].dropna().unique()),
    default=['Apple', 'Samsung']
)

price_col = 'Launched Price (USA)'

if selected_brands:
    brand_filtered = df[df['Company Name'].isin(selected_brands)]
    price_min = int(brand_filtered[price_col].min())
    price_max = int(brand_filtered[price_col].max())
else:
    price_min = int(df[price_col].min())
    price_max = int(df[price_col].max())

price_range = st.sidebar.slider(
    "Price Range (USD)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max)
)

ram_options = st.sidebar.multiselect(
    "RAM (GB)",
    options=sorted(df['RAM'].dropna().unique()),
    default=[4, 6, 8]
)

# ===== MAIN DASHBOARD =====
st.title(" Mobile Analyzer Pro")
st.markdown("Explore smartphone specs in **dark mode**")

# Filtered Data
filtered_df = df[
    (df['Company Name'].isin(selected_brands)) &
    (df[price_col].between(price_range[0], price_range[1])) &
    (df['RAM'].isin(ram_options))
]


# Replace your current metrics section with this:
st.markdown("""
<style>
:root {
    --primary: #08e8de;
    --secondary: #1a1d24;
    --glow: rgba(8, 232, 222, 0.15);
}

.glow-card {
    background: #1a1d24;
    border-radius: 10px;
    padding: 20px;
    border-left: 4px solid var(--primary);
    box-shadow: 0 4px 8px var(--glow);
    transition: all 0.3s ease;
    height: 120px;  /* Fixed height */
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.glow-card:hover {
    box-shadow: 0 6px 12px var(--glow);
    transform: translateY(-2px);
}

.glow-card h3 {
    font-size: 1rem;
    margin: 0 0 8px 0;
    color: #a6a6a6;
}

.glow-card h1 {
    font-size: 1.8rem;
    margin: 0;
    color: var(--primary);
    text-shadow: 0 0 8px var(--glow);
}
</style>
""", unsafe_allow_html=True)

cols = st.columns(3)
with cols[0]:
    st.markdown(f"""
    <div class="glow-card">
        <h3>📱 Models Found</h3>
        <h1>{len(filtered_df)}</h1>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown(f"""
    <div class="glow-card">
        <h3>💰 Avg Price</h3>
        <h1>${filtered_df[price_col].mean():.0f}</h1>
    </div>
    """, unsafe_allow_html=True)

with cols[2]:
    st.markdown(f"""
    <div class="glow-card">
        <h3>⚡ Max RAM</h3>
        <h1>{filtered_df['RAM'].max()}GB</h1>
    </div>
    """, unsafe_allow_html=True)
    
st.markdown("""
<style>
br
</style>
""", unsafe_allow_html=True)

# Metrics
# col1, col2, col3 = st.columns(3)
# col1.metric("Models Found", len(filtered_df))
# col2.metric("Avg Price", f"${filtered_df[price_col].mean():.0f}")
# col3.metric("Max RAM", f"{filtered_df['RAM'].max()}GB")


# Data Table
st.dataframe(
    filtered_df.style
    .background_gradient(subset=[price_col], cmap='YlOrRd')
    .highlight_max(color='#08e8de'),
    height=400
)

# Tabs
tab1, tab2 = st.tabs([" Price Analysis", " Specs"])

with tab1:
    fig1 = px.box(
        filtered_df,
        x='Company Name',
        y=price_col,
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.scatter(
        filtered_df,
        x='Battery Capacity',
        y='RAM',
        color='Company Name',
        template='plotly_dark',
        hover_name='Model Name'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Download Button
st.download_button(
    label=" Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_mobiles.csv",
    mime="text/csv"
)


# Add this in your visualization section (after the existing tabs)
with st.expander("Interactive Scatter Matrix"):
    st.write("Compare multiple features simultaneously:")
    features = st.multiselect(
        "Select features to compare",
        options=['RAM', 'Battery Capacity', 'Screen Size', price_col],
        default=['RAM', 'Battery Capacity']
    )
    
    if len(features) >= 2:
        fig_matrix = px.scatter_matrix(
            filtered_df,
            dimensions=features,
            color='Company Name',
            template='plotly_dark',
            hover_name='Model Name'
        )
        st.plotly_chart(fig_matrix, use_container_width=True)
    else:
        st.warning("Select at least 2 features")
        


# Initialize tabs FIRST (before any content)
tab1, tab2, tab3 = st.tabs(["Market Share","Price Analysis", "Specs"])


# ===== Tab 3: Market Share ===== 
with tab1:
    st.write("Brand distribution by price segments:")
    
    filtered_df['Price Segment'] = pd.cut(
        filtered_df[price_col],
        bins=[0, 300, 600, 900, 1200, float('inf')],
        labels=['<$300', '$300-$600', '$600-$900', '$900-$1200', '>$1200']
    )
    
    fig_sunburst = px.sunburst(
        filtered_df,
        path=['Company Name', 'Price Segment'],
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    st.plotly_chart(fig_sunburst, use_container_width=True)
    
# ===== Tab 1: Price Analysis =====
with tab2:
    st.header("Price Distribution by Brand")
    
    # Check if filtered_df exists and has data
    if not filtered_df.empty:
        fig_price = px.box(
            filtered_df,
            x='Company Name',
            y=price_col,
            template='plotly_dark',
            color='Company Name'
        )
        st.plotly_chart(fig_price, use_container_width=True)
    else:
        st.warning("No data available with current filters")

# ===== Tab 2: Specs =====
with tab3   :
    st.header("Specs Comparison")
    
    if not filtered_df.empty:
        fig_specs = px.scatter(
            filtered_df,
            x='Battery Capacity',
            y='RAM',
            color='Company Name',
            size=price_col,
            template='plotly_dark',
            hover_name='Model Name'
        )
        st.plotly_chart(fig_specs, use_container_width=True)
    else:
        st.warning("No data available with current filters")

    
# Add this in your visualization section
with st.expander("Parallel Coordinates Analysis"):
    st.write("Compare multiple specs across brands:")
    parallel_features = st.multiselect(
        "Select specs to compare",
        options=['RAM', 'Battery Capacity', 'Screen Size', price_col],
        default=['RAM', 'Battery Capacity', price_col]
    )
    
    if len(parallel_features) >= 2:
        fig_parallel = px.parallel_coordinates(
            filtered_df,
            dimensions=parallel_features,
            color=price_col,
            template='plotly_dark',
            color_continuous_scale=px.colors.sequential.Viridis
        )
        st.plotly_chart(fig_parallel, use_container_width=True)
       
