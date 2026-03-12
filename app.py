import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")

st.title("🎵 CHORALE INSHUTI ZA YESU")

menu = st.sidebar.selectbox(
    "Menu",
    ["Ahabanza", "Abaririmbyi", "Attendance", "Umusanzu", "Raporo Attendance", "Raporo Umusanzu"]
)

# ---------------- HOME ----------------
if menu == "Ahabanza":
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")

# ---------------- MEMBERS ----------------
elif menu == "Abaririmbyi":
    st.header("👥 Abaririmbyi")
    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")
    except:
        st.warning("Nta baririmbyi babonetse.")

# ---------------- ATTENDANCE ----------------
elif menu == "Attendance":

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
        "📅 Hitamo Umunsi w’Imyitozo",
        ["Wednesday", "Saturday", "Sunday"]
    )

    try:
        members = pd.read_csv("members.csv")

        if members.empty:
            st.warning("Nta baririmbyi babonetse.")
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

                st.success("Attendance yabitswe neza!")

    except:
        st.warning("members.csv ntiyabonetse.")

# ---------------- CONTRIBUTION ----------------
elif menu == "Umusanzu":

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")

    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June","July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga", min_value=0)

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Save Umusanzu"):

        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution_name],
            "Month":[month],
            "Amount":[amount],
            "Date":[today]
        })

        try:
            old = pd.read_csv("contribution.csv")
            new = pd.concat([old,new], ignore_index=True)
        except:
            pass

        new.to_csv("contribution.csv", index=False)

        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
elif menu == "Raporo Attendance":

    st.header("📊 Raporo ya Attendance")

    try:
        attendance = pd.read_csv("attendance.csv")

        if attendance.empty:
            st.info("Nta data ihari.")
        else:

            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

            day = st.selectbox(
                "Umunsi",
                ["All","Wednesday","Saturday","Sunday"]
            )

            filtered = attendance.copy()

            if day != "All":
                filtered = filtered[filtered["Day"]==day]

            st.dataframe(filtered)

            summary = filtered.groupby(["Status"]).size()

            st.subheader("Summary")

            st.write(summary)

    except:
        st.warning("attendance.csv ntiyabonetse.")

# ---------------- RAPORO CONTRIBUTION ----------------
elif menu == "Raporo Umusanzu":

    st.header("📊 Raporo y'Umusanzu")

    try:
        df = pd.read_csv("contribution.csv")

        if df.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            st.dataframe(df)

            total = df["Amount"].sum()

            st.metric("Umusanzu wose", total)

    except:
        st.warning("contribution.csv ntiyabonetse.")
