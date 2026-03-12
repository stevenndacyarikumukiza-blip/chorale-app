import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")

st.title("🎵 CHORALE INSHUTI ZA YESU")

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

    st.divider()

    st.header("📖 Amateka ya Chorale")

    st.write("""
Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya Paruwasi.

Yatangiriye mu mwaka wa 2021 mu kwezi kwa mbere aho abaririmbyi 35 bahuriraga hamwe na worship team yaho.

Abari bagize chorale icyo gihe:

Abagabo: 5  
Abagore: 5  
Abasore: 10  
Abakobwa: 15
""")

    st.write("""
Mu mwaka wa 2022 chorale yaguze impuzankano (uniform) ya mbere kandi yatangiye gukora umurimo
wo kuramya no guhimbaza Imana mu bitaramo n’iteraniro.
""")

    st.write("""
Ibikorwa by’ingenzi bya Chorale:

12/2022: Igiterane cya mbere twatumiye Chorale Seeking for Jesus

Nyuma y’icyo giterane twafunguye YouTube Channel yitwa:
"Inshuti za Yesu Choir Kinyinya"

Ubu dufite indirimbo imwe yitwa "Ikinyita".
""")

    st.write("""
Umubano n’izindi chorale:

Chorale Seeking for Jesus  
Chorale Abatwaramucyo  
Chorale Future  
Chorale Ebenezer  
Chorale Elayo  
Chorale Bonheur  
Goshen Choir Kabagari
""")

    st.write("""
Ibyuma by’umuziki:

06/2023: Umushinga wo kugura ibyuma by’umuziki warangiye

16/03/2024: Chorale yabonye Guitar Bass yayo bwite

01/04/2024: Chorale yaguze ibyuma byose by’umuziki
""")

    st.write("14/03/2024: Urugendo rwa mbere rw’ivugabutumwa rwabereye Kacyiru Kabagari.")

# ---------------- MEMBERS ----------------
with tabs[1]:

    st.header("👥 Abaririmbyi")

    try:
        members = pd.read_csv("members.csv")

        st.dataframe(members)

        st.info(f"Umubare w'Abaririmbyi: {len(members)}")

    except:
        st.warning("Nta baririmbyi babonetse.")

# ---------------- ATTENDANCE ----------------
with tabs[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
        "Hitamo Umunsi w'Imyitozo",
        ["Wednesday","Saturday","Sunday"]
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

            c1,c2,c3,c4 = st.columns(4)

            c1.metric("Abaririmbyi bose", total_members)
            c2.metric("Bari Present (Bitabiriye)", present_count)
            c3.metric("Bari Absent (Basibye)", absent_count)
            c4.metric("Basabye Uruhushya", uruhushya_count)

            if st.button("Save Attendance"):

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

    contribution_name = st.text_input("Izina ry'umusanzu (Urugero: Impuzankano)")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June","July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga", min_value=0)

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Save Umusanzu"):

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

# ---------------- RAPORO ATTENDANCE ----------------
with tabs[4]:

    st.header("📊 Raporo ya Attendance")

    try:

        attendance = pd.read_csv("attendance.csv")

        attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")

        month = st.selectbox(
            "Hitamo Ukwezi",
            ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        )

        day = st.selectbox(
            "Hitamo Umunsi",
            ["All","Wednesday","Saturday","Sunday"]
        )

        date_filter = st.date_input("Hitamo Itariki")

        filtered = attendance.copy()

        if month != "All":
            month_number = ["January","February","March","April","May","June","July","August","September","October","November","December"].index(month)+1
            filtered = filtered[filtered["Date"].dt.month == month_number]

        if day != "All":
            filtered = filtered[filtered["Day"] == day]

        filtered = filtered[filtered["Date"].dt.date == date_filter]

        st.dataframe(filtered)

    except:
        st.warning("attendance.csv ntiyabonetse")

# ---------------- RAPORO UMUSANZU ----------------
with tabs[5]:

    st.header("📊 Raporo y'Umusanzu")

    try:

        df = pd.read_csv("contribution.csv")

        month = st.selectbox(
            "Hitamo Ukwezi",
            ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        )

        contribution_name = st.text_input("Izina ry'umusanzu ushaka kureba")

        filtered = df.copy()

        if month != "All":
            filtered = filtered[filtered["Month"] == month]

        if contribution_name:
            filtered = filtered[filtered["Contribution"] == contribution_name]

        st.dataframe(filtered)

    except:
        st.warning("contribution.csv ntiyabonetse")
