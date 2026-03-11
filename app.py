# app.py
import streamlit as st
import pandas as pd
from datetime import datetime, date

# ----------------- Page Setup -----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

# ----------------- Sidebar Menu -----------------
menu = st.sidebar.selectbox(
    "Menu",
    ["Ahabanza", "Abaririmbyi", "Attendance", "Umusanzu", "Raporo Attendance", "Raporo Umusanzu"]
)

# ----------------- HOME PAGE -----------------
if menu == "Ahabanza":
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.divider()
    st.header("📖 Amateka ya Chorale")
    st.write("""
Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya, Paruwasi.
Yatangiriye mu mwaka wa 2021, mu kwezi kwa mbere, ubwo abaririmbyi 35 bahuriraga hamwe na worship team yaho.
- Abagabo: 5  
- Abagore: 5  
- Abasore: 10  
- Abakobwa: 15
""")
    st.write("""
Mu mwaka wa 2022, chorale yaguze impuzankano (uniform) ya mbere kandi yatangiye gukora umurimo wo kuramya no guhimbaza Imana mu bitaramo n’iteraniro.
""")
    st.write("""
Ibikorwa by’ingenzi:
- 12/2022: Igiterane cya mbere twatumiye chorale Seeking for Jesus  
- Nyuma y’icyo giterane: Twafunguye YouTube Channel yitwa "Inshuti za Yesu Choir Kinyinya"  
- Ubu dufite indirimbo imwe yitwa Ikinyita ifite amajwi n’amagambo gusa
""")
    st.write("""
Umubano n’izindi chorale:
- Chorale Seeking for Jesus  
- Chorale Abatwaramucyo  
- Chorale Future  
- Chorale Ebenezer  
- Chorale Elayo  
- Chorale Bonheur  
- Goshen Choir/Kabagari
""")
    st.write("""
Ibyuma n’umushinga w’umuziki:
- 06/2023: Umushinga wo kugura ibyuma by’umuziki bwite warangiye  
- 16/03/2024: Tubonye Guitar Bass yacu bwite  
- 01/04/2024: Twaguze ibyuma byose by’umuziki
""")
    st.write("📅 14/03/2024: Urugendo rwa mbere rw’ivugabutumwa mu itorero rya Kacyiru, Umudugudu wa Kabagari")
    st.write("""
Umubare w’abaririmbyi ubu:
- Abagabo: 13  
- Abagore: 9  
- Abasore: 15  
- Abakobwa: 28  
- Abandi 7 bari mu igeragezwa
""")
    st.markdown("[▶️ Reba indirimbo zacu kuri YouTube](https://www.youtube.com/channel/YOUR_CHANNEL_LINK_HERE)")

# ----------------- MEMBERS PAGE -----------------
elif menu == "Abaririmbyi":
    st.header("👥 Abaririmbyi")
    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w’Abaririmbyi: {len(df)}")
    except:
        st.warning("Nta baririmbyi babonetse. Ongera ushyiremo ababaririmbyi.")

# ----------------- ATTENDANCE PAGE -----------------
elif menu == "Attendance":
    st.header("📋 Gushyira mu Attendance")
    
    day = st.selectbox("📅 Hitamo Umunsi w’Imyitozo", ["Wednesday", "Saturday", "Sunday"])
    
    try:
        members = pd.read_csv("members.csv")
        if members.empty:
            st.warning("⚠️ Urutonde rw’Abaririmbyi ntirubonetse.")
        else:
            st.subheader("Shyira Attendance")
            attendance_list = []
            total_members = len(members)
            present_count = 0
            absent_count = 0
            today = datetime.now()
            current_month = today.month
            date_str = today.strftime("%Y-%m-%d %H:%M:%S")
            
            try:
                old_attendance = pd.read_csv("attendance.csv")
            except FileNotFoundError:
                old_attendance = pd.DataFrame(columns=["Name","Day","Status","Date"])
            
            for i, row in members.iterrows():
                member_name = row["Name"]
                
                absent_this_month = old_attendance[
                    (old_attendance["Name"]==member_name) &
                    (pd.to_datetime(old_attendance["Date"], errors='coerce').dt.month == current_month) &
                    (old_attendance["Status"]=="Absent")
                ].shape[0]
                
                if absent_this_month >= 3:
                    st.write(f"🚫 {member_name} - Ntibemerewe kuririmba (Absent ≥3 uyu kwezi)")
                    continue
                
                col1, col2 = st.columns([3,2])
                with col1:
                    st.write("👤", member_name)
                with col2:
                    status = st.radio("Status", ["Present","Absent"], key=i, horizontal=True)
                
                if status=="Present":
                    present_count += 1
                else:
                    absent_count += 1
                
                attendance_list.append({
                    "Name": member_name,
                    "Day": day,
                    "Status": status,
                    "Date": date_str
                })
            
            st.divider()
            col1, col2, col3 = st.columns(3)
            col1.metric("Abaririmbyi bose", total_members)
            col2.metric("Bari Present", present_count)
            col3.metric("Bari Absent", absent_count)
            
            if st.button("💾 Save Attendance"):
                new_data = pd.DataFrame(attendance_list)
                data = pd.concat([old_attendance, new_data], ignore_index=True)
                data.to_csv("attendance.csv", index=False)
                st.success("✅ Attendance yabitswe neza!")
                
    except FileNotFoundError:
        st.warning("⚠️ members.csv ntiyabonetse. Ongera ushyiremo.")

# ----------------- CONTRIBUTION PAGE -----------------
elif menu == "Umusanzu":
    st.header("💰 Umusanzu (Contribution)")
    name = st.text_input("Izina ry’Umuririmbyi")
    contribution_name = st.text_input("Izina ry’Umusanzu (Urugero: Impuzankano, Guitar)")
    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )
    amount = st.number_input("Amafaranga", min_value=0)
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d %H:%M:%S")
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

# ----------------- RAPORO YA ATTENDANCE -----------------
elif menu == "Raporo Attendance":
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors='coerce')
            
            day_filter = st.selectbox("Hitamo Umunsi w’Imyitozo", ["All","Wednesday","Saturday","Sunday"])
            month_filter = st.selectbox(
                "Hitamo Ukwezi", 
                ["All","January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
            date_filter = st.date_input("Hitamo Itariki (optionnel)", value=None)
            
            filtered = attendance.copy()
            
            if day_filter != "All":
                filtered = filtered[filtered["Day"] == day_filter]
            
            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month == month_number]
            
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date == date_filter]
            
            if filtered.empty:
                st.warning("Nta attendance yabonetse kuri aya ma filters.")
            else:
                attendance_summary = filtered.groupby(["Name","Status"]).size().unstack(fill_value=0)
                st.subheader("Attendance Summary")
                st.dataframe(attendance_summary)
                
                # Abataremerewe kuririmba
                current_month = datetime.now().month
                absent_counts = attendance[
                    (attendance["Date"].dt.month == current_month) &
                    (attendance["Status"]=="Absent")
                ].groupby("Name").size()
                not_allowed = absent_counts[absent_counts >= 3]
                if not_allowed.empty:
                    st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
                else:
                    st.warning("🚫 Abataremerewe kuririmba uyu kwezi:")
                    st.dataframe(not_allowed)
    except FileNotFoundError:
        st.warning("Nta data ya attendance yabonetse.")

# ----------------- RAPORO YA UMUSANZU -----------------
elif menu == "Raporo Umusanzu":
    st.header("📊 Raporo y’Umusanzu")
    try:
        contribution = pd.read_csv("contribution.csv")
        if contribution.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            contribution["Date"] = pd.to_datetime(contribution["Date"], errors='coerce')
            
            month_filter = st.selectbox(
                "Hitamo Ukwezi", 
                ["All","January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
            date_filter = st.date_input("Hitamo Itariki (optionnel)", value=None)
            
            filtered = contribution.copy()
            
            if month_filter != "All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].dt.month == month_number]
            
            if date_filter:
                filtered = filtered[filtered["Date"].dt.date == date_filter]
            
            if filtered.empty:
                st.warning("Nta musanzu wabonetse kuri aya ma filters.")
            else:
                st.subheader("Umusanzu Wabonetse")
                st.dataframe(filtered)
    except FileNotFoundError:
        st.warning("Nta data y’umusanzu yabonetse.")