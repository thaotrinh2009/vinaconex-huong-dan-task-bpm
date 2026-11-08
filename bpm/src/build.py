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
    lanes = [('LD', 'Lãnh đạo duyệt', 'Approver'), ('TK', 'Người xử lý', 'Step handler'),
             ('CV', 'Người đề xuất', 'Requester'), ('SYS', 'Base tự động', 'Base automation')]
    lc = {'LD': '#1352d0', 'TK': '#16a34a', 'CV': '#ffb300', 'SYS': '#94a3b8'}
    LH = 112
    cols = [s['id'] for s in C.STEPS]
    CW = (W - LW) / len(cols)
    X = lambda i: LW + CW * i + CW / 2
    Y = {k[0]: TOP + LH * n + LH / 2 for n, k in enumerate(lanes)}
    H = TOP + LH * len(lanes) + 10
    NW = 124
    o = [f'<svg class="flow" viewBox="0 0 {W} {H}" role="img" aria-label="Luồng phiếu BPM">',
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
    def lbl(x, y, vi, en, cls='ort', anc='middle'):
        return f'<text x="{x}" y="{y}" text-anchor="{anc}" class="lb {cls}"><tspan class="vi">{vi}</tspan><tspan class="en">{en}</tspan></text>'
    h = NW / 2
    o.append(node(0, 'LD', ('Cần bạn ngay', 'phiếu chờ duyệt'), ('Needs you', 'awaiting approval')))
    o.append(node(0, 'CV', ('Việc của tôi', 'Do tôi tạo'), ('My work', 'Created by me')))
    o.append(node(1, 'CV', ('Chọn quy trình', 'theo Ban'), ('Pick process', 'by division')))
    o.append(node(2, 'CV', ('Tạo phiếu', 'Đơn vị + bảng + file'), ('Create ticket', 'unit + table + files')))
    o.append(node(2, 'SYS', ('Tự chọn người', 'duyệt theo Đơn vị'), ('Auto-pick', 'approver by unit'), 'n sys'))
    o.append(node(3, 'CV', ('Theo dõi', 'bước · hạn · Lịch sử'), ('Track', 'step · time · history')))
    o.append(node(3, 'SYS', ('Thông báo', 'đếm hạn bước'), ('Notify', 'step timer'), 'n sys'))
    o.append(node(4, 'TK', ('Xử lý bước', 'điền trường, chọn nút'), ('Handle step', 'fill, pick outcome')))
    o.append(node(4, 'SYS', ('AI đọc file', '· phiếu con'), ('AI reads file', '· sub-jobs'), 'n sys'))
    o.append(node(5, 'LD', ('Duyệt /', 'Trả lại'), ('Approve /', 'Return'), 'n dec'))
    o.append(node(6, 'TK', ('Trình ký', '· In mẫu'), ('E-sign', '· Print'), 'n alt'))
    o.append(node(6, 'SYS', ('Ký số · Word', '/PDF tự điền'), ('E-sign · Word', '/PDF auto-fill'), 'n sys'))
    o.append(node(7, 'LD', ('Báo cáo', 'quy trình'), ('Process', 'reports')))
    o.append(node(7, 'SYS', ('Số liệu', 'tự động'), ('Live', 'numbers'), 'n sys'))
    o.append(line(X(0) + h, Y['CV'], X(1) - h - 2, Y['CV']))
    o.append(line(X(1) + h, Y['CV'], X(2) - h - 2, Y['CV']))
    o.append(line(X(2) + h, Y['CV'], X(3) - h - 2, Y['CV']))
    o.append(line(X(2), Y['SYS'] - 27, X(2), Y['CV'] + 29, 'gr', 'arG', True))
    o.append(line(X(3), Y['SYS'] - 27, X(3), Y['CV'] + 29, 'gr', 'arG', True))
    o.append(line(X(2) + 30, Y['CV'] - 27, X(4) - h, Y['TK'] + 6, 'or', 'arB'))
    o.append(lbl(X(3), Y['TK'] + 14, 'phiếu + hồ sơ', 'ticket + files'))
    o.append(line(X(4), Y['SYS'] - 27, X(4), Y['TK'] + 29, 'gr', 'arG', True))
    o.append(line(X(4) + h, Y['TK'] - 10, X(5) - 20, Y['LD'] + 29, 'or', 'arB'))
    o.append(lbl(X(4) + h + 12, Y['TK'] - 34, 'trình duyệt', 'to approval', 'ort', 'start'))
    o.append(line(X(5) - 30, Y['LD'] + 27, X(3) + 40, Y['CV'] - 29, 'rj', 'arR', True))
    o.append(lbl(X(3) + 52, Y['CV'] - 46, 'Trả lại → bổ sung', 'Return → fix', 'rjt', 'end'))
    o.append(line(X(5) + 20, Y['LD'] + 27, X(6) - 20, Y['TK'] - 29, 'gr', 'arG'))
    o.append(lbl(X(5) + h + 4, Y['LD'] + 52, 'Duyệt → bước tiếp', 'Approved → next', 'gt', 'start'))
    o.append(line(X(6), Y['SYS'] - 27, X(6), Y['TK'] + 29, 'gr', 'arG', True))
    o.append(line(X(6) + 20, Y['TK'] - 27, X(7) - 20, Y['LD'] + 29, 'gr', 'arG'))
    o.append(lbl(X(7) - 10, Y['TK'] - 22, 'Hoàn thành', 'Done', 'gt', 'end'))
    o.append(line(X(7), Y['SYS'] - 27, X(7), Y['LD'] + 29, 'gr', 'arG', True))
    o.append(line(X(0) + h, Y['LD'], X(5) - h - 2, Y['LD'], '', 'ar', True))
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
    ('b00_viec_cua_toi', ('Một danh sách cho mọi lượt đến bạn', 'One list for every ticket on your turn'),
     ('Lượt của tôi gom phiếu chờ bạn, phiếu quá hạn lên đầu, duyệt nhanh ngay trên dòng.', 'My turn gathers tickets waiting on you, overdue first, quick approve on the row.'),
     ('Chắc chắn', 'Certain'), ('54 quy trình · 8 nhóm Ban trên một app', '54 processes · 8 divisions in one app'), ('Hồ sơ giấy chuyển tay, gọi hỏi "đến đâu rồi"', 'Paper passed by hand, calls to ask "where is it"')),
    ('b10_lich_su', ('Biết phiếu đang ở tay ai, vì sao', 'Know who holds a ticket and why'),
     ('Tab Lịch sử ghi quy tắc giao, người đủ điều kiện, người được giao và giờ từng bước.', 'History logs the rule, eligible people, assignee and time of every step.'),
     ('Chắc chắn', 'Certain'), ('100% bước có người, giờ, lý do', '100% of steps have who, when, why'), ('Không rõ hồ sơ nằm ở bàn ai', 'No idea whose desk the file is on')),
    ('b09_thao_luan_sla', ('Hạn từng bước, đỏ khi trễ', 'Per-step deadlines that turn red'),
     ('Mỗi bước duyệt có hạn (thường 1–2 ngày); thanh thời gian và khối Cần bạn ngay báo trễ.', 'Each approval step has a deadline (usually 1–2 days); the timer and "Needs you now" flag delays.'),
     ('Mục tiêu', 'Target'), ('Giảm ≥30% phiếu quá hạn sau 3 tháng', '≥30% fewer overdue tickets in 3 months'), ('Không đo được hồ sơ chờ bao lâu', 'No way to measure waiting time')),
    ('b16_in_xuat', ('Một bấm ra văn bản Word/PDF', 'One click to Word/PDF'),
     ('Dữ liệu phiếu tự điền vào mẫu Đề nghị thanh toán; biên bản bàn giao ký điện tử trong phiếu.', 'Ticket data fills the payment template; handover minutes are e-signed in the ticket.'),
     ('Chắc chắn', 'Certain'), ('0 lần gõ lại số liệu khi in', 'Zero retyping when printing'), ('Gõ lại vào mẫu Word', 'Retyped into Word')),
    ('b20_bao_cao', ('Số liệu toàn BPM tức thì', 'Instant BPM-wide numbers'),
     ('Tổng phiếu, đang chạy, hoàn thành, thất bại, đã huỷ, dịch vụ nhiều phiếu nhất — theo 7/30 ngày.', 'Total, running, done, failed, cancelled, busiest services — by 7/30 days.'),
     ('Chắc chắn', 'Certain'), ('30 ngày qua: 489 phiếu, 293 đang chạy', 'Last 30 days: 489 tickets, 293 running'), ('Tổng hợp Excel cuối tháng', 'Monthly Excel roll-up')),
]

def benefits():
    o = ['<div class="ben">']
    for key, t, d, lab, num, before in BEN:
        cls = 'ok' if lab[0] == 'Chắc chắn' else 'tg'
        o.append(f'<div class="bc"><div class="bt"><h4>{LP(t)}</h4><p>{LP(d)}</p><p class="num"><span class="lab {cls}">{LP(lab)}</span>{LP(num)}</p>'
                 f'<p class="bef">{L("Trước:", "Before:")} <s>{LP(before)}</s></p><a href="{C.IMG_LINK[key]}" target="_blank" rel="noopener">{L("Xem trên Base ↗", "View on Base ↗")}</a></div>{fig(key)}</div>')
    o.append('</div>')
    o.append(f'''<div class="aiblk"><div class="aih"><span>✦ AI</span><h4>{L("AI đọc file, điền bảng và tóm tắt phiếu", "AI reads files, fills tables and summarizes tickets")}</h4>
<p>{L("Hai chỗ dùng AI trong BPM: khối AI Agent trong luồng (vd. 2. Yêu cầu vật tư tự đọc phiếu YCVT, điền Bảng vật tư) và Trợ lý AI ✦ trên mọi phiếu. Ảnh bên dưới là kết quả thật.", "Two places: the AI Agent block inside a flow (e.g. 2. Material request reads the request file and fills the table) and the ✦ assistant on every ticket. Screens below are real.")}</p>
<div class="aik"><div><b>~1 {L("phút", "min")}</b><span>{L("nắm tình hình 1 phiếu", "to grasp one ticket")}</span><em>{L("Mục tiêu", "Target")}</em></div>
<div><b>-50%</b><span>{L("thời gian nhập bảng vật tư", "time typing material tables")}</span><em>{L("Mục tiêu", "Target")}</em></div>
<div><b>0</b><span>{L("bước AI tự duyệt — người bấm nút", "steps approved by AI — people press")}</span><em>{L("Chắc chắn", "Certain")}</em></div></div></div>
<div class="aiimgs">{fig("b19_ai_bang_vat_tu")}{fig("b22_ai_tom_tat")}</div></div>''')
    return ''.join(o)

def statuses():
    st = [('Tạo phiếu', 'Created', '#94a3b8'), ('Đang chạy · chờ xử lý từng bước', 'Running · waiting per step', '#ffb300'), ('Hoàn thành', 'Completed', '#16a34a')]
    a = '<span class="sa">→</span>'.join(f'<span class="st" style="--sc:{c}">{L(v, e)}</span>' for v, e, c in st)
    return (f'<div class="stl">{a}</div><div class="stl2"><span class="st" style="--sc:#ff3b5c">{L("Thất bại", "Failed")}</span><span class="st" style="--sc:#94a3b8">{L("Đã huỷ", "Cancelled")}</span><span class="st" style="--sc:#0068ff">{L("Đóng băng", "Frozen")}</span>'
            f'<span class="stn">{L("Trong lúc Đang chạy, phiếu đi qua từng bước; Trả lại đưa phiếu về bước trước. Thất bại = nhánh từ chối không có lối đi hoặc lỗi hệ thống. Huỷ / Đóng băng do chủ quy trình bấm ở ⋯.", "While Running the ticket moves step by step; Return sends it back. Failed = a reject branch with no route or a system error. Cancel / Freeze via ⋯ by the process owner.")}</span></div>')

# ---------- AI ----------
def ai():
    q = ''.join(f'<tr><td><span class="chip" style="--rc:{ROLE[r]["color"]}">{LP(ROLE[r]["short"])}</span></td><td>{LP(t)}</td><td><button class="cpy" data-copy="{html.escape(t[0])}">{L("Chép", "Copy")}</button></td></tr>' for r, t in C.AI_QS)
    rules = [('Trợ lý ✦ đọc phiếu đang mở (bước, người, hạn, trường) — dữ liệu đủ thì trả lời đúng.', 'The ✦ assistant reads the open ticket (step, people, time, fields) — complete data, better answers.'),
             ('AI gợi ý, người quyết: Duyệt / Trả lại / Hoàn thành vẫn do người bấm.', 'AI suggests, people decide: Approve / Return / Done stay human.'),
             ('Luôn kiểm tra bảng AI điền với file gốc trước khi chuyển bước.', 'Always check AI-filled tables against the source before moving on.'),
             ('Hỏi "chỉ đọc" khi chỉ muốn tóm tắt — trợ lý có thể tạo công việc thay bạn.', 'Say "read only" when you just want a summary — the assistant can also create jobs for you.'),
             ('Không dán số tài khoản, mật khẩu vào ô hỏi.', 'Never paste account numbers or passwords.')]
    return (f'<div class="aimap"><div><h5>{L("AI Agent trong luồng", "AI Agent inside the flow")}</h5><p>{L("Tự đọc file đính kèm (PDF, Excel) và điền trường, vd. Bảng vật tư; lỗi thì người được giao bấm Thử lại.", "Reads attachments (PDF, Excel) and fills fields like the material table; on failure the assignee retries.")}</p></div>'
            f'<div><h5>{L("Trợ lý AI ✦ và nút Điền bằng AI", "✦ Assistant and Điền bằng AI")}</h5><p>{L("Tóm tắt phiếu, chỉ người đang giữ, hạn, bước tiếp; điền trường của bước từ file.", "Summarizes a ticket, holder, time, next step; fills step fields from files.")}</p></div></div>'
            f'<div class="g2">{fig("b21_tro_ly_ai", ("① nút ✦ · ② phạm vi · ③ ô hỏi", "① ✦ button · ② scope · ③ prompt box"))}{fig("b22_ai_tom_tat", ("① câu hỏi · ② trả lời · ③ ngữ cảnh phiếu", "① question · ② answer · ③ ticket context"))}</div>'
            f'<div class="g2">{fig("b19_ai_bang_vat_tu")}{fig("b17_ai_that_bai")}</div>'
            f'<h4>{L("Câu hỏi mẫu theo vai trò", "Sample prompts by role")}</h4><div class="tblw"><table class="aiq">{q}</table></div>'
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
    return (f'<div class="isbar"><input id="isq" type="search" placeholder="Gõ vấn đề, vd: không thấy nút duyệt, sai người duyệt, quá hạn…" data-ph-en="Type a problem, e.g. no approve button, wrong approver, overdue…" autocomplete="off">'
            f'<div class="ifs">{chips}</div><span id="iscnt"></span></div><div id="isl">{"".join(cards)}</div>'
            f'<p id="isnone" hidden>{L("Không thấy tình huống phù hợp. Thử từ khác, hoặc liên hệ Quản trị app.", "No match. Try other words or contact the app admin.")}</p>')

def setup():
    o = []
    for s in C.SETUP:
        o.append(f'<div class="su" id="{s["id"]}"><div class="sut"><span class="sid">{s["id"]}</span><h4>{LP(s["title"])}</h4>{pins(L(s["body"][0], s["body"][1], "p"))}</div>{fig(s["img"])}</div>')
    o.append(f'<h4>{L("Checklist khi thêm/đổi quy trình", "Checklist when adding/changing a process")}</h4><ul class="chk">' + ''.join(f'<li>{LP(c)}</li>' for c in C.CHECKLIST) + '</ul>')
    return ''.join(o)

def toc():
    parts = [
        ('I', '#2563eb', ('Tổng quan', 'Overview'), [('s-flow', ('1 · Lưu đồ phiếu BPM', '1 · Ticket flow')), ('s-status', ('2 · Trạng thái một phiếu', '2 · Ticket statuses')), ('s-ben', ('3 · Lợi ích', '3 · Benefits'))]),
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
        '{{band1}}': band('I', '#2563eb', ('Tổng quan', 'Overview'), ('Mục 1–3 · Phiếu chạy thế nào, ai làm gì', 'Sections 1–3 · How tickets flow, who does what')),
        '{{band2}}': band('II', '#0e9f6e', ('Hướng dẫn chi tiết', 'Step-by-step guide'), ('Mục 4–5 · 8 bước, ảnh thật có đánh số', 'Sections 4–5 · 8 steps, numbered real screenshots')),
        '{{band3}}': band('III', '#e5383b', ('Gặp vấn đề?', 'Troubleshooting'), ('Mục 6 · Gõ vấn đề, ra cách xử lý', 'Section 6 · Type a problem, get the fix')),
        '{{band4}}': band('IV', '#7c3aed', ('Setup cho Quản trị app', 'Admin setup'), ('S1–S6 · Thành viên, luồng, người duyệt, hạn bước, mẫu in', 'S1–S6 · Members, flow, approvers, deadlines, templates')),
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
