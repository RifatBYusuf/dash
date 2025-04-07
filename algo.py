import streamlit as st
import pandas as pd
from datetime import datetime

# Load data
DATA_FILE = "data.csv"
try:
    df = pd.read_csv(DATA_FILE)
    if df.empty or df.dropna(how="all").empty:
        df = pd.DataFrame(columns=["Date", "Hours", "Income"])
except:
    df = pd.DataFrame(columns=["Date", "Hours", "Income"])

st.title("Income Tracker")

# Input section
st.subheader("Add New Entry")
input_date = st.date_input("Select Date")
hours = st.selectbox("Hours", list(range(0, 25)))
minutes = st.selectbox("Minutes", list(range(0, 60)))
income = st.text_input("Income")

if st.button("Save Entry"):
    try:
        total_hours = hours + minutes / 60
        new_row = {"Date": input_date.strftime("%Y-%m-%d"), "Hours": total_hours, "Income": float(income)}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Entry saved!")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Delete Entries for Selected Date"):
    df = df[df["Date"] != input_date.strftime("%Y-%m-%d")]
    df.to_csv(DATA_FILE, index=False)
    st.success("Entries deleted for selected date.")

# Weekly summary
st.subheader("Weekly Summary")

if not df.empty and not df.dropna(how="all").empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df["Month"] = df["Date"].dt.month
    df["WeekOfMonth"] = df["Date"].apply(lambda x: min(((x.day - 1) // 7) + 1, 4))
    df["MonthWeek"] = df["Month"].astype(str) + "-" + df["WeekOfMonth"].astype(str)
    summary = df.groupby("MonthWeek")[["Hours", "Income"]].sum().reset_index()

    selected = st.selectbox("Select Week to Delete", summary["MonthWeek"].unique())
    if st.button("Delete Selected Week"):
        df = df[~((df["Month"].astype(str) + "-" + df["WeekOfMonth"].astype(str)) == selected)]
        df.drop(columns=["Month", "WeekOfMonth", "MonthWeek"], inplace=True, errors='ignore')
        df.to_csv(DATA_FILE, index=False)
        st.success(f"Deleted entries for week {selected}")

    st.dataframe(summary)
else:
    st.info("No data to display.")
