import os
import time
from pathlib import Path

import pandas as pd
from PIL import Image
from dotenv import load_dotenv

from app import baca_nota_gemini, baca_nota_donut, angka_rupiah

load_dotenv()

def ringkas_hasil(nama_file, nama_model, durasi, data_nota):
    return {
        "file": nama_file,
        "model": nama_model,
        "durasi_detik": round(durasi, 2),
        "jumlah_item_terbaca": len(data_nota.items),
        "subtotal": data_nota.subtotal,
        "total": data_nota.total,
        "catatan_kualitatif": "",
    }

def main():
    folder_nota = Path("contoh_nota")
    daftar_gambar = list(folder_nota.glob("*.jpg")) + list(folder_nota.glob("*.jpeg")) + list(folder_nota.glob("*.png"))

    if len(daftar_gambar) < 2:
        print("Masukkan minimal 2 gambar nota ke folder contoh_nota terlebih dahulu.")
        return

    hasil_riset = []
    api_key = os.getenv("GOOGLE_API_KEY", "")

    for path_gambar in daftar_gambar:
        gambar = Image.open(path_gambar).convert("RGB")

        if api_key:
            mulai = time.time()
            try:
                data_nota = baca_nota_gemini(gambar, api_key)
                hasil_riset.append(ringkas_hasil(path_gambar.name, "Gemini API", time.time() - mulai, data_nota))
            except Exception as e:
                hasil_riset.append({
                    "file": path_gambar.name,
                    "model": "Gemini API",
                    "durasi_detik": None,
                    "jumlah_item_terbaca": 0,
                    "subtotal": 0,
                    "total": 0,
                    "catatan_kualitatif": f"Gagal: {e}",
                })

        mulai = time.time()
        try:
            data_nota = baca_nota_donut(gambar)
            hasil_riset.append(ringkas_hasil(path_gambar.name, "Donut lokal", time.time() - mulai, data_nota))
        except Exception as e:
            hasil_riset.append({
                "file": path_gambar.name,
                "model": "Donut lokal",
                "durasi_detik": None,
                "jumlah_item_terbaca": 0,
                "subtotal": 0,
                "total": 0,
                "catatan_kualitatif": f"Gagal: {e}",
            })

    df = pd.DataFrame(hasil_riset)
    df.to_csv("hasil_riset_model.csv", index=False)
    print(df)
    print("\nFile hasil riset tersimpan sebagai hasil_riset_model.csv")

if __name__ == "__main__":
    main()
