# Hướng dẫn sử dụng Base — Vinaconex

Trang chính `index.html` có 3 tab:

| Tab | Nguồn | Nội dung |
|---|---|---|
| App Công việc | `task/index.html` | Hướng dẫn task.base.vn: 8 bước theo 4 vai trò (ủy quyền, giao việc vào Phòng, nộp – duyệt, theo dõi việc đã giao, đánh giá), tra cứu 27 tình huống, song ngữ VI/EN |
| E-office · Công văn đến, đi | `eoffice/index.html` | Công văn đến 6 bước, công văn đi 7 bước, ảnh chụp thật có đánh số |
| Booking · Đặt xe, phòng họp | `booking/index.html` | Đặt xe 8 bước, đặt phòng họp 7 bước trên Booking, BPM, Task |

Mở thẳng một tab: thêm `#task`, `#eoffice` hoặc `#booking` (link cũ `#bpm` tự chuyển sang `#task`) vào cuối địa chỉ.

## Sửa nội dung
1. Sửa `task/index.html`, `eoffice/index.html` hoặc `booking/index.html` (trang E-office dựng từ `eoffice/src/`, chạy `python3 eoffice/src/build.py`).
2. Chạy `python3 build_tabs.py` để gộp lại thành `index.html`.
3. Đẩy lên GitHub. Vercel/GitHub Pages tự cập nhật.

`index.html` chứa sẵn cả 3 trang và toàn bộ ảnh, nên cũng có thể tải riêng file này lên Vercel.
