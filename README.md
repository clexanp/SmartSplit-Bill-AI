# Smart Split Bill AI

## Deskripsi Project

Smart Split Bill AI merupakan prototype aplikasi web berbasis Artificial Intelligence yang digunakan untuk membantu pengguna membaca nota atau bill belanja secara otomatis dan melakukan pembagian tagihan (split bill) kepada beberapa peserta.

Aplikasi memanfaatkan model multimodal Gemini 2.5 Flash untuk memahami isi gambar nota dan mengekstrak informasi transaksi seperti nama item, jumlah item, harga item, subtotal, biaya tambahan, dan total bill. Setelah data transaksi berhasil dibaca, pengguna dapat menentukan siapa saja yang terlibat dalam transaksi dan memilih item yang dibayar oleh masing-masing peserta.

Project ini dikembangkan sebagai proof of concept untuk menunjukkan bagaimana teknologi AI dapat membantu proses pencatatan transaksi dan pembagian tagihan secara lebih praktis.

---

# Teknologi yang Digunakan

* Python 3.10
* Streamlit
* Google Gemini 2.5 Flash API
* Pandas
* Pillow
* Transformers
* Torch
* Anaconda

---

# Cara Menjalankan Project

## 1. Membuka Anaconda Prompt

Buka aplikasi Anaconda Prompt melalui Start Menu Windows.

---

## 2. Membuat Environment Baru

Jalankan perintah berikut:

```bash
conda create -n smartbill python=3.10
```

Ketik:

```bash
y
```

jika muncul permintaan konfirmasi.

---

## 3. Mengaktifkan Environment

```bash
conda activate smartbill
```

Jika berhasil, terminal akan menampilkan:

```bash
(smartbill)
```

---

## 4. Masuk ke Folder Project

Masuk ke folder project menggunakan perintah:

```bash
cd /d "LOKASI_FOLDER_PROJECT"
```

Contoh:

```bash
cd /d "D:\Dokumen Bootcamp Dibimbing 2025\Semua Materi dan Tugas 03 Mei 2026\SmartSplit Bill AI\Tugas\Assignment Day 54\SmartSplit Bill AI"
```

---

## 5. Install Dependency

Upgrade pip terlebih dahulu:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Install seluruh library:

```bash
pip install -r requirements.txt
```

---

## 6. Membuat API Key Gemini

Buat API Key melalui Google AI Studio.

Simpan API Key ke dalam file:

```env
.env
```

dengan format:

```env
GEMINI_API_KEY=MASUKKAN_API_KEY_ANDA
```

---

## 7. Membuka Project Menggunakan VS Code

Masih dari Anaconda Prompt:

```bash
code .
```

---

## 8. Memilih Python Interpreter

Di VS Code:

* Tekan Ctrl + Shift + P
* Pilih Python: Select Interpreter
* Pilih interpreter:

```bash
D:\Anaconda\envs\smartbill\python.exe
```

---

## 9. Menjalankan Aplikasi

Buka terminal VS Code lalu jalankan:

```bash
python -m streamlit run app.py
```

---

## 10. Membuka Aplikasi

Jika berhasil, Streamlit akan menampilkan URL:

```bash
http://localhost:8501
```

Buka URL tersebut pada browser.

---

# Cara Menggunakan Aplikasi

1. Upload gambar nota atau receipt.
2. Masukkan Gemini API Key.
3. Klik tombol "Baca Nota Dengan AI".
4. Tunggu hingga sistem menampilkan hasil ekstraksi data transaksi.
5. Masukkan nama peserta split bill.
6. Pilih item yang dibayar oleh masing-masing peserta.
7. Klik tombol "Hitung Split Bill".
8. Sistem akan menampilkan total pembayaran masing-masing peserta.

---

# Analisis Hasil Akhir Produk

Berdasarkan pengujian yang dilakukan menggunakan beberapa nota restoran dan minimarket, aplikasi mampu melakukan ekstraksi data transaksi dengan cukup baik.

Model Gemini 2.5 Flash mampu membaca informasi penting seperti nama item, jumlah item, harga item, subtotal, biaya tambahan, dan total bill. Hasil ekstraksi kemudian digunakan untuk melakukan proses pembagian tagihan kepada beberapa peserta.

Pada nota yang memiliki kualitas gambar baik, sistem mampu menghasilkan data yang cukup akurat sehingga pengguna tidak perlu melakukan input ulang secara manual.

Selain itu, sistem berhasil memastikan bahwa total pembayaran seluruh peserta mendekati total bill asli yang terdapat pada nota.

Secara keseluruhan, aplikasi berhasil memenuhi tujuan utama project yaitu membaca receipt menggunakan AI dan melakukan split bill secara otomatis.

---

# Kelemahan Model AI

Beberapa kelemahan yang ditemukan selama proses pengujian:

* Model sangat bergantung pada kualitas gambar yang diunggah.
* Nota yang blur atau memiliki pencahayaan buruk dapat menurunkan akurasi ekstraksi.
* Membutuhkan koneksi internet karena menggunakan Gemini API.
* Waktu inferensi bergantung pada kecepatan jaringan dan server API.
* Beberapa nama item yang tidak umum terkadang dapat dibaca kurang tepat.

---

# Ide Pengembangan Model AI

Beberapa pengembangan yang dapat dilakukan pada model AI:

* Menambahkan OCR lokal sebagai fallback apabila koneksi internet tidak tersedia.
* Menggunakan beberapa model sekaligus untuk meningkatkan akurasi ekstraksi.
* Melakukan fine-tuning model menggunakan dataset receipt Indonesia.
* Menambahkan confidence score pada hasil pembacaan item.
* Menambahkan validasi otomatis terhadap hasil ekstraksi sebelum ditampilkan kepada pengguna.

---

# Kelemahan Produk

Beberapa keterbatasan aplikasi saat ini:

* Belum memiliki sistem login pengguna.
* Riwayat transaksi belum tersimpan ke database.
* Belum tersedia fitur ekspor hasil split bill ke PDF atau Excel.
* Belum tersedia fitur berbagi hasil pembayaran melalui WhatsApp atau Email.
* Antarmuka masih sederhana karena fokus pada pembuatan prototype.

---

# Ide Pengembangan Produk

Beberapa pengembangan yang dapat dilakukan pada versi berikutnya:

* Menambahkan database untuk menyimpan histori transaksi pengguna.
* Menambahkan fitur ekspor hasil split bill ke PDF dan Excel.
* Menambahkan fitur scan nota langsung dari kamera smartphone.
* Integrasi dengan payment gateway atau QRIS.
* Menambahkan dashboard statistik pengeluaran pengguna.
* Menambahkan fitur rekomendasi pembagian biaya berdasarkan histori transaksi sebelumnya.

---

# Kesimpulan

Smart Split Bill AI berhasil menunjukkan bahwa teknologi multimodal AI dapat digunakan untuk membaca receipt dan membantu proses pembagian tagihan secara otomatis.

Melalui kombinasi Gemini 2.5 Flash dan Streamlit, aplikasi mampu memberikan pengalaman yang sederhana namun cukup efektif untuk membantu pengguna mengelola transaksi bersama. Walaupun masih memiliki beberapa keterbatasan, prototype ini memiliki potensi untuk dikembangkan menjadi aplikasi yang lebih lengkap pada masa mendatang.
