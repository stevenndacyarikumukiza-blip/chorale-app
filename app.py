# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")

st.title("🎵 CHORALE INSHUTI ZA YESU")

# ---------------- HEADER TABS ----------------
tabs = st.tabs([
    "🏠 Ahabanza",
    "👥 Abaririmbyi",
    "📋 Attendance",
    "💰 Umusanzu",
    "📊 Raporo Attendance",
    "📊 Raporo Umusanzu"
])

# ---------------- HOME ----------------
with tabs[0]:

    st.header("Murakaza neza muri Chorale Inshuti za Yesu")

    st.write("Iminsi y’imyitozo:")
    st.write("• Ku wa Gatatu")
    st.write("• Ku wa Gatandatu")
    st.write("• Ku Cyumweru")

# ---------------- MEMBERS ----------------
with tabs[1]:

    st.header("👥 Abaririmbyi")

    try:
        members = pd.read_csv("members.csv")

        st.dataframe(members)

        st.info(f"Umubare w'Abaririmbyi: {len(members)}")

    except:
        st.warning("⚠️ Nta baririmbyi babonetse. Shyira members.csv")

# ---------------- ATTENDANCE ----------------
with tabs[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
        "📅 Hitamo Umunsi w’Imyitozo",
        ["Wednesday","Saturday","Sunday"]
    )

    try:

        members = pd.read_csv("members.csv")

        if members.empty:

            st.warning("⚠️ Urutonde rw'Abaririmbyi ntirubonetse")

        else:

            attendance_list = []

            present_count = 0
            absent_count = 0
            uruhushya_count = 0

            total_members = len(members)

            today = datetime.now()
            current_month = today.month
            date_str = today.strftime("%Y-%m-%d %H:%M:%S")

            try:
                old = pd.read_csv("attendance.csv")
            except:
                old = pd.DataFrame(columns=["Name","Day","Status","Date"])

            for i,row in members.iterrows():

                name = row["Name"]

                absent_this_month = old[
                    (old["Name"]==name) &
                    (pd.to_datetime(old["Date"], errors="coerce").dt.month==current_month) &
                    (old["Status"]=="Absent")
                ].shape[0]

                if absent_this_month >= 3:

                    st.write(f"🚫 {name} - Ntibemerewe kuririmba (Absent ≥3)")

                    continue

                col1,col2 = st.columns([3,3])

                with col1:
                    st.write("👤", name)

                with col2:

                    status = st.radio(
                        "Status",
                        ["Present","Absent","Uruhushya"],
                        key=i,
                        horizontal=True
                    )

                if status == "Present":
                    present_count += 1

                elif status == "Absent":
                    absent_count += 1

                else:
                    uruhushya_count += 1

                attendance_list.append({
                    "Name":name,
                    "Day":day,
                    "Status":status,
                    "Date":date_str
                })

            st.divider()

            col1,col2,col3,col4 = st.columns(4)

            col1.metric("Abaririmbyi bose", total_members)

            col2.metric("Bari Present (Bitabiriye)", present_count)

            col3.metric("Bari Absent (Basibye)", absent_count)

            col4.metric("Basabye Uruhushya", uruhushya_count)

            if st.button("💾 Save Attendance"):

                new = pd.DataFrame(attendance_list)

                data = pd.concat([old,new], ignore_index=True)

                data.to_csv("attendance.csv", index=False)

                st.success("✅ Attendance yabitswe neza!")

    except:

        st.warning("⚠️ members.csv ntiyabonetse")

# ---------------- CONTRIBUTION ----------------
with tabs[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina ry'umuririmbyi")

    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga", min_value=0)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("💾 Save Umusanzu"):

        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution_name],
            "Month":[month],
            "Amount":[amount],
            "Date":[date_str]
        })

        try:
            old = pd.read_csv("contribution.csv")

            new = pd.concat([old,new], ignore_index=True)

        except:
            pass

        new.to_csv("contribution.csv", index=False)

        st.success("✅ Umusanzu wabitswe neza!")

# ---------------- ATTENDANCE REPORT ----------------
with tabs[4]:

    st.header("📊 Raporo ya Attendance")

    try:

        attendance = pd.read_csv("attendance.csv")

        if attendance.empty:

            st.info("Nta data ya attendance ihari")

        else:

            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

            day_filter = st.selectbox(
                "Hitamo Umunsi",
                ["All","Wednesday","Saturday","Sunday"]
            )

            filtered = attendance.copy()

            if day_filter != "All":
                filtered = filtered[filtered["Day"] == day_filter]

            st.dataframe(filtered)

            st.subheader("Summary")

            summary = filtered.groupby("Status").size()

            st.write(summary)

    except:

        st.warning("⚠️ attendance.csv ntiyabonetse")

# ---------------- CONTRIBUTION REPORT ----------------
with tabs[5]:

    st.header("📊 Raporo y'Umusanzu")

    try:

        df = pd.read_csv("contribution.csv")

        if df.empty:

            st.info("Nta musanzu wabonetse")

        else:

            st.dataframe(df)

            total = df["Amount"].sum()

            st.metric("Umusanzu wose", total)

    except:

        st.warning("⚠️ contribution.csv ntiyabonetse")
