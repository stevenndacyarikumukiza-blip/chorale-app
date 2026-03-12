# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date

# ----------------- PAGE SETUP -----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ----------------- HEADER TABS -----------------
tabs = ["Ahabanza", "Abaririmbyi", "Attendance", "Umusanzu", 
        "Raporo Attendance", "Raporo Umusanzu", "Abatemewe kuririmba"]
selected_tab = st.tabs(tabs)

# ----------------- HOME PAGE -----------------
with selected_tab[0]:
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.divider()
    st.subheader("📖 Amateka ya Chorale")
    st.write("""
Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya, Paruwasi.
Yatangiriye mu mwaka wa 2021, abaririmbyi 35 bahuriraga hamwe na worship team yaho.
- Abagabo: 5  
- Abagore: 5  
- Abasore: 10  
- Abakobwa: 15
    """)
    st.write("Ibikorwa by’ingenzi: giterane, YouTube channel, indirimbo, umubano n’izindi chorale, ibyuma by’umuziki.")
    st.markdown("[▶️ Reba indirimbo zacu kuri YouTube](https://www.youtube.com/channel/YOUR_CHANNEL_LINK_HERE)")

# ----------------- MEMBERS PAGE -----------------
with selected_tab[1]:
    st.header("👥 Abaririmbyi")
    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")
    except:
        st.warning("Nta baririmbyi babonetse. Ongera ushyiremo ababaririmbyi.")

# ----------------- ATTENDANCE PAGE -----------------
with selected_tab[2]:
    st.header("📋 Shyira Attendance")
    month = st.selectbox("📅 Hitamo Ukwezi", ["January","February","March","April","May","June",
                                             "July","August","September","October","November","December"])
    day = st.selectbox("📆 Hitamo Umunsi", ["Wednesday","Saturday","Sunday"])
    date_filter = st.date_input("📌 Hitamo Itariki", value=date.today())
    
    try:
        members = pd.read_csv("members.csv")
        if members.empty:
            st.warning("members.csv ntiyabonetse.")
        else:
            attendance_list = []
            present_count = 0
            absent_count = 0
            uruhushya_count = 0
            total_members = len(members)
            date_str = date_filter.strftime("%Y-%m-%d")
            
            try:
                old = pd.read_csv("attendance.csv")
            except:
                old = pd.DataFrame(columns=["Name","Day","Status","Date"])
            
            for i,row in members.iterrows():
                name = row["Name"]
                absent_this_month = old[
                    (old["Name"]==name) &
                    (pd.to_datetime(old["Date"], errors="coerce").dt.month==["January","February","March","April","May","June",
                                                                             "July","August","September","October","November","December"].index(month)+1) &
                    (old["Status"]=="Absent")
                ].shape[0]

                if absent_this_month >= 3:
                    st.write(f"🚫 {name} - Ntibemerewe kuririmba (Absent ≥3)")
                    continue

                col1, col2 = st.columns([3,3])
                with col1:
                    st.write("👤", name)
                with col2:
                    status = st.radio("Status", ["Present","Absent","Uruhushya"], key=i, horizontal=True)

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

# ----------------- CONTRIBUTION PAGE -----------------
with selected_tab[3]:
    st.header("💰 Umusanzu")
    name = st.text_input("Izina")
    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")
    month = st.selectbox("Ukwezi", ["January","February","March","April","May","June",
                                    "July","August","September","October","November","December"])
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
        st.success("Umusanzu wabitswe neza!")

# ----------------- RAPORO ATTENDANCE -----------------
with selected_tab[4]:
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors='coerce')
            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                          "July","August","September","October","November","December"])
            day_filter = st.selectbox("Hitamo Umunsi", ["All","Wednesday","Saturday","Sunday"])
            date_filter = st.date_input("Hitamo Itariki (optionnel)", value=None)
            filtered = attendance.copy()
            if month_filter!="All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month==month_number]
            if day_filter!="All":
                filtered = filtered[filtered["Day"]==day_filter]
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date==date_filter]
            st.subheader("Attendance Wabonetse")
            st.dataframe(filtered)
            st.subheader("Summary")
            summary = filtered.groupby("Status").size()
            st.write(summary)
    except:
        st.warning("attendance.csv ntiyabonetse.")

# ----------------- RAPORO CONTRIBUTION -----------------
with selected_tab[5]:
    st.header("📊 Raporo y'Umusanzu")
    try:
        df = pd.read_csv("contribution.csv")
        if df.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            contribution_filter = st.selectbox("Hitamo Umusanzu", ["All"]+df["Contribution"].unique().tolist())
            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                          "July","August","September","October","November","December"])
            filtered = df.copy()
            if contribution_filter!="All":
                filtered = filtered[filtered["Contribution"]==contribution_filter]
            if month_filter!="All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month==month_number]
            st.subheader("Umusanzu Wabonetse")
            st.dataframe(filtered)
            total = filtered["Amount"].sum()
            st.metric("Umusanzu wose", total)
    except:
        st.warning("contribution.csv ntiyabonetse.")

# ----------------- ABATEMEWE KURIRIMBA -----------------
with selected_tab[6]:
    st.header("🚫 Abataremerewe kuririmba")
    try:
        attendance = pd.read_csv("attendance.csv")
        attendance["Date"] = pd.to_datetime(attendance["Date"], errors='coerce')
        current_month = datetime.now().month
        absent_counts = attendance[
            (attendance["Date"].dt.month==current_month) & 
            (attendance["Status"]=="Absent")
        ].groupby("Name").size()
        not_allowed = absent_counts[absent_counts>=3]
        if not not_allowed.empty:
            st.dataframe(not_allowed)
        else:
            st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
    except:
        st.warning("attendance.csv ntiyabonetse.")
