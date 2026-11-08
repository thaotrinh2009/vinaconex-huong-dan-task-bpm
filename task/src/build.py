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
    lanes = [('LD', 'Lãnh đạo / Người giao', 'Leader / Assigner'), ('TK', 'Thư ký / Phối hợp', 'Assistant / Collab'),
             ('CV', 'Chuyên viên', 'Specialist'), ('SYS', 'Base tự động', 'Base automation')]
    lc = {'LD': '#1352d0', 'TK': '#16a34a', 'CV': '#ffb300', 'SYS': '#94a3b8'}
    LH = 112
    cols = [s['id'] for s in C.STEPS]
    CW = (W - LW) / len(cols)
    X = lambda i: LW + CW * i + CW / 2
    Y = {k[0]: TOP + LH * n + LH / 2 for n, k in enumerate(lanes)}
    H = TOP + LH * len(lanes) + 10
    NW = 124
    o = [f'<svg class="flow" viewBox="0 0 {W} {H}" role="img" aria-label="Luồng công việc">',
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
        s = STEPN[c]
        o.append(f'<a href="#{c}" class="colh"><text x="{X(i)}" y="22" text-anchor="middle" class="ch">{c}</text>'
                 f'<text x="{X(i)}" y="40" text-anchor="middle" class="cs"><tspan class="vi">{C.SHORT[c][0]}</tspan><tspan class="en">{C.SHORT[c][1]}</tspan></text></a>')
    def node(i, lane, vi, en, cls='n', w=NW):
        x, y = X(i), Y[lane]
        return (f'<a href="#{cols[i]}" class="nd"><rect x="{x - w / 2}" y="{y - 26}" width="{w}" height="52" rx="10" class="{cls}"/>'
                f'<text x="{x}" y="{y - 3}" text-anchor="middle" class="nt"><tspan class="vi">{vi[0]}</tspan><tspan class="en">{en[0]}</tspan></text>'
                f'<text x="{x}" y="{y + 14}" text-anchor="middle" class="nt2"><tspan class="vi">{vi[1]}</tspan><tspan class="en">{en[1]}</tspan></text></a>')
    def line(x1, y1, x2, y2, c='', m='ar', dash=False):
        return f'<path d="M{x1},{y1} L{x2},{y2}" class="ln {c}" marker-end="url(#{m})"{" stroke-dasharray=\"5 4\"" if dash else ""}/>'
    h = NW / 2
    o.append(node(0, 'LD', ('Mở Trang chủ', 'xem quá hạn'), ('Open Home', 'see overdue')))
    o.append(node(0, 'CV', ('Việc của tôi', 'theo hạn chót'), ('My work', 'by deadline')))
    o.append(node(1, 'LD', ('Ủy quyền', 'cho thư ký'), ('Delegate', 'to assistant'), 'n alt'))
    o.append(node(2, 'LD', ('Giao việc', 'vào đúng Phòng'), ('Assign to', 'a department')))
    o.append(node(2, 'TK', ('Giao thay', '"Thay mặt cho"'), ('On behalf', '"Thay mặt cho"'), 'n alt'))
    o.append(node(3, 'CV', ('Nhận & làm', 'trạng thái, việc con'), ('Receive & do', 'status, sub-tasks')))
    o.append(node(3, 'SYS', ('Nhắc hạn', 'theo ưu tiên'), ('Reminder', 'by priority'), 'n sys'))
    o.append(node(4, 'TK', ('Bình luận @', 'đôn đốc'), ('@comments', 'follow up')))
    o.append(node(4, 'SYS', ('Thông báo', 'chuông · email'), ('Notify', 'bell · email'), 'n sys'))
    o.append(node(5, 'CV', ('Nộp để duyệt', 'kèm file'), ('Submit', 'with files')))
    o.append(node(5, 'LD', ('Chấp nhận /', 'Từ chối'), ('Accept /', 'Reject'), 'n dec'))
    o.append(node(6, 'LD', ('Theo dõi', '"Do tôi giao"'), ('Track', '"Assigned by me"')))
    o.append(node(7, 'LD', ('Chấm điểm', '3 tiêu chí'), ('Score', '3 criteria')))
    o.append(node(7, 'SYS', ('Báo cáo', 'Phòng · Copilot'), ('Report', 'dept · Copilot'), 'n sys'))
    o.append(line(X(0) + h, Y['LD'], X(1) - h - 2, Y['LD']))
    o.append(line(X(1) + 10, Y['LD'] + 27, X(2) - 20, Y['TK'] - 29, 'or', 'arB', True))
    o.append(f'<text x="{X(1) + 4}" y="{Y["TK"] - 2}" text-anchor="middle" class="lb ort"><tspan class="vi">cho phép giao thay</tspan><tspan class="en">allows on-behalf</tspan></text>')
    o.append(line(X(2), Y['TK'] - 27, X(2), Y['LD'] + 29, '', 'ar', True))
    o.append(line(X(2) + 30, Y['LD'] + 27, X(3) - 20, Y['CV'] - 29, 'or', 'arB'))
    o.append(f'<text x="{X(3) - 44}" y="{Y["CV"] - 50}" text-anchor="end" class="lb ort"><tspan class="vi">việc + hạn + ưu tiên</tspan><tspan class="en">task + deadline + priority</tspan></text>')
    o.append(line(X(0) + h, Y['CV'], X(3) - h - 2, Y['CV']))
    o.append(line(X(3), Y['SYS'] - 27, X(3), Y['CV'] + 29, 'gr', 'arG', True))
    o.append(line(X(3) + h, Y['CV'] - 10, X(4) - h, Y['TK'] + 10, '', 'ar', True))
    o.append(line(X(4), Y['SYS'] - 27, X(4), Y['TK'] + 29, 'gr', 'arG', True))
    o.append(line(X(3) + h, Y['CV'], X(5) - h - 2, Y['CV']))
    o.append(line(X(5) + 22, Y['CV'] - 27, X(5) + 22, Y['LD'] + 29, 'or', 'arB'))
    o.append(line(X(5) - 22, Y['LD'] + 27, X(5) - 22, Y['CV'] - 29, 'rj', 'arR', True))
    o.append(f'<text x="{X(5) - 28}" y="{Y["TK"] + 44}" text-anchor="end" class="lb rjt"><tspan class="vi">Từ chối → làm lại</tspan><tspan class="en">Rejected → redo</tspan></text>')
    o.append(f'<text x="{X(5) + 28}" y="{Y["TK"] + 4}" class="lb ort"><tspan class="vi">bài nộp</tspan><tspan class="en">submission</tspan></text>')
    o.append(line(X(5) + h, Y['LD'], X(6) - h - 2, Y['LD'], 'gr', 'arG'))
    o.append(f'<text x="{(X(5) + X(6)) / 2}" y="{Y["LD"] - 34}" text-anchor="middle" class="lb gt"><tspan class="vi">Hoàn thành</tspan><tspan class="en">Done</tspan></text>')
    o.append(line(X(6) + h, Y['LD'], X(7) - h - 2, Y['LD']))
    o.append(line(X(7), Y['SYS'] - 27, X(7), Y['LD'] + 29, 'gr', 'arG', True))
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
    ('t00_trang_chu', ('Một màn hình thấy toàn bộ việc', 'One screen for all work'),
     ('Trang chủ đếm sẵn việc hoạt động, quá hạn, tạm dừng, hoàn thành — không cần hỏi từng Phòng.', 'Home counts active, overdue, paused and done tasks — no need to ask each department.'),
     ('Chắc chắn', 'Certain'), ('Hiện tại: 43 hoạt động · 13 quá hạn', 'Now: 43 active · 13 overdue'), ('Tổng hợp qua Zalo, sổ tay, gọi điện', 'Compiled from chat, notebooks, calls')),
    ('t36_nhac_nho', ('Nhắc hạn tự động', 'Automatic reminders'),
     ('Hệ thống tự nhắc trước hạn theo độ ưu tiên và cảnh báo lặp khi quá hạn.', 'The system reminds before deadlines by priority and repeats when overdue.'),
     ('Chắc chắn', 'Certain'), ('Khẩn cấp: trước 3 ngày', 'Urgent: 3 days ahead'), ('Thư ký nhắc thủ công', 'Assistants reminded by hand')),
    ('t18_duyet_bai_nop', ('Duyệt có dấu vết', 'Traceable approval'),
     ('Mọi bài nộp, lần từ chối, lý do đều lưu trong việc.', 'Every submission, rejection and reason is kept with the task.'),
     ('Chắc chắn', 'Certain'), ('100% việc hoàn thành có người chấp nhận', '100% of done tasks have an approver'), ('Báo miệng "xong rồi"', '"Done" by word of mouth')),
    ('t37_bao_cao', ('Báo cáo Phòng tức thì', 'Instant department report'),
     ('Tỉ lệ đúng hạn, thời gian chu kỳ, danh sách cần chú ý — xuất file cho giao ban.', 'On-time rate, cycle time, needs-attention list — export for briefings.'),
     ('Mục tiêu', 'Target'), ('Giảm ≥30% việc quá hạn sau 3 tháng', '≥30% fewer overdue tasks in 3 months'), ('Tổng hợp Excel cuối tuần', 'Weekly Excel compilation')),
    ('t28_phieu_danh_gia', ('Đánh giá có trọng số', 'Weighted appraisal'),
     ('Chất lượng 40% · Tiến độ 30% · Khối lượng 30% — điểm cộng dồn theo người.', 'Quality 40% · Timeliness 30% · Volume 30% — scores accumulate per person.'),
     ('Mục tiêu', 'Target'), ('100% việc quan trọng có điểm', '100% of key tasks scored'), ('Đánh giá cảm tính cuối kỳ', 'Gut-feel year-end review')),
]

def benefits():
    o = ['<div class="ben">']
    for key, t, d, lab, num, before in BEN:
        cls = 'ok' if lab[0] == 'Chắc chắn' else 'tg'
        o.append(f'<div class="bc"><div class="bt"><h4>{LP(t)}</h4><p>{LP(d)}</p><p class="num"><span class="lab {cls}">{LP(lab)}</span>{LP(num)}</p>'
                 f'<p class="bef">{L("Trước:", "Before:")} <s>{LP(before)}</s></p><a href="{C.IMG_LINK[key]}" target="_blank" rel="noopener">{L("Xem trên Base ↗", "View on Base ↗")}</a></div>{fig(key)}</div>')
    o.append('</div>')
    o.append(f'''<div class="aiblk"><div class="aih"><span>✦ AI</span><h4>{L("Copilot đọc việc, tóm tắt và gợi ý bước tiếp", "Copilot reads the task, summarizes and suggests next steps")}</h4>
<p>{L("Có sẵn ở tab COPILOT trong form giao việc và trong từng việc. Câu trả lời bên dưới là thật, chạy trên việc Bệnh viện HTC.", "Built into the COPILOT tab of the assign form and every task. The answer below is real, run on the Bệnh viện HTC task.")}</p>
<div class="aik"><div><b>~1 {L("phút", "min")}</b><span>{L("đọc nắm tình hình 1 việc", "to grasp one task")}</span><em>{L("Mục tiêu", "Target")}</em></div>
<div><b>-50%</b><span>{L("thời gian soạn mô tả", "time writing descriptions")}</span><em>{L("Mục tiêu", "Target")}</em></div>
<div><b>0</b><span>{L("thao tác AI tự lưu — người bấm duyệt", "AI auto-saves — people approve")}</span><em>{L("Chắc chắn", "Certain")}</em></div></div></div>
<div class="aiimgs">{fig("t25_copilot_tra_loi")}{fig("t26_copilot_buoc_tiep")}</div></div>''')
    return ''.join(o)

def statuses():
    st = [('Mở', 'Open', '#94a3b8'), ('Đang thực hiện', 'In progress', '#ffb300'), ('Đang duyệt', 'Under review', '#0068ff'), ('Hoàn thành', 'Done', '#16a34a')]
    a = '<span class="sa">→</span>'.join(f'<span class="st" style="--sc:{c}">{L(v, e)}</span>' for v, e, c in st)
    return (f'<div class="stl">{a}</div><div class="stl2"><span class="st" style="--sc:#94a3b8">{L("Tạm dừng", "Paused")}</span><span class="st" style="--sc:#ff3b5c">{L("Đã huỷ", "Cancelled")}</span>'
            f'<span class="stn">{L("Đang duyệt → Từ chối quay lại Mở/Đang thực hiện. Chỉ người có quyền Lifecycle đổi trạng thái trực tiếp.", "Under review → Rejected returns to Open/In progress. Only Lifecycle holders change status directly.")}</span></div>')

# ---------- AI ----------
def ai():
    q = ''.join(f'<tr><td><span class="chip" style="--rc:{ROLE[r]["color"]}">{LP(ROLE[r]["short"])}</span></td><td>{LP(t)}</td><td><button class="cpy" data-copy="{html.escape(t[0])}">{L("Chép", "Copy")}</button></td></tr>' for r, t in C.AI_QS)
    rules = [('Copilot chỉ đọc dữ liệu việc bạn đang mở — mô tả càng rõ, trả lời càng đúng.', 'Copilot reads only the open task — richer descriptions, better answers.'),
             ('AI gợi ý, người quyết: Chấp nhận / Từ chối vẫn do người bấm.', 'AI suggests, people decide: Accept / Reject stays human.'),
             ('Không dán mật khẩu, số tài khoản vào ô hỏi.', 'Never paste passwords or account numbers.'),
             ('Kiểm tra lại số liệu, ngày tháng trước khi gửi đi.', 'Double-check figures and dates before sending.'),
             ('Câu hỏi tốt = Việc gì + muốn biết gì + để làm gì.', 'A good prompt = which task + what you want + why.')]
    return (f'<div class="aimap"><div><h5>{L("Copilot trong form giao việc", "Copilot in the assign form")}</h5><p>{L("Soạn, trau chuốt, kiểm tra yêu cầu trước khi tạo.", "Draft, polish and check a request before creating.")}</p></div>'
            f'<div><h5>{L("Copilot trên từng việc", "Copilot on each task")}</h5><p>{L("Tóm tắt, chỉ việc con trễ, gợi ý bước tiếp, đọc bài nộp.", "Summarize, flag late sub-tasks, suggest next steps, read submissions.")}</p></div></div>'
            f'<div class="g2">{fig("t24_copilot_form", ("① tab COPILOT · ② ô hỏi", "① COPILOT tab · ② prompt box"))}{fig("t25_copilot_tra_loi", ("① câu hỏi · ② câu trả lời có cấu trúc", "① question · ② structured answer"))}</div>'
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
    return (f'<div class="isbar"><input id="isq" type="search" placeholder="Gõ vấn đề, vd: không hoàn thành được, giao nhầm, quá hạn…" data-ph-en="Type a problem, e.g. can\'t complete, wrong assignee, overdue…" autocomplete="off">'
            f'<div class="ifs">{chips}</div><span id="iscnt"></span></div><div id="isl">{"".join(cards)}</div>'
            f'<p id="isnone" hidden>{L("Không thấy tình huống phù hợp. Thử từ khác, hoặc liên hệ Quản trị app.", "No match. Try other words or contact the app admin.")}</p>')

def setup():
    o = []
    for s in C.SETUP:
        o.append(f'<div class="su" id="{s["id"]}"><div class="sut"><span class="sid">{s["id"]}</span><h4>{LP(s["title"])}</h4>{pins(L(s["body"][0], s["body"][1], "p"))}</div>{fig(s["img"])}</div>')
    o.append(f'<h4>{L("Checklist khi thêm/đổi Phòng", "Checklist when adding/changing a department")}</h4><ul class="chk">' + ''.join(f'<li>{LP(c)}</li>' for c in C.CHECKLIST) + '</ul>')
    return ''.join(o)

def toc():
    parts = [
        ('I', '#2563eb', ('Tổng quan', 'Overview'), [('s-flow', ('1 · Lưu đồ công việc', '1 · Work flow')), ('s-status', ('2 · Trạng thái một việc', '2 · Task statuses')), ('s-ben', ('3 · Lợi ích', '3 · Benefits'))]),
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
        '{{band1}}': band('I', '#2563eb', ('Tổng quan', 'Overview'), ('Mục 1–3 · Việc chạy thế nào, ai làm gì', 'Sections 1–3 · How work flows, who does what')),
        '{{band2}}': band('II', '#0e9f6e', ('Hướng dẫn chi tiết', 'Step-by-step guide'), ('Mục 4–5 · 8 bước, ảnh thật có đánh số', 'Sections 4–5 · 8 steps, numbered real screenshots')),
        '{{band3}}': band('III', '#e5383b', ('Gặp vấn đề?', 'Troubleshooting'), ('Mục 6 · Gõ vấn đề, ra cách xử lý', 'Section 6 · Type a problem, get the fix')),
        '{{band4}}': band('IV', '#7c3aed', ('Setup cho Quản trị app', 'Admin setup'), ('S1–S7 · Cài đặt Phòng, phân quyền, nhắc hạn', 'S1–S7 · Department settings, permissions, reminders')),
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
