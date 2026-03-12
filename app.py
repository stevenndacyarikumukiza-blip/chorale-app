# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4B0082;'>🎵 CHORALE INSHUTI ZA YESU</h1>", unsafe_allow_html=True)

# ----------------- Header Navigation (Tabs) -----------------
tabs = st.tabs(["Ahabanza", "Abaririmbyi", "Attendance", "Umusanzu",
                "Raporo Attendance", "Raporo Umusanzu", "Abatemewe kuririmba"])

# ----------------- HOME -----------------
with tabs[0]:
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.divider()
    st.header("📖 Amateka ya Chorale")
    st.write("""
Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya, Paruwasi.
Yatangiriye mu mwaka wa 2021, ubwo abaririmbyi 35 bahuriraga hamwe na worship team yaho.
- Abagabo: 13  
- Abagore: 9  
- Abasore: 15  
- Abakobwa: 28  
- Abandi 7 bari mu igeragezwa
""")
    st.markdown("[▶️ Reba indirimbo zacu kuri YouTube](https://www.youtube.com/channel/YOUR_CHANNEL_LINK_HERE)")

# ----------------- MEMBERS -----------------
with tabs[1]:
    st.header("👥 Abaririmbyi")
    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")
    except:
        st.warning("Nta baririmbyi babonetse.")

# ----------------- ATTENDANCE -----------------
with tabs[2]:
    st.header("📋 Shyira Attendance")
    month = st.selectbox(
        "📅 Hitamo Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )
    day = st.selectbox("📆 Hitamo Umunsi", ["Wednesday","Saturday","Sunday"])
    date_input = st.date_input("📌 Hitamo Itariki", value=date.today())

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
            date_str = date_input.strftime("%Y-%m-%d")

            try:
                old = pd.read_csv("attendance.csv")
            except:
                old = pd.DataFrame(columns=["Name","Day","Status","Date"])

            for i,row in members.iterrows():
                name = row["Name"]
                absent_this_month = old[
                    (old["Name"]==name) &
                    (pd.to_datetime(old["Date"], errors="coerce").dt.month==date_input.month) &
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

                if status=="Present":
                    present_count += 1
                elif status=="Absent":
                    absent_count += 1
                else:
                    uruhushya_count += 1

                attendance_list.append({
                    "Name": name,
                    "Day": day,
                    "Status": status,
                    "Date": date_str
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

# ----------------- CONTRIBUTION -----------------
with tabs[3]:
    st.header("💰 Umusanzu")
    name = st.text_input("Izina")
    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")
    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )
    amount = st.number_input("Amafaranga", min_value=0)
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if st.button("💾 Save Umusanzu"):
        new = pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution_name],
            "Month":[month],
            "Amount":[amount],
            "Date":[today_str]
        })
        try:
            old = pd.read_csv("contribution.csv")
            new = pd.concat([old,new], ignore_index=True)
        except:
            pass
        new.to_csv("contribution.csv", index=False)
        st.success("Umusanzu wabitswe neza!")

# ----------------- RAPORO ATTENDANCE -----------------
with tabs[4]:
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")
            day_filter = st.selectbox("Umunsi", ["All","Wednesday","Saturday","Sunday"])
            month_filter = st.selectbox(
                "Ukwezi",
                ["All","January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
            date_filter = st.date_input("Hitamo Itariki (optionnel)", value=None)

            filtered = attendance.copy()
            if day_filter!="All":
                filtered = filtered[filtered["Day"]==day_filter]
            if month_filter!="All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month==month_number]
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date==date_filter]

            if filtered.empty:
                st.warning("Nta attendance yabonetse kuri aya ma filters.")
            else:
                st.subheader("Attendance Yabonetse")
                st.dataframe(filtered)

# ----------------- RAPORO UMUSANZU -----------------
with tabs[5]:
    st.header("📊 Raporo y'Umusanzu")
    try:
        contribution = pd.read_csv("contribution.csv")
        if contribution.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            contribution["Date"] = pd.to_datetime(contribution["Date"], errors="coerce")
            contribution_name_filter = st.text_input("Shakisha Umusanzu (Urugero: Impuzankano)")
            filtered = contribution.copy()
            if contribution_name_filter:
                filtered = filtered[filtered["Contribution"].str.contains(contribution_name_filter, case=False)]
            if filtered.empty:
                st.warning("Nta musanzu wabonetse kuri aya ma filters.")
            else:
                st.subheader("Umusanzu Wabonetse")
                st.dataframe(filtered)
                st.metric("Umusanzu wose", filtered["Amount"].sum())

# ----------------- ABATEMEWE KURIRIMBA -----------------
with tabs[6]:
    st.header("🚫 Abatemewe Kuririmba")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")
            current_month = datetime.now().month
            absent_counts = attendance[
                (attendance["Date"].dt.month==current_month) & (attendance["Status"]=="Absent")
            ].groupby("Name").size()
            not_allowed = absent_counts[absent_counts>=3]
            if not_allowed.empty:
                st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
            else:
                st.warning("🚫 Abataremerewe kuririmba uyu kwezi:")
                st.dataframe(not_allowed)
