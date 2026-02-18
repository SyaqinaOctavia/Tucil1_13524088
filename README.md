# Tucil1_Stima

<h2 id="deskripsi">Deskripsi</h2>
Queens adalah gim logika yang tersedia pada situs jejaring profesional LinkedIn. Tujuan dari gim ini adalah menempatkan queen pada sebuah papan persegi berwarna sehingga terdapat hanya satu queen pada tiap baris, kolom, dan daerah warna. Selain itu, satu queen tidak dapat ditempatkan bersebelahan dengan queen lainnya, termasuk secara diagonal.

Program ini merupakan solver untuk game Queens. Algoritma yang digunakan adalah brute force yang dituliskan dalam bahasa C++, serta GUI yang ditulis dalam bahasa Python.


<h2 id="table-of-contents">Daftar Isi</h2>
- <a href="#deskripsi">Deskripsi</a><br/>
- <a href="#table-of-contents">Daftar Isi</a><br/>
- <a href="#algortima">Algoritma</a><br/>
- <a href="#install">Library yang perlu di-instal</a><br/>
- <a href="#how-to-run">Cara Menjalankan Program</a><br/>
- <a href="#alur">Alur Singkat Program</a><br/>

<h2 id="algoritma">Algoritma</h2>
Terdapat 2 opsi untuk algoritma yang digunakan
1. Pure Brute Force. Kompleksitas O( C(n*n,n) )
2. Optimized Brute Force, dengan cara mencari berdasarkan baris (tidak ada >1 queen pada baris yang sama). Kom O(n^n)

<h2 id="install">Library yang perlu di-instal</h2>
```bash
pip install Pillow
```

<h2 id="#how-to-run">Cara Menjalankan Program</h2>

pergi ke folder src

```bash
cd src
```

run gui
```bash
python gui.py
```

Made by: Syaqina Octavia Rizha, NIM: 13524088