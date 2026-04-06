import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
current_dir = os.path.dirname(os.path.abspath(__file__))


@st.cache_data
def load_data():
	hour_path = os.path.join(current_dir, "hour.csv")
	day_path = os.path.join(current_dir, "day.csv")
	hour_data = pd.read_csv(hour_path, parse_dates=["dteday"])
	day_data = pd.read_csv(day_path, parse_dates=["dteday"])

	return hour_data, day_data


hour_df, day_df = load_data()

min_date = hour_df["dteday"].min().date()
max_date = hour_df["dteday"].max().date()

st.title("Bike Sharing Dashboard")
st.caption("Analisis fokus pada periode 2011-2012 dan dapat dipersempit lewat filter tanggal di sidebar.")

st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input(
	"Rentang tanggal",
	value=(min_date, max_date),
	min_value=min_date,
	max_value=max_date,
)

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
	start_date, end_date = date_range
else:
	start_date = end_date = date_range

start_ts = pd.Timestamp(start_date)
end_ts = pd.Timestamp(end_date)

filtered_hour_df = hour_df.loc[
	(hour_df["dteday"] >= start_ts) & (hour_df["dteday"] <= end_ts)
].copy()

filtered_day_df = day_df.loc[
	(day_df["dteday"] >= start_ts) & (day_df["dteday"] <= end_ts)
].copy()

if filtered_hour_df.empty:
	st.warning("Tidak ada data pada rentang tanggal yang dipilih.")
	st.stop()

metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("Total penyewaan", f"{int(filtered_hour_df['cnt'].sum()):,}")
metric_col2.metric("Rata-rata per jam", f"{filtered_hour_df['cnt'].mean():.1f}")
metric_col3.metric("Hari teramati", f"{filtered_day_df['dteday'].nunique():,}")

st.divider()

st.subheader("1) Pola rata-rata penggunaan sepeda per jam")
hourly_usage = filtered_hour_df.groupby("hr")["cnt"].mean().reindex(range(24))
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(x=hourly_usage.index, y=hourly_usage.values, ax=ax1, marker="o")
ax1.set_title("Rata-rata penggunaan sepeda per jam")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata pengguna")
ax1.set_xticks(range(0, 24, 2))
st.pyplot(fig1, use_container_width=True)

st.subheader("2) Hari kerja vs hari libur")
day_usage = filtered_hour_df.groupby("workingday")["cnt"].mean().reindex([0, 1])
fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x=day_usage.index, y=day_usage.values, ax=ax2, palette="Blues_r")
ax2.set_xticks([0, 1])
ax2.set_xticklabels(["Libur", "Hari Kerja"])
ax2.set_title("Perbandingan penggunaan: hari kerja vs hari libur")
ax2.set_xlabel("")
ax2.set_ylabel("Rata-rata pengguna")
st.pyplot(fig2, use_container_width=True)

st.subheader("3) Pengaruh cuaca terhadap penyewaan")
weather_map = {
	1: "Cerah / sebagian berawan",
	2: "Berkabut / mendung",
	3: "Hujan ringan / salju ringan",
	4: "Hujan lebat / cuaca buruk",
}
weather_usage = filtered_hour_df.groupby("weathersit")["cnt"].mean().reindex([1, 2, 3, 4])
weather_labels = [weather_map[i] for i in weather_usage.index]
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.barplot(x=weather_labels, y=weather_usage.values, ax=ax3, palette="Greens_d")
ax3.set_title("Pengaruh cuaca terhadap penggunaan sepeda")
ax3.set_xlabel("Kondisi cuaca")
ax3.set_ylabel("Rata-rata pengguna")
ax3.tick_params(axis="x", rotation=15)
plt.tight_layout()
st.pyplot(fig3, use_container_width=True)