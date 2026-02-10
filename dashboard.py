import streamlit as st 
from streamlit_option_menu import option_menu
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt


#baca dataset+convert
df_hour = pd.read_csv('hour.csv')
df_day = pd.read_csv('day.csv')
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
df_day['dteday'] = pd.to_datetime(df_day['dteday'])

#ubah musim
season_map = {
    1: "Spring",
    2: "Summer",
    3: "Fall",
    4: "Winter"
}
df_day["season"] = df_day["season"].map(season_map)

#setting awal
st.set_page_config(
    page_title="Dashboard Peminjaman Sepeda",
    layout="wide"
)

#Sidebar
with st.sidebar:
    selected = option_menu(
        "MENU",
        ["Identitas",
         "Pertanyaan",
         "Analisis Peminjaman Per-Jam",
         "Analisis Peminjaman Per-Musim",
         "Analisis Peminjaman Kategori Hari",
         "Analisis Peminjaman Kategori Workingday Per-Musim",
         "Analisis Peminjaman Per-Tahun Tahun",
         "Analisis Total Pengguna Casual dan Registered"],
        default_index=0
    )
        
            
#main
if selected == "Identitas":
    st.header("Proyek Analisis Data: Bike-Sharing-Dataset")
    st.subheader("""
                Kelompok : IF2-10124063 
                Anggota :
                 
                    10124063 - Egi Nugraha
                    
                    10124071 - Panji Gumilang
                    
                    10124077 - M Nazib Al Qoys
                    
                    10124072 - Excel Al Kautsar
                    
                    10124045 - Fikri Sofyansah
                    
                    10124803 - Muhammad Syarifuddin Rahiman
                
                """)
    
elif selected =="Pertanyaan":
    st.header("Pertanyaan Analisi Data: Bike-Sharing-Dataset")
    st.markdown(
        """ 
            1. Bagaimana pola rata-rata permintaan penyewaan sepeda sepanjang hari? 

            2. Bagaimana rata-rata jumlah penyewaan sepeda pada setiap musim? 

            3. Berapa rata-rata tertinggi total penyewaan sepeda pada setiap kategori hari, dalam setiap tahun? 

            4. Berapa Total Sepeda yang disewakan pada kategori hari (workingday) disetiap musimnya? 

            5. Total penyewaan sepeda setiap tahunnya, dan buatkan visualisasinya menggunakan grafik? 

            6. Manakah tipe pengguna yang lebih banyak menyewa sepeda secara keseluruhan (casual atau registed)? 
        """
    )

elif selected == "Analisis Peminjaman Per-Jam" :             
        with st.container():
            st.title('Grafik Rata-Rata Peminjaman Sepeda per Jam')
            #menghitung rata rata perjam+rename column
            Rata_per_jam = df_hour.groupby("hr")["cnt"].mean().reset_index().rename(columns={"hr": "Jam",
                                                                                             "cnt": "Rata-Rata Peminjaman"})
            #tampilkan dalam tabel
            st.dataframe(Rata_per_jam)
            #tampilkan dalam grafik line
            chart = alt.Chart(Rata_per_jam).mark_line(point=True).encode(
            x=alt.X("Jam:O", title="Jam",axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Rata-Rata Peminjaman:Q", title="Rata-rata Peminjaman")
            )
            st.altair_chart(chart, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa rata-rata 
                         permintaan penyewaan sepeda perjam memiliki Aktivitas penyewaan 
                         paling rendah pada dini hari (00.00–05.00) lebih tepatnya 04:00, 
                         kemudian meningkat tajam pada jam berangkat kerja (sekitar 07.00–09.00). 
                         Setelah itu jumlah penyewaan kembali menurun pada siang hari, lalu mengalami 
                         puncak tertinggi kedua pada jam pulang kerja yaitu sekitar (16.00–19.00) 
                         tepatnya pukul 17:00.
                         """)
            
elif selected == "Analisis Peminjaman Per-Musim":
        with st.container():
            st.title("Grafik Rata-Rata Peminjaman Sepeda per Musim")
            #menghitung rata rata per musim+rename column
            Rata_per_season = df_day.groupby("season")["cnt"].mean().reset_index().rename(columns={"season": "Musim",
                                                                                             "cnt": "Rata-Rata Peminjaman"})
            #tampilkan dalam tabel
            st.dataframe(Rata_per_season)
            #tampilkan dalam grafik bar
            bar = alt.Chart(Rata_per_season).mark_bar().encode(
                x=alt.X("Musim:N", title="Musim", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Rata-Rata Peminjaman:Q", title="Rata-rata Jumlah Peminjaman"),
            )
            text = alt.Chart(Rata_per_season).mark_text(
                align="center",
                baseline="bottom",
                dy=-5 
            ).encode(
                x="Musim:N",
                y="Rata-Rata Peminjaman:Q",
                text=alt.Text("Rata-Rata Peminjaman:Q", format=".1f")
            )
            chart = (bar + text)
            st.altair_chart(chart, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa rata-rata 
                         permintaan penyewaan sepeda per musim mengalami puncak tertinggi 
                         pada musim Fall, disusul Summer, kemudian Winter, dan yang paling rendah 
                         adalah Spring.
                         """)
            
elif selected == "Analisis Peminjaman Per-Tahun Tahun":
        with st.container():
            st.title("Grafik Rata-Rata Peminjaman Sepeda Per-Tahun")
            #perhitungan 
            total_per_tahun = df_day.groupby("yr")["cnt"].sum().reset_index().rename(columns={"yr": "Tahun",
                                                                "cnt": "Rata-Rata Peminjaman"})
            #konversi tahun
            total_per_tahun["Tahun"] = total_per_tahun["Tahun"].map({
                0: 2011,
                1: 2012
            })
            #tampilkan dalam tabel
            st.dataframe(total_per_tahun)
            #tampilkan dalam barchart
            bar = alt.Chart(total_per_tahun).mark_bar().encode(
                x=alt.X("Tahun:O", title="Tahun", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Rata-Rata Peminjaman:Q", title="Total Peminjaman"),
                tooltip=[
                    alt.Tooltip("Tahun:O", title="Tahun"),
                    alt.Tooltip("Rata-Rata Peminjaman:Q", title="Total", format=",")
                ]
            )
            text = alt.Chart(total_per_tahun).mark_text(
                dy=-5
            ).encode(
                x="Tahun:O",
                y="Rata-Rata Peminjaman:Q",
                text=alt.Text("Rata-Rata Peminjaman:Q", format=",")
            )
            st.altair_chart(bar + text, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa rata-rata 
                         permintaan penyewaan sepeda tiap tahunya menunjukkan adanya 
                         pertumbuhan penggunaan bike-sharing system dari tahun ke tahun.
                         Terlihat bahwa tahun 2012 memiliki jumlah penyewaan sepeda yang 
                         lebih tinggi dibandingkan tahun 2011.
                         """)

elif selected == "Analisis Peminjaman Kategori Hari":
        with st.container():
            st.title("Grafik Rata-Rata total penyewaan sepeda pada setiap kategori hari, dalam setiap tahun")
            #inisiasi awal
            def categorize(row):
                if row["holiday"] == 1:
                    return "Holiday"
                elif row["workingday"] == 1:
                    return "Working"
                else:
                    return "Weekday"

            df_day["day_category"] = df_day.apply(categorize, axis=1)
            # Konversi tahun
            df_day["year"] = df_day["yr"].map({0: 2011, 1: 2012})
            # Hitung rata-rata per kategori hari dan tahun
            Rata_per_year_cat = df_day.groupby(["year", "day_category"])["cnt"].mean().reset_index()
            # Pivot tabel 1 tampilannya
            Rata_hari = Rata_per_year_cat.pivot(index="year", columns="day_category", values="cnt")
            #tampilkan dalam tabel
            st.dataframe(Rata_hari)
            #tampilkan dalam grafik bar
            bar_chart = alt.Chart(Rata_per_year_cat).mark_bar().encode(
                x=alt.X("year:O", title="Tahun", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("cnt:Q", title="Rata-rata Jumlah Peminjaman"),
                color=alt.Color("day_category:N", title="Kategori Hari"),
                xOffset="day_category:N",
                tooltip=[
                    alt.Tooltip("year:O", title="Tahun"),
                    alt.Tooltip("day_category:N", title="Kategori"),
                    alt.Tooltip("cnt:Q", title="Rata-rata", format=".0f")
                ]
            )
            text_chart = alt.Chart(Rata_per_year_cat).mark_text(
                dy=-5,
                dx=25,              
                size=12,
                align="center",
                color="black"
            ).encode(
                x="year:O",
                y="cnt:Q",
                xOffset="day_category:N",
                text=alt.Text("cnt:Q", format=".0f")
            )
            st.altair_chart(bar_chart + text_chart, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa 
                         rata-rata permintaan penyewaan sepeda per kategori hari menunjukan bahwa  
                         hari Working Day memiliki rata-rata penyewaan yang paling tinggi baik 
                         pada tahun 2011 maupun 2012 dari pada holiday dan weekend.
                         """)
            
elif selected == "Analisis Peminjaman Kategori Workingday Per-Musim":
        with st.container():
            st.title("Grafik Total Sepeda yang Disewa Pada Kategori Hari Workingday per-Musim")
            #inisiasi
            total_permusim = df_day[df_day['workingday'] == 1].groupby('season')['cnt'].sum().reset_index().rename(columns={"cnt": "Rata-Rata Peminjaman"})
            #tampilkan dalam tabel
            st.dataframe(total_permusim)
            #tampilkan dalam grafik bar
            bar = alt.Chart(total_permusim).mark_bar().encode(
                x=alt.X("season:N", title="Musim", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("Rata-Rata Peminjaman:Q", title="Total Peminjaman"),
                tooltip=[
                    alt.Tooltip("season:N", title="Musim"),
                    alt.Tooltip("Rata-Rata Peminjaman:Q", title="Total", format=",")
                ]
            )
            text = alt.Chart(total_permusim).mark_text(
                dy=-5,
                align="center",
                baseline="bottom"
            ).encode(
                x="season:N",
                y="Rata-Rata Peminjaman:Q",
                text=alt.Text("Rata-Rata Peminjaman:Q")
            )
            st.altair_chart(bar + text, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa 
                         rata-rata permintaan penyewaan sepeda per kategori workingday 
                         di setiap musim menunjukan total penyewaan sepeda tertinggi terjadi
                         pada musim Fall, diikuti oleh Summer, Winter, dan paling rendah pada Spring.
                         """)
            
            
elif selected == "Analisis Total Pengguna Casual dan Registered":
        with st.container():
            st.title("Grafik Total Pengguna Casual dan Registered")
            #inisiasi awal
            total_casual = df_day['casual'].sum()
            total_registered = df_day['registered'].sum()
            #inisiasi col
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Casual", f"{total_casual:,}")
            with col2:
                st.metric("Total Registered", f"{total_registered:,}") 
                
            #tampilkan dalam piechart
            df_user = pd.DataFrame({
                "Tipe User": ["Casual", "Registered"],
                "Total": [total_casual, total_registered]
            })
            pie = alt.Chart(df_user).mark_arc(
                innerRadius=90
            ).encode(
                theta=alt.Theta("Total:Q"),
                color=alt.Color("Tipe User:N", legend=alt.Legend(title="Tipe User")),
                tooltip=[
                    alt.Tooltip("Tipe User:N", title="Tipe"),
                    alt.Tooltip("Total:Q", title="Total", format=",")
                ]
            )
            text = alt.Chart(df_user).mark_text(
                radius=200,
                size=14,
                color="black"
            ).transform_joinaggregate(
                total_sum='sum(Total)'
            ).transform_calculate(
                percent='datum.Total / datum.total_sum'
            ).encode(
                theta=alt.Theta("Total:Q"),
                text=alt.Text('percent:Q', format='.1%')
            )

            st.altair_chart(pie + text, use_container_width=True)
            
            #membuat conclusion
            with st.expander("Conclusion"):
                st.write("""
                         Berdasarkan diagram di atas dapat disimpulkan bahwa 
                         tipe pengguna yang lebih banyak menyewa sepeda adalah 
                         registered dengan persentase 81,2%
                         """)

    