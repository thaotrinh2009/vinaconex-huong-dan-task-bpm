# -*- coding: utf-8 -*-
import base64, json, os, re, html, unicodedata
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
CIRC = '①②③④⑤⑥⑦⑧⑨⑩'

def L(vi, en, tag='span'):
    return f'<{tag} class="vi">{vi}</{tag}><{tag} class="en">{en}</{tag}>'

def LP(p, tag='span'):
    return L(p[0], p[1], tag)

def nodia(s):
    s = re.sub('<[^>]+>', ' ', s)
    s = unicodedata.normalize('NFD', s.replace('đ', 'd').replace('Đ', 'D'))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()

def pins(s):
    return re.sub('[①-⑩]', lambda m: f'<i class="pin">{CIRC.index(m.group(0)) + 1}</i>', s)

_IMG = {}
def img_uri(key):
    if key not in _IMG:
        b = open(os.path.join(HERE, 'web', key + '.webp'), 'rb').read()
        _IMG[key] = 'data:image/webp;base64,' + base64.b64encode(b).decode()
    return _IMG[key]

def fig(key, cap=None):
    link = C.IMG_LINK.get(key)
    lk = (' · ' if cap else '') + f'<a href="{link}" target="_blank" rel="noopener">{L("Mở màn hình này ↗", "Open this screen ↗")}</a>' if link else ''
    cp = (LP(cap) if cap else '') + lk
    img_uri(key)
    from PIL import Image
    w, h = Image.open(os.path.join(HERE, 'web', key + '.webp')).size
    z = ' zoomshot' if w < 1300 else ''
    return (f'<figure class="shot{z}"><div class="win"><i></i><i></i><i></i></div><img data-k="{key}" width="{w}" height="{h}" alt="{key}" data-zoom>'
            f'<figcaption>{cp}</figcaption></figure>')

ROLE = {r['id']: r for r in C.ROLES}
ISS = {i['id']: i for i in C.ISSUES}
STEPN = {s['id']: s for s in C.STEPS}

# ---------- Lưu đồ swimlane ----------
def flow():
    W, LW, TOP = 1290, 150, 50
    lanes = [('LD', 'Chủ trì', 'Chair'), ('TK', 'Thư ký / Tổ chức', 'Secretary'),
             ('CV', 'Thành viên', 'Attendee'), ('QT', 'Văn phòng (Booking)', 'Office (Booking)'), ('SYS', 'Base tự động', 'Base automation')]
    lc = {'LD': '#1352d0', 'TK': '#16a34a', 'CV': '#ffb300', 'QT': '#8b5cf6', 'SYS': '#94a3b8'}
    LH = 100
    cols = [s['id'] for s in C.STEPS]
    CW = (W - LW) / len(cols)
    X = lambda i: LW + CW * i + CW / 2
    Y = {k[0]: TOP + LH * n + LH / 2 for n, k in enumerate(lanes)}
    H = TOP + LH * len(lanes) + 10
    NW = 124
    o = [f'<svg class="flow" viewBox="0 0 {W} {H}" role="img" aria-label="Luồng cuộc họp">',
         '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#94a3b8"/></marker>'
         '<marker id="arR" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#ff3b5c"/></marker>'
         '<marker id="arB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#0047cc"/></marker>'
         '<marker id="arG" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="#16a34a"/></marker></defs>']
    for n, (k, vi, en) in enumerate(lanes):
        y = TOP + LH * n
        o.append(f'<rect x="0" y="{y}" width="{W}" height="{LH}" class="lane{n % 2}"/>')
        o.append(f'<rect x="0" y="{y}" width="5" height="{LH}" fill="{lc[k]}"/>')
        o.append(f'<text x="16" y="{y + LH / 2 + 5}" class="lt"><tspan class="vi">{vi}</tspan><tspan class="en">{en}</tspan></text>')
    for i, c in enumerate(cols):
        o.append(f'<a href="#{c}" class="colh"><text x="{X(i)}" y="22" text-anchor="middle" class="ch">{c}</text>'
                 f'<text x="{X(i)}" y="40" text-anchor="middle" class="cs"><tspan class="vi">{C.SHORT[c][0]}</tspan><tspan class="en">{C.SHORT[c][1]}</tspan></text></a>')
    def node(i, lane, vi, en, cls='n', w=NW):
        x, y = X(i), Y[lane]
        return (f'<a href="#{cols[i]}" class="nd"><rect x="{x - w / 2}" y="{y - 26}" width="{w}" height="52" rx="10" class="{cls}"/>'
                f'<text x="{x}" y="{y - 3}" text-anchor="middle" class="nt"><tspan class="vi">{vi[0]}</tspan><tspan class="en">{en[0]}</tspan></text>'
                f'<text x="{x}" y="{y + 14}" text-anchor="middle" class="nt2"><tspan class="vi">{vi[1]}</tspan><tspan class="en">{en[1]}</tspan></text></a>')
    def line(x1, y1, x2, y2, c='', m='ar', dash=False):
        return f'<path d="M{x1},{y1} L{x2},{y2}" class="ln {c}" marker-end="url(#{m})"{" stroke-dasharray=\"5 4\"" if dash else ""}/>'
    def lb(x, y, vi, en, cls='ort', anchor='middle'):
        return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="lb {cls}"><tspan class="vi">{vi}</tspan><tspan class="en">{en}</tspan></text>'
    h = NW / 2
    o.append(node(0, 'LD', ('Trang chủ', 'lịch họp'), ('Home', 'meeting list')))
    o.append(node(0, 'CV', ('Cuộc họp', 'của tôi'), ('My', 'meetings')))
    o.append(node(1, 'TK', ('Tạo cuộc họp', 'mời · chương trình'), ('Create', 'invite · agenda')))
    o.append(node(1, 'LD', ('Lãnh đạo', 'tự tạo'), ('Leader', 'creates'), 'n alt'))
    o.append(node(2, 'TK', ('Đặt phòng', 'link họp online'), ('Book room', 'video link')))
    o.append(node(2, 'QT', ('Duyệt phòng', 'Admin VP › CVP'), ('Approve room', 'Admin › Chief'), 'n dec'))
    o.append(node(2, 'SYS', ('Lời mời', 'email + lịch'), ('Invites', 'email + calendar'), 'n sys'))
    o.append(node(3, 'CV', ('Phản hồi', 'đọc tài liệu'), ('RSVP', 'read papers')))
    o.append(node(3, 'LD', ('Xem ai dự', 'chuẩn bị'), ('Who attends', 'prep notes')))
    o.append(node(4, 'TK', ('Ghi âm', 'ghi chú'), ('Record', 'notes')))
    o.append(node(4, 'LD', ('Điều hành', 'biểu quyết'), ('Chair', 'vote')))
    o.append(node(4, 'SYS', ('Chép lời', 'tự động'), ('Transcript', 'auto'), 'n sys'))
    o.append(node(5, 'SYS', ('Phân tích AI', 'quyết định · việc'), ('AI analysis', 'decisions · actions'), 'n sys'))
    o.append(node(5, 'TK', ('Lưu ghi chú', 'in biên bản'), ('Save notes', 'print minutes')))
    o.append(node(5, 'LD', ('Chốt', 'kết luận'), ('Confirm', 'conclusions'), 'n dec'))
    o.append(node(6, 'TK', ('Tạo việc', 'vào Phòng (Task)'), ('Create task', 'into dept (Task)')))
    o.append(node(6, 'CV', ('Nhận việc', 'bên Task'), ('Receive', 'in Task')))
    o.append(node(7, 'LD', ('Báo cáo', 'rà kết luận'), ('Reports', 'review')))
    o.append(node(7, 'SYS', ('Họp lặp lại', 'tự sinh kỳ sau'), ('Repeat', 'next occurrence'), 'n sys'))
    # B1 -> B2
    o.append(line(X(0) + h, Y['LD'] + 10, X(1) - h - 2, Y['TK'] - 10))
    o.append(line(X(1), Y['LD'] + 27, X(1), Y['TK'] - 29, '', 'ar', True))
    # B2 -> B3
    o.append(line(X(1) + h, Y['TK'], X(2) - h - 2, Y['TK']))
    o.append(line(X(2), Y['TK'] + 27, X(2), Y['QT'] - 29, 'or', 'arB'))
    o.append(lb(X(2) - 6, Y['CV'] + 4, 'yêu cầu phòng', 'room request', 'ort', 'end'))
    o.append(line(X(2) + 30, Y['QT'] - 27, X(2) + 30, Y['TK'] + 29, 'gr', 'arG', True))
    o.append(line(X(2) + h, Y['SYS'] - 8, X(3) - 20, Y['CV'] + 29, 'gr', 'arG', True))
    o.append(lb(X(3) - 4, Y['QT'] + 30, 'gửi lời mời', 'sends invites', 'gt', 'start'))
    # B3 -> B4 -> B5
    o.append(line(X(3) + 20, Y['CV'] - 27, X(3) + 20, Y['LD'] + 29, 'or', 'arB'))
    o.append(lb(X(3) + 14, Y['TK'] + 4, 'phản hồi', 'RSVP', 'ort', 'end'))
    o.append(line(X(3) + h, Y['LD'], X(4) - h - 2, Y['LD']))
    o.append(line(X(4), Y['LD'] + 27, X(4), Y['TK'] - 29, '', 'ar', True))
    o.append(line(X(4), Y['TK'] + 27, X(4), Y['SYS'] - 29, 'gr', 'arG', True))
    # B5 -> B6
    o.append(line(X(4) + h, Y['SYS'], X(5) - h - 2, Y['SYS'], 'gr', 'arG'))
    o.append(line(X(5), Y['SYS'] - 27, X(5), Y['TK'] + 29, 'gr', 'arG'))
    o.append(lb(X(5) + 6, Y['QT'] - 2, 'gợi ý', 'suggests', 'gt', 'start'))
    o.append(line(X(5) - 20, Y['TK'] - 27, X(5) - 20, Y['LD'] + 29, 'or', 'arB'))
    o.append(line(X(5) + 20, Y['LD'] + 27, X(5) + 20, Y['TK'] - 29, 'rj', 'arR', True))
    o.append(lb(X(5) + 26, Y['LD'] + 48, 'sửa lại', 'fix', 'rjt', 'start'))
    # B6 -> B7 -> B8
    o.append(line(X(5) + h, Y['LD'], X(6) - 10, Y['TK'] - 29, 'or', 'arB'))
    o.append(lb(X(6) - 6, Y['LD'] - 4, 'kết luận', 'conclusions', 'ort', 'middle'))
    o.append(line(X(6), Y['TK'] + 27, X(6), Y['CV'] - 29, 'or', 'arB'))
    o.append(lb(X(6) + 6, Y['CV'] - 36, 'việc + hạn', 'task + deadline', 'ort', 'start'))
    o.append(line(X(6) + h, Y['TK'] - 10, X(7) - h - 2, Y['LD'] + 10))
    o.append(line(X(7), Y['SYS'] - 27, X(7) - 40, Y['LD'] + 29, 'gr', 'arG', True))
    o.append('</svg>')
    return ''.join(o)

def short(t):
    return t.split('&')[0].split(' và ')[0].split(' một ')[0].split(' a ')[0][:24].strip()

# ---------- Ma trận ----------
def matrix():
    h = ['<div class="tblw"><table class="mx"><thead><tr><th>' + L('Vai trò', 'Role') + '</th>']
    for s in C.STEPS:
        h.append(f'<th><a href="#{s["id"]}" class="mxs" data-step="{s["id"]}">{s["id"]}</a><small>{LP(C.SHORT[s["id"]])}</small></th>')
    h.append('</tr></thead><tbody>')
    for r in C.ROLES:
        h.append(f'<tr><th><button class="mxr" data-role="{r["id"]}" style="--rc:{r["color"]}"><i></i>{LP(r["name"])}</button><small>{LP(r["desc"])}</small></th>')
        for s in C.STEPS:
            v = C.RMAP[s['id']].get(r['id'], '')
            sym = {'m': '●', 'p': '○', '': '·'}[v]
            tip = C.RDO.get(s['id'], {}).get(r['id'])
            tt = f' title="{html.escape(tip[0])}"' if tip else ''
            h.append(f'<td class="m{v}"{tt} style="--rc:{r["color"]}">{sym}</td>')
        h.append('</tr>')
    h.append('</tbody></table></div><p class="legend">● ' + L('làm chính', 'main') + ' &nbsp; ○ ' + L('phối hợp / xem', 'collaborate / view') + ' &nbsp; · ' + L('không tham gia', 'not involved') + '</p>')
    return ''.join(h)

def rail():
    o = ['<div class="rail">']
    for s in C.STEPS:
        who = ''.join(f'<span class="chip" style="--rc:{ROLE[k]["color"]}">{LP(ROLE[k]["short"])}</span>' for k, v in C.RMAP[s['id']].items() if v == 'm')
        o.append(f'<a class="rc" href="#{s["id"]}" data-step="{s["id"]}"><b>{s["id"]}</b><span class="rt">{LP(s["title"])}</span>'
                 f'<span class="ra">{LP(s["app"])} · {LP(s["dur"])}</span><span class="who">{who}</span><span class="rnote"></span></a>')
    o.append('</div>')
    return ''.join(o)

def jnav():
    rs = ''.join(f'<button class="jr" data-role="{r["id"]}" style="--rc:{r["color"]}"><i></i>{LP(r["short"])}<em>{sum(1 for s in C.STEPS if C.RMAP[s["id"]].get(r["id"]))}</em></button>' for r in C.ROLES)
    ss = ''.join(f'<a class="js" href="#{s["id"]}" data-step="{s["id"]}">{s["id"]}</a>' for s in C.STEPS)
    return (f'<div id="jnav"><div class="jrow"><span class="jl">{L("Vị trí", "Role")}</span>{rs}<button id="jnext">{L("Bước tiếp của tôi ↓", "My next step ↓")}</button></div>'
            f'<div class="jrow"><span class="jl">{L("Bước", "Step")}</span>{ss}<span id="jncur"></span></div></div>')

# ---------- Hướng dẫn từng bước ----------
def steps_html():
    o = []
    for s in C.STEPS:
        sid = s['id']
        roles = ''.join(f'<span class="chip" style="--rc:{ROLE[k]["color"]}">{LP(ROLE[k]["short"])}{" &nbsp;○" if v == "p" else ""}</span>' for k, v in C.RMAP[sid].items() if v)
        links = ''.join(f'<a href="{u}" target="_blank" rel="noopener">{LP(t)} ↗</a>' for t, u in s['links'])
        w5 = ''.join(f'<div><b>{LP(a)}</b><span>{LP(b)}</span></div>' for a, b in s['w5'])
        acts = []
        n = 0
        for (vi, en), key in s['acts']:
            if key == '__h':
                acts.append(f'<li class="ash" id="{sid}-{len(acts)}">{L(vi, en)}</li>')
                continue
            n += 1
            acts.append(f'<li><span class="an">{n}</span><div class="at">{pins(L(vi, en, "p"))}</div>' + (fig(key) if key else '') + '</li>')
        errs = ''.join(f'<li><a href="#{e}" class="isslink" data-iss="{e}">{LP(ISS[e]["q"])}</a></li>' for e in s['errs'])
        done = ''.join(f'<li>{LP(d)}</li>' for d in s['done'])
        rdo = ''.join(f'<p class="rdo" data-role="{k}" style="--rc:{ROLE[k]["color"]}"><b>{LP(ROLE[k]["short"])}</b> {L("ở bước này:", "here:")} {LP(v)}</p>' for k, v in C.RDO[sid].items())
        o.append(f'''<section class="step" id="{sid}" data-step="{sid}">
<header class="sh"><span class="sid">{sid}</span><h3>{LP(s["title"])}</h3></header>
<div class="pills">{roles}<span class="pill">{LP(s["app"])}</span><span class="pill">⏱ {LP(s["dur"])}</span></div>
<div class="lbar"><span>{L("Mở trên Base:", "Open on Base:")}</span>{links}</div>
<div class="rnote2">{rdo}<p class="rdo none">{L("Vai trò bạn chọn không tham gia bước này.", "Your role is not involved in this step.")}</p></div>
<div class="w5">{w5}</div>
<div class="ailine">✦ <b>{L("Dùng AI ở bước này", "Use AI here")}</b> — {LP(s["ai"])}</div>
<h4>{L("Cách làm", "How to")}</h4><ol class="acts">{"".join(acts)}</ol>
<div class="tri"><div><h5>{L("Sau đó", "Next")}</h5><p>{LP(s["after"])}</p></div>
<div><h5>{L("Lỗi hay gặp", "Common issues")}</h5><ul>{errs}</ul></div>
<div><h5>{L(f"Xong {sid} khi", f"{sid} is done when")}</h5><ul class="chk">{done}</ul></div></div>
</section>''')
    return ''.join(o)

# ---------- Lợi ích ----------
BEN = [
    ('m00_trang_chu', ('Một màn hình thấy lịch họp', 'One screen for all meetings'),
     ('Trang chủ đếm họp hôm nay, sắp tới, đã xong; Lịch tháng tránh trùng giờ.', 'Home counts today, upcoming and done; the month calendar avoids clashes.'),
     ('Chắc chắn', 'Certain'), ('16 cuộc họp đã lên Base', '16 meetings already on Base'), ('Lịch giấy, nhắn Zalo từng người', 'Paper schedules, chat each person')),
    ('m36_luong_duyet_phong', ('Đặt phòng ngay trong form họp', 'Book the room inside the meeting'),
     ('Chọn phòng, hậu cần, số người; luồng duyệt Văn phòng hiện sẵn.', 'Room, logistics, headcount; Office approval path shown.'),
     ('Chắc chắn', 'Certain'), ('5 phòng · 2 cấp duyệt', '5 rooms · 2 approval levels'), ('Gọi Văn phòng giữ phòng', 'Phone the Office to hold a room')),
    ('m21_phan_hoi', ('Biết trước ai dự', 'Know who attends'),
     ('Mỗi người bấm Tham dự / Có thể / Từ chối; thư ký nhắc người chưa trả lời.', 'Everyone RSVPs; the secretary nudges the rest.'),
     ('Chắc chắn', 'Certain'), ('TB 6 người/cuộc họp', 'Avg. 6 attendees per meeting'), ('Gọi điện xác nhận', 'Confirmation calls')),
    ('m25_ai_hieu_qua', ('AI chấm hiệu quả cuộc họp', 'AI scores meeting effectiveness'),
     ('Đạt mục đích, hoàn thành chương trình, đúng giờ — từ chính bản ghi.', 'Purpose, agenda coverage, timing — from the recording.'),
     ('Chắc chắn', 'Certain'), ('Họp mẫu: 75/100 · 88/60 phút', 'Sample: 75/100 · 88 vs 60 min'), ('Không đo được', 'Not measured')),
    ('m09_form_cong_viec', ('Kết luận thành việc có hạn', 'Conclusions become tasks with deadlines'),
     ('Thêm công việc ngay trên cuộc họp, việc chạy bên Task đúng Phòng.', 'Add tasks on the meeting; they run in Task in the right department.'),
     ('Mục tiêu', 'Target'), ('100% kết luận cần làm có việc Task', '100% of actions have a Task item'), ('Kết luận nằm trong biên bản giấy', 'Conclusions buried in paper minutes')),
    ('m46_bao_cao', ('Báo cáo họp tức thì', 'Instant meeting report'),
     ('Số cuộc họp, tổng giờ họp, phản hồi RSVP, người tổ chức nhiều nhất.', 'Meetings, total hours, RSVPs, top organizers.'),
     ('Mục tiêu', 'Target'), ('Biên bản xong ≤30 phút sau họp', 'Minutes done ≤30 min after'), ('Thư ký gõ biên bản 1–2 ngày', 'Secretaries type minutes for 1–2 days')),
]

def benefits():
    o = ['<div class="ben">']
    for key, t, d, lab, num, before in BEN:
        cls = 'ok' if lab[0] == 'Chắc chắn' else 'tg'
        o.append(f'<div class="bc"><div class="bt"><h4>{LP(t)}</h4><p>{LP(d)}</p><p class="num"><span class="lab {cls}">{LP(lab)}</span>{LP(num)}</p>'
                 f'<p class="bef">{L("Trước:", "Before:")} <s>{LP(before)}</s></p><a href="{C.IMG_LINK[key]}" target="_blank" rel="noopener">{L("Xem trên Base ↗", "View on Base ↗")}</a></div>{fig(key)}</div>')
    o.append('</div>')
    o.append(f'''<div class="aiblk"><div class="aih"><span>✦ AI</span><h4>{L("Ghi âm → chép lời → AI rút quyết định và việc cần làm", "Record → transcript → AI extracts decisions and actions")}</h4>
<p>{L("Tab Phân tích AI của mỗi cuộc họp. Ảnh dưới là kết quả thật trên một cuộc họp của Vinaconex (nội dung đã làm mờ).", "The Phân tích AI tab of each meeting. Below is a real Vinaconex result (content blurred).")}</p>
<div class="aik"><div><b>6</b><span>{L("phần AI tạo sẵn: tóm tắt → việc cần làm", "AI sections: summary → actions")}</span><em>{L("Chắc chắn", "Certain")}</em></div>
<div><b>≤30 {L("phút", "min")}</b><span>{L("từ lúc họp xong tới biên bản", "from meeting end to minutes")}</span><em>{L("Mục tiêu", "Target")}</em></div>
<div><b>0</b><span>{L("thứ AI tự lưu — người bấm Lưu / Tạo công việc", "things AI saves itself — people click save")}</span><em>{L("Chắc chắn", "Certain")}</em></div></div></div>
<div class="aiimgs">{fig("m24_ai_tom_tat")}{fig("m26_ai_quyet_dinh_viec")}</div></div>''')
    return ''.join(o)

def statuses():
    st = [('Đang hoạt động', 'Active', '#0068ff'), ('Hoàn thành', 'Completed', '#16a34a')]
    a = '<span class="sa">→</span>'.join(f'<span class="st" style="--sc:{c}">{L(v, e)}</span>' for v, e, c in st)
    rs = [('Chưa phản hồi', 'No reply', '#94a3b8'), ('Tham dự', 'Attending', '#16a34a'), ('Có thể tham dự', 'Maybe', '#ffb300'), ('Từ chối', 'Declined', '#ff3b5c')]
    r = ''.join(f'<span class="st" style="--sc:{c}">{L(v, e)}</span>' for v, e, c in rs)
    bk = '<span class="sa">→</span>'.join(f'<span class="st" style="--sc:{c}">{L(v, e)}</span>' for v, e, c in [('Chờ duyệt', 'Pending', '#ffb300'), ('Đã duyệt', 'Approved', '#16a34a')])
    return (f'<div class="stl"><b class="stk">{L("Cuộc họp", "Meeting")}</b>{a}<span class="st" style="--sc:#ff3b5c">{L("Đã hủy", "Cancelled")}</span></div>'
            f'<div class="stl"><b class="stk">{L("Người dự", "Attendee")}</b>{r}</div>'
            f'<div class="stl"><b class="stk">{L("Phòng họp", "Room")}</b>{bk}</div>'
            f'<div class="stl2"><span class="stn">{L("Hết giờ không tự chuyển Hoàn thành: thư ký bấm ⋯ › Đánh dấu hoàn thành. Phòng họp do Văn phòng duyệt trên Booking.", "Meetings do not auto-complete: the secretary uses ⋯ › Đánh dấu hoàn thành. Rooms are approved by the Office in Booking.")}</span></div>')

# ---------- AI ----------
def ai():
    q = ''.join(f'<tr><td><span class="chip" style="--rc:{ROLE[r]["color"]}">{LP(ROLE[r]["short"])}</span></td><td>{LP(t)}</td><td><button class="cpy" data-copy="{html.escape(t[0])}">{L("Chép", "Copy")}</button></td></tr>' for r, t in C.AI_QS)
    rules = [('AI chỉ dựa vào bản chép lời — điều không nói ra thì AI không biết.', 'AI only uses the transcript — unspoken points are unknown to it.'),
             ('AI gợi ý, người quyết: Lưu thành ghi chú, Tạo công việc vẫn do người bấm.', 'AI suggests, people decide: saving and creating tasks stay human.'),
             ('Họp mật: không ghi âm, hoặc đặt loại cuộc họp "chỉ theo lời mời" (S4).', 'Confidential: do not record, or set the type to invite-only (S4).'),
             ('Đọc lại tên người, số liệu, ngày tháng trước khi lưu và gửi.', 'Recheck names, figures and dates before saving or sending.'),
             ('Nói rõ "Kết luận: ai – làm gì – hạn nào" để AI rút việc đúng.', 'Say "Conclusion: who – what – by when" so AI extracts tasks right.')]
    return (f'<div class="aimap"><div><h5>{L("Ghi âm & chép lời", "Recording & transcript")}</h5><p>{L("Ghi âm ngay trên máy, tải file lên, hoặc mời bot vào Google Meet.", "Record on the device, upload a file, or invite the bot to Google Meet.")}</p></div>'
            f'<div><h5>{L("Phân tích AI", "AI analysis")}</h5><p>{L("Tóm tắt, nội dung chi tiết, hiệu quả, rủi ro, quyết định, việc cần làm → Lưu thành ghi chú / Tạo công việc.", "Summary, details, effectiveness, risks, decisions, actions → save as note / create task.")}</p></div></div>'
            f'<div class="g2">{fig("m14_ghi_am", ("② Ghi âm ngay · ③ Tải âm thanh lên", "② Record now · ③ Upload audio"))}{fig("m15_ai_trong", ("② Phân tích · ③ 6 phần AI tạo", "② Analyse · ③ 6 AI sections"))}</div>'
            f'<h4>{L("Câu nói mẫu giúp AI rút đúng quyết định & việc", "Phrases that help AI capture decisions & actions")}</h4><div class="tblw"><table class="aiq">{q}</table></div>'
            f'<h4>{L("5 nguyên tắc", "5 rules")}</h4><ol class="rules">{"".join(f"<li>{LP(r)}</li>" for r in rules)}</ol>')

# ---------- Tình huống ----------
def issues():
    chips = f'<button class="if on" data-r="">{L("Tất cả", "All")}</button>' + ''.join(f'<button class="if" data-r="{r["id"]}" style="--rc:{r["color"]}">{LP(r["short"])}</button>' for r in C.ROLES)
    cards = []
    for i in C.ISSUES:
        rc = ''.join(f'<span class="chip" style="--rc:{ROLE[k]["color"]}">{LP(ROLE[k]["short"])}</span>' for k in i['roles'])
        idx = nodia(' '.join([i['q'][0], i['q'][1], i['cause'][0], i['fix'][0], i['kw'], i['tag'][0]]))
        cause = '' if i['cause'][0] == '—' else f'<p><b>{L("Nguyên nhân:", "Cause:")}</b> {LP(i["cause"])}</p>'
        qi = nodia(i['q'][0] + ' ' + i['q'][1] + ' ' + i['kw'])
        cards.append(f'''<details class="iss" id="{i["id"]}" data-roles="{" ".join(i["roles"])}" data-idx="{html.escape(idx)}" data-q="{html.escape(qi)}">
<summary><span class="itag">{LP(i["tag"])}</span><span class="iq">{LP(i["q"])}</span>{rc}</summary>
<div class="ib"><div>{cause}<p class="fix"><b>{L("Cách xử lý:", "Fix:")}</b> {LP(i["fix"])}</p>
<p class="ilk"><a href="#{i["step"]}">{L("Xem hướng dẫn", "See guide")} {i["step"]} →</a></p></div>{fig(i["img"])}</div></details>''')
    return (f'<div class="isbar"><input id="isq" type="search" placeholder="Gõ vấn đề, vd: đặt phòng, không nhận lời mời, AI trống…" data-ph-en="Type a problem, e.g. room, no invite, AI empty…" autocomplete="off">'
            f'<div class="ifs">{chips}</div><span id="iscnt"></span></div><div id="isl">{"".join(cards)}</div>'
            f'<p id="isnone" hidden>{L("Không thấy tình huống phù hợp. Thử từ khác, hoặc liên hệ Quản trị app.", "No match. Try other words or contact the app admin.")}</p>')

def setup():
    o = []
    for s in C.SETUP:
        o.append(f'<div class="su" id="{s["id"]}"><div class="sut"><span class="sid">{s["id"]}</span><h4>{LP(s["title"])}</h4>{pins(L(s["body"][0], s["body"][1], "p"))}</div>{fig(s["img"])}</div>')
    o.append(f'<h4>{L("Checklist cho Văn phòng / Quản trị", "Checklist for the Office / admins")}</h4><ul class="chk">' + ''.join(f'<li>{LP(c)}</li>' for c in C.CHECKLIST) + '</ul>')
    return ''.join(o)

def toc():
    parts = [
        ('I', '#2563eb', ('Tổng quan', 'Overview'), [('s-flow', ('1 · Lưu đồ cuộc họp', '1 · Meeting flow')), ('s-status', ('2 · Trạng thái', '2 · Statuses')), ('s-ben', ('3 · Lợi ích', '3 · Benefits'))]),
        ('II', '#0e9f6e', ('Hướng dẫn chi tiết', 'Step-by-step'), [('s-matrix', ('4 · Hành trình × Vai trò', '4 · Journey × Roles'))] + [(s['id'], (f'{s["id"]} · ' + s['title'][0], f'{s["id"]} · ' + s['title'][1])) for s in C.STEPS] + [('s-ai', ('5 · Dùng AI', '5 · Using AI'))]),
        ('III', '#e5383b', ('Gặp vấn đề?', 'Troubleshooting'), [('s-iss', ('6 · Tra cứu tình huống', '6 · Find a fix'))]),
        ('IV', '#7c3aed', ('Setup cho Quản trị', 'Admin setup'), [(s['id'], (f'{s["id"]} · ' + s['title'][0], f'{s["id"]} · ' + s['title'][1])) for s in C.SETUP]),
    ]
    o = []
    for n, c, t, items in parts:
        li = ''.join(f'<a href="#{a}">{LP(b)}</a>' for a, b in items)
        o.append(f'<details open class="tp" style="--pc:{c}"><summary><b>{n}</b> {LP(t)}</summary>{li}</details>')
    return ''.join(o)

def band(n, color, title, sub):
    return f'<div class="part"><span class="eyebrow">{L("PHẦN", "PART")} {n}</span><h2>{LP(title)}</h2><p>{LP(sub)}</p></div>'

def main():
    t = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    nimg = len([k for k in os.listdir(os.path.join(HERE, 'web'))])
    R = {
        '{{toc}}': toc(), '{{flow}}': flow(), '{{status}}': statuses(), '{{ben}}': benefits(), '{{matrix}}': matrix(),
        '{{rail}}': rail(), '{{jnav}}': jnav(), '{{steps}}': steps_html(), '{{ai}}': ai(), '{{issues}}': issues(), '{{setup}}': setup(),
        '{{band1}}': band('I', '#2563eb', ('Tổng quan', 'Overview'), ('Mục 1–3 · Cuộc họp chạy thế nào, ai làm gì', 'Sections 1–3 · How a meeting runs, who does what')),
        '{{band2}}': band('II', '#0e9f6e', ('Hướng dẫn chi tiết', 'Step-by-step guide'), ('Mục 4–5 · 8 bước, ảnh thật có đánh số', 'Sections 4–5 · 8 steps, numbered real screenshots')),
        '{{band3}}': band('III', '#e5383b', ('Gặp vấn đề?', 'Troubleshooting'), ('Mục 6 · Gõ vấn đề, ra cách xử lý', 'Section 6 · Type a problem, get the fix')),
        '{{band4}}': band('IV', '#7c3aed', ('Setup cho Quản trị app', 'Admin setup'), ('S1–S7 · Loại cuộc họp, quyền, mẫu biên bản, kết nối', 'S1–S7 · Meeting types, permissions, minutes template, connections')),
        '{{rolemap}}': json.dumps({'map': C.RMAP, 'steps': [s['id'] for s in C.STEPS], 'rdo': {k: {r: v[0] for r, v in d.items()} for k, d in C.RDO.items()}, 'rdoen': {k: {r: v[1] for r, v in d.items()} for k, d in C.RDO.items()}}, ensure_ascii=False),
        '{{imgs}}': json.dumps(_IMG).replace('</', '<\\/'),
        '{{nimg}}': str(len(_IMG)),
        '{{vcxlogo}}': 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'vcx_logo.png'), 'rb').read()).decode(), '{{niss}}': str(len(C.ISSUES)),
    }
    for k, v in R.items():
        t = t.replace(k, v)
    out = os.path.join(HERE, 'out')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(t)
    print('size MB', round(len(t.encode()) / 1e6, 2))

if __name__ == '__main__':
    main()
