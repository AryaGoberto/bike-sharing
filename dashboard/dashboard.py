import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Bike Sharing Dashboard", layout="centered")
parent_dir = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
	hour_data = pd.read_csv("./hour.csv")
	day_data = pd.read_csv("./day.csv")
	return hour_data, day_data


hour_df, day_df = load_data()

st.title("🚲 Bike Sharing Dashboard")

st.subheader("1) Rata-rata Penggunaan Sepeda per Jam")
hourly_usage = hour_df.groupby("hr")["cnt"].mean()
fig1, ax1 = plt.subplots(figsize=(7, 4))
sns.lineplot(x=hourly_usage.index, y=hourly_usage.values, ax=ax1)
ax1.set_title("Rata-rata Penggunaan Sepeda per Jam")
ax1.set_xlabel("Jam")
ax1.set_ylabel("Rata-rata Pengguna")
st.pyplot(fig1, use_container_width=False)

st.subheader("2) Perbandingan Penggunaan: Hari Kerja vs Libur")
day_usage = hour_df.groupby("workingday")["cnt"].mean()
fig2, ax2 = plt.subplots(figsize=(6, 4))
sns.barplot(x=day_usage.index, y=day_usage.values, ax=ax2)
ax2.set_xticks([0, 1])
ax2.set_xticklabels(["Libur", "Hari Kerja"])
ax2.set_title("Perbandingan Penggunaan: Hari Kerja vs Libur")
ax2.set_xlabel("workingday")
ax2.set_ylabel("Rata-rata Pengguna")
st.pyplot(fig2, use_container_width=False)

st.subheader("3) Pengaruh Cuaca terhadap Penggunaan Sepeda")
weather_map = {
	1: "Cerah / sebagian berawan",
	2: "Berkabut / mendung",
	3: "Hujan ringan / salju ringan",
	4: "Hujan lebat / cuaca buruk",
}
weather_usage = hour_df.groupby("weathersit")["cnt"].mean().reindex([1, 2, 3, 4])
weather_labels = [weather_map[i] for i in weather_usage.index]
fig3, ax3 = plt.subplots(figsize=(7, 4))
sns.barplot(x=weather_labels, y=weather_usage.values, ax=ax3)
ax3.set_title("Pengaruh Cuaca terhadap Penggunaan Sepeda")
ax3.set_xlabel("Kondisi Cuaca")
ax3.set_ylabel("Rata-rata Pengguna")
ax3.tick_params(axis="x", rotation=15)
plt.tight_layout()
st.pyplot(fig3, use_container_width=False)

st.subheader("4) Perbandingan Casual vs Registered")
user_type = hour_df[["casual", "registered"]].mean()
fig4, ax4 = plt.subplots(figsize=(6, 4))
user_type.plot(kind="bar", ax=ax4)
ax4.set_title("Perbandingan Casual vs Registered")
ax4.set_ylabel("Rata-rata Pengguna")
ax4.set_xlabel("")
st.pyplot(fig4, use_container_width=False)