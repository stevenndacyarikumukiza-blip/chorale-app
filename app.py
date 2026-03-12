# app.py
import streamlit as st
import pandas as pd
from datetime import datetime

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ----------------- Header Tabs -----------------
tabs = st.columns([1,1,1,1,1,1])
pages = ["Ahabanza","Abaririmbyi","Attendance","Umusanzu","Raporo Attendance","Raporo Umusanzu"]
page = None
for i, tab in enumerate(tabs):
    if tab.button(pages[i]):
        page = pages[i]

# Default to home if nothing clicked
if page is None:
    page = "Ahabanza"


# ---------------- HOME ----------------
if menu == "Ahabanza":
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.subheader("📖 Amateka ya Chorale")
    st.write("""
Chorale Inshuti za Yesu ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya. 
Yatangiriye mu 2021 abaririmbyi 35 bahurira hamwe na worship team.
Mu 2022 yatangiye gukora umurimo wo kuramya no guhimbaza Imana mu bitaramo.
""")

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

    try:
        members = pd.read_csv("members.csv")
        if members.empty:
            st.warning("Nta baririmbyi babonetse.")
        else:
            # ---------------- Filters ----------------
            month = st.selectbox(
                "📅 Hitamo Ukwezi",
                ["January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
            day = st.selectbox(
                "📆 Hitamo Umunsi",
                ["Wednesday","Saturday","Sunday"]
            )
            date_input = st.date_input("📌 Hitamo Itariki", value=datetime.now().date())

            attendance_list = []
            total_members = len(members)
            present_count = 0
            absent_count = 0
            uruhushya_count = 0

            try:
                old_attendance = pd.read_csv("attendance.csv")
            except FileNotFoundError:
                old_attendance = pd.DataFrame(columns=["Name","Day","Status","Date"])

            for i,row in members.iterrows():
                name = row["Name"]

                # Reba absent >=3
                absent_this_month = old_attendance[
                    (old_attendance["Name"]==name) &
                    (pd.to_datetime(old_attendance["Date"], errors="coerce").dt.month == ["January","February","March","April","May","June",
                                                                                     "July","August","September","October","November","December"].index(month)+1) &
                    (old_attendance["Status"]=="Absent")
                ].shape[0]

                if absent_this_month >=3:
                    st.write(f"🚫 {name} - Ntibemerewe kuririmba (Absent ≥3 uyu kwezi)")
                    continue

                col1, col2 = st.columns([3,3])
                with col1:
                    st.write("👤", name)
                with col2:
                    status = st.radio(
                        "Status",
                        ["Present","Absent","Uruhushya"],
                        key=i,
                        horizontal=True
                    )

                if status=="Present":
                    present_count +=1
                elif status=="Absent":
                    absent_count +=1
                else:
                    uruhushya_count +=1

                attendance_list.append({
                    "Name":name,
                    "Day":day,
                    "Status":status,
                    "Date":datetime.combine(date_input, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
                })

            st.divider()
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Abaririmbyi bose", total_members)
            col2.metric("Bari Present (Bitabiriye)", present_count)
            col3.metric("Bari Absent (Basibye)", absent_count)
            col4.metric("Basabye Uruhushya", uruhushya_count)

            if st.button("💾 Save Attendance"):
                new_data = pd.DataFrame(attendance_list)
                data = pd.concat([old_attendance,new_data],ignore_index=True)
                data.to_csv("attendance.csv",index=False)
                st.success("Attendance yabitswe neza!")

    except FileNotFoundError:
        st.warning("members.csv ntiyabonetse.")

# ---------------- CONTRIBUTION ----------------
elif menu == "Umusanzu":
    st.header("💰 Umusanzu")
    name = st.text_input("Izina")
    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")
    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )
    amount = st.number_input("Amafaranga", min_value=0)
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if st.button("💾 Save Umusanzu"):
        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution_name],
            "Month":[month],
            "Amount":[amount],
            "Date":[today]
        })
        try:
            old = pd.read_csv("contribution.csv")
            new = pd.concat([old,new],ignore_index=True)
        except:
            pass
        new.to_csv("contribution.csv",index=False)
        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
elif menu == "Raporo Attendance":
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                         "July","August","September","October","November","December"])
            day_filter = st.selectbox("Hitamo Umunsi", ["All","Wednesday","Saturday","Sunday"])
            date_filter = st.date_input("Hitamo Itariki", value=None)

            filtered = attendance.copy()

            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month == month_number]
            if day_filter != "All":
                filtered = filtered[filtered["Day"]==day_filter]
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date == date_filter]

            st.subheader("Attendance y'igihe wahisemo")
            st.dataframe(filtered)

            summary = filtered.groupby("Status").size()
            st.subheader("Summary")
            st.write(summary)

    except FileNotFoundError:
        st.warning("attendance.csv ntiyabonetse.")

# ---------------- RAPORO CONTRIBUTION ----------------
elif menu == "Raporo Umusanzu":
    st.header("📊 Raporo y'Umusanzu")
    try:
        df = pd.read_csv("contribution.csv")
        if df.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                          "July","August","September","October","November","December"])
            contribution_filter = st.text_input("Hitamo Umusanzu (Urugero: Impuzankano)")
            filtered = df.copy()
            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[df["Date"].dt.month == month_number]
            if contribution_filter:
                filtered = filtered[df["Contribution"]==contribution_filter]

            st.subheader("Raporo y'Umusanzu")
            st.dataframe(filtered)
            total = filtered["Amount"].sum()
            st.metric("Umusanzu wose", total)

    except FileNotFoundError:
        st.warning("contribution.csv ntiyabonetse.")

# ---------------- ABATEMEWE KURIRIMBA ----------------
elif menu == "Abatemewe Kuririmba":
    st.header("🚫 Abatemewe Kuririmba")
    try:
        attendance = pd.read_csv("attendance.csv")
        attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")
        current_month = datetime.now().month
        absent_counts = attendance[
            (attendance["Date"].dt.month == current_month) & 
            (attendance["Status"]=="Absent")
        ].groupby("Name").size()
        not_allowed = absent_counts[absent_counts >= 3]
        if not_allowed.empty:
            st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
        else:
            st.dataframe(not_allowed)
    except FileNotFoundError:
        st.warning("attendance.csv ntiyabonetse.")import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ---------------- Header Navigation ----------------
menu = st.selectbox(
    "Menu",
    ["Ahabanza","Abaririmbyi","Attendance","Umusanzu","Raporo Attendance","Raporo Umusanzu","Abatemewe Kuririmba"],
    index=0
)

# ---------------- HOME ----------------
if menu == "Ahabanza":
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.subheader("📖 Amateka ya Chorale")
    st.write("""
Chorale Inshuti za Yesu ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya. 
Yatangiriye mu 2021 abaririmbyi 35 bahurira hamwe na worship team.
Mu 2022 yatangiye gukora umurimo wo kuramya no guhimbaza Imana mu bitaramo.
""")

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

    try:
        members = pd.read_csv("members.csv")
        if members.empty:
            st.warning("Nta baririmbyi babonetse.")
        else:
            # ---------------- Filters ----------------
            month = st.selectbox(
                "📅 Hitamo Ukwezi",
                ["January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
            day = st.selectbox(
                "📆 Hitamo Umunsi",
                ["Wednesday","Saturday","Sunday"]
            )
            date_input = st.date_input("📌 Hitamo Itariki", value=datetime.now().date())

            attendance_list = []
            total_members = len(members)
            present_count = 0
            absent_count = 0
            uruhushya_count = 0

            try:
                old_attendance = pd.read_csv("attendance.csv")
            except FileNotFoundError:
                old_attendance = pd.DataFrame(columns=["Name","Day","Status","Date"])

            for i,row in members.iterrows():
                name = row["Name"]

                # Reba absent >=3
                absent_this_month = old_attendance[
                    (old_attendance["Name"]==name) &
                    (pd.to_datetime(old_attendance["Date"], errors="coerce").dt.month == ["January","February","March","April","May","June",
                                                                                     "July","August","September","October","November","December"].index(month)+1) &
                    (old_attendance["Status"]=="Absent")
                ].shape[0]

                if absent_this_month >=3:
                    st.write(f"🚫 {name} - Ntibemerewe kuririmba (Absent ≥3 uyu kwezi)")
                    continue

                col1, col2 = st.columns([3,3])
                with col1:
                    st.write("👤", name)
                with col2:
                    status = st.radio(
                        "Status",
                        ["Present","Absent","Uruhushya"],
                        key=i,
                        horizontal=True
                    )

                if status=="Present":
                    present_count +=1
                elif status=="Absent":
                    absent_count +=1
                else:
                    uruhushya_count +=1

                attendance_list.append({
                    "Name":name,
                    "Day":day,
                    "Status":status,
                    "Date":datetime.combine(date_input, datetime.now().time()).strftime("%Y-%m-%d %H:%M:%S")
                })

            st.divider()
            col1,col2,col3,col4 = st.columns(4)
            col1.metric("Abaririmbyi bose", total_members)
            col2.metric("Bari Present (Bitabiriye)", present_count)
            col3.metric("Bari Absent (Basibye)", absent_count)
            col4.metric("Basabye Uruhushya", uruhushya_count)

            if st.button("💾 Save Attendance"):
                new_data = pd.DataFrame(attendance_list)
                data = pd.concat([old_attendance,new_data],ignore_index=True)
                data.to_csv("attendance.csv",index=False)
                st.success("Attendance yabitswe neza!")

    except FileNotFoundError:
        st.warning("members.csv ntiyabonetse.")

# ---------------- CONTRIBUTION ----------------
elif menu == "Umusanzu":
    st.header("💰 Umusanzu")
    name = st.text_input("Izina")
    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")
    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )
    amount = st.number_input("Amafaranga", min_value=0)
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if st.button("💾 Save Umusanzu"):
        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution_name],
            "Month":[month],
            "Amount":[amount],
            "Date":[today]
        })
        try:
            old = pd.read_csv("contribution.csv")
            new = pd.concat([old,new],ignore_index=True)
        except:
            pass
        new.to_csv("contribution.csv",index=False)
        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
elif menu == "Raporo Attendance":
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                         "July","August","September","October","November","December"])
            day_filter = st.selectbox("Hitamo Umunsi", ["All","Wednesday","Saturday","Sunday"])
            date_filter = st.date_input("Hitamo Itariki", value=None)

            filtered = attendance.copy()

            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month == month_number]
            if day_filter != "All":
                filtered = filtered[filtered["Day"]==day_filter]
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date == date_filter]

            st.subheader("Attendance y'igihe wahisemo")
            st.dataframe(filtered)

            summary = filtered.groupby("Status").size()
            st.subheader("Summary")
            st.write(summary)

    except FileNotFoundError:
        st.warning("attendance.csv ntiyabonetse.")

# ---------------- RAPORO CONTRIBUTION ----------------
elif menu == "Raporo Umusanzu":
    st.header("📊 Raporo y'Umusanzu")
    try:
        df = pd.read_csv("contribution.csv")
        if df.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                          "July","August","September","October","November","December"])
            contribution_filter = st.text_input("Hitamo Umusanzu (Urugero: Impuzankano)")
            filtered = df.copy()
            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[df["Date"].dt.month == month_number]
            if contribution_filter:
                filtered = filtered[df["Contribution"]==contribution_filter]

            st.subheader("Raporo y'Umusanzu")
            st.dataframe(filtered)
            total = filtered["Amount"].sum()
            st.metric("Umusanzu wose", total)

    except FileNotFoundError:
        st.warning("contribution.csv ntiyabonetse.")

# ---------------- ABATEMEWE KURIRIMBA ----------------
elif menu == "Abatemewe Kuririmba":
    st.header("🚫 Abatemewe Kuririmba")
    try:
        attendance = pd.read_csv("attendance.csv")
        attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")
        current_month = datetime.now().month
        absent_counts = attendance[
            (attendance["Date"].dt.month == current_month) & 
            (attendance["Status"]=="Absent")
        ].groupby("Name").size()
        not_allowed = absent_counts[absent_counts >= 3]
        if not_allowed.empty:
            st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
        else:
            st.dataframe(not_allowed)
    except FileNotFoundError:
        st.warning("attendance.csv ntiyabonetse.")
