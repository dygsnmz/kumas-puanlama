# Kumaş Hata Puanlama Çoklu Girişli ve Bilgi Toplamalı Form (Streamlit)

import streamlit as st
import pandas as pd
from datetime import date
import io

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

st.set_page_config(layout="wide")
st.title("🧵 Örme Kumaş Kalite Puanlama ve Hata Takip Formu")

# 📌 Form Genel Bilgileri
st.header("🔖 Genel Bilgiler")
col1, col2, col3 = st.columns(3)
with col1:
    musteri = st.text_input("Müşteri")
    kumascifirma = st.text_input("Kumaşçı Firma")
    tarih = st.date_input("Tarih", value=date.today())
with col2:
    model_no = st.text_input("Model No")
    kull_en = st.number_input("Kullanılabilir En (cm)", min_value=0.0, step=0.1)
    kumaskodu = st.text_input("Kumaş Kodu")
with col3:
    agirlik = st.number_input("Ağırlık (gr/m2)", min_value=0.0, step=0.1)
    kompozisyon = st.text_input("Kompozisyon")
    kontrol_personel = st.text_input("Kontrol Eden Personel")

st.header("📋 Rulo ve Hata Bilgileri")
rulo_sayisi = st.number_input("Kaç rulo için giriş yapacaksınız?", min_value=1, max_value=20, value=1, step=1)

rulo_kayitlari = []

for i in range(rulo_sayisi):
    st.markdown(f"### 📦 Rulo {i+1}")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        rulo_no = st.text_input(f"Rulo No #{i+1}", key=f"rulo{i}")
        en_cm = st.number_input(f"Kullanılabilir En #{i+1} (cm)", min_value=0.0, step=0.1, key=f"en{i}")
    with col2:
        parti_no = st.text_input(f"Parti / Lot No #{i+1}", key=f"parti{i}")
        gelen_mkg = st.number_input(f"Gelen M/Kg #{i+1}", min_value=0.0, step=0.1, key=f"gelen{i}")
    with col3:
        varyant = st.text_input(f"Desen / Varyant #{i+1}", key=f"varyant{i}")
        olculen_mkg = st.number_input(f"Ölçülen M/Kg #{i+1}", min_value=0.0, step=0.1, key=f"olculen{i}")
    with col4:
        hata_sayisi = st.number_input(f"Hata Sayısı #{i+1}", min_value=1, max_value=10, value=2, key=f"hata_sayi{i}")
    with col5:
        aciklama = st.text_area(f"Açıklama (Rulo {i+1})", key=f"aciklama{i}", height=70)

    toplam_puan = 0
    hata_detay = []

    hata_df = pd.DataFrame(columns=["Hata Türü", "Adet", "Puan"])
    hata_cols = st.columns(hata_sayisi)
    for j in range(hata_sayisi):
        with hata_cols[j]:
            hata_tur = st.selectbox(f"Hata Türü {j+1} (Rulo {i+1})", list(hata_puanlari.keys()), key=f"tur{i}_{j}")
            adet = st.number_input(f"Adet {j+1} (Rulo {i+1})", min_value=0, step=1, key=f"adet{i}_{j}")
            puan = hata_puanlari[hata_tur]["puan"]
            toplam_puan += puan * adet
            hata_df.loc[j] = [hata_tur, adet, puan]

    kumaş_uzunlugu = olculen_mkg
    puan_metre = round(toplam_puan / kumaş_uzunlugu, 2) if kumaş_uzunlugu > 0 else 0
    kabul_red = "Kabul" if puan_metre <= 1 else "Red"

    rulo_kayitlari.append({
        "Rulo No": rulo_no,
        "Parti/Lot No": parti_no,
        "Desen/Varyant": varyant,
        "Gelen M/kg": gelen_mkg,
        "Ölçülen M/kg": olculen_mkg,
        "Kullanılabilir En": en_cm,
        "Toplam Puan": toplam_puan,
        "Puan/Metre": puan_metre,
        "Kabul/Red": kabul_red,
        "Açıklama": aciklama
    })

if st.button("✅ Tüm Verileri Göster"):
    st.subheader("🧾 Rulo Kalite Sonuçları")
    rulo_df = pd.DataFrame(rulo_kayitlari)
    st.dataframe(rulo_df)

    st.subheader("📦 Genel Form Verileri")
    st.write(f"**Müşteri:** {musteri}")
    st.write(f"**Model No:** {model_no}")
    st.write(f"**Kumaşçı Firma:** {kumascifirma}")
    st.write(f"**Kullanılabilir En:** {kull_en} cm")
    st.write(f"**Ağırlık:** {agirlik} gr/m2")
    st.write(f"**Tarih:** {tarih}")
    st.write(f"**Kumaş Kodu:** {kumaskodu}")
    st.write(f"**Kompozisyon:** {kompozisyon}")
    st.write(f"**Kontrol Eden Personel:** {kontrol_personel}")

    # Excel olarak indir
    towrite = io.BytesIO()
    with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
        rulo_df.to_excel(writer, index=False, sheet_name='Rulo Verileri')
        genel_df = pd.DataFrame([{
            "Müşteri": musteri,
            "Model No": model_no,
            "Kumaşçı Firma": kumascifirma,
            "Kullanılabilir En": kull_en,
            "Ağırlık": agirlik,
            "Tarih": tarih,
            "Kumaş Kodu": kumaskodu,
            "Kompozisyon": kompozisyon,
            "Kontrol Eden Personel": kontrol_personel
        }])
        genel_df.to_excel(writer, index=False, sheet_name='Genel Bilgiler')
        # writer.save() satırı kaldırıldı çünkü 'with' bloğu otomatik kaydeder
        towrite.seek(0)
st.download_button(
    label="📥 Excel Olarak İndir",
    data=towrite,
    file_name="kumas_kalite_puanlama.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
