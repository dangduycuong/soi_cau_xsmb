import json
import os
import re
import urllib.request

LOCAL_JSON_FILE = 'xsmb_result.json'
MINH_NGOC_URL = 'https://minhngoc.net'

def fetch_and_update_from_minhngoc():
    if not os.path.exists(LOCAL_JSON_FILE):
        print(f"Không tìm thấy file {LOCAL_JSON_FILE}")
        return

    with open(LOCAL_JSON_FILE, 'r', encoding='utf-8') as f:
        local_data = json.load(f)

    last_local_date = local_data[-1]['date'][:10] if local_data else ""
    print(f"Ngày mới nhất hiện có trong file JSON: {last_local_date}")

    req = urllib.request.Request(
        MINH_NGOC_URL,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }
    )

    with urllib.request.urlopen(req, timeout=20) as response:
        html = response.read().decode('utf-8', errors='ignore')

    # Tách theo từng bảng kết quả (bắt đầu từ class="bkqtinhmienbac")
    tables = html.split('class="bkqtinhmienbac"')
    print(f"Tìm thấy {len(tables) - 1} bảng kết quả trên trang Minh Ngọc.")
    new_records = []

    for table in tables[1:]:
        # Tìm ngày quay thưởng dạng dd/mm/yyyy
        date_match = re.search(r'(\d{2})/(\d{2})/(\d{4})', table)
        if not date_match:
            continue

        day, month, year = date_match.groups()
        iso_date_prefix = f"{year}-{month}-{day}"

        if iso_date_prefix <= last_local_date:
            continue

        def get_prize_2digits(css_class):
            m = re.search(rf'class="{css_class}"[^>]*>(.*?)</td>', table, re.DOTALL)
            if not m:
                return []
            # Lấy tất cả các số có 2 đến 5 chữ số bên trong ô giải
            nums = re.findall(r'\b\d{2,5}\b', re.sub(r'<[^>]+>', ' ', m.group(1)))
            return [int(n[-2:]) for n in nums]

        db = get_prize_2digits('giaidb')
        g1 = get_prize_2digits('giai1')
        g2 = get_prize_2digits('giai2')
        g3 = get_prize_2digits('giai3')
        g4 = get_prize_2digits('giai4')
        g5 = get_prize_2digits('giai5')
        g6 = get_prize_2digits('giai6')
        g7 = get_prize_2digits('giai7')

        print(f"Kiểm tra ngày {iso_date_prefix}: ĐB={db}, G1={g1}, G7={g7}")

        if (len(db) == 1 and len(g1) == 1 and len(g2) == 2 and len(g3) == 6 and
                len(g4) == 4 and len(g5) == 6 and len(g6) == 3 and len(g7) == 4):
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
        new_records.sort(key=lambda x: x['date'])
        local_data.extend(new_records)
        with open(LOCAL_JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(local_data, f, indent=4)
        print(f"THÀNH CÔNG! Đã thêm {len(new_records)} ngày mới vào {LOCAL_JSON_FILE}.")
    else:
        print("Không có bản ghi mới hợp lệ để thêm.")

if __name__ == '__main__':
    fetch_and_update_from_minhngoc()
