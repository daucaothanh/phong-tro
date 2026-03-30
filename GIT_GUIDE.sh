# HƯỚNG DẪN GIT — DEVOPS MINI PROJECT
# Sinh viên: Đậu Cao Thanh | MSSV: 2251220276 | Lớp: 22CT2
# =============================================================

# ──────────────────────────────────────────────
# BƯỚC 1: Khởi tạo Git & tạo repo trên GitHub
# ──────────────────────────────────────────────
# Vào thư mục project
cd phong-tro

# Khởi tạo git
git init

# Thêm remote (thay YOUR_USERNAME bằng GitHub username của bạn)
git remote add origin https://github.com/YOUR_USERNAME/phong-tro.git

# ──────────────────────────────────────────────
# BƯỚC 2: Branch MAIN — commit đầu tiên
# ──────────────────────────────────────────────
git checkout -b main

git add .
git commit -m "feat: initial project structure - Flask + MySQL + Docker"

git push -u origin main

# ──────────────────────────────────────────────
# BƯỚC 3: Branch DEVELOP
# ──────────────────────────────────────────────
git checkout -b develop

# (Chỉnh sửa nhỏ, ví dụ thêm comment vào app.py, hoặc update README)
# Sau đó commit:
git add .
git commit -m "feat: add database seed data and update README"

git push -u origin develop

# ──────────────────────────────────────────────
# BƯỚC 4: Branch FEATURE/rooms
# ──────────────────────────────────────────────
git checkout -b feature/rooms

# (Ví dụ thêm field mới hoặc sửa gì đó trong rooms API)
git add backend/app.py
git commit -m "feat: add room stats endpoint /api/stats"

git push -u origin feature/rooms

# ──────────────────────────────────────────────
# BƯỚC 5: Branch FEATURE/tenants
# ──────────────────────────────────────────────
git checkout -b feature/tenants

git add backend/app.py frontend/index.html
git commit -m "feat: add tenant management - POST and DELETE endpoints"

git push -u origin feature/tenants

# ──────────────────────────────────────────────
# BƯỚC 6: Merge feature -> develop -> main
# ──────────────────────────────────────────────
git checkout develop
git merge feature/rooms
git merge feature/tenants
git push origin develop
git commit -m "chore: merge feature branches into develop" --allow-empty

git checkout main
git merge develop
git commit -m "release: v1.0.0 - full phong tro management system"
git push origin main

# ──────────────────────────────────────────────
# KIỂM TRA — phải có ít nhất:
# ✅ 5+ commits
# ✅ 3+ branches: main, develop, feature/rooms (hoặc feature/tenants)
# ──────────────────────────────────────────────
git log --oneline --all
git branch -a
