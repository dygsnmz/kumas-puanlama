import streamlit as st
import pandas as pd

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

st.title("🧵 Örme Kumaş Hata Puanlama Formu")

rulo_no = st.text_input("Rulo No")
kumas_uzunlugu = st.number_input("Kumaş Uzunluğu (metre)", min_value=1.0, step=0.5)
hata_turu = st.selectbox("Hata Türü", list(hata_puanlari.keys()))
hata_adedi = st.number_input("Hata Adedi", min_value=1, step=1)

if st.button("Puanlamayı Hesapla"):
    puan_adet = hata_puanlari[hata_turu]["puan"]
    kategori = hata_puanlari[hata_turu]["kategori"]
    toplam_puan = puan_adedi * hata_adedi
    puan_metre = round(toplam_puan / kumas_uzunlugu, 2)

    kalite_sinifi = "A (Kabul)" if puan_metre <= 1 else ("B (Orta)" if puan_metre <= 1.5 else "C (Red)")

    st.subheader("📊 Sonuçlar")
    st.write(f"**Toplam Puan:** {toplam_puan}")
    st.write(f"**Puan/Metre:** {puan_metre}")
    st.write(f"**Hata Kategorisi:** {kategori}")
    st.write(f"**Genel Kalite Sınıfı:** {kalite_sinifi}")

    for musteri, tolerans in musteri_tolerans.items():
        sonuc = "Kabul" if puan_metre <= tolerans else "Red"
        st.write(f"**{musteri} için Durum:** {sonuc}")
