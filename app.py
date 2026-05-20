import json
import re
from io import BytesIO

import streamlit as st
import pandas as pd
from PIL import Image
import google.generativeai as genai

st.set_page_config(
    page_title="Smart Split Bill AI",
    page_icon="🧾",
    layout="wide"
)

# Proses 1 Membuat Fungsi Penunjang Project

def ubah_ke_angka(nilai):
    if nilai is None:
        return 0

    if isinstance(nilai, (int, float)):
        return int(nilai)

    nilai = str(nilai)
    nilai = nilai.replace("Rp", "")
    nilai = nilai.replace("IDR", "")
    nilai = nilai.replace(",", "")
    nilai = nilai.replace(".", "")
    nilai = nilai.strip()

    angka = re.sub(r"[^0-9]", "", nilai)

    if angka == "":
        return 0

    return int(angka)


def ambil_json_dari_teks(teks):
    teks = teks.strip()
    teks = teks.replace("```json", "").replace("```", "").strip()

    awal = teks.find("{")
    akhir = teks.rfind("}")

    if awal != -1 and akhir != -1:
        teks = teks[awal:akhir + 1]

    return json.loads(teks)


def rapihkan_data_bill(data_bill):
    hasil = {
        "items": [],
        "subtotal": 0,
        "biaya_tambahan": [],
        "total_bill": 0
    }

    daftar_item = data_bill.get("items", [])

    for item in daftar_item:
        nama_item = item.get("nama_item", "")
        jumlah = ubah_ke_angka(item.get("jumlah", 1))
        harga_per_item = ubah_ke_angka(item.get("harga_per_item", 0))
        total_harga_item = ubah_ke_angka(item.get("total_harga_item", 0))

        if jumlah == 0:
            jumlah = 1

        if total_harga_item == 0:
            total_harga_item = jumlah * harga_per_item

        hasil["items"].append({
            "nama_item": nama_item,
            "jumlah": jumlah,
            "harga_per_item": harga_per_item,
            "total_harga_item": total_harga_item
        })

    hasil["subtotal"] = ubah_ke_angka(data_bill.get("subtotal", 0))
    hasil["total_bill"] = ubah_ke_angka(data_bill.get("total_bill", 0))

    daftar_biaya = data_bill.get("biaya_tambahan", [])

    for biaya in daftar_biaya:
        hasil["biaya_tambahan"].append({
            "nama_biaya": biaya.get("nama_biaya", "Biaya tambahan"),
            "jumlah": ubah_ke_angka(biaya.get("jumlah", 0))
        })

    if hasil["subtotal"] == 0:
        hasil["subtotal"] = sum(item["total_harga_item"] for item in hasil["items"])

    total_biaya_tambahan = sum(biaya["jumlah"] for biaya in hasil["biaya_tambahan"])

    if hasil["total_bill"] == 0:
        hasil["total_bill"] = hasil["subtotal"] + total_biaya_tambahan

    return hasil

# Proses 2 Membuat Fungsi Untuk Membaca Nota Atau Bill Dengan Gemini API
def baca_nota_dengan_gemini(file_gambar, api_key):
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-2.5-flash")

    gambar = Image.open(file_gambar)

    prompt = """
    Kamu adalah sistem AI untuk membaca nota belanja atau bill restoran.

    Tolong baca gambar nota ini dan ekstrak data transaksi ke dalam JSON valid.

    Data yang wajib diambil:
    1. items:
       - nama_item
       - jumlah
       - harga_per_item
       - total_harga_item
    2. subtotal
    3. biaya_tambahan seperti pajak, service charge, diskon, rounding, dll
    4. total_bill

    Format output wajib seperti ini:
    {
      "items": [
        {
          "nama_item": "nama item",
          "jumlah": 1,
          "harga_per_item": 10000,
          "total_harga_item": 10000
        }
      ],
      "subtotal": 10000,
      "biaya_tambahan": [
        {
          "nama_biaya": "pajak",
          "jumlah": 1000
        }
      ],
      "total_bill": 11000
    }

    Aturan:
    - Jangan menambahkan penjelasan.
    - Jangan gunakan markdown.
    - Jangan gunakan ```json.
    - Jawab hanya JSON valid.
    - Semua angka harus berupa integer tanpa Rp, titik, atau koma.
    - Jika ada data yang tidak terbaca, isi dengan 0 atau string kosong.
    """

    response = model.generate_content([prompt, gambar])
    teks_hasil = response.text

    data_bill = ambil_json_dari_teks(teks_hasil)
    data_bill = rapihkan_data_bill(data_bill)

    return data_bill

# Proses 3 Membuat Fungsi Split Bill
def hitung_split_bill(data_bill, pilihan_pembayar):
    hasil_split = {}

    for item in data_bill["items"]:
        nama_item = item["nama_item"]
        total_item = item["total_harga_item"]

        daftar_orang = pilihan_pembayar.get(nama_item, [])

        if len(daftar_orang) == 0:
            continue

        bagian_per_orang = total_item / len(daftar_orang)

        for orang in daftar_orang:
            if orang not in hasil_split:
                hasil_split[orang] = {
                    "total_item": 0,
                    "biaya_tambahan": 0,
                    "total_bayar": 0
                }

            hasil_split[orang]["total_item"] += bagian_per_orang

    total_item_semua_orang = sum(nilai["total_item"] for nilai in hasil_split.values())

    total_biaya_tambahan = sum(
        biaya["jumlah"] for biaya in data_bill["biaya_tambahan"]
    )

    if total_item_semua_orang > 0:
        for orang in hasil_split:
            proporsi = hasil_split[orang]["total_item"] / total_item_semua_orang
            biaya_tambahan_orang = total_biaya_tambahan * proporsi

            hasil_split[orang]["biaya_tambahan"] = biaya_tambahan_orang
            hasil_split[orang]["total_bayar"] = (
                hasil_split[orang]["total_item"] + biaya_tambahan_orang
            )

    return hasil_split


def format_rupiah(nilai):
    return f"Rp {int(round(nilai)):,.0f}".replace(",", ".")

# Proses 4 Membuat Tampilan Aplikasi
st.title("🧾 Smart Split Bill AI")
st.write(
    "Prototype sederhana untuk membaca nota belanja menggunakan Gemini API, "
    "lalu membagi pembayaran ke beberapa orang."
)

with st.sidebar:
    st.header("Pengaturan API")
    api_key = st.text_input(
        "Masukkan Gemini API Key",
        type="password"
    )

    st.caption("API key hanya digunakan saat aplikasi berjalan di lokal.")


tab_upload, tab_split = st.tabs(["1. Baca Nota", "2. Split Bill"])

# Proses 5 Mengupload Dan Membaca Data Pada Nota Atau Bill
with tab_upload:
    st.subheader("Upload Gambar Nota")

    file_nota = st.file_uploader(
        "Pilih gambar nota",
        type=["jpg", "jpeg", "png"]
    )

    if file_nota is not None:
        gambar_preview = Image.open(file_nota)
        st.image(gambar_preview, caption="Preview nota", width=350)

        if st.button("Baca nota dengan AI"):
            if api_key.strip() == "":
                st.error("API Key Gemini belum diisi.")
            else:
                try:
                    with st.spinner("AI sedang membaca nota..."):
                        file_nota.seek(0)
                        data_bill = baca_nota_dengan_gemini(file_nota, api_key)
                        st.session_state["data_bill"] = data_bill

                    st.success("Nota berhasil dibaca.")

                except Exception as e:
                    st.error(f"Gagal membaca nota: {e}")

    if "data_bill" in st.session_state:
        data_bill = st.session_state["data_bill"]

        st.subheader("Hasil Pembacaan Item")

        df_item = pd.DataFrame(data_bill["items"])

        if len(df_item) > 0:
            df_tampil = df_item.copy()
            df_tampil["harga_per_item"] = df_tampil["harga_per_item"].apply(format_rupiah)
            df_tampil["total_harga_item"] = df_tampil["total_harga_item"].apply(format_rupiah)
            st.dataframe(df_tampil, use_container_width=True)
        else:
            st.warning("Item belum terbaca.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Subtotal", format_rupiah(data_bill["subtotal"]))

        with col2:
            total_biaya_tambahan = sum(
                biaya["jumlah"] for biaya in data_bill["biaya_tambahan"]
            )
            st.metric("Biaya Tambahan", format_rupiah(total_biaya_tambahan))

        with col3:
            st.metric("Total Bill", format_rupiah(data_bill["total_bill"]))

        st.subheader("Detail Biaya Tambahan")

        if len(data_bill["biaya_tambahan"]) > 0:
            df_biaya = pd.DataFrame(data_bill["biaya_tambahan"])
            df_biaya["jumlah"] = df_biaya["jumlah"].apply(format_rupiah)
            st.dataframe(df_biaya, use_container_width=True)
        else:
            st.info("Tidak ada biaya tambahan yang terbaca.")

# Proses 6 Menginput Peserta Yang Diajak Split Bill
with tab_split:
    st.subheader("Input Peserta Split Bill")

    if "data_bill" not in st.session_state:
        st.warning("Silakan baca nota terlebih dahulu di tab pertama.")
    else:
        data_bill = st.session_state["data_bill"]

        input_nama = st.text_area(
            "Masukkan nama peserta, pisahkan dengan koma",
            placeholder="Contoh: Raihan, Budi, Salsa"
        )

        daftar_nama = [
            nama.strip()
            for nama in input_nama.split(",")
            if nama.strip() != ""
        ]

        if len(daftar_nama) > 0:
            st.write("Peserta:")
            st.write(", ".join(daftar_nama))

            st.subheader("Pilih Pembayar Untuk Tiap Item")

            pilihan_pembayar = {}

            for item in data_bill["items"]:
                nama_item = item["nama_item"]
                total_item = item["total_harga_item"]

                pilihan = st.multiselect(
                    label=f"{nama_item} - {format_rupiah(total_item)}",
                    options=daftar_nama,
                    key=f"item_{nama_item}"
                )

                pilihan_pembayar[nama_item] = pilihan

            if st.button("Hitung Split Bill"):
                hasil_split = hitung_split_bill(data_bill, pilihan_pembayar)

                if len(hasil_split) == 0:
                    st.error("Belum ada item yang dipilih oleh peserta.")
                else:
                    st.subheader("Hasil Split Bill")

                    data_tabel = []

                    for nama, nilai in hasil_split.items():
                        data_tabel.append({
                            "nama": nama,
                            "total_item": nilai["total_item"],
                            "biaya_tambahan": nilai["biaya_tambahan"],
                            "total_bayar": nilai["total_bayar"]
                        })

                    df_hasil = pd.DataFrame(data_tabel)

                    df_tampil = df_hasil.copy()
                    df_tampil["total_item"] = df_tampil["total_item"].apply(format_rupiah)
                    df_tampil["biaya_tambahan"] = df_tampil["biaya_tambahan"].apply(format_rupiah)
                    df_tampil["total_bayar"] = df_tampil["total_bayar"].apply(format_rupiah)

                    st.dataframe(df_tampil, use_container_width=True)

                    total_semua_orang = df_hasil["total_bayar"].sum()

                    st.metric(
                        "Total pembayaran semua orang",
                        format_rupiah(total_semua_orang)
                    )

                    selisih = data_bill["total_bill"] - total_semua_orang

                    if abs(selisih) <= 2:
                        st.success("Total pembayaran peserta sudah sesuai dengan total bill.")
                    else:
                        st.warning(
                            f"Masih ada selisih {format_rupiah(selisih)} "
                            "dengan total bill. Cek kembali item yang belum dipilih."
                        )
        else:
            st.info("Masukkan minimal satu nama peserta terlebih dahulu.")