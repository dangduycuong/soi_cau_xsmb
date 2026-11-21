import json
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import re

JSON_FILE = 'xsmb_result.json'
# Nguồn RSS chính thức cập nhật kết quả XSMB hàng ngày
RSS_URL = 'https://xskt.com.vn'

def parse_rss_and_update():
    if not os.path.exists(JSON_FILE):
        print(f"Không tìm thấy file {JSON_FILE}")
        return

    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Lấy ngày mới nhất hiện có trong file JSON
    last_entry_date = data[-1]['date'][:10] if data else ""

    # Tải dữ liệu RSS
    req = urllib.request.Request(RSS_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as response:
        xml_data = response.read().decode('utf-8')

    root = ET.fromstring(xml_data)
    items = root.findall('./channel/item')

    new_records = []
    for item in items:
        title = item.find('title').text or ''
        desc = item.find('description').text or ''

        # Trích xuất ngày từ tiêu đề (vd: "KẾT QUẢ XỔ SỐ MIỀN BẮC NGÀY 21/11/2026")
        date_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', title)
        if not date_match:
            continue

        day, month, year = date_match.groups()
        iso_date_prefix = f"{year}-{month}-{day}"

        # Bỏ qua nếu ngày này đã có trong file JSON
        if iso_date_prefix <= last_entry_date:
            continue

        # Trích xuất các giải từ phần mô tả RSS
        def get_nums(pattern):
            m = re.search(pattern, desc)
            if not m:
                return []
            # Lấy 2 số cuối của từng giải
            raw_nums = re.findall(r'\d+', m.group(1))
            return [int(n[-2:]) for n in raw_nums]

        db = get_nums(r'ĐB:\s*([\d\s-]+)')
        g1 = get_nums(r'1:\s*([\d\s-]+)')
        g2 = get_nums(r'2:\s*([\d\s-]+)')
        g3 = get_nums(r'3:\s*([\d\s-]+)')
        g4 = get_nums(r'4:\s*([\d\s-]+)')
        g5 = get_nums(r'5:\s*([\d\s-]+)')
        g6 = get_nums(r'6:\s*([\d\s-]+)')
        g7 = get_nums(r'7:\s*([\d\s-]+)')

        # Chỉ lưu khi đã quay đủ tất cả 27 giải
        if len(db) == 1 and len(g1) == 1 and len(g2) == 2 and len(g3) == 6 and \
           len(g4) == 4 and len(g5) == 6 and len(g6) == 3 and len(g7) == 4:
            record = {
                "date": f"{iso_date_prefix}T00:00:00.000",
                "special": db[0],
                "prize1": g1[0],
                "prize2_1": g2[0], "prize2_2": g2[1],
                "prize3_1": g3[0], "prize3_2": g3[1], "prize3_3": g3[2],
                "prize3_4": g3[3], "prize3_5": g3[4], "prize3_6": g3[5],
                "prize4_1": g4[0], "prize4_2": g4[1], "prize4_3": g4[2], "prize4_4": g4[3],
                "prize5_1": g5[0], "prize5_2": g5[1], "prize5_3": g5[2],
                "prize5_4": g5[3], "prize5_5": g5[4], "prize5_6": g5[5],
                "prize6_1": g6[0], "prize6_2": g6[1], "prize6_3": g6[2],
                "prize7_1": g7[0], "prize7_2": g7[1], "prize7_3": g7[2], "prize7_4": g7[3]
            }
            new_records.append(record)

    if new_records:
        # Sắp xếp từ cũ đến mới rồi nối vào cuối file JSON
        new_records.sort(key=lambda x: x['date'])
        data.extend(new_records)
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Đã cập nhật thêm {len(new_records)} ngày mới!")
    else:
        print("Chưa có kết quả ngày mới hoặc dữ liệu đã là mới nhất.")

if __name__ == '__main__':
    parse_rss_and_update()
