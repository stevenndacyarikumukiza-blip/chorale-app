import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ---------------- FILE PATHS ----------------
BASE_DIR = os.getcwd()

MEMBERS_FILE = os.path.join(BASE_DIR, "members.csv")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.csv")
CONTRIBUTION_FILE = os.path.join(BASE_DIR, "contribution.csv")

# ---------------- DEBUG SECTION ----------------
with st.expander("⚙️ Debug Info (if file not found)"):
    st.write("Current directory:", BASE_DIR)
    st.write("Files available:", os.listdir(BASE_DIR))

# ---------------- TABS ----------------
tabs = st.tabs([
    "Ahabanza",
    "Abaririmbyi",
    "Attendance",
    "Umusanzu",
    "Raporo Attendance",
    "Raporo Umusanzu",
    "Abataremerewe kuririmba"
])

# ---------------- HOME ----------------
with tabs[0]:
    st.header("Murakaza neza")
    st.write("• Wednesday • Saturday • Sunday")

# ---------------- MEMBERS ----------------
with tabs[1]:

    st.header("👥 Abaririmbyi")

    # Upload option (backup solution)
    uploaded_file = st.file_uploader("Shyiramo members.csv niba itaboneka", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        df.to_csv(MEMBERS_FILE, index=False)
        st.success("File yashyizwemo neza!")

    if os.path.exists(MEMBERS_FILE):

        try:
            df = pd.read_csv(MEMBERS_FILE)

            if df.empty:
                st.warning("members.csv irimo ubusa.")
            else:
                st.dataframe(df)
                st.info(f"Abari muri system: {len(df)}")

        except Exception as e:
            st.error(f"Error reading CSV: {e}")

    else:
        st.error("members.csv ntiboneka.")

# ---------------- ATTENDANCE ----------------
with tabs[2]:

    st.header("📋 Shyira Attendance")

    if not os.path.exists(MEMBERS_FILE):
        st.warning("Banza ushyiremo members.csv")
    else:

        members = pd.read_csv(MEMBERS_FILE)

        day = st.selectbox("Umunsi", ["Wednesday","Saturday","Sunday"])
        selected_date = st.date_input("Itariki", value=date.today())
        date_str = selected_date.strftime("%Y-%m-%d")

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

        st.write(f"Present: {present} | Absent: {absent} | Uruhushya: {uruhushya}")

        if st.button("💾 Save Attendance"):

            new = pd.DataFrame(attendance_list)

            if os.path.exists(ATTENDANCE_FILE):
                old = pd.read_csv(ATTENDANCE_FILE)
                new = pd.concat([old, new], ignore_index=True)

            new.to_csv(ATTENDANCE_FILE, index=False)

            st.success("Attendance saved!")

# ---------------- RAPORO ATTENDANCE ----------------
with tabs[4]:

    st.header("📊 Raporo ya Attendance")

    if os.path.exists(ATTENDANCE_FILE):

        df = pd.read_csv(ATTENDANCE_FILE)
        df["Date"] = pd.to_datetime(df["Date"])

        col1, col2 = st.columns(2)

        with col1:
            chosen_date = st.date_input("Hitamo Itariki", value=date.today())

        with col2:
            day_filter = st.selectbox("Umunsi", ["All","Wednesday","Saturday","Sunday"])

        filtered = df.copy()

        if chosen_date:
            filtered = filtered[filtered["Date"].dt.date == chosen_date]

        if day_filter != "All":
            filtered = filtered[filtered["Day"] == day_filter]

        st.subheader("Results")

        if filtered.empty:
            st.warning("Nta data ihari.")
        else:
            st.dataframe(filtered)

        st.subheader("Summary")
        st.write(filtered.groupby("Status").size())

        if st.checkbox("Show all data"):
            st.dataframe(df)

    else:
        st.warning("Nta attendance irabikwa.")

# ---------------- CONTRIBUTION ----------------
with tabs[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")
    contribution = st.text_input("Ubwoko bw'umusanzu")
    month = st.selectbox("Ukwezi", ["January","February","March","April","May","June",
                                   "July","August","September","October","November","December"])
    amount = st.number_input("Amafaranga", min_value=0)

    if st.button("Save"):

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

        st.success("Saved!")

# ---------------- RAPORO CONTRIBUTION ----------------
with tabs[5]:

    st.header("📊 Raporo Umusanzu")

    if os.path.exists(CONTRIBUTION_FILE):

        df = pd.read_csv(CONTRIBUTION_FILE)
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

        st.dataframe(df)
        st.metric("Total", df["Amount"].sum())

    else:
        st.warning("Nta data ihari.")

# ---------------- ABATAREMEWE ----------------
with tabs[6]:

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
            st.success("Nta barengeje 3.")
        else:
            st.dataframe(banned)

    else:
        st.warning("Nta attendance irabikwa.")
