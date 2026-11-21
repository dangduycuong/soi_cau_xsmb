import json
import os
import re
import urllib.request

LOCAL_JSON_FILE = 'xsmb_result.json'
MINH_NGOC_URL = 'https://www.minhngoc.net/ket-qua-xo-so/mien-bac.html'

def fetch_and_update_from_minhngoc():
    if not os.path.exists(LOCAL_JSON_FILE):
        print(f"Không tìm thấy file {LOCAL_JSON_FILE}")
        return

    with open(LOCAL_JSON_FILE, 'r', encoding='utf-8') as f:
        local_data = json.load(f)

    # Lấy ngày mới nhất hiện đang có trong file của bạn (vd: "2026-11-20")
    last_local_date = local_data[-1]['date'][:10] if local_data else ""
    print(f"Ngày mới nhất hiện có trong file JSON: {last_local_date}")

    req = urllib.request.Request(
        MINH_NGOC_URL,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        html = response.read().decode('utf-8', errors='ignore')

    # Tách từng khối bảng kết quả theo ngày trên trang Minh Ngọc
    blocks = html.split('KẾT QUẢ XỔ SỐ Miền Bắc - ')
    new_records = []

    for block in blocks[1:]:
        # 1. Lấy ngày quay thưởng (vd: 21/11/2026)
        date_match = re.search(r'^(\d{2})/(\d{2})/(\d{4})', block)
        if not date_match:
            continue

        day, month, year = date_match.groups()
        iso_date_prefix = f"{year}-{month}-{day}"

        # Bỏ qua nếu ngày này đã có trong file JSON
        if iso_date_prefix <= last_local_date:
            continue

        # 2. Cắt phần nội dung của riêng ngày này (dừng trước nút Xem Bảng Loto)
        table_part = block.split('Xem Bảng Loto')[0]
        # Loại bỏ toàn bộ thẻ HTML để lấy chuỗi văn bản sạch
        clean_text = re.sub(r'<[^>]+>', ' ', table_part)
        clean_text = re.sub(r'\s+', ' ', clean_text)

        def extract_2digits(start_label, end_label):
            pattern = rf'{start_label}\s*(.*?)\s*{end_label}'
            m = re.search(pattern, clean_text)
            if not m:
                return []
            nums = re.findall(r'\b\d{2,5}\b', m.group(1))
            return [int(n[-2:]) for n in nums]

        db = extract_2digits('Giải ĐB', 'Giải nhất')
        g1 = extract_2digits('Giải nhất', 'Giải nhì')
        g2 = extract_2digits('Giải nhì', 'Giải ba')
        g3 = extract_2digits('Giải ba', 'Giải tư')
        g4 = extract_2digits('Giải tư', 'Giải năm')
        g5 = extract_2digits('Giải năm', 'Giải sáu')
        g6 = extract_2digits('Giải sáu', 'Giải bảy')
        g7 = extract_2digits('Giải bảy', 'Normal')

        # Chỉ lưu khi đã quay xong đủ 27 giải (tránh lưu dở dang lúc đang quay)
        if (len(db) == 1 and len(g1) == 1 and len(g2) == 2 and len(g3) == 6 and
                len(g4) == 4 and len(g5) == 6 and len(g6) == 3 and len(g7) == 4):
            record = {
                "date": f"{iso_date_prefix}T00:00:00.000",
                "special": db,
                "prize1": g1,
                "prize2_1": g2, "prize2_2": g2,
                "prize3_1": g3, "prize3_2": g3, "prize3_3": g3,
                "prize3_4": g3, "prize3_5": g3, "prize3_6": g3,
                "prize4_1": g4, "prize4_2": g4, "prize4_3": g4, "prize4_4": g4,
                "prize5_1": g5, "prize5_2": g5, "prize5_3": g5,
                "prize5_4": g5, "prize5_5": g5, "prize5_6": g5,
                "prize6_1": g6, "prize6_2": g6, "prize6_3": g6,
                "prize7_1": g7, "prize7_2": g7, "prize7_3": g7, "prize7_4": g7
            }
            new_records.append(record)
            print(f"Đã bóc tách thành công ngày {iso_date_prefix} (ĐB: {db:02d})")

    if new_records:
        new_records.sort(key=lambda x: x['date'])
        local_data.extend(new_records)
        with open(LOCAL_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(local_data, f, indent=4)
        print(f"Hoàn tất! Đã thêm {len(new_records)} ngày mới vào {LOCAL_JSON_FILE}.")
    else:
        print("Chưa có kết quả ngày mới hoặc dữ liệu đã cập nhật đủ.")

if __name__ == '__main__':
    fetch_and_update_from_minhngoc()
