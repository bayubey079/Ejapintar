import streamlit as st 
import re
st.set_page_config(page_title="EjaPintar - Checker Ejaan", page_icon="📝")

st.title("📝 pinterEJA")
st.subheader("Prototipe Pemindai Ejaan & Tanda Baca (EYD V)")

KAMUS_BAKU = {
    "praktek": "praktik",
    "apotik": "apotek",
    "rejeki": "rezeki",
    "analisa": "analisis",
    "kreatifitas": "kreativitas",
    "efektifitas": "efektivitas",
    "nomer": "nomor",
    "kwalitas": "kualitas"
}

KATA_HUBUNG_KOMA = ["tetapi", "melainkan", "sedangkan", "namun"]

def analisis_teks(teks):
    kesalahan = []
    teks_direvisi = teks
    
    for kata_salah, kata_benar in KAMUS_BAKU.items():
        pattern = re.compile(rf'\b{kata_salah}\b', re.IGNORECASE)
        matches = list(pattern.finditer(teks))
        if matches:
            for m in matches:
                kesalahan.append({
                    "jenis": "Kata Tidak Baku",
                    "salah": m.group(),
                    "saran": kata_benar,
                    "penjelasan": f"Kata '{m.group()}' tidak baku. Gunakan '{kata_benar}'."
                })
            teks_direvisi = pattern.sub(kata_benar, teks_direvisi)
            
    for kh in KATA_HUBUNG_KOMA:
        pattern = re.compile(rf'(?<!,)\s+\b{kh}\b', re.IGNORECASE)
        matches = list(pattern.finditer(teks_direvisi))
        if matches:
            for m in matches:
                kesalahan.append({
                    "jenis": "Tanda Baca (Koma)",
                    "salah": kh,
                    "saran": f", {kh}",
                    "penjelasan": f"Sebelum kata hubung '{kh}', gunakan tanda koma (,)."
                })

    return kesalahan, teks_direvisi

input_teks = st.text_area("Masukkan teks di sini:", height=150, placeholder="Contoh: Saya sedang analisa praktek kerja tetapi hasilnya kurang efektifitas.")

if st.button("🔍 Cek Ejaan", type="primary"):
    if not input_teks.strip():
        st.warning("Masukkan teks terlebih dahulu!")
    else:
        kesalahan, teks_hasil = analisis_teks(input_teks)
        st.write(f"*Total Kesalahan:* {len(kesalahan)}")
        for item in kesalahan:
            st.error(f"❌ *{item['jenis']}: '{item['salah']}' ➔ *{item['saran']}** ({item['penjelasan']})")
        st.subheader("✨ Hasil Revisi:")
        st.text_area("Teks Perbaikan:", teks_hasil, height=150)
