# API Kết Quả Xổ Số Miền Bắc (XSMB JSON API) - Tự Động Cập Nhật Hàng Ngày

Kho lưu trữ dữ liệu mở cung cấp **API Kết quả Xổ số Miền Bắc (XSMB)** định dạng **JSON** (2 số cuối từ Giải Đặc Biệt đến Giải Bảy), được tự động cập nhật hàng ngày lúc **18:35** ngay sau giờ quay thưởng.

Dữ liệu phù hợp cho các lập trình viên làm ứng dụng di động (Flutter, React Native, Android, iOS), website thống kê, soi cầu, phân tích dữ liệu (Data Analysis) hoặc nghiên cứu xác suất.

---

## 🔗 Link API JSON Trực Tiếp (Miễn phí - Không giới hạn)

Bạn có thể gọi trực tiếp đường dẫn Raw dưới đây bằng phương thức `GET` mà không cần API Key:

```text
https://githubusercontent.com
```

---

## 📋 Cấu trúc dữ liệu JSON (2 số cuối các giải)

Mỗi phần tử trong mảng JSON đại diện cho kết quả mở thưởng của một ngày (sắp xếp từ cũ nhất đến mới nhất):

```json
{
    "date": "2026-11-20T00:00:00.000",
    "special": 60,
    "prize1": 87,
    "prize2_1": 78,
    "prize2_2": 92,
    "prize3_1": 28,
    "prize3_2": 26,
    "prize3_3": 60,
    "prize3_4": 19,
    "prize3_5": 87,
    "prize3_6": 44,
    "prize4_1": 17,
    "prize4_2": 20,
    "prize4_3": 9,
    "prize4_4": 92,
    "prize5_1": 96,
    "prize5_2": 84,
    "prize5_3": 94,
    "prize5_4": 89,
    "prize5_5": 51,
    "prize5_6": 92,
    "prize6_1": 49,
    "prize6_2": 84,
    "prize6_3": 2,
    "prize7_1": 68,
    "prize7_2": 95,
    "prize7_3": 46,
    "prize7_4": 19
}
```

---

## ⚙️ Cơ chế hoạt động

* **Nguồn dữ liệu:** Lịch sử đầy đủ từ năm 2005 đến nay.
* **Tự động hóa:** Sử dụng **GitHub Actions** tự động thu thập và cập nhật kết quả mới nhất vào lúc **18:35 - 18:50** mỗi ngày.
* **Giấy phép:** Mã nguồn mở (Public), tự do sử dụng cho mục đích cá nhân và học tập.
