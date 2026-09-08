import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Amazon E-Commerce Analytics Hub", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        .insight-box { background-color: #f1f3f5; padding: 15px; border-radius: 8px; border-left: 5px solid #008080; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛒 Amazon E-Commerce Insights Dashboard")
st.markdown("Actionable business intelligence and visual performance analytics.")

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_amazon_ecommerce.csv')

df = load_data()

# 3. Sidebar Slicers & Filters
st.sidebar.header("🎛️ Dashboard Slicers")

categories = sorted(df['category'].dropna().unique())
sel_cat = st.sidebar.selectbox("Category Filter", ["All"] + categories)
df_f = df[df['category'] == sel_cat] if sel_cat != "All" else df

subcats = sorted(df_f['subcategory'].dropna().unique())
sel_subcat = st.sidebar.selectbox("Subcategory Filter", ["All"] + subcats)
if sel_subcat != "All": df_f = df_f[df_f['subcategory'] == sel_subcat]

brands = sorted(df_f['brand'].dropna().unique())
sel_brand = st.sidebar.selectbox("Brand Filter", ["All"] + brands)
if sel_brand != "All": df_f = df_f[df_f['brand'] == sel_brand]

# 4. Clean Core Metrics (Only Top 4 Display Numbers)
total_gmv = df_f['final_price'].sum()
total_orders = len(df_f)
avg_price = df_f['final_price'].mean() if total_orders > 0 else 0
avg_rating = df_f['rating'].mean() if 'rating' in df_f.columns and total_orders > 0 else 0

gmv_str = f"${total_gmv/1e9:,.2f}B" if total_gmv >= 1e9 else f"${total_gmv/1e6:,.2f}M"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue (GMV)", gmv_str)
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Average Final Price", f"${avg_price:,.2f}")
col4.metric("Average Rating", f"{avg_rating:.2f} ⭐")

st.markdown("---")

# 5. Visual Insights Layout (Charts & Key Takeaways)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("🏆 Top Revenue Generating Brands")
    top_brands = df_f.groupby('brand')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(8)
    fig_brand = px.bar(top_brands, x='final_price', y='brand', orientation='h', color='final_price', color_continuous_scale='Teal', template='plotly_white')
    fig_brand.update_layout(yaxis={'categoryorder':'total ascending'}, margin=dict(t=10, b=10, l=10, r=10), showlegend=False)
    st.plotly_chart(fig_brand, use_container_width=True)

with chart_col2:
    st.subheader("📦 Revenue Distribution by Category")
    top_cats = df_f.groupby('category')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False)
    fig_cat = px.pie(top_cats, names='category', values='final_price', hole=0.5, template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_cat.update_layout(margin=dict(t=10, b=10, l=10, r=10))
    st.plotly_chart(fig_cat, use_container_width=True)

# 6. Analytical Insights Summary Section
st.markdown("---")
st.subheader("💡 Key Analytical Insights")

# Dynamically compute text insights
top_brand = top_brands.iloc[0]['brand'] if not top_brands.empty else "N/A"
top_cat = top_cats.iloc[0]['category'] if not top_cats.empty else "N/A"
max_rev = top_brands.iloc[0]['final_price'] if not top_brands.empty else 0

ins_col1, ins_col2, ins_col3 = st.columns(3)

with ins_col1:
    st.markdown(f"""
        <div class="insight-box">
            <b>🔥 Dominant Brand:</b><br>
            <b>{top_brand}</b> leads total sales performance, capturing the highest revenue share in the selected filter view.
        </div>
    """, unsafe_allow_html=True)

with ins_col2:
    st.markdown(f"""
        <div class="insight-box">
            <b>📈 Core Category:</b><br>
            <b>{top_cat}</b> is the primary revenue driver, accounting for the largest share of overall marketplace GMV.
        </div>
    """, unsafe_allow_html=True)

with ins_col3:
    st.markdown(f"""
        <div class="insight-box">
            <b>⭐ Quality & Pricing:</b><br>
            Products maintain an average rating of <b>{avg_rating:.2f} stars</b> with a median transaction ticket size of <b>${avg_price:,.2f}</b>.
        </div>
    """, unsafe_allow_html=True)