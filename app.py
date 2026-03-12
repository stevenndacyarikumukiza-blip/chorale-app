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

# ----------------- HOME PAGE -----------------
if page == "Ahabanza":
    st.header("Murakaza neza muri Chorale Inshuti za Yesu")
    st.write("Iminsi y’imyitozo: Ku wa Gatatu, Ku wa Gatandatu, Ku Cyumweru")
    st.divider()
    st.write("""
    Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana mu itorero rya ADEPR Kinyinya, Paruwasi.
    Yatangiriye mu mwaka wa 2021...
    """)
    
# ----------------- MEMBERS PAGE -----------------
elif page == "Abaririmbyi":
    st.header("👥 Abaririmbyi")
    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")
    except:
        st.warning("members.csv ntiyabonetse.")

# ----------------- ATTENDANCE PAGE -----------------
elif page == "Attendance":
    st.header("📋 Shyira Attendance")
    
    # Hitamo Ukwezi, Umunsi, Itariki
    month = st.selectbox("📅 Hitamo Ukwezi", 
        ["January","February","March","April","May","June","July","August","September","October","November","December"])
    day = st.selectbox("📆 Hitamo Umunsi", ["Wednesday","Saturday","Sunday"])
    date_input = st.date_input("📌 Hitamo Itariki", value=datetime.today())

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

            for i, row in members.iterrows():
                name = row["Name"]
                
                absent_this_month = old[
                    (old["Name"]==name) &
                    (pd.to_datetime(old["Date"], errors="coerce").dt.month == datetime.strptime(month,"%B").month) &
                    (old["Status"]=="Absent")
                ].shape[0]

                if absent_this_month >= 3:
                    st.write(f"🚫 {name} - Ntibemerewe kuririmba (Absent ≥3 uyu kwezi)")
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

# ----------------- CONTRIBUTION PAGE -----------------
elif page == "Umusanzu":
    st.header("💰 Umusanzu")
    name = st.text_input("Izina ry’Umuririmbyi")
    contribution_name = st.text_input("Izina ry’Umusanzu (Urugero: Impuzankano)")
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
            new = pd.concat([old,new], ignore_index=True)
        except:
            pass
        new.to_csv("contribution.csv", index=False)
        st.success("✅ Umusanzu wabitswe neza!")

# ----------------- RAPORO ATTENDANCE -----------------
elif page == "Raporo Attendance":
    st.header("📊 Raporo ya Attendance")
    try:
        attendance = pd.read_csv("attendance.csv")
        if attendance.empty:
            st.info("Nta data ya attendance yabonetse.")
        else:
            attendance["Date"] = pd.to_datetime(attendance["Date"], errors="coerce")
            
            month_filter = st.selectbox(
                "Hitamo Ukwezi",
                ["All","January","February","March","April","May","June",
                 "July","August","September","October","November","December"]
            )
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

            st.subheader("Attendance y'ahantu wahisemo")
            st.dataframe(filtered)

            summary = filtered.groupby("Status").size()
            st.subheader("Summary")
            st.write(summary)

            # Abataremerewe kuririmba
            current_month = datetime.now().month
            absent_counts = attendance[
                (attendance["Date"].dt.month==current_month) &
                (attendance["Status"]=="Absent")
            ].groupby("Name").size()
            not_allowed = absent_counts[absent_counts>=3]
            if not not_allowed.empty:
                st.warning("🚫 Abataremerewe kuririmba uyu kwezi:")
                st.dataframe(not_allowed)

    except:
        st.warning("attendance.csv ntiyabonetse.")

# ----------------- RAPORO UMUSANZU -----------------
elif page == "Raporo Umusanzu":
    st.header("📊 Raporo y'Umusanzu")
    try:
        df = pd.read_csv("contribution.csv")
        if df.empty:
            st.info("Nta musanzu wabonetse.")
        else:
            df["Contribution"] = df["Contribution"].fillna("Other")
            month_filter = st.selectbox("Hitamo Ukwezi", ["All","January","February","March","April","May","June",
                                                         "July","August","September","October","November","December"])
            contribution_filter = st.selectbox("Hitamo Umusanzu", ["All"] + df["Contribution"].unique().tolist())

            filtered = df.copy()
            if month_filter!="All":
                month_number = ["January","February","March","April","May","June",
                                "July","August","September","October","November","December"].index(month_filter)+1
                filtered = filtered[filtered["Date"].apply(lambda x: pd.to_datetime(x, errors="coerce").month)==month_number]
            if contribution_filter!="All":
                filtered = filtered[filtered["Contribution"]==contribution_filter]

            st.subheader("Umusanzu wabonetse")
            st.dataframe(filtered)
            st.metric("Umusanzu wose", filtered["Amount"].sum())
    except:
        st.warning("contribution.csv ntiyabonetse.")
