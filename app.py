import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Custom CSS for Styling
st.set_page_config(page_title="Amazon E-Commerce Analytics", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .metric-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🛒 Amazon E-Commerce Analytics Dashboard")
st.markdown("Explore executive performance metrics, brand distribution, and deep-dive product insights.")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_amazon_ecommerce.csv')

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("🔍 Filters")

all_categories = sorted(df['category'].dropna().unique())
selected_category = st.sidebar.selectbox("Category", options=["All"] + all_categories)

if selected_category != "All":
    df_filtered = df[df['category'] == selected_category]
else:
    df_filtered = df

all_brands = sorted(df_filtered['brand'].dropna().unique())
selected_brand = st.sidebar.selectbox("Brand", options=["All"] + all_brands)

if selected_brand != "All":
    df_filtered = df_filtered[df_filtered['brand'] == selected_brand]

# 4. Formatted Executive Metrics Row
total_rev = df_filtered['final_price'].sum()
total_orders = len(df_filtered)
avg_price = df_filtered['final_price'].mean()
avg_rating = df_filtered['rating'].mean() if 'rating' in df_filtered.columns else 0

# Format GMV cleanly to avoid overflow clipping
if total_rev >= 1e9:
    rev_str = f"${total_rev / 1e9:,.2f}B"
elif total_rev >= 1e6:
    rev_str = f"${total_rev / 1e6:,.2f}M"
else:
    rev_str = f"${total_rev:,.2f}"

st.markdown("### 📊 Executive Summary")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue (GMV)", rev_str)
col2.metric("Total Transactions", f"{total_orders:,}")
col3.metric("Avg Final Price", f"${avg_price:,.2f}")
col4.metric("Average Rating", f"{avg_rating:.2f} ⭐")

st.markdown("---")

# 5. Visualizations Section with Professional Color Palettes
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader("🏆 Top Brands by Revenue")
    top_brands = df_filtered.groupby('brand')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(10)
    fig_brand = px.bar(
        top_brands, x='final_price', y='brand', orientation='h',
        color='final_price', color_continuous_scale='Teal',
        template='plotly_white'
    )
    fig_brand.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_brand, use_container_width=True)

with row1_col2:
    st.subheader("📦 Revenue Breakdown by Subcategory")
    if 'subcategory' in df_filtered.columns:
        top_subcat = df_filtered.groupby('subcategory')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(8)
        fig_subcat = px.pie(
            top_subcat, names='subcategory', values='final_price', hole=0.5,
            template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_subcat.update_layout(margin=dict(t=10, b=10, l=10, r=10))
        st.plotly_chart(fig_subcat, use_container_width=True)
    else:
        st.info("Subcategory column not available.")

# 6. Interactive Data Explorer Table
st.markdown("---")
st.subheader("📋 Filtered Transaction Data Explorer")
st.dataframe(df_filtered.head(100), use_container_width=True)

# 7. Export Options
csv_data = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name='filtered_amazon_sales.csv',
    mime='text/csv'
)