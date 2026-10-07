# -*- coding: utf-8 -*-
E = 'https://eoffice.base.vn'
L = dict(
    in_k=E + '/incoming/aF7kRgc9-eJekthpi5S-6aqNTQcFxK8',
    in_new=E + '/create?service_id=aF7kRgc9-eJekthpi5S-6aqNTQcFxK8&type=incoming',
    out_k=E + '/outgoing/aF7r5dEr-Qbfb67UgOH-m7dALsEQ75h',
    out_new=E + '/create?service_id=aF7r5dEr-Qbfb67UgOH-m7dALsEQ75h&type=outgoing',
    docs=E + '/docs', appr=E + '/approvals', cnt=E + '/counter-requests',
    d_in=E + '/document/aF8rnlfE-02ALZJzaWQ-gCwzyukFbhP',
    d_reply=E + '/document/aF8zCCJ4-RdBWBkzBkI-Jhen2MnZWAE',
    d_sign=E + '/document/aF8ytRzh-LeWmFrjRAq-FzW2YO6zxkR',
    d_num=E + '/document/aF7r7XWq-wjIKEfWYdz-PDbvNl765Fn',
)

SHOT = {
    '01': ('01-den-kanban.jpg', 'Kanban VPTCT - Công văn đến', 'in_k'),
    '02': ('02-den-tao-1.jpg', 'Form tạo văn bản đến, phần đầu', 'in_new'),
    '03': ('03-den-tao-2.jpg', 'Form tạo văn bản đến, người gửi và phân loại', 'in_new'),
    '04': ('04-den-tao-3.jpg', 'Form tạo văn bản đến, trường tùy chỉnh', 'in_new'),
    '05': ('05-den-tao-4.jpg', 'Form tạo văn bản đến, tệp đính kèm', 'in_new'),
    '06': ('06-den-thuky.jpg', 'Văn bản 2/2026 ở bước Thư ký tiếp nhận', 'd_in'),
    '07': ('07-den-danhso.jpg', 'Kết quả Đánh số VB của văn bản 2/2026', 'd_in'),
    '08': ('08-den-chitiet.jpg', 'Chi tiết văn bản 2/2026', 'd_in'),
    '09': ('09-den-tep.jpg', 'Trường tùy chỉnh và tệp đính kèm', 'd_in'),
    '10': ('10-den-congviec.jpg', 'Công việc, Lưu hồ sơ và thẻ', 'd_in'),
    '11': ('11-den-butphe.jpg', 'Màn hình Bút phê', 'd_in'),
    '12': ('12-den-chuyenbuoc.jpg', 'Menu Chuyển bước', 'd_in'),
    '13': ('13-den-phancong.jpg', 'Hộp Phân công người thực hiện', 'd_in'),
    '14': ('14-vanban.jpg', 'Danh sách Văn bản', 'docs'),
    '15': ('15-pheduyet.jpg', 'Phê duyệt & Ký', 'appr'),
    '16': ('16-di-kanban.jpg', 'Kanban VPTCT - Công văn đi', 'out_k'),
    '17': ('17-di-tao-1.jpg', 'Form tạo văn bản đi, phần đầu', 'out_new'),
    '18': ('18-di-tao-2.jpg', 'Form tạo văn bản đi, phân loại và tệp', 'out_new'),
    '19': ('19-di-soan.jpg', 'Bản phúc đáp ở bước Soạn công văn', 'd_reply'),
    '20': ('20-di-tep.jpg', 'Đính kèm bản thảo, văn bản liên quan', 'd_reply'),
    '21': ('21-di-bldky.jpg', 'Văn bản "Hợp đồng" ở bước BLĐ ký', 'd_sign'),
    '22': ('22-di-kydt.jpg', 'Mục Ký điện tử của văn bản', 'd_sign'),
    '23': ('23-di-xemxet.jpg', 'Kết quả xem xét của Lãnh đạo Ban và Thư ký', 'd_sign'),
    '24': ('24-di-capso.jpg', 'Văn bản ở bước Cấp số', 'd_num'),
    '25': ('25-socapso.jpg', 'Sổ cấp số › Yêu cầu cấp số', 'cnt'),
}

ROLES = {
    'vanthu': ('Văn thư', 'Tiếp nhận văn bản đến, cấp số văn bản đi'),
    'thuky': ('Thư ký', 'Xem xét, bút phê, chuyển lãnh đạo'),
    'lanhdao': ('Lãnh đạo', 'Bút phê, cho ý kiến, ký'),
    'donvi': ('Đơn vị chủ trì', 'Thực hiện, giao việc, phúc đáp'),
    'nguoisoan': ('Người soạn', 'Soạn văn bản đi, trình ký'),
    'quantri': ('Người phụ trách dịch vụ', 'Toàn quyền, phân công lại khi cần'),
}
ORDER = ['vanthu', 'thuky', 'lanhdao', 'donvi', 'nguoisoan', 'quantri']

# block: (title, shot or None, [(x,y,text)], extra boxes [(x0,y0,x1,y1)])
IN = [
 dict(id='d1', n=1, name='Văn thư tiếp nhận', role='vanthu', sla='8 giờ',
  who='Văn thư. Người tạo văn bản tự thành người phụ trách.',
  form='Form Văn bản đến mới, việc Đánh số VB',
  done='Việc Đánh số VB hoàn tất. Văn bản tự sang Thư ký tiếp nhận.',
  links=[('Kanban Công văn đến', 'in_k'), ('Tạo văn bản đến', 'in_new'), ('Văn bản mẫu 2/2026', 'd_in')],
  rt={'vanthu': 'Tạo văn bản, nhập thông tin, đánh số', 'quantri': 'Sửa thông tin, phân công lại'},
  blocks=[
   ('Mở kanban và bấm Văn bản mới', '01', [
     (41, 100, 'Bấm <b>Văn phòng</b> trên thanh trái.'),
     (219, 320, 'Chọn <b>VPTCT - Công văn đến</b>.'),
     (1460, 90, 'Bấm <b>+ Văn bản mới</b>.'),
     (480, 217, 'Văn bản mới nằm ở cột <b>Văn thư tiếp nhận</b>. Nhãn "Chưa vào sổ" nghĩa là chưa đánh số.')], []),
   ('Nhập trích yếu, hoặc quét bản giấy', '02', [
     (896, 202, 'Có bản giấy: bấm <b>Quét tệp</b> hoặc thả PDF, ảnh vào khung. AI đọc và điền sẵn biểu mẫu, bạn soát lại từng ô.'),
     (655, 345, 'Nhập <b>Tiêu đề / trích yếu</b> của văn bản.'),
     (698, 462, '<b>Người phụ trách</b> tự điền là bạn. Chỉ đổi khi giao cho văn thư khác.'),
     (698, 627, 'Nhập <b>Tóm tắt</b> ngắn, sửa được sau.'),
     (1300, 360, 'Khung bên phải cho biết các bước văn bản sẽ đi qua.')], [(424, 153, 974, 252)]),
   ('Điền người gửi và phân loại', '03', [
     (571, 257, '<b>Mã văn bản gốc</b>: số ký hiệu bên gửi đóng dấu, ví dụ 241/TB-KTHT.'),
     (825, 257, '<b>Ngày tiếp nhận</b>: để trống là hôm nay.'),
     (571, 389, '<b>Người gửi — Tên</b>: cá nhân hoặc đầu mối gửi văn bản.'),
     (825, 389, '<b>Người gửi — Cơ quan</b>.'),
     (528, 646, '<b>Loại văn bản, Mức độ khẩn, Mức độ mật</b>: không bắt buộc, điền sau được.')], []),
   ('Điền trường tùy chỉnh', '04', [
     (698, 244, '<b>Lãnh đạo chỉ đạo</b>, nếu đã biết.'),
     (698, 329, '<b>Lãnh đạo phối hợp</b>, nếu có.'),
     (698, 438, '<b>Yêu cầu giải quyết</b> (bắt buộc).'),
     (698, 555, '<b>Thời hạn hoàn thành</b>.'),
     (698, 640, '<b>Phòng ban chủ trì</b> (bắt buộc). Ô này quyết định ai nhận việc ở bước 4.'),
     (645, 722, '<b>Phòng ban phối hợp</b>: bấm chọn một hoặc nhiều đơn vị.')], [(453, 620, 944, 661)]),
   ('Đính kèm và tạo văn bản', '05', [
     (522, 261, '<b>Chọn tệp</b>: tải bản scan văn bản gốc.'),
     (698, 374, '<b>Thẻ</b>: gõ nhãn rồi Enter. AI có thể gợi ý từ bản quét.'),
     (698, 502, '<b>Ghi chú nội bộ</b> cho người xử lý sau.'),
     (962, 90, 'Bấm <b>Tạo mới</b>.')], []),
   ('Đánh số văn bản', '07', [
     (517, 231, 'Mở văn bản vừa tạo, mở khối bước <b>Văn thư tiếp nhận</b>.'),
     (505, 289, 'Thực hiện việc <b>Đánh số VB</b> (bắt buộc).'),
     (575, 402, 'Kết quả hiện số nội bộ, ví dụ <b>Đã cấp số: 2/2026</b>.'),
     (1407, 289, 'Việc chuyển <b>Hoàn tất</b>, văn bản tự sang Thư ký tiếp nhận.')], []),
  ],
  note='Chọn đúng Phòng ban chủ trì ngay từ đầu. Chọn sai thì việc ở bước 4 giao nhầm đơn vị.'),

 dict(id='d2', n=2, name='Thư ký tiếp nhận', role='thuky', sla='24 giờ',
  who='Thư ký được gán cho văn bản.',
  form='Việc Xem xét và cho ý kiến, việc Bút phê',
  done='Hai việc bắt buộc hoàn tất, bạn bấm Chuyển bước. Văn bản sang BLĐ bút phê.',
  links=[('Văn bản chờ xử lý', 'docs'), ('Văn bản mẫu 2/2026', 'd_in')],
  rt={'thuky': 'Xem xét, bút phê, chọn lãnh đạo, chuyển bước', 'quantri': 'Phân công lại khi Thư ký vắng'},
  blocks=[
   ('Tìm văn bản đang chờ bạn', '14', [
     (219, 193, 'Bấm <b>Văn bản</b> ở menu trái.'),
     (650, 90, 'Tab <b>Đến</b> chỉ hiện văn bản đến.'),
     (418, 148, 'Bộ lọc <b>người xử lý</b>: các văn bản đang giao cho bạn.'),
     (975, 310, 'Cột <b>Giai đoạn</b> cho biết văn bản đang ở bước nào, ví dụ 2/6.')], []),
   ('Xem việc cần làm ở bước Thư ký', '06', [
     (670, 151, 'Thanh bước: bước đang làm tô xanh, bước xong có dấu tích.'),
     (548, 526, '<b>Xem xét và cho ý kiến</b> (bắt buộc): mở việc, ghi ý kiến, hoàn tất.'),
     (1403, 617, '<b>Bút phê</b> (bắt buộc): bấm để ghi ý kiến lên văn bản.'),
     (1355, 409, '<b>Phân công người thực hiện</b>: đổi người làm các việc của bước.'),
     (1366, 90, '<b>Chuyển bước</b> khi mọi việc bắt buộc đã xong.')], []),
   ('Đọc nội dung văn bản', '08', [
     (440, 213, '<b>Tóm tắt AI</b>: bấm Xem thêm để đọc đủ.'),
     (474, 385, '<b>Số tham chiếu gốc</b> của bên gửi.'),
     (1000, 385, '<b>Số nội bộ</b> văn thư đã cấp.'),
     (1000, 484, '<b>Nơi gửi · Cơ quan</b>.'),
     (458, 662, '<b>Trường tùy chỉnh</b>: bấm biểu tượng bút bên phải để sửa.')], []),
   ('Kiểm tra thông tin và mở tệp', '09', [
     (640, 283, 'Kiểm tra <b>Phòng ban chủ trì</b>, Yêu cầu giải quyết, Thời hạn hoàn thành.'),
     (1290, 342, '<b>Xem tài liệu</b>: mở tệp đính kèm.'),
     (1424, 342, '<b>Bút phê</b>: mở trình ghi ý kiến lên văn bản.'),
     (830, 410, 'Danh sách tệp. Bấm <b>Hiển thị</b> để xem từng tệp.')], []),
   ('Ghi bút phê lên văn bản', '11', [
     (408, 26, 'Chuyển giữa các tệp, ví dụ 1/4.'),
     (1512, 118, '<b>Bút (viết)</b>: ghi ý kiến, ký tay.'),
     (1512, 236, '<b>Bút tô</b>: tô dòng cần chú ý.'),
     (1512, 295, '<b>Bình luận</b>: chạm vào từ hoặc kéo chọn đoạn.'),
     (1512, 471, '<b>Tẩy</b>: xoá nét đã vẽ.'),
     (1512, 604, '<b>Giao việc</b> ngay từ văn bản.'),
     (66, 26, 'Bấm <b>Đóng</b> để về trang văn bản.')], []),
   ('Phân công người thực hiện', '13', [
     (500, 304, 'Mỗi việc ghi cách chọn người: Chọn thủ công hoặc theo quy tắc.'),
     (780, 381, 'Gõ tên để thêm người làm việc này.'),
     (1012, 425, '<b>Áp dụng kết quả quy tắc</b>: trả về người theo quy tắc của bước.'),
     (780, 599, 'Việc Bút phê: chọn người bút phê.'),
     (1113, 661, 'Bấm <b>Lưu</b>. Bấm Huỷ nếu không đổi gì.')], []),
   ('Chuyển bước hoặc trả lại', '12', [
     (1366, 90, '<b>Chuyển bước</b>: sang bước kế tiếp.'),
     (1464, 90, 'Bấm mũi tên để mở thêm lựa chọn.'),
     (1300, 143, '<b>Chuyển đến bước</b>: nhảy tới một bước chỉ định.'),
     (1256, 189, '<b>Trả lại</b>: trả về bước trước để bổ sung thông tin.')], []),
  ],
  note='Sau khi chuyển sang BLĐ bút phê, mở lại văn bản và dùng Phân công người thực hiện để giao đúng lãnh đạo nếu hệ thống chưa gán.'),

 dict(id='d3', n=3, name='BLĐ bút phê', role='lanhdao', sla='48 giờ',
  who='Lãnh đạo được giao cho văn bản.',
  form='Việc Lãnh đạo phê duyệt, Bút phê',
  done='Việc phê duyệt hoàn tất. Văn bản tự sang Đơn vị chủ trì nhận văn bản.',
  links=[('Phê duyệt & Ký', 'appr'), ('Văn bản chờ xử lý', 'docs')],
  rt={'lanhdao': 'Đọc, bút phê chỉ đạo, phê duyệt', 'thuky': 'Theo dõi, sửa thông tin khi lãnh đạo yêu cầu'},
  blocks=[
   ('Mở văn bản chờ bạn duyệt', '15', [
     (219, 236, 'Bấm <b>Phê duyệt & Ký</b>.'),
     (633, 90, '<b>Tất cả</b>: mọi văn bản đang chờ bạn.'),
     (760, 90, '<b>Phê duyệt</b>: văn bản đến chờ bút phê, phê duyệt.'),
     (873, 90, '<b>Ký</b>: văn bản đi chờ bạn ký.'),
     (1510, 232, 'Bấm nút ở cột <b>Hành động</b> để xử lý.')], []),
   ('Đọc, bút phê, phê duyệt', '09', [
     (1290, 342, '<b>Xem tài liệu</b> để đọc bản gốc.'),
     (1424, 342, '<b>Bút phê</b>: ghi ý kiến chỉ đạo lên văn bản (cách dùng như ảnh Ghi bút phê ở bước 2).'),
     (640, 283, 'Thấy <b>Phòng ban chủ trì</b> sai, báo Thư ký sửa trước khi duyệt.')], []),
  ],
  after=['Cuộn lên khối <b>Việc cần làm</b>, hoàn tất việc <b>Lãnh đạo phê duyệt</b>.'],
  note='Người nhận ở bước 4 được giao theo Phòng ban chủ trì, nên ô này phải đúng trước khi bạn duyệt.'),

 dict(id='d4', n=4, name='Đơn vị chủ trì nhận văn bản', role='donvi', sla='24 giờ',
  who='Người phụ trách của đơn vị chủ trì, hệ thống tự giao theo Phòng ban chủ trì (bảng ở Phụ lục).',
  form='Việc Thực hiện theo ý kiến phê duyệt (có Tạo phúc đáp), mục Công việc',
  done='Việc Thực hiện theo ý kiến phê duyệt hoàn tất. Văn bản sang Hoàn tất.',
  links=[('Văn bản chờ xử lý', 'docs'), ('Kanban Công văn đi', 'out_k')],
  rt={'donvi': 'Thực hiện, giao việc trong đơn vị, tạo phúc đáp'},
  blocks=[
   ('Giao việc cho người trong đơn vị', '10', [
     (1420, 458, 'Bấm <b>Giao việc</b> ở mục Công việc, chọn người và hạn.')], []),
  ],
  after=['Đọc ý kiến bút phê, Yêu cầu giải quyết, Thời hạn hoàn thành.',
         'Cần trả lời bên gửi: ở việc Thực hiện theo ý kiến phê duyệt, chọn <b>Tạo phúc đáp</b>. Hệ thống tạo văn bản đi "Phúc đáp: …" ở bước Soạn công văn, hai văn bản liên kết với nhau (xem <a href="#o1">Văn bản đi, bước 1</a>).',
         'Xong việc: hoàn tất việc <b>Thực hiện theo ý kiến phê duyệt</b>.'],
  note='Ban Quản lý Tòa nhà Vinaconex chưa có quy tắc tự giao. Chọn đơn vị này thì việc giữ nguyên người ở bước trước.'),

 dict(id='d5', n=5, name='Hoàn tất', role='donvi', sla='Không giới hạn',
  who='Người phụ trách văn bản, thường là người của đơn vị chủ trì.',
  form='Không có việc bắt buộc',
  done='Bạn bấm Chuyển bước. Bước này không tự chuyển.',
  links=[('Văn bản chờ xử lý', 'docs')],
  rt={'donvi': 'Kiểm tra kết quả, chuyển sang Lưu trữ'},
  blocks=[], after=['Kiểm tra kết quả xử lý và tệp đính kèm đã đủ.', 'Bấm <b>Chuyển bước</b> để sang Lưu trữ.'], note=''),

 dict(id='d6', n=6, name='Lưu trữ', role='donvi', sla='Không giới hạn',
  who='Người phụ trách văn bản.',
  form='Mục Lưu hồ sơ & thẻ',
  done='Văn bản ở cột Lưu trữ, vẫn tra cứu được trong Văn bản và Tủ hồ sơ.',
  links=[('Văn bản mẫu 2/2026', 'd_in')],
  rt={'donvi': 'Gán tủ hồ sơ, kiểm tra thẻ', 'vanthu': 'Gán tủ hồ sơ nếu Văn phòng quản lý'},
  blocks=[
   ('Gán vào tủ hồ sơ', '10', [
     (668, 609, 'Bấm <b>Gán vào tủ hồ sơ</b> và chọn tủ phù hợp.'),
     (670, 657, 'Kiểm tra <b>thẻ</b> AI gợi ý, sửa nếu cần.')], []),
  ], note=''),
]

OUT = [
 dict(id='o1', n=1, name='Soạn công văn', role='nguoisoan', sla='24 giờ',
  who='Người soạn. Phải chọn người phụ trách khi tạo, bước này không tự đặt.',
  form='Form Văn bản đi mới, tệp bản thảo',
  done='Bạn bấm Chuyển giai đoạn. Văn bản sang Lãnh đạo Ban kiểm tra.',
  links=[('Kanban Công văn đi', 'out_k'), ('Tạo văn bản đi', 'out_new'), ('Bản phúc đáp mẫu', 'd_reply')],
  rt={'nguoisoan': 'Tạo, soạn, đính kèm bản thảo', 'donvi': 'Soạn phúc đáp từ văn bản đến'},
  blocks=[
   ('Mở kanban và bấm Văn bản mới', '16', [
     (219, 405, 'Chọn <b>VPTCT - Công văn đi</b>.'),
     (1460, 90, 'Bấm <b>+ Văn bản mới</b>.'),
     (469, 217, 'Cột <b>Soạn công văn</b> chứa các bản đang soạn.'),
     (564, 315, 'Bản <b>Phúc đáp: …</b> tạo từ văn bản đến đã nằm sẵn ở đây. Mở nó, không tạo mới.')], []),
   ('Nhập trích yếu và người phụ trách', '17', [
     (655, 226, 'Nhập <b>Tiêu đề / trích yếu</b>.'),
     (698, 341, '<b>Người phụ trách</b> (bắt buộc): chọn người chịu trách nhiệm bản thảo.'),
     (692, 388, 'Bước Soạn công văn không tự đặt người phụ trách, nên ô này không bỏ trống được.'),
     (698, 497, 'Nhập <b>Tóm tắt</b>.'),
     (1300, 360, 'Khung bên phải: 7 bước của văn bản đi.')], []),
   ('Phân loại, đính kèm, tạo', '18', [
     (528, 154, '<b>Loại văn bản, Mức độ khẩn, Mức độ mật</b>.'),
     (522, 337, '<b>Chọn tệp</b>: tải bản thảo Word hoặc PDF.'),
     (698, 450, '<b>Thẻ</b>: gõ nhãn rồi Enter.'),
     (698, 578, '<b>Ghi chú nội bộ</b> cho người kiểm tra.'),
     (962, 90, 'Bấm <b>Tạo mới</b>.')], []),
   ('Chuyển bản thảo đi kiểm tra', '19', [
     (459, 151, 'Văn bản đang ở bước 1 <b>Soạn công văn</b>.'),
     (930, 427, '<b>Chuyển giai đoạn</b>: bấm khi bản thảo đã xong.'),
     (1355, 371, '<b>Phân công người thực hiện</b> nếu cần đổi người.'),
     (1366, 90, 'Hoặc bấm <b>Chuyển bước</b> ở góc trên.')], []),
   ('Đính kèm thêm bản thảo', '20', [
     (1459, 316, 'Bấm <b>⋯</b> ở mục Tệp đính kèm.'),
     (1290, 383, '<b>Tải lên văn bản</b>: PDF, ảnh hoặc Office.'),
     (1283, 437, '<b>Quét văn bản</b>: tải lên và để AI bóc tách nguyên văn, tóm tắt.'),
     (930, 636, '<b>Văn bản liên quan</b>: bấm để mở văn bản đến được phúc đáp.')], []),
  ], note=''),

 dict(id='o2', n=2, name='Lãnh đạo Ban kiểm tra', role='lanhdao', sla='24 giờ',
  who='Quản lý trực tiếp của người soạn, hệ thống tự giao theo sơ đồ tổ chức.',
  form='Việc Xem xét và cho ý kiến',
  done='Ý kiến đã ghi, việc Hoàn tất, bạn chuyển bước sang Thư ký kiểm tra.',
  links=[('Văn bản chờ xử lý', 'docs'), ('Văn bản mẫu "Hợp đồng"', 'd_sign')],
  rt={'lanhdao': 'Đọc bản thảo, cho ý kiến', 'nguoisoan': 'Sửa khi bị trả lại'},
  blocks=[
   ('Cho ý kiến về bản thảo', '23', [
     (536, 413, 'Mở khối bước <b>Lãnh đạo Ban kiểm tra</b>.'),
     (548, 470, 'Mở việc <b>Xem xét và cho ý kiến</b> (bắt buộc), ghi ý kiến.'),
     (530, 608, 'Ý kiến hiện ở <b>Kết quả</b>, ví dụ "đồng ý".'),
     (1407, 470, 'Việc chuyển <b>Hoàn tất</b>.')], []),
  ],
  after=['Bản thảo cần sửa: bấm mũi tên cạnh Chuyển bước › <b>Trả lại</b> (như <a href="#d2">văn bản đến, bước 2</a>).',
         'Đồng ý: bấm <b>Chuyển bước</b>.'],
  note='Người soạn chưa có quản lý trực tiếp trên sơ đồ tổ chức thì bước này không có người nhận. Báo người phụ trách dịch vụ.'),

 dict(id='o3', n=3, name='Thư ký kiểm tra', role='thuky', sla='24 giờ',
  who='Thư ký được gán cho văn bản.',
  form='Việc Xem xét và cho ý kiến',
  done='Việc xem xét hoàn tất, bạn chuyển bước sang BLĐ ký.',
  links=[('Văn bản chờ xử lý', 'docs'), ('Văn bản mẫu "Hợp đồng"', 'd_sign')],
  rt={'thuky': 'Kiểm tra thể thức, cho ý kiến, chuyển ký'},
  blocks=[
   ('Kiểm tra thể thức và cho ý kiến', '23', [
     (548, 191, 'Mở việc <b>Xem xét và cho ý kiến</b> ở bước Thư ký kiểm tra.'),
     (515, 330, 'Ghi ý kiến. Kết quả hiện ngay dưới việc, ví dụ "ok".')], []),
  ],
  after=['Dùng <b>Phân công người thực hiện</b> để chọn lãnh đạo ký nếu hệ thống chưa gán.',
         'Bấm <b>Chuyển bước</b> sang BLĐ ký.'], note=''),

 dict(id='o4', n=4, name='BLĐ ký', role='lanhdao', sla='24 giờ',
  who='Người soạn trình ký, Lãnh đạo ký điện tử.',
  form='Việc Trình ký người có thẩm quyền, mục Ký điện tử',
  done='Mọi người trong bì thư đã ký. Văn bản sang Cấp số.',
  links=[('Phê duyệt & Ký', 'appr'), ('Văn bản mẫu "Hợp đồng"', 'd_sign')],
  rt={'nguoisoan': 'Trình ký người có thẩm quyền', 'lanhdao': 'Ký điện tử'},
  blocks=[
   ('Người soạn: trình ký', '21', [
     (1037, 151, 'Văn bản đang ở bước 4 <b>BLĐ ký</b>.'),
     (580, 489, 'Bấm <b>Trình ký người có thẩm quyền</b>, chọn tài liệu và người ký.'),
     (590, 602, 'Kết quả: <b>1 bì thư ký</b>. Bấm Ký điện tử để xem.'),
     (1407, 489, 'Việc trình ký chuyển <b>Hoàn tất</b>.')], []),
   ('Lãnh đạo: ký điện tử', '22', [
     (428, 415, 'Mục <b>Ký điện tử</b> trên trang văn bản.'),
     (435, 473, 'Bì thư: người gửi, ký song song, số tài liệu.'),
     (484, 537, 'Trạng thái: <b>Đang chờ bạn 0/1</b>.'),
     (1290, 268, '<b>Xem tài liệu</b> trước khi ký.'),
     (1379, 473, 'Bấm <b>Ký ngay</b>.')], []),
   ('Lãnh đạo: ký từ Phê duyệt & Ký', '15', [
     (873, 90, 'Mở tab <b>Ký</b> để thấy mọi văn bản chờ bạn ký.'),
     (1510, 232, 'Bấm <b>Ký</b> ở cột Hành động.')], []),
  ],
  note='Văn bản chưa hiện trong tab Ký của lãnh đạo khi người soạn chưa trình ký.'),

 dict(id='o5', n=5, name='Cấp số', role='vanthu', sla='8 giờ',
  who='Văn thư, hệ thống tự giao theo quy tắc Văn thư.',
  form='Việc Đăng ký và cấp số văn bản',
  done='Số đã cấp. Văn bản tự sang Đã ban hành.',
  links=[('Yêu cầu cấp số', 'cnt'), ('Văn bản mẫu đã cấp số', 'd_num')],
  rt={'vanthu': 'Đăng ký và cấp số'},
  blocks=[
   ('Cấp số trên văn bản', '24', [
     (1162, 151, 'Văn bản ở bước 5 <b>Cấp số</b>.'),
     (567, 526, 'Thực hiện việc <b>Đăng ký và cấp số văn bản</b> (bắt buộc).'),
     (668, 639, 'Kết quả: số đã cấp, kèm lý do nếu cấp số lùi.'),
     (698, 90, 'Số mới hiện trên tiêu đề văn bản.')], []),
   ('Theo dõi yêu cầu cấp số', '25', [
     (41, 250, 'Bấm <b>Sổ cấp số</b> trên thanh trái.'),
     (219, 152, '<b>Yêu cầu cấp số</b>: các văn bản đang xin số.'),
     (643, 90, 'Tab <b>Chờ xử lý</b>.'),
     (173, 193, '<b>Sổ cấp số</b>: các sổ và mẫu số đang dùng.'),
     (1511, 277, 'Bấm mũi tên để mở một yêu cầu.')], []),
  ], note=''),

 dict(id='o6', n=6, name='Đã ban hành', role='vanthu', sla='Không giới hạn',
  who='Văn thư.',
  form='Không có việc bắt buộc',
  done='Bạn bấm Chuyển bước sang Lưu trữ.',
  links=[('Kanban Công văn đi', 'out_k')],
  rt={'vanthu': 'Phát hành tới nơi nhận'},
  blocks=[], after=['Văn bản đã ký và có số. Gửi tới nơi nhận theo cách Văn phòng đang dùng.', 'Bấm <b>Chuyển bước</b> sang Lưu trữ.'], note=''),

 dict(id='o7', n=7, name='Lưu trữ', role='vanthu', sla='Không giới hạn',
  who='Văn thư.',
  form='Mục Lưu hồ sơ & thẻ',
  done='Văn bản ở cột Lưu trữ.',
  links=[('Kanban Công văn đi', 'out_k')],
  rt={'vanthu': 'Gán tủ hồ sơ'},
  blocks=[
   ('Gán vào tủ hồ sơ', '10', [
     (668, 609, 'Bấm <b>Gán vào tủ hồ sơ</b>, chọn tủ, ví dụ VP TCT › Sổ Chính quyền › Công văn đi.'),
     (670, 657, 'Kiểm tra <b>thẻ</b>.')], []),
  ], note=''),
]

RULES = [['Ban Kiểm toán nội bộ', 'Vũ Văn Mạnh'], ['Ban QLDA ĐT Đông Bắc', 'Vũ Minh Tuấn'], ['Ban QLDA Thăng Long', 'Nguyễn Xuân Thanh'], ['Ban QL các dự án trọng điểm', 'Vũ Văn Khoa'], ['Tổ công tác Ban điều hành Ban QLDA 3', 'Nguyễn Thị Thành Minh'], ['Ban QLDA 1', 'Nguyễn Duy Hiếu'], ['Ban Quản lý Tòa nhà Vinaconex', 'Chưa có quy tắc'], ['Ban Quản lý Giá & Hợp đồng', 'Nguyễn Hồng Dương'], ['Ban Kiểm soát', 'Vũ Văn Mạnh'], ['Ban Xây dựng', 'Lê Văn Thắng'], ['Ban Đầu tư', 'Nguyễn Minh Thắng'], ['Ban Truyền thông, Thương hiệu & Marketing', 'Nguyễn Cẩm Vân'], ['Ban Đối ngoại - Pháp chế', 'Vũ Mạnh Hùng'], ['Ban Phát triển Nhân lực', 'Nguyễn Quốc Huy'], ['Ban Quản lý & Giám sát Đầu tư Tài chính', 'Nguyễn Thị Quỳnh Trang'], ['Ban Tài chính Kế hoạch', 'Nguyễn Thị Thúy Hồng'], ['Văn phòng TCT', 'Dương Đức Vũ'], ['Tiểu ban Thư ký - Tổng hợp', 'Nguyễn Quốc Huy']]
