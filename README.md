# 🏠 Quản Lý Phòng Trọ

Hệ thống quản lý phòng trọ: phòng, khách thuê, doanh thu.

**Sinh viên:** Đậu Cao Thanh — MSSV: 2251220276 — Lớp: 22CT2

---

## Tech Stack

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3.11 + Flask |
| Frontend | HTML / CSS / Vanilla JS |
| Database | MySQL 8.0 |
| Container | Docker + Docker Compose |

---

## Tính năng

- 📊 Dashboard tổng quan (số phòng, doanh thu)
- 🚪 Quản lý phòng: thêm, xem, xóa
- 👥 Quản lý khách thuê: thêm, xem, xóa
- 🔗 Endpoint `/health` — health check
- 👤 Trang `/about` — thông tin sinh viên

---

## Chạy với Docker Compose

```bash
# 1. Clone repo
git clone <your-repo-url>
cd phong-tro

# 2. Copy env
cp backend/.env.example backend/.env

# 3. Chạy toàn bộ hệ thống
docker compose up --build -d

# 4. Truy cập
#   Frontend : http://localhost:3000
#   Backend  : http://localhost:5000
#   Health   : http://localhost:5000/health
#   About    : http://localhost:5000/about
```

---

## API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/about` | Thông tin sinh viên |
| GET | `/api/rooms` | Lấy danh sách phòng |
| POST | `/api/rooms` | Thêm phòng mới |
| PUT | `/api/rooms/:id` | Cập nhật phòng |
| DELETE | `/api/rooms/:id` | Xóa phòng |
| GET | `/api/tenants` | Lấy danh sách khách thuê |
| POST | `/api/tenants` | Thêm khách thuê |
| DELETE | `/api/tenants/:id` | Xóa khách thuê |
| GET | `/api/stats` | Thống kê tổng quan |

---

## Docker Hub

```bash
# Build & push backend
docker build -t daucaothanh/phongtro-backend ./backend
docker push daucaothanh/phongtro-backend

# Build & push frontend
docker build -t daucaothanh/phongtro-frontend ./frontend
docker push daucaothanh/phongtro-frontend
```
