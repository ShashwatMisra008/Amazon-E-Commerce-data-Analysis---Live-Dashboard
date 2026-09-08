import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Wide Layout optimized for CEO Presentation View)
st.set_page_config(page_title="CEO E-Commerce Executive Briefing", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 0.8rem; padding-bottom: 0rem; }
        h1 { font-size: 1.4rem !important; margin-bottom: 0rem !important; }
        h3 { font-size: 1.0rem !important; margin-top: 0rem !important; margin-bottom: 0.1rem !important; }
        .rec-box { background-color: #f8f9fa; padding: 10px; border-radius: 6px; border-left: 4px solid #008080; font-size: 0.85rem; height: 100%; }
    </style>
""", unsafe_allow_html=True)

st.title("👔 CEO Executive Performance & Strategy Dashboard")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_amazon_ecommerce.csv')

df = load_data()

# 3. Sidebar Slicers for Interactive CEO Deep Dives
st.sidebar.header("🎛️ Executive Slicers")
categories = sorted(df['category'].dropna().unique())
sel_cat = st.sidebar.selectbox("Category View", ["All"] + categories)
df_f = df[df['category'] == sel_cat] if sel_cat != "All" else df

brands = sorted(df_f['brand'].dropna().unique())
sel_brand = st.sidebar.selectbox("Brand View", ["All"] + brands)
if sel_brand != "All": df_f = df_f[df_f['brand'] == sel_brand]

# 4. Core Financial Metrics Row (4 Key Numbers)
total_gmv = df_f['final_price'].sum()
total_orders = len(df_f)
avg_price = df_f['final_price'].mean() if total_orders > 0 else 0
avg_rating = df_f['rating'].mean() if 'rating' in df_f.columns and total_orders > 0 else 0

gmv_str = f"${total_gmv/1e9:,.2f}B" if total_gmv >= 1e9 else f"${total_gmv/1e6:,.2f}M"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (GMV)", gmv_str)
col2.metric("Total Transactions", f"{total_orders:,}")
col3.metric("Average Ticket Size", f"${avg_price:,.2f}")
col4.metric("Marketplace Rating", f"{avg_rating:.2f} ⭐")

st.markdown("---")

# 5. Visual Insights Layout (Charts side-by-side)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🏆 Top Revenue Generating Brands")
    top_brands = df_f.groupby('brand')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(5)
    fig_brand = px.bar(top_brands, x='final_price', y='brand', orientation='h', color='final_price', color_continuous_scale='Teal', template='plotly_white')
    fig_brand.update_layout(yaxis={'categoryorder':'total ascending'}, height=190, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
    st.plotly_chart(fig_brand, use_container_width=True)

with chart_col2:
    st.subheader("📦 Revenue Breakdown by Category")
    top_cats = df_f.groupby('category')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(5)
    fig_cat = px.pie(top_cats, names='category', values='final_price', hole=0.5, template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_cat.update_layout(height=190, margin=dict(t=5, b=5, l=5, r=5))
    st.plotly_chart(fig_cat, use_container_width=True)

# 6. Strategic CEO Recommendations & Risk Analysis Box (Zero Scroll Layout)
st.markdown("### 💡 Executive Recommendations & Bottleneck Analysis")

rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown("""
        <div class="rec-box">
            <b>🚀 1. Scale High-Margin Partnerships</b><br>
            Allocate priority search placement and co-op marketing budgets to top-performing anchors like LG and Nike to maximize GMV expansion.
        </div>
    """, unsafe_allow_html=True)

with rec2:
    st.markdown("""
        <div class="rec-box">
            <b>⚠️ 2. Address Quality Bottlenecks</b><br>
            Mitigate customer churn by enforcing automated supplier reviews for product tiers dipping below a 3.8-star satisfaction threshold.
        </div>
    """, unsafe_allow_html=True)

with rec3:
    st.markdown("""
        <div class="rec-box">
            <b>📊 3. Refine Discount Architecture</b><br>
            Curb blanket discounting (>50%) on slow movers and pivot toward bundle cross-selling to safeguard net operational margins.
        </div>
    """, unsafe_allow_html=True)