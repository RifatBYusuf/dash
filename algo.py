import streamlit as st
import pandas as pd
from datetime import datetime
import time

# Load data
DATA_FILE = "data.csv"
try:
    df = pd.read_csv(DATA_FILE)
    if df.empty or df.dropna(how="all").empty:
        df = pd.DataFrame(columns=["Date", "Hours", "Income"])
except:
    df = pd.DataFrame(columns=["Date", "Hours", "Income"])

st.set_page_config(page_title="Income Tracker", page_icon="💸", layout="centered")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

st.title("💼 Income Tracker")
st.markdown("Keep track of your daily hours and earnings. Data updates weekly.")

with st.spinner("Loading interface..."):
    time.sleep(0.5)

# Input section
st.subheader("📅 Add New Entry")
input_date = st.date_input("Select Date")
hours = st.slider("Hours", 0, 24, 0)
minutes = st.slider("Minutes", 0, 59, 0)
income = st.text_input("Income", placeholder="Enter amount")

if st.button("💾 Save Entry"):
    try:
        total_hours = hours + minutes / 60
        new_row = {"Date": input_date.strftime("%Y-%m-%d"), "Hours": total_hours, "Income": float(income)}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("✅ Entry saved!")
    except Exception as e:
        st.error(f"❌ Error: {e}")

# Delete by date
st.subheader("🗑️ Delete Entries")
if st.button("Delete Entries for Selected Date"):
    df = df[df["Date"] != input_date.strftime("%Y-%m-%d")]
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ Entries deleted for selected date.")

# Weekly summary
st.subheader("📊 Weekly Summary")

if not df.empty and not df.dropna(how="all").empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["WeekOfMonth"] = df["Date"].apply(lambda x: min(((x.day - 1) // 7) + 1, 4))
    df["MonthWeek"] = df["Month"].astype(str) + "-" + df["WeekOfMonth"].astype(str)
    summary = df.groupby("MonthWeek")[["Hours", "Income"]].sum().reset_index()

    st.dataframe(summary.style.format({"Hours": "{:.2f}", "Income": "${:.2f}"}), use_container_width=True)

    selected = st.selectbox("Select Week to Delete", summary["MonthWeek"].unique())
    if st.button("🗑️ Delete Selected Week"):
        df = df[~((df["Month"].astype(str) + "-" + df["WeekOfMonth"].astype(str)) == selected)]
        df.drop(columns=["Month", "WeekOfMonth", "MonthWeek"], inplace=True, errors='ignore')
        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ Deleted entries for week {selected}")
else:
    st.info("ℹ️ No data to display.")
