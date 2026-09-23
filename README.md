# Refactoring Monolith App

Project ini merupakan hasil refactoring dari aplikasi Python sederhana yang awalnya mencampurkan domain logic, storage, dan CLI dalam satu bagian kode.

Tujuan refactoring adalah memisahkan responsibility setiap bagian aplikasi agar kode lebih mudah dipahami, diuji, dan dikembangkan.

## 1. Struktur Project

```text
monolithapp/
│
├── adapters/
│   └── json_file_repo.py
│
├── tests/
│   ├── test_domain.py
│   ├── test_json_file_repo.py
│   └── test_services.py
│
├── cli.py
├── domain.py
├── ports.py
├── services.py
├── users.json
└── pytest.ini
```

## 2. Responsibility Setiap Module

### `domain.py`

Berisi aturan bisnis atau domain logic aplikasi.

Contohnya:

* Validasi nama user.
* Validasi email.
* Pengecekan email yang sudah digunakan.
* Pembuatan ID user.

Module ini tidak mengetahui bagaimana data disimpan atau bagaimana user berinteraksi dengan aplikasi.

### `ports.py`

Berisi interface repository menggunakan `Protocol`.

`UserRepository` mendefinisikan operasi yang dibutuhkan oleh service:

```text
load_all()
save_all()
```

Dengan adanya interface ini, service tidak perlu bergantung langsung kepada implementasi JSON.

### `services.py`

Berisi application/use-case logic.

Contohnya adalah proses membuat user:

```text
Load data
    ↓
Validasi user
    ↓
Cek email
    ↓
Generate ID
    ↓
Simpan user
```

Service menerima repository sebagai dependency sehingga dapat menggunakan berbagai implementasi repository.

### `adapters/json_file_repo.py`

Berisi implementasi repository menggunakan file JSON.

Responsibility module ini hanya menangani:

* Membaca `users.json`.
* Menyimpan data ke `users.json`.

Storage tidak dicampurkan dengan domain logic.

### `cli.py`

Berfungsi sebagai interface command-line.

CLI menangani:

* Input nama.
* Input email.
* Memanggil service.
* Menampilkan hasil atau error.

CLI tidak menangani business rules secara langsung.

### `tests/`

Berisi automated test untuk masing-masing responsibility:

```text
test_domain.py
    → menguji domain logic

test_services.py
    → menguji application logic

test_json_file_repo.py
    → menguji JSON storage
```

---

# 3. Dependency Map Sebelum Refactoring

Pada struktur awal, CLI, business logic, validation, dan storage berada dalam satu bagian aplikasi.

```text
┌─────────────────────────────────┐
│        MONOLITH APPLICATION     │
│                                 │
│  CLI                            │
│  Business Logic                 │
│  Validation                     │
│  JSON Storage                   │
└───────────────┬─────────────────┘
                │
                ▼
           users.json
```

Semua responsibility saling bercampur. Akibatnya, perubahan pada storage atau interface dapat berdampak langsung terhadap bagian business logic.

---

# 4. Dependency Map Sesudah Refactoring

Setelah refactoring, responsibility dipisahkan menjadi beberapa module.

```text
                    ┌──────────────┐
                    │    cli.py    │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ services.py  │
                    └──────┬───────┘
                           │
                  ┌────────┴────────┐
                  ▼                 ▼
           ┌────────────┐    ┌────────────┐
           │ domain.py  │    │  ports.py  │
           └────────────┘    └──────┬─────┘
                                    ▲
                                    │
                              implements
                                    │
                           ┌────────┴──────────┐
                           │ JSON File Adapter │
                           │  json_file_repo   │
                           └────────┬──────────┘
                                    │
                                    ▼
                               users.json
```

Arah dependency menjadi lebih terkontrol:

```text
CLI
 ↓
Services
 ↓
Domain

Services
 ↓
Repository Interface
 ↑
JSON Repository Adapter
 ↓
users.json
```

Service tidak bergantung langsung kepada `users.json`.

---

# 5. Perubahan Dependency

Sebelum refactoring:

```text
CLI
 ↓
Business Logic
 ↓
JSON File
```

Business logic mengetahui detail penyimpanan data.

Setelah refactoring:

```text
CLI
 ↓
Service
 ↓
Repository Interface
 ↑
JSON Adapter
 ↓
JSON File
```

Service hanya mengetahui interface `UserRepository`.

Dengan demikian, implementasi storage dapat diganti tanpa mengubah domain logic dan service.

Contohnya, JSON repository dapat diganti dengan database:

```text
UserRepository
      ▲
      │
 ┌────┴─────┐
 │          │
JSON       Database
Adapter    Adapter
```

Service tetap menggunakan interface yang sama.

---

# 6. Alasan Pembagian Module

Pembagian module dilakukan berdasarkan responsibility.

| Module        | Responsibility                |
| ------------- | ----------------------------- |
| `domain.py`   | Business rules dan validation |
| `ports.py`    | Interface repository          |
| `services.py` | Application/use-case logic    |
| `adapters/`   | Implementasi storage          |
| `cli.py`      | User interface                |
| `tests/`      | Automated testing             |

Pembagian ini membuat setiap module memiliki tanggung jawab yang lebih jelas dan mengurangi ketergantungan antarbagian.

---

# 7. Manfaat Struktur Akhir

Beberapa manfaat setelah refactoring:

### 1. Lebih mudah dipahami

Setiap module mempunyai responsibility yang jelas sehingga developer dapat mencari kode sesuai kebutuhannya.

### 2. Lebih mudah diuji

Domain logic dan service dapat diuji tanpa harus menggunakan file JSON.

### 3. Storage lebih mudah diganti

Implementasi JSON dapat diganti dengan database atau storage lain tanpa mengubah business logic.

### 4. Dependency lebih terkontrol

Service bergantung pada interface repository, bukan langsung pada implementasi storage.

### 5. Lebih mudah dikembangkan

Jika aplikasi bertambah besar, module baru dapat ditambahkan tanpa membuat satu file menjadi terlalu kompleks.

---

# 8. Testing

Project menggunakan `pytest`.

Untuk menjalankan seluruh test:

```bash
pytest
```

Test dipisahkan berdasarkan responsibility:

```text
test_domain.py
    ↓
Domain/business rules

test_services.py
    ↓
Application logic

test_json_file_repo.py
    ↓
Storage adapter
```

Service menggunakan repository sederhana/in-memory saat testing sehingga tidak bergantung pada file JSON.

---

# 9. Kesimpulan

Refactoring mengubah aplikasi yang awalnya memiliki responsibility yang tercampur menjadi beberapa module dengan tanggung jawab yang lebih jelas.

Domain logic dipisahkan dari storage dan CLI. Storage diakses melalui repository interface sehingga dependency menjadi lebih fleksibel.

Struktur akhir membuat aplikasi lebih mudah dipahami, diuji, dikembangkan, dan memungkinkan implementasi storage diganti tanpa mengubah business logic.
