# -*- coding: utf-8 -*-
import base64, json, os, html
from data import *
from coords import C

HERE = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(HERE, '..', 'anh')
W, H = 1568, 746

def pct(v, t): return '%.2f%%' % (v * 100.0 / t)

IMGS = {}
def anno(key, marks, boxes):
    f, cap, lk = SHOT[key]
    s = '<figure class="fig"><button type="button" class="anno" aria-label="Phóng to ảnh: %s">' % html.escape(cap)
    s += '<img src="%s" width="%d" height="%d" alt="%s" decoding="async">' % (IMGS[key], W, H, html.escape(cap))
    for (x0, y0, x1, y1) in boxes:
        s += '<span class="bx" style="left:%s;top:%s;width:%s;height:%s"></span>' % (pct(x0, W), pct(y0, H), pct(x1 - x0, W), pct(y1 - y0, H))
    for i, m in enumerate(marks):
        s += '<span class="mk %s" style="left:%s;top:%s"><b>%d</b></span>' % (m[3] if len(m) > 3 else 'l', pct(m[0], W), pct(m[1], H), i + 1)
    s += '</button><figcaption>%s · <a href="%s" target="_blank" rel="noopener">Mở màn hình này ↗</a></figcaption></figure>' % (html.escape(cap), L[lk])
    return s

def links(ls):
    return '<div class="links"><span class="ll">Mở trên E-office</span>' + ''.join(
        '<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (L[k], html.escape(t)) for t, k in ls) + '</div>'

def step(s, proc):
    roles = ' '.join(s['rt'].keys())
    o = '<article class="step" id="%s" data-roles="%s">' % (s['id'], roles)
    o += '<header class="sh"><span class="sn">%s%d</span><div class="st"><h3>%s</h3><div class="pills">' % (
        'Đ' if proc == 'in' else 'Đi', s['n'], s['name'])
    o += '<span class="pill role" style="--c:var(--r-%s)">%s</span>' % (s['role'], ROLES[s['role']][0])
    o += '<span class="pill sla">⏱ %s</span></div></div></header>' % s['sla']
    o += '<div class="you" hidden></div>'
    o += '<dl class="w5"><div><dt>Ai làm</dt><dd>%s</dd></div><div><dt>Biểu mẫu, việc</dt><dd>%s</dd></div><div><dt>Xong khi</dt><dd>%s</dd></div></dl>' % (
        s['who'], html.escape(s['form']), s['done'])
    o += '<div class="who">' + ''.join('<span class="chip-s" style="--c:var(--r-%s)"><b>%s</b> %s</span>' % (r, ROLES[r][0], t) for r, t in s['rt'].items()) + '</div>'
    o += links(s['links'])
    k = 0
    for bi, (title, key, marks, boxes) in enumerate(s['blocks']):
        k += 1
        cc = C.get((s['id'], bi))
        if cc:
            assert len(cc) == len(marks), (s['id'], bi)
            marks = [(c[0], c[1], m[2], c[2]) for c, m in zip(cc, marks)]
        o += '<section class="blk"><h4><span class="tk">Thao tác %d</span>%s</h4>' % (k, title)
        o += anno(key, marks, boxes)
        o += '<ol class="acts">' + ''.join('<li><span class="n">%d</span><span>%s</span></li>' % (i + 1, m[2]) for i, m in enumerate(marks)) + '</ol></section>'
    if s.get('after'):
        k += 1
        o += '<section class="blk"><h4><span class="tk">Thao tác %d</span>%s</h4><ol class="plain">%s</ol></section>' % (
            k, 'Tiếp theo' if s['blocks'] else 'Cách làm', ''.join('<li>%s</li>' % a for a in s['after']))
    if s.get('note'):
        o += '<p class="note"><b>Lưu ý.</b> %s</p>' % s['note']
    o += '</article>'
    return o

OVL = {
 'in': [('Văn thư (người tạo)', '8 giờ', 'Form văn bản đến, Đánh số VB'), ('Thư ký (gán thủ công)', '24 giờ', 'Xem xét và cho ý kiến, Bút phê'),
        ('Lãnh đạo được giao', '48 giờ', 'Lãnh đạo phê duyệt'), ('Đơn vị chủ trì (tự giao theo Phòng ban chủ trì)', '24 giờ', 'Thực hiện theo ý kiến, Tạo phúc đáp'),
        ('Người phụ trách văn bản', '—', 'Không có việc bắt buộc'), ('Người phụ trách văn bản', '—', 'Gán tủ hồ sơ')],
 'out': [('Người soạn (chọn khi tạo)', '24 giờ', 'Form văn bản đi, bản thảo'), ('Quản lý trực tiếp người soạn', '24 giờ', 'Xem xét và cho ý kiến'),
         ('Thư ký (gán thủ công)', '24 giờ', 'Xem xét và cho ý kiến'), ('Người soạn trình, Lãnh đạo ký', '24 giờ', 'Trình ký, Ký điện tử'),
         ('Văn thư (tự giao)', '8 giờ', 'Đăng ký và cấp số'), ('Văn thư', '—', 'Không có việc bắt buộc'), ('Văn thư', '—', 'Gán tủ hồ sơ')],
}

def overview(lst, key):
    n = len(lst)
    o = '<div class="ovw"><div class="ov" style="grid-template-columns:110px repeat(%d,minmax(118px,1fr))">' % n
    o += '<div class="lane">Flow</div>' + ''.join('<a class="chev" href="#%s" data-roles="%s" style="--c:var(--r-%s)"><span>%d</span>%s</a>' % (
        s['id'], ' '.join(s['rt']), s['role'], s['n'], s['name']) for s in lst)
    for i, lane in enumerate(['Người thực hiện', 'Thời gian', 'Biểu mẫu']):
        o += '<div class="lane">%s</div>' % lane
        for j, r in enumerate(OVL[key]):
            o += '<div class="cell%s" data-roles="%s">%s</div>' % (' t' if i == 1 else '', ' '.join(lst[j]['rt']), r[i])
    return o + '</div></div>'

def matrix():
    cols = [('Đ', s) for s in IN] + [('Đi', s) for s in OUT]
    o = '<div class="tw"><table class="mx"><thead><tr><th>Vai trò</th>'
    o += '<th colspan="%d" class="grp">Văn bản đến</th><th colspan="%d" class="grp">Văn bản đi</th></tr><tr><th></th>' % (len(IN), len(OUT))
    o += ''.join('<th><a href="#%s" title="%s">%s%d</a></th>' % (s['id'], s['name'], p, s['n']) for p, s in cols) + '</tr></thead><tbody>'
    for r in ORDER:
        o += '<tr data-r="%s" style="--c:var(--r-%s)"><th><button type="button" class="rpick" data-r="%s">%s</button></th>' % (r, r, r, ROLES[r][0])
        for p, s in cols:
            if r == 'quantri':
                o += '<td><span class="dot o" title="Xử lý thay khi cần">○</span></td>'
            elif r in s['rt']:
                main = s['role'] == r
                o += '<td><span class="dot%s" title="%s">%s</span></td>' % ('' if main else ' o', html.escape(s['rt'][r]), '●' if main else '○')
            else:
                o += '<td></td>'
        o += '</tr>'
    return o + '</tbody></table></div><p class="legend"><span class="dot">●</span> làm chính ở bước <span class="dot o">○</span> tham gia hoặc làm thay. Bấm tên vai trò để lọc tài liệu theo vai trò đó.</p>'

def rolecards():
    o = '<div class="rcards">'
    for r in ORDER:
        ins = [s for s in IN if r in s['rt']]; outs = [s for s in OUT if r in s['rt']]
        o += '<div class="rc" style="--c:var(--r-%s)"><h3>%s</h3><p>%s</p>' % (r, ROLES[r][0], ROLES[r][1])
        if r == 'quantri':
            o += '<p class="sm">Thấy và xử lý được mọi văn bản của dịch vụ. Dùng Phân công người thực hiện khi ai đó vắng.</p>'
        else:
            if ins: o += '<h4>Văn bản đến</h4><ul>' + ''.join('<li><a href="#%s">B%d %s</a>: %s</li>' % (s['id'], s['n'], s['name'], s['rt'][r]) for s in ins) + '</ul>'
            if outs: o += '<h4>Văn bản đi</h4><ul>' + ''.join('<li><a href="#%s">B%d %s</a>: %s</li>' % (s['id'], s['n'], s['name'], s['rt'][r]) for s in outs) + '</ul>'
        o += '</div>'
    return o + '</div>'

def toc():
    o = '<nav class="toc" aria-label="Mục lục"><p class="tl">Mục lục</p><a href="#tong-quan">I. Tổng quan</a>'
    o += '<a href="#den">II. Văn bản đến</a>' + ''.join('<a class="s" href="#%s" data-roles="%s">B%d %s</a>' % (s['id'], ' '.join(s['rt']), s['n'], s['name']) for s in IN)
    o += '<a href="#di">III. Văn bản đi</a>' + ''.join('<a class="s" href="#%s" data-roles="%s">B%d %s</a>' % (s['id'], ' '.join(s['rt']), s['n'], s['name']) for s in OUT)
    o += '<a href="#phu-luc">IV. Phụ lục</a><a class="s" href="#can-xac-nhan">Cần xác nhận</a><a class="s" href="#hoi-nhanh">Hỏi nhanh</a></nav>'
    return o

def imgs():
    d = {}
    for k, (f, c, l) in SHOT.items():
        d[k] = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(SHOTS, f), 'rb').read()).decode()
    return json.dumps(d)

for _k, (_f, _c, _l) in SHOT.items():
    IMGS[_k] = 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(SHOTS, _f), 'rb').read()).decode()
t = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
rules = ''.join('<tr><td>%s</td><td%s>%s</td></tr>' % (html.escape(a), ' class="flag"' if b.startswith('Chưa') else '', html.escape(b)) for a, b in RULES)
chips = ''.join('<button type="button" class="chip" data-r="%s" aria-pressed="false" style="--c:var(--r-%s)">%s</button>' % (r, r, ROLES[r][0]) for r in ORDER)
rt = {s['id']: s['rt'] for s in IN + OUT}
rn = {r: ROLES[r][0] for r in ORDER}
rep = {
 '{{toc}}': toc(), '{{chips}}': chips, '{{ov_in}}': overview(IN, 'in'), '{{ov_out}}': overview(OUT, 'out'),
 
 '{{steps_in}}': ''.join(step(s, 'in') for s in IN), '{{steps_out}}': ''.join(step(s, 'out') for s in OUT),
 '{{rules}}': rules, '{{L_in_k}}': L['in_k'], '{{L_out_k}}': L['out_k'], '{{L_docs}}': L['docs'], '{{L_appr}}': L['appr'],
 '{{L_in_new}}': L['in_new'], '{{L_out_new}}': L['out_new'], '{{L_cnt}}': L['cnt'], '{{L_d_num}}': L['d_num'], '{{L_d_in}}': L['d_in'],
 '{{rt}}': json.dumps(rt, ensure_ascii=False), '{{rn}}': json.dumps(rn, ensure_ascii=False), 
}
for k, v in rep.items():
    t = t.replace(k, v)
assert '{{' not in t, t[t.index('{{'):t.index('{{') + 40]
out = os.path.join(HERE, '..', 'index.html')
open(out, 'w', encoding='utf-8').write(t)
print(out, os.path.getsize(out))
