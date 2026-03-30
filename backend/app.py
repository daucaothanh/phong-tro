from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_db_connection
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

APP_NAME = os.getenv("APP_NAME", "Quản Lý Phòng Trọ")

# ═══════════════════════════════════════════════
#  HEALTH CHECK
# ═══════════════════════════════════════════════
@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ═══════════════════════════════════════════════
#  ABOUT
# ═══════════════════════════════════════════════
@app.route("/about")
def about():
    return jsonify({
        "app_name": APP_NAME,
        "description": "Hệ thống quản lý phòng trọ: phòng, khách thuê",
        "developer": {
            "full_name": "Đậu Cao Thanh",
            "student_id": "2251220276",
            "class": "22CT2"
        }
    })

# ═══════════════════════════════════════════════
#  ROOMS - GET ALL
# ═══════════════════════════════════════════════
@app.route("/api/rooms", methods=["GET"])
def get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rooms ORDER BY room_number")
    rooms = cursor.fetchall()
    cursor.close()
    conn.close()
    # convert Decimal -> float for JSON
    for r in rooms:
        r["price"] = float(r["price"])
    return jsonify(rooms)

# ═══════════════════════════════════════════════
#  ROOMS - ADD
# ═══════════════════════════════════════════════
@app.route("/api/rooms", methods=["POST"])
def add_room():
    data = request.get_json()
    room_number = data.get("room_number", "").strip()
    floor       = data.get("floor")
    area        = data.get("area")
    price       = data.get("price")
    status      = data.get("status", "available")
    description = data.get("description", "")

    if not all([room_number, floor, area, price]):
        return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO rooms (room_number, floor, area, price, status, description) VALUES (%s,%s,%s,%s,%s,%s)",
            (room_number, floor, area, price, status, description)
        )
        conn.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Thêm phòng thành công", "id": new_id}), 201

# ═══════════════════════════════════════════════
#  ROOMS - UPDATE
# ═══════════════════════════════════════════════
@app.route("/api/rooms/<int:room_id>", methods=["PUT"])
def update_room(room_id):
    data  = request.get_json()
    price  = data.get("price")
    status = data.get("status")
    description = data.get("description", "")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE rooms SET price=%s, status=%s, description=%s WHERE id=%s",
        (price, status, description, room_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Cập nhật phòng thành công"})

# ═══════════════════════════════════════════════
#  ROOMS - DELETE
# ═══════════════════════════════════════════════
@app.route("/api/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM rooms WHERE id=%s", (room_id,))
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Xóa phòng thành công"})

# ═══════════════════════════════════════════════
#  TENANTS - GET ALL
# ═══════════════════════════════════════════════
@app.route("/api/tenants", methods=["GET"])
def get_tenants():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.*, r.room_number
        FROM tenants t
        LEFT JOIN rooms r ON t.room_id = r.id
        ORDER BY t.created_at DESC
    """)
    tenants = cursor.fetchall()
    cursor.close()
    conn.close()
    # convert date -> string
    for t in tenants:
        if t["start_date"]:
            t["start_date"] = str(t["start_date"])
        if t["end_date"]:
            t["end_date"] = str(t["end_date"])
        if t["created_at"]:
            t["created_at"] = str(t["created_at"])
    return jsonify(tenants)

# ═══════════════════════════════════════════════
#  TENANTS - ADD
# ═══════════════════════════════════════════════
@app.route("/api/tenants", methods=["POST"])
def add_tenant():
    data       = request.get_json()
    full_name  = data.get("full_name", "").strip()
    phone      = data.get("phone", "").strip()
    cccd       = data.get("cccd", "").strip()
    room_id    = data.get("room_id")
    start_date = data.get("start_date")

    if not all([full_name, phone, cccd, start_date]):
        return jsonify({"error": "Thiếu thông tin bắt buộc"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tenants (full_name, phone, cccd, room_id, start_date) VALUES (%s,%s,%s,%s,%s)",
            (full_name, phone, cccd, room_id if room_id else None, start_date)
        )
        # update room status -> occupied
        if room_id:
            cursor.execute("UPDATE rooms SET status='occupied' WHERE id=%s", (room_id,))
        conn.commit()
        new_id = cursor.lastrowid
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Thêm khách thuê thành công", "id": new_id}), 201

# ═══════════════════════════════════════════════
#  TENANTS - DELETE
# ═══════════════════════════════════════════════
@app.route("/api/tenants/<int:tenant_id>", methods=["DELETE"])
def delete_tenant(tenant_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # get room_id before delete
    cursor.execute("SELECT room_id FROM tenants WHERE id=%s", (tenant_id,))
    row = cursor.fetchone()
    cursor.execute("DELETE FROM tenants WHERE id=%s", (tenant_id,))
    if row and row["room_id"]:
        cursor.execute("UPDATE rooms SET status='available' WHERE id=%s", (row["room_id"],))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Xóa khách thuê thành công"})

# ═══════════════════════════════════════════════
#  STATS
# ═══════════════════════════════════════════════
@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) as total FROM rooms")
    total = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as cnt FROM rooms WHERE status='available'")
    available = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM rooms WHERE status='occupied'")
    occupied = cursor.fetchone()["cnt"]
    cursor.execute("SELECT COUNT(*) as cnt FROM tenants")
    tenants = cursor.fetchone()["cnt"]
    cursor.execute("SELECT SUM(price) as rev FROM rooms WHERE status='occupied'")
    revenue = cursor.fetchone()["rev"] or 0
    cursor.close()
    conn.close()
    return jsonify({
        "total_rooms": total,
        "available": available,
        "occupied": occupied,
        "total_tenants": tenants,
        "monthly_revenue": float(revenue)
    })

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
