import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Amazon E-Commerce Live Dashboard", layout="wide")
st.title("🛒 Amazon E-Commerce Performance Dashboard")

@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_amazon_ecommerce.csv')
    return df

df = load_data()

# Metrics
total_rev = df['final_price'].sum()
total_orders = len(df)
avg_price = df['final_price'].mean()

col1, col2, col3 = st.cols(3)
col1.metric("Total GMV", f"${total_rev:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Avg Final Price", f"${avg_price:,.2f}")

st.markdown("---")
st.subheader("Top Categories by Revenue")
top_cats = df.groupby('category')['final_price'].sum().reset_index().sort_values(by='final_price', ascending=False)
fig = px.bar(top_cats, x='category', y='final_price', color='final_price', template='plotly_white')
st.plotly_chart(fig, use_container_width=True)