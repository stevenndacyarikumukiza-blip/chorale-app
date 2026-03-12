import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Chorale System", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>

.stApp {
background-image: url("https://images.unsplash.com/photo-1507838153414-b4b713384a76");
background-size: cover;
background-attachment: fixed;
}

html, body, [class*="css"]  {
font-family: 'Poppins', sans-serif;
}

h1 {
color: gold;
text-align:center;
}

</style>
""", unsafe_allow_html=True)

st.title("🎵 CHORALE INSHUTI ZA YESU SYSTEM")

tabs = st.tabs([
"🏠 Ahabanza",
"👥 Abaririmbyi",
"📋 Attendance",
"💰 Umusanzu",
"📊 Raporo Attendance",
"📊 Raporo Umusanzu"
])

# ---------- HOME ----------
with tabs[0]:

    st.header("Murakaza neza")

    st.write("Iminsi y’imyitozo:")
    st.write("• Wednesday")
    st.write("• Saturday")
    st.write("• Sunday")

    st.divider()

    st.header("📖 Amateka ya Chorale")

    st.write("""
Chorale Inshuti za Yesu yatangiye 2021.

Yatangiranye n’abaririmbyi 35.

Abagabo: 5  
Abagore: 5  
Abasore: 10  
Abakobwa: 15
""")

    st.write("""
2022 Chorale yagize ibikorwa byinshi birimo igiterane cya mbere
twatumiye Chorale Seeking for Jesus.
""")

    st.write("""
YouTube channel:
Inshuti za Yesu Choir Kinyinya
""")

    st.write("""
Indirimbo:
Ikinyita
""")

# ---------- MEMBERS ----------
with tabs[1]:

    st.header("👥 Abaririmbyi")

    try:

        members = pd.read_csv("members.csv")

        search = st.text_input("🔍 Shakisha umuririmbyi")

        if search:
            members = members[members["Name"].str.contains(search, case=False)]

        st.dataframe(members)

        st.info(f"Umubare w'abantu: {len(members)}")

    except:

        st.warning("members.csv ntiyabonetse")

# ---------- ATTENDANCE ----------
with tabs[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
    "Hitamo Umunsi",
    ["Wednesday","Saturday","Sunday"]
    )

    try:

        members = pd.read_csv("members.csv")

        present = 0
        absent = 0
        uruhushya = 0

        attendance_list = []

        today = datetime.now()
        current_month = today.month
        date_str = today.strftime("%Y-%m-%d %H:%M:%S")

        try:
            old = pd.read_csv("attendance.csv")
        except:
            old = pd.DataFrame(columns=["Name","Day","Status","Date"])

        for i,row in members.iterrows():

            name = row["Name"]

            absent_month = old[
            (old["Name"]==name) &
            (pd.to_datetime(old["Date"], errors="coerce").dt.month==current_month) &
            (old["Status"]=="Absent")
            ].shape[0]

            if absent_month >=3:

                st.write(f"🚫 {name} ntaririmba (Absent ≥3)")
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
                present+=1
            elif status=="Absent":
                absent+=1
            else:
                uruhushya+=1

            attendance_list.append({
            "Name":name,
            "Day":day,
            "Status":status,
            "Date":date_str
            })

        st.divider()

        c1,c2,c3,c4 = st.columns(4)

        c1.metric("Abaririmbyi bose",len(members))
        c2.metric("Present",present)
        c3.metric("Absent",absent)
        c4.metric("Uruhushya",uruhushya)

        if st.button("Save Attendance"):

            new = pd.DataFrame(attendance_list)

            data = pd.concat([old,new],ignore_index=True)

            data.to_csv("attendance.csv",index=False)

            st.success("Attendance saved")

    except:

        st.warning("members.csv ntiyabonetse")

# ---------- CONTRIBUTION ----------
with tabs[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")

    contribution_name = st.text_input("Izina ry'umusanzu")

    month = st.selectbox(
    "Ukwezi",
    ["January","February","March","April","May","June","July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga",0)

    if st.button("Save Contribution"):

        date = datetime.now().strftime("%Y-%m-%d")

        new = pd.DataFrame({
        "Name":[name],
        "Contribution":[contribution_name],
        "Month":[month],
        "Amount":[amount],
        "Date":[date]
        })

        try:
            old = pd.read_csv("contribution.csv")
            new = pd.concat([old,new],ignore_index=True)
        except:
            pass

        new.to_csv("contribution.csv",index=False)

        st.success("Umusanzu saved")

# ---------- REPORT ATTENDANCE ----------
with tabs[4]:

    st.header("📊 Raporo Attendance")

    try:

        attendance = pd.read_csv("attendance.csv")

        attendance["Date"] = pd.to_datetime(attendance["Date"],errors="coerce")

        month = st.selectbox(
        "Ukwezi",
        ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        )

        day = st.selectbox(
        "Umunsi",
        ["All","Wednesday","Saturday","Sunday"]
        )

        date = st.date_input("Itariki")

        filtered = attendance.copy()

        if month!="All":

            month_number = [
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
            ].index(month)+1

            filtered = filtered[filtered["Date"].dt.month==month_number]

        if day!="All":
            filtered = filtered[filtered["Day"]==day]

        filtered = filtered[filtered["Date"].dt.date==date]

        st.dataframe(filtered)

        csv = filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
        "⬇️ Download Report",
        csv,
        "attendance_report.csv",
        "text/csv"
        )

    except:

        st.warning("attendance.csv ntiyabonetse")

# ---------- REPORT CONTRIBUTION ----------
with tabs[5]:

    st.header("📊 Raporo Umusanzu")

    try:

        df = pd.read_csv("contribution.csv")

        month = st.selectbox(
        "Ukwezi",
        ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        )

        name = st.text_input("Izina ry'umusanzu")

        filtered = df.copy()

        if month!="All":
            filtered = filtered[filtered["Month"]==month]

        if name:
            filtered = filtered[filtered["Contribution"]==name]

        st.dataframe(filtered)

        csv = filtered.to_csv(index=False).encode("utf-8")

        st.download_button(
        "⬇️ Download Report",
        csv,
        "contribution_report.csv",
        "text/csv"
        )

    except:

        st.warning("contribution.csv ntiyabonetse")
