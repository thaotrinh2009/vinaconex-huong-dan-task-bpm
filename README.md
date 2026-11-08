# Hướng dẫn sử dụng Base — Vinaconex

Trang chính `index.html` có 4 tab:

| Tab | Nguồn | Nội dung |
|---|---|---|
| Task | `task/index.html` | Hướng dẫn task.base.vn: 8 bước theo 4 vai trò (ủy quyền, giao việc vào Phòng, giao việc lặp lại bằng Lịch trình, quyền người theo dõi, nộp – duyệt, theo dõi việc đã giao, đánh giá), tra cứu 29 tình huống, song ngữ VI/EN |
| BPM · Quy trình phê duyệt | `bpm/index.html` | Hướng dẫn bpm.base.vn: 8 bước theo 4 vai trò (người đề xuất, người xử lý, lãnh đạo duyệt, quản trị) trên 3 quy trình thật (Cấp thiết bị CNTT, Thanh toán CP văn phòng – CBNV, Yêu cầu vật tư có AI), tra cứu 26 tình huống, song ngữ VI/EN |
| E-office · Công văn đến, đi | `eoffice/index.html` | Công văn đến 6 bước, công văn đi 7 bước, ảnh chụp thật có đánh số |
| Booking · Đặt xe, phòng họp | `booking/index.html` | Đặt xe 8 bước, đặt phòng họp 7 bước trên Booking, BPM, Task |

Mở thẳng một tab: thêm `#task`, `#bpm`, `#eoffice` hoặc `#booking` vào cuối địa chỉ.

## Sửa nội dung
1. Sửa `task/index.html`, `eoffice/index.html` hoặc `booking/index.html` (trang E-office dựng từ `eoffice/src/`, chạy `python3 eoffice/src/build.py`; trang Task dựng từ `task/src/`, trang BPM dựng từ `bpm/src/` — sửa `content.py`, ảnh gốc để ở `<app>/src/img/`, chạy `annos.py` rồi `build.py`, chép `out/index.html` thành `<app>/index.html`).
2. Chạy `python3 build_tabs.py` để gộp lại thành `index.html`.
3. Đẩy lên GitHub. Vercel/GitHub Pages tự cập nhật.

`index.html` chứa sẵn cả 3 trang và toàn bộ ảnh, nên cũng có thể tải riêng file này lên Vercel.
