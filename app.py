

import streamlit as st
import pandas as pd
import plotly.express as px
import re

# ===== DARK THEME SETUP =====
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
st.sidebar.header("🔮 Filter Options")

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

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Models Found", len(filtered_df))
col2.metric("Avg Price", f"${filtered_df[price_col].mean():.0f}")
col3.metric("Max RAM", f"{filtered_df['RAM'].max()}GB")

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



# import streamlit as st
# import pandas as pd
# import plotly.express as px

# # ===== DARK THEME SETUP =====
# st.markdown("""
# <style>
# :root {
#     --primary: #08e8de;
#     --secondary: #a777e3;
# }

# .stApp {
#     background-color: #0e1117 !important;
#     color: #ffffff !important;
# }

# .stSidebar {
#     background-color: #1a1d24 !important;
#     border-right: 1px solid #2a2e36;
# }

# .stDataFrame {
#     background-color: #1a1d24 !important;
#     color: white !important;
# }

# .stMetric {
#     background-color: #1a1d24 !important;
#     border: 1px solid #2a2e36;
# }

# h1, h2, h3 {
#     color: var(--primary) !important;
#     text-shadow: 0 0 8px var(--primary);
# }

# .stButton>button {
#     background: linear-gradient(135deg, var(--primary), var(--secondary));
#     color: black !important;
#     font-weight: bold;
#     border: none;
# }

# .stSelectbox, .stMultiselect, .stSlider {
#     background-color: #1a1d24 !important;
# }

# /* Plotly dark theme */
# .js-plotly-plot .plotly, .js-plotly-plot .plotly .modebar {
#     background-color: #1a1d24 !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # ===== DATA LOADING =====
# @st.cache_data
# def load_data():
#     df = pd.read_csv("Mobiles Dataset (2025).csv", encoding='ISO-8859-1')
#     # Add your data cleaning code here
#     return df

# df = load_data()

# # ===== DARK MODE UI =====
# st.title("📱 Mobile Analyzer Pro")
# st.markdown("Explore smartphone specs in **dark mode**")

# # Sidebar Filters
# with st.sidebar:
#     st.header("🔮 Filters")
#     selected_brands = st.multiselect(
#         "Select Brands",
#         options=sorted(df['Company Name'].unique()),
#         default=['Apple', 'Samsung']
#     )
#     price_range = st.slider(
#         "Price Range (USD)",
#         min_value=int(df['Launched Price (USA)'].min()),
#         max_value=int(df['Launched Price (USA)'].max()),
#         value=(500, 1000)
#     )

# # Apply Filters
# filtered_df = df[
#     (df['Company Name'].isin(selected_brands)) &
#     (df['Launched Price (USA)'].between(price_range[0], price_range[1]))
# ]

# # Metrics Cards
# col1, col2, col3 = st.columns(3)
# col1.metric("Total Models", len(filtered_df))
# col2.metric("Avg Price", f"${filtered_df['Launched Price (USA)'].mean():.0f}")
# col3.metric("Max RAM", f"{filtered_df['RAM'].max()}GB")

# # Dark-themed Data Table
# st.dataframe(
#     filtered_df.style
#     .background_gradient(subset=['Launched Price (USA)'], cmap='YlOrRd')
#     .highlight_max(color='#08e8de'),
#     height=400
# )

# # Dark Visualizations
# tab1, tab2 = st.tabs(["📉 Price Analysis", "🔋 Specs"])

# with tab1:
#     fig = px.box(filtered_df, 
#                 x='Company Name', 
#                 y='Launched Price (USA)',
#                 template='plotly_dark')
#     st.plotly_chart(fig, use_container_width=True)

# with tab2:
#     fig = px.scatter(filtered_df,
#                    x='Battery Capacity',
#                    y='RAM',
#                    color='Company Name',
#                    template='plotly_dark',
#                    hover_name='Model Name')
#     st.plotly_chart(fig, use_container_width=True)

# # Glowing Download Button
# st.download_button(
#     label=" Download Data",
#     data=filtered_df.to_csv(index=False),
#     file_name="filtered_mobiles.csv",
#     mime="text/csv"
# )

# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px
# # import re

# # @st.cache_data
# # def load_data():
# #     try:
# #         df = pd.read_excel("Mobiles Dataset (2025).xlsx")
# #     except:
# #         df = pd.read_csv("Mobiles Dataset (2025).csv", encoding='ISO-8859-1')
    
# #     # Clean data conversions
# #     df.columns = df.columns.str.strip()
    
# #     # Custom function to clean price strings
# #     def clean_price(price_str):
# #         if isinstance(price_str, str):
# #             # Remove all non-numeric characters except decimal point
# #             cleaned = re.sub(r'[^\d.]', '', price_str)
# #             return float(cleaned) if cleaned else None
# #         return price_str
    
# #     # Convert price columns
# #     price_columns = [
# #         'Launched Price (Pakistan)',
# #         'Launched Price (India)',
# #         'Launched Price (China)',
# #         'Launched Price (USA)',
# #         'Launched Price (Dubai)'
# #     ]
    
# #     for col in price_columns:
# #         df[col] = df[col].apply(clean_price)
# #         df[col] = pd.to_numeric(df[col], errors='coerce')
    
# #     # Convert other numeric columns
# #     numeric_conversions = {
# #         'Mobile Weight': ('g', 1),
# #         'RAM': ('GB', 1),
# #         'Battery Capacity': ('mAh', 1),
# #         'Screen Size': ('inches', 1)
# #     }
    
# #     for col, (unit, multiplier) in numeric_conversions.items():
# #         if col in df.columns:
# #             df[col] = df[col].astype(str).str.replace(unit, '')
# #             df[col] = pd.to_numeric(df[col], errors='coerce') * multiplier
    
# #     # Drop rows with missing critical values
# #     df = df.dropna(subset=['Launched Price (USA)'])
    
# #     return df

# # try:
# #     df = load_data()
# # except Exception as e:
# #     st.error(f"Error loading data: {str(e)}")
# #     st.stop()

# # # ==================== SIDEBAR FILTERS ====================
# # st.sidebar.header("Filter Options")

# # # 1. Brand Selection
# # selected_brands = st.sidebar.multiselect(
# #     "Select Brands",
# #     options=sorted(df['Company Name'].unique()),
# #     default=['Apple', 'Samsung']
# # )

# # # 2. Price Range Slider
# # price_col = 'Launched Price (USA)'

# # if len(selected_brands) > 0:
# #     brand_filtered = df[df['Company Name'].isin(selected_brands)]
# #     price_min = int(brand_filtered[price_col].min())
# #     price_max = int(brand_filtered[price_col].max())
# # else:
# #     price_min = int(df[price_col].min())
# #     price_max = int(df[price_col].max())

# # price_range = st.sidebar.slider(
# #     "Price Range (USD)",
# #     min_value=price_min,
# #     max_value=price_max,
# #     value=(price_min, price_max)
# # )

# # # Rest of your dashboard code...

# # # 3. RAM Filter
# # ram_options = st.sidebar.multiselect(
# #     "RAM (GB)",
# #     options=sorted(df['RAM'].unique()),
# #     default=[4, 6, 8]
# # )

# # # ==================== MAIN DASHBOARD ====================
# # st.title("Mobile Phone Comparison Dashboard")

# # # Apply filters
# # filtered_df = df[
# #     (df['Company Name'].isin(selected_brands)) &
# #     (df[price_col].between(price_range[0], price_range[1])) &
# #     (df['RAM'].isin(ram_options))
# # ]

# # # Display metrics and data
# # col1, col2, col3 = st.columns(3)
# # col1.metric("Models Found", len(filtered_df))
# # col2.metric("Avg Price", f"${filtered_df[price_col].mean():.0f}")
# # col3.metric("Max RAM", f"{filtered_df['RAM'].max()}GB")

# # st.dataframe(filtered_df)

# # # Visualization
# # st.header("Price Distribution")
# # fig = px.box(filtered_df, x='Company Name', y=price_col)
# # st.plotly_chart(fig, use_container_width=True)


# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import base64
# from io import BytesIO
# import time

# # --- Data Loading ---
# @st.cache_data
# def load_data():
#     df = pd.read_csv("Mobiles Dataset (2025).csv", encoding='ISO-8859-1')
    
#     # Data cleaning (add your existing cleaning code here)
#     return df

# df = load_data()

# # --- Creative Enhancements ---

# # 1. Animated Header (No Lottie needed)
# st.markdown("""
# <h1 style='text-align: center; animation: pulse 2s infinite;'>
#      <span style='color: #08e8de'>Mobile</span> <span style='color: #a777e3'>Analyzer</span>
# </h1>
# <style>
# @keyframes pulse {
#     0% { transform: scale(1); }
#     50% { transform: scale(1.05); }
#     100% { transform: scale(1); }
# }
# </style>
# """, unsafe_allow_html=True)

# # 2. Interactive Filters (Improved)
# with st.sidebar:
#     st.header(" Filters")
    
#     # Dynamic brand filter
#     selected_brands = st.multiselect(
#         "Select Brands",
#         options=sorted(df['Company Name'].unique()),
#         default=['Apple', 'Samsung']
#     )
    
#     # Real-time search
#     search_term = st.text_input("Search Models")

# # 3. Animated Metrics
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.markdown("""
#     <div style='background: linear-gradient(135deg, #6e8efb, #a777e3);
#                 padding: 15px;
#                 border-radius: 10px;
#                 color: white;
#                 text-align: center;'>
#         <h3>Total Models</h3>
#         <h2>{}</h2>
#     </div>
#     """.format(len(df)), unsafe_allow_html=True)
    
# dark = st.checkbox("Dark Mode")
# if dark:
#     st.markdown("<style>.stApp {background-color: #1e1e1e;}</style>", unsafe_allow_html=True)

# # 4. Interactive Comparison Tool
# with st.expander(" Compare Phones", expanded=True):
#     cols = st.columns(2)
#     with cols[0]:
#         phone1 = st.selectbox("Select Phone 1", df['Model Name'].unique())
#     with cols[1]:
#         phone2 = st.selectbox("Select Phone 2", df['Model Name'].unique())
    
#     compare_df = df[df['Model Name'].isin([phone1, phone2])].set_index('Model Name').T
#     st.dataframe(compare_df.style.highlight_max(axis=1, color='lightgreen'))

# # 5. Dynamic Visualization
# tab1, tab2 = st.tabs([" Price Analysis", " Specs Overview"])

# with tab1:
#     fig = px.box(df, x='Company Name', y='Launched Price (USA)')
#     st.plotly_chart(fig, use_container_width=True)

# with tab2:
#     fig = px.scatter(df, x='Battery Capacity', y='RAM', color='Company Name')
#     st.plotly_chart(fig, use_container_width=True)

# # 6. Download Button
# def to_excel(df):
#     output = BytesIO()
#     writer = pd.ExcelWriter(output, engine='xlsxwriter')
#     df.to_excel(writer, index=False, sheet_name='Sheet1')
#     writer.close()
#     processed_data = output.getvalue()
#     return processed_data

# st.download_button(
#     label=" Download Full Data",
#     data=to_excel(df),
#     file_name='mobile_data.xlsx',
#     mime='application/vnd.ms-excel'
# )

# # 7. Confetti Effect (Native Streamlit)
# if st.button("🎉 Celebrate!"):
#     st.balloons()

# # --- Custom CSS ---
# st.markdown("""
# <style>
# /* Animated background */
# .stApp {
#     background-image: linear-gradient(to bottom right, #f5f7fa, #e4e8f0);
# }

# /* Hover effects */
# .stDataFrame {
#     transition: transform 0.3s;
# }
# .stDataFrame:hover {
#     transform: scale(1.01);
# }
# </style>
# """, unsafe_allow_html=True)


# # 1. Animated Welcome Header

# from streamlit_lottie import st_lottie
# import requests

# # Load Lottie animation
# def load_lottie(url):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()

# lottie_phone = load_lottie("https://lottie.host/a3d2a5e5-1a23-4f7a-a5a1-2d6f3f8d3b3e/5pQ0XwY4Zk.json")
# st_lottie(lottie_phone, height=200, key="phone")

# # 2. Neon Glow Title

# st.markdown("""
# <h1 style='text-align: center; color: #08e8de; 
# text-shadow: 0 0 10px #00ffea, 0 0 20px #0084ff;'>
# 📱 Mobile Analyzer Pro
# </h1>
# """, unsafe_allow_html=True)

# # Interactive 3D scatterplot

# import plotly.express as px
# fig = px.scatter_3d(filtered_df, 
#                    x='Battery Capacity', 
#                    y='RAM', 
#                    z=price_col,
#                    color='Company Name',
#                    hover_name='Model Name')
# st.plotly_chart(fig, use_container_width=True)

# # Dynamic Price converter

# with st.expander("💱 Real-time Price Converter"):
#     usd = st.number_input("USD Amount", value=100)
#     col1, col2, col3 = st.columns(3)
#     col1.metric("PKR", f"Rs {usd * 278:.2f}")
#     col2.metric("EUR", f"€ {usd * 0.92:.2f}")
#     col3.metric("AED", f"AED {usd * 3.67:.2f}")


