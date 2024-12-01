import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

##day_df = pd.read_csv(r"D:\Dashboard Dicoding\day.csv")
##hour_df = pd.read_csv(r"D:\Dashboard Dicoding\hour.csv")

days_df = pd.read_csv("day.csv")
hours_df = pd.read_csv("hour.csv")



def get_total_count_by_hour_df(hour_df):
  hour_count_df =  hour_df.groupby(by="hr").agg({"cnt": ["sum"]})
  return hour_count_df

def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query(str('dteday >= "2011-01-01" and dteday < "2012-12-31"'))
    return day_df_count_2011

def total_registered_df(day_df):
   reg_df =  day_df.groupby(by="dteday").agg({
      "registered": "sum"
    })
   reg_df = reg_df.reset_index()
   reg_df.rename(columns={
        "registered": "register_sum"
    }, inplace=True)
   return reg_df

def total_casual_df(day_df):
   cas_df =  day_df.groupby(by="dteday").agg({
      "casual": ["sum"]
    })
   cas_df = cas_df.reset_index()
   cas_df.rename(columns={
        "casual": "casual_sum"
    }, inplace=True)
   return cas_df

def sum_order (hour_df):
    sum_order_items_df = hour_df.groupby("hr").cnt.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df

def jenis_season (day_df): 
    season_df = day_df.groupby(by="season").cnt.sum().reset_index() 
    return season_df

# Menghitung Humidity
days_df['hum'] = days_df['hum']*100
hours_df['hum'] = hours_df['hum']*100

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)   

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    
        # Mengambil start_date & end_date dari date_input
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=(min_date_days, max_date_days)  # Default value adalah rentang penuh
    )

    # Validasi apakah date_range adalah tuple dengan dua elemen
    if not isinstance(date_range, tuple) or len(date_range) != 2:
        st.error("Mohon diisi tanggal start & end-nya.")
    else:
        start_date, end_date = date_range
        if start_date > end_date:
            st.error("Start Date tidak boleh lebih besar dari End Date")
        else:
            # Filter DataFrame jika input valid
            main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) & 
                                   (days_df["dteday"] <= pd.to_datetime(end_date))]
            main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) & 
                                    (hours_df["dteday"] <= pd.to_datetime(end_date))]

            # Validasi jika DataFrame kosong
            if main_df_days.empty or main_df_hour.empty:
                st.warning("tidak ada data.")
            else:
                # Lanjutkan proses logika di sini
                st.success("Tanggal valid")

            if main_df_days.empty or main_df_hour.empty:
                st.warning("No data available for the selected date range.")
            else:


                hour_count_df = get_total_count_by_hour_df(main_df_hour)
                day_df_count_2011 = count_by_day_df(main_df_days)
                reg_df = total_registered_df(main_df_days)
                cas_df = total_casual_df(main_df_days)
                sum_order_items_df = sum_order(main_df_hour)
                season_df = jenis_season(main_df_hour)



#Melengkapi Dashboard dengan Berbagai Visualisasi Data
st.header('Bike Insight  :sparkles: :sparkles: :sunglasses:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)
 
with col1:
    total_orders = day_df_count_2011.cnt.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

st.subheader("Performa penjualan perusahaan dalam beberapa tahun terakhir")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

st.subheader("pada jam berapa yang paling banyak dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(x="hr", y="cnt", data=sum_order_items_df.head(5), palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)
 
sns.barplot(x="hr", y="cnt", data=sum_order_items_df.sort_values(by="hr", ascending=True).head(5), palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3","#90CAF9"], ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)",  fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


st.subheader("Pengaruh tingkat kelembaban terhadap jumlah penyewa")

# Membuat kolom baru bernama classify_humidity yang berisi klasifikasi tingkat kelembaban
def classify_humidity(row):
    if row["hum"] < 45:
        return "Terlalu kering"
    elif row["hum"] >= 45 and row["hum"] < 65:
        return "Ideal"
    else:
        return "Terlalu Lembab"


days_df["humidity_category"] = days_df.apply(classify_humidity, axis=1 )


# melakukan grouping terhadap hours dan cnt
humidity_sum = days_df.groupby(["humidity_category"]).cnt.sum().sort_values(ascending=False).reset_index()


# membuat bar chart untuk melihat korelasi antara tingkat kelembaban dengan jumlah penyewa
plt.figure(figsize=(35, 15))
 
# membuat barplot untuk penyewa sepeda terbanyak 
sns.barplot(x="humidity_category", y="cnt", data=humidity_sum, palette=["#90CAF9", "#D3D3D3", "#D3D3D3"])

# mengatur label dan judul untuk subplot pertama
plt.ylabel(None)
plt.xlabel("Humidity Category (tingkat kelembaban)", fontsize=30)
plt.title("Jumlah Penyewa based on humidity", loc="center", fontsize=30)
plt.tick_params(axis='y', labelsize=35)
plt.tick_params(axis='x', labelsize=30)

fig = plt.gcf() 
st.pyplot(fig)



st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',colors=["#D3D3D3", "#90CAF9"],
        shadow=True, startangle=90)
ax1.axis('equal')  

st.pyplot(fig1)
