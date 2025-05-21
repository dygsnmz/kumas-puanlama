import streamlit as st
import pandas as pd

# Hata puanları ve kategorileri
hata_puanlari = {
    "Barré": {"puan": 2, "kategori": "Büyük"},
    "Delik": {"puan": 4, "kategori": "Kritik"},
    "İplik Atlaması": {"puan": 1, "kategori": "Küçük"},
    "Leke": {"puan": 3, "kategori": "Büyük"},
    "Delikçik": {"puan": 2, "kategori": "Kritik"},
}

musteri_tolerans = {
    "Müşteri A": 1.0,
    "Müşteri B": 0.75,
    "Müşteri C": 0.5
}

st.title("🧵 Çoklu Örme Kumaş Hata Puanlama")

rulo_no = st.text_input("Rulo No")
kumas_uzunlugu = st.number_input("Kumaş Uzunluğu (metre)", min_value=1.0, step=0.5)

st.markdown("### 🔢 Hataları Girin")

hata_sayisi = st.number_input("Kaç farklı hata türü gireceksiniz?", min_value=1, max_value=10, value=3, step=1)

hata_verileri = []

for i in range(hata_sayisi):
    st.markdown(f"#### Hata {i+1}")
    hata_turu = st.selectbox(f"Hata Türü #{i+1}", list(hata_puanlari.keys()), key=f"tur{i}")
    hata_adedi = st.number_input(f"Hata Adedi #{i+1}", min_value=0, step=1, key=f"adet{i}")
    hata_verileri.append({"Tür": hata_turu, "Adet": hata_adedi})

if st.button("Puanlamayı Hesapla"):
    if kumas_uzunlugu <= 0:
        st.error("⚠️ Kumaş uzunluğu 0 olamaz.")
    else:
        toplam_puan = 0
        detaylar = []

        for hata in hata_verileri:
            tur = hata["Tür"]
            adet = hata["Adet"]
            puan = hata_puanlari[tur]["puan"]
            kategori = hata_puanlari[tur]["kategori"]
            alt_puan = puan * adet
            toplam_puan += alt_puan
            detaylar.append({
                "Hata Türü": tur,
                "Kategori": kategori,
                "Adet": adet,
                "Puan/Adet": puan,
                "Toplam Puan": alt_puan
            })

        df = pd.DataFrame(detaylar)
        puan_metre = round(toplam_puan / kumas_uzunlugu, 2)
        kalite_sinifi = "A (Kabul)" if puan_metre <= 1 else ("B (Orta)" if puan_metre <= 1.5 else "C (Red)")

        st.markdown("## 🧾 Detaylı Puanlama")
        st.dataframe(df)

        st.markdown("## 📊 Genel Sonuç")
        st.write(f"**Toplam Puan:** {toplam_puan}")
        st.write(f"**Puan/Metre:** {puan_metre}")
        st.write(f"**Genel Kalite Sınıfı:** {kalite_sinifi}")

        for musteri, tolerans in musteri_tolerans.items():
            sonuc = "Kabul" if puan_metre <= tolerans else "Red"
            st.write(f"**{musteri} için Durum:** {sonuc}")


