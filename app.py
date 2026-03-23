import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, date
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

MEMBERS_FILE = "members.csv"
ATTENDANCE_FILE = "attendance.csv"
CONTRIBUTION_FILE = "contribution.csv"

# ---------------- DATABASE ----------------
conn = sqlite3.connect("chorale.db", check_same_thread=False)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS attendance (
    Name TEXT, Day TEXT, Status TEXT, Date TEXT)""")

c.execute("""CREATE TABLE IF NOT EXISTS contribution (
    Name TEXT, Contribution TEXT, Month TEXT, Amount REAL, Date TEXT)""")

conn.commit()

# ---------------- FUNCTIONS ----------------
def load_members():
    if os.path.exists(MEMBERS_FILE):
        return pd.read_csv(MEMBERS_FILE)
    return pd.DataFrame()

def load_table(table):
    return pd.read_sql(f"SELECT * FROM {table}", conn)

def insert_attendance(data):
    c.executemany("INSERT INTO attendance VALUES (?,?,?,?)", data)
    conn.commit()

    # SAVE ALSO TO CSV
    df = pd.DataFrame(data, columns=["Name","Day","Status","Date"])
    if os.path.exists(ATTENDANCE_FILE):
        old = pd.read_csv(ATTENDANCE_FILE)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(ATTENDANCE_FILE, index=False)

def insert_contribution(data):
    c.execute("INSERT INTO contribution VALUES (?,?,?,?,?)", data)
    conn.commit()

    # SAVE ALSO TO CSV
    df = pd.DataFrame([data], columns=["Name","Contribution","Month","Amount","Date"])
    if os.path.exists(CONTRIBUTION_FILE):
        old = pd.read_csv(CONTRIBUTION_FILE)
        df = pd.concat([old, df], ignore_index=True)
    df.to_csv(CONTRIBUTION_FILE, index=False)

# ---------------- TABS ----------------
tabs = st.tabs([
    "Ahabanza","Abaririmbyi","Attendance","Umusanzu",
    "Raporo Attendance","Raporo Umusanzu","Abataremerewe"
])

# ---------------- MEMBERS ----------------
with tabs[1]:
    members = load_members()
    if members.empty:
        st.warning("members.csv ntiboneka")
    else:
        st.dataframe(members)

# ---------------- ATTENDANCE ----------------
with tabs[2]:
    members = load_members()
    if not members.empty:
        day = st.selectbox("Umunsi", ["Wednesday","Saturday","Sunday"])
        selected_date = st.date_input("Itariki", value=date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

        data = []

        for i, row in members.iterrows():
            name = row["Name"]
            status = st.radio(name, ["Present","Absent","Uruhushya"], key=i)
            data.append((name, day, status, date_str))

        if st.button("Save Attendance"):
            insert_attendance(data)
            st.success("Attendance yabitswe muri DB na CSV!")

# ---------------- UMUSANZU ----------------
with tabs[3]:
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

    if st.button("Save Contribution"):
        insert_contribution((name, contribution, month, amount, str(datetime.now())))
        st.success(f"Umusanzu wa {name} wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
with tabs[4]:
    df = load_table("attendance")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])

        day = st.selectbox("Umunsi", ["All","Wednesday","Saturday","Sunday"])
        if day != "All":
            df = df[df["Day"] == day]

        st.dataframe(df)
        st.write(df.groupby("Status").size())

# ---------------- RAPORO UMUSANZU ----------------
with tabs[5]:
    df = load_table("contribution")

    if not df.empty:

        name = st.selectbox("Izina", ["All"] + df["Name"].unique().tolist())
        contrib = st.selectbox("Ubwoko", ["All"] + df["Contribution"].dropna().unique().tolist())
        month = st.selectbox("Ukwezi", ["All"] + df["Month"].unique().tolist())

        filtered = df.copy()

        if name != "All":
            filtered = filtered[filtered["Name"] == name]

        if contrib != "All":
            filtered = filtered[filtered["Contribution"] == contrib]

        if month != "All":
            filtered = filtered[filtered["Month"] == month]

        st.dataframe(filtered)
        st.metric("Total", filtered["Amount"].sum())

# ---------------- ABATAREMEWE ----------------
with tabs[6]:
    df = load_table("attendance")

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])
        month = datetime.now().month

        absent = df[(df["Date"].dt.month == month) & (df["Status"]=="Absent")]
        counts = absent.groupby("Name").size()
        banned = counts[counts >= 3]

        st.dataframe(banned if not banned.empty else pd.DataFrame({"Message":["Nta barengeje 3"]}))
