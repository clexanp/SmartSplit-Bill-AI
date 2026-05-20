# Cara Menjalankan Project SmartSplit Bill AI

---

## 1. Buka Anaconda Prompt

Cari aplikasi berikut di Windows:

```bash
Anaconda Prompt
```

Gunakan Anaconda Prompt untuk membuat environment dan install library.

---

## 2. Buat Environment Baru

Jalankan perintah berikut:

```bash
conda create -n smartbill python=3.10
```

Jika muncul pertanyaan konfirmasi, ketik:

```bash
y
```

Tunggu sampai proses selesai.

---

## 3. Aktifkan Environment

Jalankan:

```bash
conda activate smartbill
```

Jika berhasil, terminal akan berubah menjadi seperti ini:

```bash
(smartbill)
```

---

## 4. Masuk ke Folder Project

Masuk ke folder project menggunakan perintah `cd`.

Contoh:

```bash
cd /d "D:\Dokumen Bootcamp Dibimbing 2025\Semua Materi dan Tugas 03 Mei 2026\SmartSplit Bill AI\Tugas\Assignment Day 54\SmartSplit Bill AI"
```

Pastikan folder tersebut berisi file:

```bash
app.py
requirements.txt
README.md
```

Untuk mengecek isi folder, jalankan:

```bash
dir
```

---

## 5. Upgrade pip, setuptools, dan wheel

Jalankan:

```bash
python -m pip install --upgrade pip setuptools wheel
```

Langkah ini berguna supaya proses install library lebih stabil.

---

## 6. Install Library Project

Jalankan:

```bash
pip install -r requirements.txt
```

Tunggu sampai semua library selesai terinstall.

---

## 7. Buka Project di VS Code

Masih di Anaconda Prompt dan masih berada di folder project, jalankan:

```bash
code .
```

VS Code akan terbuka langsung pada folder project.

---

## 8. Pilih Python Interpreter di VS Code

Di VS Code, tekan:

```bash
Ctrl + Shift + P
```

Lalu cari:

```bash
Python: Select Interpreter
```

Pilih interpreter berikut:

```bash
D:\Anaconda\envs\smartbill\python.exe
```

atau yang memiliki nama:

```bash
smartbill Python 3.10
```

---

## 9. Buat File `.env`

Di folder utama project, buat file baru bernama:

```bash
.env
```

Isi file tersebut dengan format berikut:

```env
GEMINI_API_KEY=MASUKKAN_API_KEY_KAMU
```

Contoh:

```env
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxx
```

API key dapat dibuat melalui Google AI Studio.

---

## 10. Jalankan Aplikasi Streamlit

Buka terminal di VS Code, lalu pastikan environment yang digunakan adalah `smartbill`.

Cek Python yang aktif:

```bash
where python
```

Pastikan hasil paling atas mengarah ke:

```bash
D:\Anaconda\envs\smartbill\python.exe
```

Setelah itu jalankan aplikasi:

```bash
python -m streamlit run app.py
```

---

## 11. Buka Aplikasi di Browser

Jika berhasil, terminal akan menampilkan URL seperti:

```bash
http://localhost:8501
```

Buka link tersebut di browser.

---

## 12. Cara Menggunakan Aplikasi

1. Upload gambar nota atau bill belanja.
2. Klik tombol **Baca nota dengan AI**.
3. Tunggu sampai sistem menampilkan hasil pembacaan item.
4. Masukkan nama peserta split bill.
5. Pilih siapa saja yang membayar tiap item.
6. Klik tombol **Hitung Split Bill**.
7. Sistem akan menampilkan total pembayaran masing-masing orang.

---

## 13. Jika Aplikasi Error Karena Model Gemini

Pastikan di file `app.py` bagian model menggunakan:

```python
model = genai.GenerativeModel("gemini-2.5-flash")
```

---

## 14. Jika Streamlit Tidak Jalan

Gunakan perintah berikut:

```bash
python -m streamlit run app.py
```

Jangan menggunakan:

```bash
streamlit run app.py
```

karena terkadang Streamlit yang dipanggil berasal dari environment Python lain.

---

## 15. Jika Environment VS Code Salah

Cek dengan:

```bash
where python
```

Jika hasilnya bukan:

```bash
D:\Anaconda\envs\smartbill\python.exe
```

maka pilih ulang interpreter di VS Code:

```bash
Ctrl + Shift + P
Python: Select Interpreter
```

Lalu pilih environment:

```bash
smartbill Python 3.10
```

---

## 16. Menjalankan Project di Lain Waktu

Jika project sudah pernah berhasil dijalankan, langkah berikutnya cukup:

```bash
conda activate smartbill
```

Masuk ke folder project:

```bash
cd /d "LOKASI_FOLDER_PROJECT"
```

Lalu jalankan:

```bash
python -m streamlit run app.py
```