import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration (Wide Mode to prevent scrolling)
st.set_page_config(page_title="Amazon Executive Analytics Hub", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for compact card layout
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 0rem; padding-left: 1rem; padding-right: 1rem; }
        h1 { font-size: 1.5rem !important; margin-bottom: 0rem !important; }
        h3 { font-size: 1.1rem !important; margin-top: 0rem !important; margin-bottom: 0.2rem !important; }
        .metric-card { background: #f8f9fa; padding: 8px; border-radius: 6px; border: 1px solid #e9ecef; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv('cleaned_amazon_ecommerce.csv')

df = load_data()

# 3. Comprehensive Sidebar Filters & Slicers (Multi-Filter Architecture)
st.sidebar.header("🎛️ Dashboard Slicers & Filters")

# Filter 1: Category
categories = sorted(df['category'].dropna().unique())
sel_cat = st.sidebar.selectbox("Category", ["All"] + categories)
df_f = df[df['category'] == sel_cat] if sel_cat != "All" else df

# Filter 2: Subcategory
subcats = sorted(df_f['subcategory'].dropna().unique())
sel_subcat = st.sidebar.selectbox("Subcategory", ["All"] + subcats)
if sel_subcat != "All": df_f = df_f[df_f['subcategory'] == sel_subcat]

# Filter 3: Brand
brands = sorted(df_f['brand'].dropna().unique())
sel_brand = st.sidebar.selectbox("Brand", ["All"] + brands)
if sel_brand != "All": df_f = df_f[df_f['brand'] == sel_brand]

# Advanced Slicers inside Expander
with st.sidebar.expander("Advanced Numerical Slicers"):
    # Filter 4: Price Range Slider
    min_p, max_p = float(df['final_price'].min()), float(df['final_price'].max())
    price_range = st.slider("Final Price Range ($)", min_p, max_p, (min_p, max_p))
    df_f = df_f[(df_f['final_price'] >= price_range[0]) & (df_f['final_price'] <= price_range[1])]
    
    # Filter 5: Rating Slicer
    min_r, max_r = float(df['rating'].min()), float(df['rating'].max()) if 'rating' in df.columns else (0.0, 5.0)
    rating_range = st.slider("Rating Slicer", min_r, max_r, (min_r, max_r))
    if 'rating' in df.columns:
        df_f = df_f[(df_f['rating'] >= rating_range[0]) & (df_f['rating'] <= rating_range[1])]

# 4. Header Title
st.markdown("### 🛒 Amazon Executive Performance Hub")

# 5. Computing Over 20 Insights & KPIs
total_gmv = df_f['final_price'].sum()
total_orders = len(df_f)
avg_price = df_f['final_price'].mean() if total_orders > 0 else 0
median_price = df_f['final_price'].median() if total_orders > 0 else 0
max_price = df_f['final_price'].max() if total_orders > 0 else 0
min_price = df_f['final_price'].min() if total_orders > 0 else 0

avg_rating = df_f['rating'].mean() if 'rating' in df_f.columns and total_orders > 0 else 0
total_reviews = df_f['review_count'].sum() if 'review_count' in df_f.columns else 0
avg_discount = df_f['discount'].mean() if 'discount' in df_f.columns and total_orders > 0 else 0
total_stock = df_f['stock'].sum() if 'stock' in df_f.columns else 0
avg_seller_rating = df_f['seller_rating'].mean() if 'seller_rating' in df_f.columns and total_orders > 0 else 0

unique_categories = df_f['category'].nunique()
unique_subcats = df_f['subcategory'].nunique() if 'subcategory' in df_f.columns else 0
unique_brands = df_f['brand'].nunique() if 'brand' in df_f.columns else 0
unique_sellers = df_f['seller_id'].nunique() if 'seller_id' in df_f.columns else 0
unique_users = df_f['user_id'].nunique() if 'user_id' in df_f.columns else 0

top_brand_name = df_f['brand'].mode()[0] if not df_f.empty else "N/A"
top_cat_name = df_f['category'].mode()[0] if not df_f.empty else "N/A"
max_discount = df_f['discount'].max() if 'discount' in df_f.columns and not df_f.empty else 0
avg_stock_per_item = df_f['stock'].mean() if 'stock' in df_f.columns and total_orders > 0 else 0

# Format GMV cleanly
gmv_str = f"${total_gmv/1e9:,.2f}B" if total_gmv >= 1e9 else f"${total_gmv/1e6:,.2f}M"

# 6. Ultra-Compact 5-Column Metrics Grid (Displaying 20+ Insights Instantly without scrolling)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("1. Total GMV", gmv_str)
c2.metric("2. Transactions", f"{total_orders:,}")
c3.metric("3. Avg Price", f"${avg_price:,.1f}")
c4.metric("4. Median Price", f"${median_price:,.1f}")
c5.metric("5. Avg Rating", f"{avg_rating:.2f} ⭐")

c6, c7, c8, c9, c10 = st.columns(5)
c6.metric("6. Max Price", f"${max_price:,.1f}")
c7.metric("7. Min Price", f"${min_price:,.1f}")
c8.metric("8. Total Reviews", f"{total_reviews:,}")
c9.metric("9. Avg Discount", f"{avg_discount:.1f}%")
c10.metric("10. Total Stock", f"{total_stock:,}")

c11, c12, c13, c14, c15 = st.columns(5)
c11.metric("11. Seller Rating", f"{avg_seller_rating:.2f}")
c12.metric("12. Categories", f"{unique_categories}")
c13.metric("13. Subcategories", f"{unique_subcats}")
c14.metric("14. Unique Brands", f"{unique_brands}")
c15.metric("15. Active Sellers", f"{unique_sellers}")

c16, c17, c18, c19, c20 = st.columns(5)
c16.metric("16. Active Users", f"{unique_users}")
c17.metric("17. Top Brand", str(top_brand_name)[:12])
c18.metric("18. Top Category", str(top_cat_name)[:12])
c19.metric("19. Max Discount", f"{max_discount:.1f}%")
c20.metric("20. Avg Stock/Item", f"{avg_stock_per_item:.1f}")

# 7. Side-by-Side Professional Visualizations (Zero Scroll Footprint)
st.markdown("---")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    top_brands_df = df_f.groupby('brand')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(5)
    fig1 = px.bar(top_brands_df, x='final_price', y='brand', orientation='h', color='final_price', color_continuous_scale='Teal', template='plotly_white')
    fig1.update_layout(title="Top 5 Brands by Revenue", height=220, margin=dict(t=30, b=0, l=0, r=0), showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    top_cats_df = df_f.groupby('category')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(5)
    fig2 = px.pie(top_cats_df, names='category', values='final_price', hole=0.4, template='plotly_white', color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(title="Top Categories Share", height=220, margin=dict(t=30, b=0, l=0, r=0))
    st.plotly_chart(fig2, use_container_width=True)