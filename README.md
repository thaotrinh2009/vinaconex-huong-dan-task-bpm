# Hướng dẫn sử dụng Base — Vinaconex

Trang chính `index.html` có 2 tab:

| Tab | Nguồn | Nội dung |
|---|---|---|
| App Công việc & BPM | `bpm/index.html` | Hướng dẫn task.base.vn và bpm.base.vn (song ngữ VI/EN) |
| E-office · Công văn đến, đi | `eoffice/index.html` | Công văn đến 6 bước, công văn đi 7 bước, ảnh chụp thật có đánh số |

Mở thẳng một tab: thêm `#bpm` hoặc `#eoffice` vào cuối địa chỉ.

## Sửa nội dung
1. Sửa `bpm/index.html` hoặc `eoffice/index.html` (trang E-office dựng từ `eoffice/src/`, chạy `python3 eoffice/src/build.py`).
2. Chạy `python3 build_tabs.py` để gộp lại thành `index.html`.
3. Đẩy lên GitHub. Vercel/GitHub Pages tự cập nhật.

`index.html` chứa sẵn cả 2 trang và toàn bộ ảnh, nên cũng có thể tải riêng file này lên Vercel.
