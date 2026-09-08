import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Layout Optimization
st.set_page_config(page_title="CEO E-Commerce Executive Briefing", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2.5rem; padding-bottom: 0rem; }
        h1 { font-size: 1.4rem !important; margin-bottom: 0.3rem !important; color: #2c3e50; }
        .rec-box { background-color: #f8f9fa; padding: 10px; border-radius: 6px; border-left: 4px solid #008080; font-size: 0.78rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("👔 CEO Executive Performance & Strategy Dashboard")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_amazon_ecommerce.csv')

df = load_data()

# 3. Sidebar Slicers
st.sidebar.header("🎛️ Executive Slicers")
categories = sorted(df['category'].dropna().unique())
sel_cat = st.sidebar.selectbox("Category View", ["All"] + categories)
df_f = df[df['category'] == sel_cat] if sel_cat != "All" else df

brands = sorted(df_f['brand'].dropna().unique())
sel_brand = st.sidebar.selectbox("Brand View", ["All"] + brands)
if sel_brand != "All": df_f = df_f[df_f['brand'] == sel_brand]

# 4. Core Financial Metrics
total_gmv = df_f['final_price'].sum()
total_orders = len(df_f)
avg_price = df_f['final_price'].mean() if total_orders > 0 else 0
avg_rating = df_f['rating'].mean() if 'rating' in df_f.columns and total_orders > 0 else 0
avg_disc = df_f['discount'].mean() if 'discount' in df_f.columns and total_orders > 0 else 0

gmv_str = f"${total_gmv/1e9:,.2f}B" if total_gmv >= 1e9 else f"${total_gmv/1e6:,.2f}M"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (GMV)", gmv_str)
col2.metric("Total Transactions", f"{total_orders:,}")
col3.metric("Average Ticket Size", f"${avg_price:,.2f}")
col4.metric("Marketplace Rating", f"{avg_rating:.2f} ⭐")

st.markdown("---")

# 5. Advanced Interactive Visualizations with Deep Insights
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Brand Revenue vs. Average Rating Matrix")
    # Group by brand to show revenue and quality relationship
    brand_perf = df_f.groupby('brand').agg({'final_price': 'sum', 'rating': 'mean', 'product_id': 'count'}).reset_index()
    brand_perf = brand_perf.sort_values(by='final_price', ascending=False).head(10)
    
    fig_scatter = px.scatter(
        brand_perf, x='final_price', y='rating', size='product_id', color='brand',
        template='plotly_white', hover_name='brand',
        labels={'final_price': 'Total Revenue ($)', 'rating': 'Avg Rating (⭐)', 'product_id': 'Catalog Size'}
    )
    fig_scatter.update_layout(height=190, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
    st.plotly_chart(fig_scatter, use_container_width=True)

with chart_col2:
    st.subheader("📦 Subcategory Margin & Discount Sensitivity")
    # Group by subcategory to show price vs discount correlation
    if 'subcategory' in df_f.columns:
        subcat_perf = df_f.groupby('subcategory').agg({'final_price': 'mean', 'discount': 'mean', 'review_count': 'sum'}).reset_index()
        subcat_perf = subcat_perf.sort_values(by='final_price', ascending=False).head(8)
        
        fig_bubble = px.bar(
            subcat_perf, x='subcategory', y='final_price', color='discount',
            color_continuous_scale='Teal', template='plotly_white',
            labels={'final_price': 'Avg Ticket ($)', 'discount': 'Avg Discount (%)', 'subcategory': 'Subcategory'}
        )
        fig_bubble.update_layout(height=190, margin=dict(t=5, b=5, l=5, r=5))
        st.plotly_chart(fig_bubble, use_container_width=True)
    else:
        st.info("Subcategory details unavailable.")

# 6. Strategic Recommendations Backed by Granular Data
st.markdown("**💡 Data-Backed Executive Recommendations & Insights**")

rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown(f"""
        <div class="rec-box">
            <b>🚀 1. Scale Top Brand Partnerships</b><br>
            <b>Data Insight:</b> High-revenue brands maintain superior catalog concentration and customer trust.<br>
            <b>Action:</b> Prioritize co-op marketing and prime search placements for top-tier volume drivers.
        </div>
    """, unsafe_allow_html=True)

with rec2:
    st.markdown(f"""
        <div class="rec-box">
            <b>⚠️ 2. Mitigate Quality & Churn Risks</b><br>
            <b>Data Insight:</b> Marketplace health averages <b>{avg_rating:.2f} ⭐</b>, highlighting segments vulnerable to drop-offs.<br>
            <b>Action:</b> Enforce automated supplier quality thresholds to protect brand equity and lower return liabilities.
        </div>
    """, unsafe_allow_html=True)

with rec3:
    st.markdown(f"""
        <div class="rec-box">
            <b>📊 3. Restructure Discount Architecture</b><br>
            <b>Data Insight:</b> Catalog discounting averages <b>{avg_disc:.1f}%</b>, impacting unit margin realization.<br>
            <b>Action:</b> Restrict blanket markdowns on slow movers; transition to bundle cross-selling to safeguard operating margins.
        </div>
    """, unsafe_allow_html=True)