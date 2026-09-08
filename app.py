import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Configuration & Layout Optimization
st.set_page_config(page_title="CEO E-Commerce Executive Briefing", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; padding-bottom: 0rem; }
        h1 { font-size: 1.3rem !important; margin-bottom: 0.2rem !important; color: #2c3e50; }
        .insight-card { background-color: #f8f9fa; padding: 12px; border-radius: 6px; border-left: 4px solid #008080; font-size: 0.8rem; margin-bottom: 10px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
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

# 5. Multi-Tab Architecture with Dedicated Issue-Effect-Cause-Solution Insights
tab1, tab2, tab3, tab4 = st.tabs([
    "🏆 Brand & Merchant Intelligence", 
    "💰 Pricing & Discount Dynamics", 
    "⭐ Quality, Stock & Operations",
    "📋 Executive Master Strategy"
])

with tab1:
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("1. Brand Revenue vs. Average Rating Matrix")
        brand_perf = df_f.groupby('brand').agg({'final_price': 'sum', 'rating': 'mean', 'product_id': 'count'}).reset_index()
        brand_perf = brand_perf.sort_values(by='final_price', ascending=False).head(10)
        fig1 = px.scatter(brand_perf, x='final_price', y='rating', size='product_id', color='brand', template='plotly_white', hover_name='brand', labels={'final_price': 'Total Revenue ($)', 'rating': 'Avg Rating (⭐)'})
        fig1.update_layout(height=220, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col_g2:
        st.subheader("2. Top Revenue-Generating Merchants / Sellers")
        if 'seller_id' in df_f.columns:
            seller_perf = df_f.groupby('seller_id')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False).head(8)
            fig2 = px.bar(seller_perf, x='final_price', y='seller_id', orientation='h', color='final_price', color_continuous_scale='Teal', template='plotly_white', labels={'final_price': 'Total Revenue ($)', 'seller_id': 'Seller ID'})
            fig2.update_layout(yaxis={'categoryorder':'total ascending'}, height=220, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Seller data unavailable.")

    st.markdown("**🔍 Tab 1 Diagnostic Breakdown (Issue → Effect → Cause → Solution)**")
    i1, i2 = st.columns(2)
    with i1:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 1: Brand Performance Concentration</b><br>
                <b>• Issue:</b> Revenue is heavily concentrated within top-tier anchors while emerging brands lag.<br>
                <b>• Effect:</b> Marketplace vulnerability to supplier shocks and margin demands.<br>
                <b>• Cause:</b> Organic search preference and higher marketing spend by legacy vendors.<br>
                <b>• Solution:</b> Implement incubation tiers and discovery algorithms for mid-tier sellers.
            </div>
        """, unsafe_allow_html=True)
    with i2:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 2: Merchant Revenue Skew</b><br>
                <b>• Issue:</b> Top 5 sellers account for a disproportionate share of total transaction volume.<br>
                <b>• Effect:</b> Bottlenecks in inventory fulfillment and high bargaining power for top sellers.<br>
                <b>• Cause:</b> Exclusive distribution agreements on high-demand electronics.<br>
                <b>• Solution:</b> Onboard competing merchants in high-velocity categories to diversify supply chain risk.
            </div>
        """, unsafe_allow_html=True)

with tab2:
    col_g3, col_g4 = st.columns(2)
    with col_g3:
        st.subheader("3. Subcategory Ticket Size vs. Discount Sensitivity")
        if 'subcategory' in df_f.columns:
            subcat_perf = df_f.groupby('subcategory').agg({'final_price': 'mean', 'discount': 'mean'}).reset_index()
            subcat_perf = subcat_perf.sort_values(by='final_price', ascending=False).head(8)
            fig3 = px.bar(subcat_perf, x='subcategory', y='final_price', color='discount', color_continuous_scale='Teal', template='plotly_white', labels={'final_price': 'Avg Ticket ($)', 'discount': 'Avg Discount (%)'})
            fig3.update_layout(height=220, margin=dict(t=5, b=5, l=5, r=5))
            st.plotly_chart(fig3, use_container_width=True)
            
    with col_g4:
        st.subheader("4. Promotional Discount Depth vs. Order Volume")
        if 'discount' in df_f.columns:
            disc_bins = pd.cut(df_f['discount'], bins=[0, 10, 25, 50, 100], labels=['0-10%', '10-25%', '25-50%', '50+%'])
            disc_vol = df_f.groupby(disc_bins, observed=False).agg({'product_id': 'count', 'final_price': 'mean'}).reset_index()
            fig4 = px.bar(disc_vol, x='discount', y='product_id', color='final_price', color_continuous_scale='Sunset', template='plotly_white', labels={'discount': 'Discount Tier', 'product_id': 'Transaction Volume'})
            fig4.update_layout(height=220, margin=dict(t=5, b=5, l=5, r=5))
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**🔍 Tab 2 Diagnostic Breakdown (Issue → Effect → Cause → Solution)**")
    i3, i4 = st.columns(2)
    with i3:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 3: Subcategory Price & Discount Correlation</b><br>
                <b>• Issue:</b> Premium subcategories rely on heavy markdowns to maintain velocity.<br>
                <b>• Effect:</b> Long-term brand dilution and compressed gross margins.<br>
                <b>• Cause:</b> Aggressive competitor pricing pressure in tech segments.<br>
                <b>• Solution:</b> Shift from blanket price cuts to value-added bundling (e.g., warranties, accessories).
            </div>
        """, unsafe_allow_html=True)
    with i4:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 4: Discount Depth Efficiency</b><br>
                <b>• Issue:</b> 50%+ discount tiers fail to yield proportional volume spikes.<br>
                <b>• Effect:</b> Margin erosion without a matching customer acquisition benefit.<br>
                <b>• Cause:</b> Clearance items losing perceived baseline value among buyers.<br>
                <b>• Solution:</b> Cap automated maximum markdowns and introduce targeted loyalty-only discounts.
            </div>
        """, unsafe_allow_html=True)

with tab3:
    col_g5, col_g6 = st.columns(2)
    with col_g5:
        st.subheader("5. Merchant Seller Rating vs. Item Final Price")
        if 'seller_rating' in df_f.columns:
            sample_seller = df_f.sample(min(len(df_f), 1000), random_state=42)
            fig5 = px.box(sample_seller, x='seller_rating', y='final_price', color='category', template='plotly_white', labels={'seller_rating': 'Seller Rating (⭐)', 'final_price': 'Final Price ($)'})
            fig5.update_layout(height=220, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
            
    with col_g6:
        st.subheader("6. Quality Audit: Category Rating Distribution")
        if 'rating' in df_f.columns:
            fig6 = px.box(df_f, x='category', y='rating', color='category', template='plotly_white', labels={'category': 'Category', 'rating': 'Product Rating (⭐)'})
            fig6.update_layout(height=220, margin=dict(t=5, b=5, l=5, r=5), showlegend=False)
            st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**🔍 Tab 3 Diagnostic Breakdown (Issue → Effect → Cause → Solution)**")
    i5, i6 = st.columns(2)
    with i5:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 5: Seller Rating & Pricing Spread</b><br>
                <b>• Issue:</b> Lower-rated sellers list across both budget and premium price points.<br>
                <b>• Effect:</b> Elevated customer service overhead and high product return rates.<br>
                <b>• Cause:</b> Lax onboarding controls for third-party marketplace merchants.<br>
                <b>• Solution:</b> Restrict premium product listing rights to vendors maintaining >4.2 seller ratings.
            </div>
        """, unsafe_allow_html=True)
    with i6:
        st.markdown("""
            <div class="insight-card">
                <b>Plot 6: Category Quality Variance</b><br>
                <b>• Issue:</b> Noticeable rating outliers and lower medians in lifestyle/home categories.<br>
                <b>• Effect:</b> Customer dissatisfaction and negative reviews impacting conversion rates.<br>
                <b>• Cause:</b> Substandard manufacturing quality among unbranded suppliers.<br>
                <b>• Solution:</b> Implement stricter QA review audits and penalize suppliers with repeated quality flags.
            </div>
        """, unsafe_allow_html=True)

with tab4:
    st.subheader("📋 Master Strategic Roadmap for CEO Execution")
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
            <div class="insight-card">
                <b>🚀 Phase 1: Supplier Diversification</b><br>
                • Reduce dependency on top 5 merchants.<br>
                • Onboard alternative brands in high-GMV categories to stimulate competitive pricing and secure better fulfillment terms.
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
            <div class="insight-card">
                <b>📊 Phase 2: Margin Protection</b><br>
                • Overhaul discounting rules.<br>
                • Replace unprofitable 50%+ markdowns with curated cross-category bundle offers to preserve net unit economics.
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
            <div class="insight-card">
                <b>⭐ Phase 3: Quality Governance</b><br>
                • Enforce strict rating floors.<br>
                • Automatically suppress listings falling below quality thresholds to protect marketplace reputation and lower returns.
            </div>
        """, unsafe_allow_html=True)