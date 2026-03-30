CREATE DATABASE IF NOT EXISTS phongtro_db;
USE phongtro_db;

CREATE TABLE IF NOT EXISTS rooms (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_number VARCHAR(20)  NOT NULL UNIQUE,
    floor       INT          NOT NULL DEFAULT 1,
    area        FLOAT        NOT NULL,
    price       DECIMAL(12,0) NOT NULL,
    status      ENUM('available','occupied','maintenance') DEFAULT 'available',
    description TEXT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tenants (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    full_name   VARCHAR(100) NOT NULL,
    phone       VARCHAR(15)  NOT NULL,
    cccd        VARCHAR(20)  NOT NULL UNIQUE,
    room_id     INT,
    start_date  DATE         NOT NULL,
    end_date    DATE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE SET NULL
);

-- Seed data mẫu
INSERT INTO rooms (room_number, floor, area, price, status, description) VALUES
('P101', 1, 20.0, 2500000, 'occupied',   'Phòng có gác lửng, ban công'),
('P102', 1, 18.0, 2200000, 'available',  'Phòng tiêu chuẩn, cửa sổ thoáng'),
('P201', 2, 22.0, 2800000, 'occupied',   'Phòng rộng, có bếp riêng'),
('P202', 2, 18.0, 2200000, 'maintenance','Đang sửa chữa điện'),
('P301', 3, 25.0, 3200000, 'available',  'Phòng view đẹp, tầng cao');

INSERT INTO tenants (full_name, phone, cccd, room_id, start_date) VALUES
('Nguyễn Văn An',   '0901234567', '079201001234', 1, '2024-01-15'),
('Trần Thị Bích',   '0912345678', '079202005678', 3, '2024-03-01');
