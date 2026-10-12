import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(page_title="Mental Health Progress Tracker", layout="wide")

st.title("Mental Health Progress Tracker")
st.caption("Clinician dashboard for tracking mood, anxiety, sleep, and energy over time")

if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "date", "mood", "anxiety", "sleep_hours", "energy", "notes"
    ])

st.sidebar.header("Log a New Entry")
with st.sidebar.form("entry_form"):
    entry_date = st.date_input("Date", value=date.today())
    mood = st.slider("Mood (1 = very low, 10 = excellent)", 1, 10, 5)
    anxiety = st.slider("Anxiety (1 = minimal, 10 = severe)", 1, 10, 5)
    sleep = st.number_input("Sleep hours", min_value=0.0, max_value=24.0, value=7.0, step=0.5)
    energy = st.slider("Energy level (1–10)", 1, 10, 5)
    notes = st.text_area("Clinical notes / observations")
    submitted = st.form_submit_button("Add Entry")

    if submitted:
        new_row = pd.DataFrame([{
            "date": entry_date,
            "mood": mood,
            "anxiety": anxiety,
            "sleep_hours": sleep,
            "energy": energy,
            "notes": notes
        }])
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
        st.sidebar.success("Entry added!")

if st.sidebar.button("Load sample data (for demo)"):
    sample = pd.DataFrame({
        "date": pd.date_range(end=date.today(), periods=14, freq="D"),
        "mood": [4,5,6,5,7,6,8,7,6,7,8,9,7,8],
        "anxiety": [7,6,5,6,4,5,3,4,5,4,3,2,4,3],
        "sleep_hours": [5.5,6,7,6.5,8,7.5,8,7,6,7.5,8,8.5,7,7.5],
        "energy": [3,4,5,4,6,5,7,6,5,6,7,8,6,7],
        "notes": [""] * 14
    })
    st.session_state.data = sample
    st.sidebar.success("Sample data loaded")

if st.session_state.data.empty:
    st.info("No data yet. Use the sidebar to add an entry or load sample data.")
else:
    df = st.session_state.data.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Avg Mood", f"{df['mood'].mean():.1f}")
    col2.metric("Avg Anxiety", f"{df['anxiety'].mean():.1f}")
    col3.metric("Avg Sleep (hrs)", f"{df['sleep_hours'].mean():.1f}")
    col4.metric("Entries", len(df))

    st.subheader("Trends Over Time")
    fig = px.line(df, x="date", y=["mood", "anxiety", "energy"],
                  markers=True, title="Mood, Anxiety & Energy")
    fig.update_layout(yaxis_title="Score (1–10)", legend_title="Metric")
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(df, x="date", y="sleep_hours", markers=True, title="Sleep Hours")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Recent Entries & Notes")
    st.dataframe(df.sort_values("date", ascending=False).reset_index(drop=True),
                 use_container_width=True)

    if len(df) >= 3:
        recent_mood = df["mood"].tail(3).mean()
        earlier_mood = df["mood"].head(3).mean() if len(df) > 3 else df["mood"].mean()
        if recent_mood > earlier_mood + 0.5:
            st.success("Positive trend: recent mood scores are higher than earlier ones.")
        elif recent_mood < earlier_mood - 0.5:
            st.warning("Recent mood scores are lower — consider reviewing interventions.")
        else:
            st.info("Mood scores are relatively stable.")

st.markdown("---")
st.caption("Demo tool for educational / portfolio use. Not a substitute for clinical assessment.")