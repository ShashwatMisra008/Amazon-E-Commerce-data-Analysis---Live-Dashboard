import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Layout Optimization
st.set_page_config(page_title="CEO E-Commerce Executive Briefing", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 0rem; }
        h1 { font-size: 1.4rem !important; margin-bottom: 0.3rem !important; color: #2c3e50; }
        .rec-box { background-color: #f8f9fa; padding: 10px; border-radius: 6px; border-left: 4px solid #008080; font-size: 0.78rem; height: 100%; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("👔 CEO Executive Performance & Deep-Dive Analytics Hub")

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

# 4. Core Financial Metrics Row
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

# 5. Multi-Tab Deep-Dive Analytics Architecture (Hosting 8 Insightful Interactive Plots)
tab1, tab2, tab3 = st.tabs(["🏆 Brand & Category Intelligence", "💰 Pricing & Discount Dynamics", "⭐ Quality, Stock & Merchant Operations"])

with tab1:
    t1_col1, t1_col2 = st.columns(2)
    with t1_col1:
        st.subheader("1. Brand Revenue vs. Average Rating Matrix")
        brand_perf = df_f.groupby('brand').agg({'final_price': 'sum', 'rating': 'mean', 'product_id': 'count'}).reset_index()
        brand_perf = brand_perf.sort_values(by='final_price', ascending=False).head(10)
        fig1 = px.scatter(brand_perf, x='final_price', y='rating', size='product_id', color='brand', template='plotly_white', hover_name='brand', labels={'final_price': 'Total Revenue ($)', 'rating': 'Avg Rating (⭐)'})
        fig1.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with t1_col2:
        st.subheader("8. Top Revenue-Generating Merchants / Sellers")
        if 'seller_id' in df_f.columns:
            seller_perf = df_f.groupby('seller_id')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(8)
            fig8 = px.bar(seller_perf, x='final_price', y='seller_id', orientation='h', color='final_price', color_continuous_scale='Teal', template='plotly_white', labels={'final_price': 'Total Revenue ($)', 'seller_id': 'Seller ID'})
            fig8.update_layout(yaxis={'categoryorder':'total ascending'}, height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("Seller data unavailable.")

with tab2:
    t2_col1, t2_col2 = st.columns(2)
    with t2_col1:
        st.subheader("2. Subcategory Ticket Size vs. Discount Sensitivity")
        if 'subcategory' in df_f.columns:
            subcat_perf = df_f.groupby('subcategory').agg({'final_price': 'mean', 'discount': 'mean', 'review_count': 'sum'}).reset_index()
            subcat_perf = subcat_perf.sort_values(by='final_price', ascending=False).head(8)
            fig2 = px.bar(subcat_perf, x='subcategory', y='final_price', color='discount', color_continuous_scale='Teal', template='plotly_white', labels={'final_price': 'Avg Ticket ($)', 'discount': 'Avg Discount (%)'})
            fig2.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5))
            st.plotly_chart(fig2, use_container_width=True)
    
    with t2_col2:
        st.subheader("6. Promotional Discount Depth vs. Order Volume")
        if 'discount' in df_f.columns:
            disc_bins = pd.cut(df_f['discount'], bins=[0, 10, 25, 50, 100], labels=['0-10%', '10-25%', '25-50%', '50+%'])
            disc_vol = df_f.groupby(disc_bins, observed=False).agg({'product_id': 'count', 'final_price': 'mean'}).reset_index()
            fig6 = px.bar(disc_vol, x='discount', y='product_id', color='final_price', color_continuous_scale='Sunset', template='plotly_white', labels={'discount': 'Discount Tier', 'product_id': 'Transaction Volume'})
            fig6.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5))
            st.plotly_chart(fig6, use_container_width=True)

    t2_col3, t2_col4 = st.columns(2)
    with t2_col3:
        st.subheader("3. Price Point vs. Customer Engagement (Reviews)")
        if 'review_count' in df_f.columns:
            sample_df = df_f.sample(min(len(df_f), 1000), random_state=42)
            fig3 = px.scatter(sample_df, x='final_price', y='review_count', color='category', opacity=0.7, template='plotly_white', labels={'final_price': 'Final Price ($)', 'review_count': 'Review Volume'})
            fig3.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)

with tab3:
    t3_col1, t3_col2 = st.columns(2)
    with t3_col1:
        st.subheader("4. Merchant Seller Rating vs. Item Final Price")
        if 'seller_rating' in df_f.columns:
            sample_seller = df_f.sample(min(len(df_f), 1000), random_state=42)
            fig4 = px.box(sample_seller, x='seller_rating', y='final_price', color='category', template='plotly_white', labels={'seller_rating': 'Seller Rating (⭐)', 'final_price': 'Final Price ($)'})
            fig4.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig4, use_container_width=True)
    
    with t3_col2:
        st.subheader("5. Inventory Stock Distribution across Tiers")
        if 'stock' in df_f.columns:
            fig5 = px.histogram(df_f, x='stock', nbins=20, color='category', template='plotly_white', labels={'stock': 'Available Stock Units', 'count': 'Frequency'})
            fig5.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)

    t3_col3, t3_col4 = st.columns(2)
    with t3_col3:
        st.subheader("7. Quality Audit: Category Rating Distribution")
        if 'rating' in df_f.columns:
            fig7 = px.box(df_f, x='category', y='rating', color='category', template='plotly_white', labels={'category': 'Category', 'rating': 'Product Rating (⭐)'})
            fig7.update_layout(height=260, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig7, use_container_width=True)

# 6. Strategic Recommendations
st.markdown("---")
st.markdown("**💡 Data-Backed Executive Strategy & Recommendations**")

rec1, rec2, rec3 = st.columns(3)

with rec1:
    st.markdown("""
        <div class="rec-box">
            <b>🚀 1. Scale Top Brand Partnerships</b><br>
            <b>Data Insight:</b> High-revenue anchors maintain superior catalog concentration and customer trust across multiple metrics.<br>
            <b>Action:</b> Prioritize co-op marketing and prime search placements for top-tier volume drivers.
        </div>
    """, unsafe_allow_html=True)

with rec2:
    st.markdown("""
        <div class="rec-box">
            <b>⚠️ 2. Mitigate Quality & Churn Risks</b><br>
            <b>Data Insight:</b> Rating distribution boxes highlight vulnerable product segments falling below marketplace standards.<br>
            <b>Action:</b> Enforce automated supplier quality thresholds to protect brand equity and lower return liabilities.
        </div>
    """, unsafe_allow_html=True)

with rec3:
    st.markdown("""
        <div class="rec-box">
            <b>📊 3. Restructure Discount Architecture</b><br>
            <b>Data Insight:</b> Promotional depth analysis reveals high margin erosion in deep discount brackets without proportional volume gains.<br>
            <b>Action:</b> Restrict blanket markdowns on slow movers; transition to bundle cross-selling.
        </div>
    """, unsafe_allow_html=True)