# Hướng dẫn sử dụng Base — Vinaconex

| Trang | Đường dẫn | Nội dung |
|---|---|---|
| App Công việc & BPM | `/` (`index.html`) | Hướng dẫn 1 trang (song ngữ VI/EN) cho task.base.vn và bpm.base.vn |
| E-office VPTCT | `/eoffice` (`eoffice/index.html`) | Xử lý Công văn đến (6 bước) và Công văn đi (7 bước) theo vai trò, ảnh chụp thật có đánh số thao tác |

Deploy: import repo này vào Vercel → Deploy.

## Cập nhật trang E-office
- `eoffice/anh/`: 25 ảnh chụp màn hình E-office (1568×746).
- `eoffice/src/data.py`: nội dung từng bước, vai trò, link E-office.
- `eoffice/src/coords.py`: vị trí ghim số trên từng ảnh.
- Chạy `python3 eoffice/src/build.py` để dựng lại `eoffice/index.html`.
