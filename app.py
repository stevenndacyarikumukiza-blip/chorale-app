import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# ---------------- FILE PATH SETUP ----------------
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

MEMBERS_FILE = f"{DATA_FOLDER}/members.csv"
ATTENDANCE_FILE = f"{DATA_FOLDER}/attendance.csv"
CONTRIBUTION_FILE = f"{DATA_FOLDER}/contribution.csv"

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

tabs = [
    "Ahabanza",
    "Abaririmbyi",
    "Attendance",
    "Umusanzu",
    "Raporo Attendance",
    "Raporo Umusanzu",
    "Abataremerewe kuririmba"
]

selected_tab = st.tabs(tabs)

# ---------------- HOME ----------------
with selected_tab[0]:

    st.header("Murakaza neza muri Chorale Inshuti za Yesu")

    st.write("Iminsi y’imyitozo:")
    st.write("• Wednesday • Saturday • Sunday")

    st.divider()

    st.subheader("📖 Amateka ya Chorale")

    st.write("""
Chorale Inshuti za Yesu ikorera umurimo w’Imana muri ADEPR Kinyinya.

Yatangiriye mu 2021 igizwe n’abaririmbyi 35.
""")

# ---------------- MEMBERS ----------------
with selected_tab[1]:

    st.header("👥 Abaririmbyi")

    if os.path.exists(MEMBERS_FILE):
        df = pd.read_csv(MEMBERS_FILE)
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")
    else:
        st.warning("members.csv ntiyabonetse.")

# ---------------- ATTENDANCE ----------------
with selected_tab[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox("Hitamo Umunsi", ["Wednesday","Saturday","Sunday"])

    selected_date = st.date_input("Hitamo Itariki", value=date.today())
    date_str = selected_date.strftime("%Y-%m-%d")

    if os.path.exists(MEMBERS_FILE):

        members = pd.read_csv(MEMBERS_FILE)

        if os.path.exists(ATTENDANCE_FILE):
            old = pd.read_csv(ATTENDANCE_FILE)
        else:
            old = pd.DataFrame(columns=["Name","Day","Status","Date"])

        attendance_list = []

        present = 0
        absent = 0
        uruhushya = 0

        for i, row in members.iterrows():

            name = row["Name"]

            col1, col2 = st.columns([3,3])

            with col1:
                st.write(name)

            with col2:
                status = st.radio(
                    "Status",
                    ["Present","Absent","Uruhushya"],
                    key=f"{name}_{i}",
                    horizontal=True
                )

            if status == "Present":
                present += 1
            elif status == "Absent":
                absent += 1
            else:
                uruhushya += 1

            attendance_list.append({
                "Name": name,
                "Day": day,
                "Status": status,
                "Date": date_str
            })

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Abaririmbyi bose", len(members))
        col2.metric("Present", present)
        col3.metric("Absent", absent)
        col4.metric("Uruhushya", uruhushya)

        if st.button("💾 Save Attendance"):

            new = pd.DataFrame(attendance_list)
            data = pd.concat([old, new], ignore_index=True)

            data.to_csv(ATTENDANCE_FILE, index=False)

            st.success("Attendance yabitswe neza!")

    else:
        st.warning("members.csv ntiyabonetse.")

# ---------------- CONTRIBUTION ----------------
with selected_tab[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")
    contribution = st.text_input("Ubwoko bw'umusanzu")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga", min_value=0)

    if st.button("💾 Save Umusanzu"):

        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution],
            "Month":[month],
            "Amount":[amount],
            "Date":[datetime.now()]
        })

        if os.path.exists(CONTRIBUTION_FILE):
            old = pd.read_csv(CONTRIBUTION_FILE)
            new = pd.concat([old, new], ignore_index=True)

        new.to_csv(CONTRIBUTION_FILE, index=False)

        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
with selected_tab[4]:

    st.header("📊 Raporo ya Attendance")

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)
        df["Date"] = pd.to_datetime(df["Date"])

        col1, col2 = st.columns(2)

        with col1:
            chosen_date = st.date_input("Hitamo Itariki", value=date.today())

        with col2:
            day_filter = st.selectbox(
                "Hitamo Umunsi",
                ["All","Wednesday","Saturday","Sunday"]
            )

        filtered = df.copy()

        if chosen_date:
            filtered = filtered[filtered["Date"].dt.date == chosen_date]

        if day_filter != "All":
            filtered = filtered[filtered["Day"] == day_filter]

        st.subheader("📋 Attendance wabonye")

        if filtered.empty:
            st.warning("Nta data ihari kuri ayo mahitamo.")
        else:
            st.dataframe(filtered)

        st.subheader("📈 Summary")

        summary = filtered.groupby("Status").size()
        st.write(summary)

        # BONUS: View all data
        if st.checkbox("Reba Attendance zose"):
            st.dataframe(df)

    else:
        st.warning("Nta attendance irabikwa. Banza uyishyiremo.")

# ---------------- RAPORO CONTRIBUTION ----------------
with selected_tab[5]:

    st.header("📊 Raporo y'Umusanzu")

    if os.path.exists(CONTRIBUTION_FILE):

        df = pd.read_csv(CONTRIBUTION_FILE)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        contribution_filter = st.selectbox(
            "Hitamo Umusanzu",
            ["All"] + df["Contribution"].dropna().unique().tolist()
        )

        month_filter = st.selectbox(
            "Hitamo Ukwezi",
            ["All","January","February","March","April","May","June",
             "July","August","September","October","November","December"]
        )

        filtered = df.copy()

        if contribution_filter != "All":
            filtered = filtered[filtered["Contribution"] == contribution_filter]

        if month_filter != "All":
            month_number = [
                "January","February","March","April","May","June",
                "July","August","September","October","November","December"
            ].index(month_filter) + 1

            filtered = filtered[filtered["Date"].dt.month == month_number]

        st.dataframe(filtered)

        total = filtered["Amount"].sum()
        st.metric("Umusanzu wose", total)

    else:
        st.warning("Nta musanzu urabikwa.")

# ---------------- ABATAREMEWE ----------------
with selected_tab[6]:

    st.header("🚫 Abataremerewe kuririmba")

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)
        df["Date"] = pd.to_datetime(df["Date"])

        month = datetime.now().month

        absent = df[
            (df["Date"].dt.month == month) &
            (df["Status"] == "Absent")
        ]

        counts = absent.groupby("Name").size()
        banned = counts[counts >= 3]

        if banned.empty:
            st.success("Nta baririmbyi bafite absent ≥3.")
        else:
            st.dataframe(banned)

    else:
        st.warning("Nta attendance irabikwa.")
