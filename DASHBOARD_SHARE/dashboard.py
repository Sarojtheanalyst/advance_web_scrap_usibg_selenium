import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NEPSE Live Dashboard",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# DATA LOADING
# ==========================================

@st.cache_data(ttl=30)
def load_data():

    url = "https://api.nepalytix.com/api/live-market/floorsheet/"

    response = requests.get(url)

    data = response.json()

    return data

data = load_data()

summary = data["summary"]

amount_df = pd.DataFrame(
    data["top_5_by_amount"]
)

qty_df = pd.DataFrame(
    data["top_5_by_quantity"]
)

bulk_df = pd.DataFrame(
    data["bulk_transactions"]["data"]
)

amount_df["amount_cr"] = (
    amount_df["amount"] / 10000000
)

# ==========================================
# HEADER
# ==========================================

st.title("📈 NEPSE Live Floorsheet Dashboard")

st.markdown("---")

# ==========================================
# KPI CARDS
# ==========================================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Transactions",
    f"{summary['total_transactions']:,}"
)

c2.metric(
    "Quantity",
    f"{summary['total_quantity']:,}"
)

c3.metric(
    "Amount (Cr)",
    f"{summary['total_amount']/10000000:.2f}"
)

c4.metric(
    "Average Deal",
    f"{summary['avg_deal_size']:,.0f}"
)

c5.metric(
    "Largest Deal (Cr)",
    f"{data['largest_transaction']['amount']/10000000:.2f}"
)

st.markdown("---")

# ==========================================
# CHARTS
# ==========================================

col1, col2 = st.columns(2)

# ------------------------------------------
# TREEMAP
# ------------------------------------------

with col1:

    fig1 = px.treemap(
        amount_df,
        path=["symbol"],
        values="amount_cr",
        title="Top 5 Stocks by Amount (Cr)"
    )

    fig1.update_layout(
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

# ------------------------------------------
# QUANTITY BAR
# ------------------------------------------

with col2:

    fig2 = px.bar(
        qty_df,
        x="quantity",
        y="symbol",
        orientation="h",
        text="quantity",
        title="Top 5 Stocks by Quantity"
    )

    fig2.update_layout(
        height=500,
        yaxis_title="Symbol",
        xaxis_title="Quantity"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ==========================================
# BULK TRANSACTIONS
# ==========================================

st.markdown("---")

st.subheader("📊 Bulk Transactions")

st.dataframe(
    bulk_df,
    use_container_width=True,
    height=400
)

# ==========================================
# TOP AMOUNT TABLE
# ==========================================

st.markdown("---")

left,right = st.columns(2)

with left:

    st.subheader("💰 Top Stocks by Amount")

    st.dataframe(
        amount_df,
        use_container_width=True
    )

with right:

    st.subheader("📦 Top Stocks by Quantity")

    st.dataframe(
        qty_df,
        use_container_width=True
    )

# ==========================================
# AUTO REFRESH INFO
# ==========================================

st.markdown("---")

st.info(
    "Dashboard refreshes every 30 seconds (cache enabled)."
)