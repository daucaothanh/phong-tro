# HƯỚNG DẪN PUSH DOCKER HUB
# Docker Hub username: daucaothanh
# =============================================

# 1. Đăng nhập Docker Hub
docker login

# 2. Build & Push BACKEND
docker build -t daucaothanh/phongtro-backend:latest ./backend
docker push daucaothanh/phongtro-backend:latest

# 3. Build & Push FRONTEND
docker build -t daucaothanh/phongtro-frontend:latest ./frontend
docker push daucaothanh/phongtro-frontend:latest

# 4. Kiểm tra images
docker images | grep daucaothanh

# ── Chạy từ Docker Hub (không cần build local) ──
# docker pull daucaothanh/phongtro-backend:latest
# docker pull daucaothanh/phongtro-frontend:latest
