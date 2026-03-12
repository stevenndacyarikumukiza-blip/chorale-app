import streamlit as st
import pandas as pd
from datetime import datetime, date

# ---------------- PAGE SETUP ----------------
st.set_page_config(page_title="Chorale Inshuti za Yesu", layout="wide")
st.title("🎵 CHORALE INSHUTI ZA YESU")

tabs = [
"Ahabanza",
"Abaririmbyi",
"Attendance",
"Umusanzu",
"Raporo Attendance",
"Raporo Umusanzu",
"Abataremerewe kuririmba"
]

selected_tab = st.tabs(tabs)

# ---------------- HOME ----------------
with selected_tab[0]:

    st.header("Murakaza neza muri Chorale Inshuti za Yesu")

    st.write("Iminsi y’imyitozo:")
    st.write("• Wednesday")
    st.write("• Saturday")
    st.write("• Sunday")

    st.divider()

    st.subheader("📖 Amateka ya Chorale")

    st.write("""
Chorale Inshuti za Yesu ni chorale ikorera umurimo w’Imana
mu itorero rya ADEPR Kinyinya.

Yatangiriye mu 2021 igizwe n’abaririmbyi 35.

Abari bagize chorale:
- Abagabo: 5
- Abagore: 5
- Abasore: 10
- Abakobwa: 15
""")

    st.write("""
Ibikorwa by’ingenzi:
• Giterane cya mbere
• YouTube channel
• Indirimbo "Ikinyita"
• Umubano n’izindi chorale
• Kugura ibyuma by’umuziki
""")

# ---------------- MEMBERS ----------------
with selected_tab[1]:

    st.header("👥 Abaririmbyi")

    try:
        df = pd.read_csv("members.csv")
        st.dataframe(df)
        st.info(f"Umubare w'Abaririmbyi: {len(df)}")

    except:
        st.warning("members.csv ntiyabonetse.")

# ---------------- ATTENDANCE ----------------
with selected_tab[2]:

    st.header("📋 Shyira Attendance")

    day = st.selectbox(
        "Hitamo Umunsi",
        ["Wednesday","Saturday","Sunday"]
    )

    selected_date = st.date_input(
        "Hitamo Itariki",
        value=date.today()
    )

    date_str = selected_date.strftime("%Y-%m-%d")

    try:

        members = pd.read_csv("members.csv")

        try:
            old = pd.read_csv("attendance.csv")
        except:
            old = pd.DataFrame(columns=["Name","Day","Status","Date"])

        attendance_list = []

        present=0
        absent=0
        uruhushya=0

        for i,row in members.iterrows():

            name=row["Name"]

            col1,col2=st.columns([3,3])

            with col1:
                st.write(name)

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

        col1,col2,col3,col4 = st.columns(4)

        col1.metric("Abaririmbyi bose",len(members))
        col2.metric("Present",present)
        col3.metric("Absent",absent)
        col4.metric("Uruhushya",uruhushya)

        if st.button("💾 Save Attendance"):

            new=pd.DataFrame(attendance_list)

            data=pd.concat([old,new],ignore_index=True)

            data.to_csv("attendance.csv",index=False)

            st.success("Attendance yabitswe neza!")

    except:
        st.warning("members.csv ntiyabonetse.")

# ---------------- CONTRIBUTION ----------------
with selected_tab[3]:

    st.header("💰 Umusanzu")

    name = st.text_input("Izina")

    contribution = st.text_input("Izina ry'umusanzu")

    month = st.selectbox(
        "Ukwezi",
        ["January","February","March","April","May","June",
         "July","August","September","October","November","December"]
    )

    amount = st.number_input("Amafaranga",min_value=0)

    date_now = datetime.now()

    if st.button("💾 Save Umusanzu"):

        new=pd.DataFrame({
            "Name":[name],
            "Contribution":[contribution],
            "Month":[month],
            "Amount":[amount],
            "Date":[date_now]
        })

        try:
            old=pd.read_csv("contribution.csv")
            new=pd.concat([old,new],ignore_index=True)
        except:
            pass

        new.to_csv("contribution.csv",index=False)

        st.success("Umusanzu wabitswe neza!")

# ---------------- RAPORO ATTENDANCE ----------------
with selected_tab[4]:

    st.header("📊 Raporo ya Attendance")

    try:

        df=pd.read_csv("attendance.csv")

        df["Date"]=pd.to_datetime(df["Date"])

        chosen_date = st.date_input(
            "Hitamo Itariki",
            value=date.today()
        )

        filtered=df[df["Date"].dt.date==chosen_date]

        st.subheader("Attendance kuri iyi tariki")

        st.dataframe(filtered)

        st.subheader("Summary y'ukwezi")

        month=chosen_date.month

        monthly=df[df["Date"].dt.month==month]

        summary=monthly.groupby("Status").size()

        st.write(summary)

    except:
        st.warning("attendance.csv ntiyabonetse.")

# ---------------- RAPORO CONTRIBUTION ----------------
with selected_tab[5]:

    st.header("📊 Raporo y'Umusanzu")

    try:

        df=pd.read_csv("contribution.csv")

        df["Date"]=pd.to_datetime(df["Date"],errors="coerce")

        contribution_filter = st.selectbox(
            "Hitamo Izina ry'Umusanzu",
            ["All"]+df["Contribution"].dropna().unique().tolist()
        )

        month_filter = st.selectbox(
            "Hitamo Ukwezi",
            ["All","January","February","March","April","May","June",
             "July","August","September","October","November","December"]
        )

        filtered=df.copy()

        if contribution_filter!="All":
            filtered=filtered[filtered["Contribution"]==contribution_filter]

        if month_filter!="All":

            month_number=[
            "January","February","March","April","May","June",
            "July","August","September","October","November","December"
            ].index(month_filter)+1

            filtered=filtered[filtered["Date"].dt.month==month_number]

        st.subheader("Umusanzu Wabonetse")

        st.dataframe(filtered)

        total=filtered["Amount"].sum()

        st.metric("Umusanzu wose",total)

    except:
        st.warning("contribution.csv ntiyabonetse.")

# ---------------- ABATAREMEWE KURIRIMBA ----------------
with selected_tab[6]:

    st.header("🚫 Abataremerewe kuririmba")

    try:

        df=pd.read_csv("attendance.csv")

        df["Date"]=pd.to_datetime(df["Date"])

        month=datetime.now().month

        absent=df[
            (df["Date"].dt.month==month) &
            (df["Status"]=="Absent")
        ]

        counts=absent.groupby("Name").size()

        banned=counts[counts>=3]

        if banned.empty:
            st.success("Nta baririmbyi bafite absent ≥3 uyu kwezi.")
        else:
            st.dataframe(banned)

    except:
        st.warning("attendance.csv ntiyabonetse.")
