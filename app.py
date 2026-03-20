import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ---------------- FILE ----------------
MEMBERS_FILE = "members.csv"

# ---------------- DATABASE ----------------
conn = sqlite3.connect("chorale.db", check_same_thread=False)
c = conn.cursor()

# Tables
c.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    Name TEXT,
    Day TEXT,
    Status TEXT,
    Date TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS contribution (
    Name TEXT,
    Contribution TEXT,
    Month TEXT,
    Amount REAL,
    Date TEXT
)
""")

conn.commit()

# ---------------- LOAD MEMBERS ----------------
def load_members():
    if os.path.exists(MEMBERS_FILE):
        df = pd.read_csv(MEMBERS_FILE)
        return df
    else:
        return pd.DataFrame()

def load_table(table):
    return pd.read_sql(f"SELECT * FROM {table}", conn)

def insert_attendance(data):
    c.executemany("INSERT INTO attendance VALUES (?,?,?,?)", data)
    conn.commit()

def insert_contribution(data):
    c.execute("INSERT INTO contribution VALUES (?,?,?,?,?)", data)
    conn.commit()

# ---------------- TABS ----------------
tabs = st.tabs([
    "Ahabanza",
    "Abaririmbyi",
    "Attendance",
    "Umusanzu",
    "Raporo Attendance",
    "Raporo Umusanzu",
    "Abataremerewe"
])

# ---------------- HOME ----------------
with tabs[0]:
    st.header("Murakaza neza")
    st.write("• Imyitozo: Kuwa Gatatu & Gatandatu")
    st.write("• Amateraniro: Ku Cyumweru")

# ---------------- MEMBERS ----------------
with tabs[1]:
    st.header("👥 Abaririmbyi")

    members = load_members()

    if members.empty:
        st.error("members.csv ntiboneka cyangwa irimo ubusa")
    else:
        st.dataframe(members)
        st.info(f"Abari muri chorale: {len(members)}")

# ---------------- ATTENDANCE ----------------
with tabs[2]:
    st.header("📋 Attendance")

    members = load_members()

    if members.empty:
        st.warning("Nta members ihari")
    else:
        day = st.selectbox("Umunsi", ["Wednesday","Saturday","Sunday"])
        selected_date = st.date_input("Itariki", value=date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

        attendance_data = []
        present = absent = uruhushya = 0

        for i, row in members.iterrows():
            name = row["Name"]

            col1, col2 = st.columns([3,3])
            with col1:
                st.write(name)

            with col2:
                status = st.radio(
                    f"Status {name}",
                    ["Present","Absent","Uruhushya"],
                    key=f"{name}_{i}",
                    horizontal=True
                )

            if status == "Present": present += 1
            elif status == "Absent": absent += 1
            else: uruhushya += 1

            attendance_data.append((name, day, status, date_str))

        st.write(f"✅ Present: {present} | ❌ Absent: {absent} | 📄 Uruhushya: {uruhushya}")

        if st.button("💾 Save Attendance"):
            insert_attendance(attendance_data)
            st.success("Attendance yabitswe neza!")

# ---------------- UMUSANZU ----------------
with tabs[3]:
    st.header("💰 Umusanzu")

    members = load_members()

    if not members.empty:
        name = st.selectbox("Izina", members["Name"])
    else:
        name = st.text_input("Izina")

    contribution = st.text_input("Ubwoko bw'umusanzu")
    month = st.selectbox("Ukwezi", [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ])
    amount = st.number_input("Amafaranga", min_value=0)

    if st.button("💾 Save Umusanzu"):
        insert_contribution((name, contribution, month, amount, str(datetime.now())))
        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
with tabs[4]:
    st.header("📊 Raporo Attendance")

    df = load_table("attendance")

    if df.empty:
        st.warning("Nta data ihari")
    else:
        df["Date"] = pd.to_datetime(df["Date"])

        chosen_date = st.date_input("Hitamo Itariki", value=date.today())
        day_filter = st.selectbox("Umunsi", ["All","Wednesday","Saturday","Sunday"])

        filtered = df.copy()

        if chosen_date:
            filtered = filtered[filtered["Date"].dt.date == chosen_date]

        if day_filter != "All":
            filtered = filtered[filtered["Day"] == day_filter]

        st.dataframe(filtered)
        st.write(filtered.groupby("Status").size())

# ---------------- RAPORO UMUSANZU ----------------
with tabs[5]:
    st.header("📊 Raporo Umusanzu")

    df = load_table("contribution")

    if df.empty:
        st.warning("Nta data ihari")
    else:
        name_filter = st.selectbox("Izina", ["All"] + df["Name"].unique().tolist())

        filtered = df.copy()

        if name_filter != "All":
            filtered = filtered[filtered["Name"] == name_filter]

        st.dataframe(filtered)
        st.metric("Total amafaranga", filtered["Amount"].sum())

# ---------------- ABATAREMEWE ----------------
with tabs[6]:
    st.header("🚫 Abataremerewe kuririmba")

    df = load_table("attendance")

    if df.empty:
        st.warning("Nta data ihari")
    else:
        df["Date"] = pd.to_datetime(df["Date"])

        month = datetime.now().month
        absent = df[(df["Date"].dt.month == month) & (df["Status"] == "Absent")]

        counts = absent.groupby("Name").size()
        banned = counts[counts >= 3]

        if banned.empty:
            st.success("Nta barengeje 3")
        else:
            st.dataframe(banned)
