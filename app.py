import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")

st.title("🎵 CHORALE INSHUTI ZA YESU")

tabs = st.tabs([
"Ahabanza",
"Abaririmbyi",
"Attendance",
"Umusanzu",
"Raporo Attendance",
"Raporo Umusanzu",
"Abatemewe Kuririmba"
])

# ---------------- HOME ----------------
with tabs[0]:

    st.header("Murakaza neza muri Chorale Inshuti za Yesu")

    st.write("Iminsi y’imyitozo:")
    st.write("• Wednesday")
    st.write("• Saturday")
    st.write("• Sunday")


# ---------------- MEMBERS ----------------
with tabs[1]:

    st.header("👥 Abaririmbyi")

    try:
        df = pd.read_csv("members.csv")

        st.dataframe(df)

        st.info(f"Umubare w'Abaririmbyi: {len(df)}")

    except:
        st.warning("Nta baririmbyi babonetse.")


# ---------------- ATTENDANCE ----------------
with tabs[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
        "📅 Hitamo Umunsi w’Imyitozo",
        ["Wednesday","Saturday","Sunday"]
    )

    try:

        members = pd.read_csv("members.csv")

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
        col2.metric("Bari Present", present_count)
        col3.metric("Bari Absent", absent_count)
        col4.metric("Basabye Uruhushya", uruhushya_count)

        if st.button("💾 Save Attendance"):

            new = pd.DataFrame(attendance_list)

            data = pd.concat([old,new], ignore_index=True)

            data.to_csv("attendance.csv", index=False)

            st.success("Attendance yabitswe neza!")

    except:
        st.warning("members.csv ntiyabonetse.")


# ---------------- CONTRIBUTION ----------------
with tabs[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")

    contribution_name = st.text_input("Izina ry'umusanzu")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga", min_value=0)

    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Bika Umusanzu"):

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
with tabs[4]:

    st.header("📊 Raporo ya Attendance")

    try:

        attendance = pd.read_csv("attendance.csv")

        attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

        month = st.selectbox(
            "Hitamo Ukwezi",
            ["All","January","February","March","April","May","June",
             "July","August","September","October","November","December"]
        )

        day = st.selectbox(
            "Hitamo Umunsi",
            ["All","Wednesday","Saturday","Sunday"]
        )

        date = st.date_input("Hitamo Itariki")

        filtered = attendance.copy()

        if month != "All":

            month_number = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
            ].index(month)+1

            filtered = filtered[filtered["Date"].dt.month == month_number]

        if day != "All":
            filtered = filtered[filtered["Day"] == day]

        filtered = filtered[filtered["Date"].dt.date == date]

        st.dataframe(filtered)

    except:

        st.warning("attendance.csv ntiyabonetse.")


# ---------------- RAPORO CONTRIBUTION ----------------
with tabs[5]:

    st.header("📊 Raporo y'Umusanzu")

    try:

        df = pd.read_csv("contribution.csv")

        contribution_name = st.text_input("Andika Izina ry'umusanzu ushaka kureba")

        if contribution_name:

            filtered = df[df["Contribution"]==contribution_name]

            st.dataframe(filtered)

            st.metric("Total", filtered["Amount"].sum())

        else:

            st.dataframe(df)

    except:

        st.warning("contribution.csv ntiyabonetse.")


# ---------------- DISCIPLINE ----------------
with tabs[6]:

    st.header("🚫 Abatemewe Kuririmba")

    try:

        attendance = pd.read_csv("attendance.csv")

        attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

        month = datetime.now().month

        absent = attendance[
            (attendance["Status"]=="Absent") &
            (attendance["Date"].dt.month==month)
        ]

        banned = absent.groupby("Name").size().reset_index(name="Absent")

        banned = banned[banned["Absent"]>=3]

        if banned.empty:

            st.success("Nta muntu utemewe kuririmba.")

        else:

            st.dataframe(banned)

    except:

        st.warning("attendance.csv ntiyabonetse.")
