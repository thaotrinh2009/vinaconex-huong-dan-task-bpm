# -*- coding: utf-8 -*-
"""Gộp 2 trang hướng dẫn thành index.html có 2 tab.
Chạy: python3 build_tabs.py  (đọc bpm/index.html và eoffice/index.html)"""
import html, os

HERE = os.path.dirname(os.path.abspath(__file__))
TABS = [
    ('bpm', 'App Công việc & BPM', 'bpm/index.html'),
    ('eoffice', 'E-office · Công văn đến, đi', 'eoffice/index.html'),
]

FIX = '''<script>document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="#"]');if(!a)return;var id=decodeURIComponent(a.getAttribute('href').slice(1));e.preventDefault();var t=id?document.getElementById(id):null;if(t)t.scrollIntoView({behavior:'smooth',block:'start'});else if(!id)window.scrollTo(0,0)},true);</script>'''
frames, buttons = [], []
for i, (key, label, path) in enumerate(TABS):
    src = open(os.path.join(HERE, path), encoding='utf-8').read()
    # Trong iframe srcdoc, link "#muc" bị hiểu theo địa chỉ trang ngoài và tải lại cả trang.
    # Chặn lại và cuộn trong chính tài liệu.
    src += FIX
    buttons.append('<button type="button" role="tab" id="t-%s" data-k="%s" aria-controls="p-%s" aria-selected="%s">%s</button>'
                   % (key, key, key, 'true' if i == 0 else 'false', html.escape(label)))
    frames.append('<iframe id="p-%s" role="tabpanel" aria-labelledby="t-%s" title="%s"%s srcdoc="%s"></iframe>'
                  % (key, key, html.escape(label), '' if i == 0 else ' hidden', html.escape(src, quote=True)))

page = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Hướng dẫn sử dụng Base · Vinaconex</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@500;600;700&display=swap">
<style>
:root{--bar:#ffffff;--ink:#122038;--mute:#56657d;--line:#d9e1ec;--navy:#003989;--on:#ffffff;color-scheme:light}
@media (prefers-color-scheme: dark){:root{--bar:#131d2e;--ink:#e6edf8;--mute:#9aabc4;--line:#26354d;--navy:#8fb4ff;--on:#0c1320;color-scheme:dark}}
*{box-sizing:border-box}
html,body{height:100%;margin:0}
body{background:var(--bar);color:var(--ink);font:500 14px "Lexend",system-ui,-apple-system,"Segoe UI",sans-serif;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:18px;padding:8px 16px;padding-top:calc(8px + env(safe-area-inset-top,0px));border-bottom:1px solid var(--line);background:var(--bar);flex:none;flex-wrap:wrap}
.brand{font-weight:700;font-size:16px;color:var(--navy);white-space:nowrap}
.brand span{color:var(--mute);font-weight:500}
.tabs{display:flex;gap:6px;flex-wrap:wrap}
.tabs button{font:600 14px "Lexend",system-ui,sans-serif;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:999px;padding:7px 16px;cursor:pointer}
.tabs button:hover{border-color:var(--navy)}
.tabs button[aria-selected="true"]{background:var(--navy);border-color:var(--navy);color:var(--on)}
.tabs button:focus-visible{outline:2px solid var(--navy);outline-offset:2px}
iframe{flex:1;width:100%;border:0;display:block;min-height:0}
iframe[hidden]{display:none}
@media (max-width:600px){.brand span{display:none}.top{gap:10px}.tabs button{padding:6px 12px;font-size:13px}}
</style>
</head>
<body>
<header class="top">
  <div class="brand">Base.vn × Vinaconex <span>· Hướng dẫn sử dụng</span></div>
  <nav class="tabs" role="tablist" aria-label="Chọn tài liệu">""" + ''.join(buttons) + """</nav>
</header>
""" + '\n'.join(frames) + """
<script>
(function(){
  var btns=[].slice.call(document.querySelectorAll('.tabs button'));
  function show(k,push){
    if(!document.getElementById('p-'+k)) k=btns[0].getAttribute('data-k');
    btns.forEach(function(b){
      var on=b.getAttribute('data-k')===k;
      b.setAttribute('aria-selected',on?'true':'false');
      document.getElementById('p-'+b.getAttribute('data-k')).hidden=!on;
    });
    if(push && location.hash!=='#'+k){try{history.replaceState(null,'','#'+k)}catch(e){location.hash=k}}
  }
  btns.forEach(function(b){b.addEventListener('click',function(){show(b.getAttribute('data-k'),true)})});
  show((location.hash||'').slice(1),false);
  addEventListener('hashchange',function(){show(location.hash.slice(1),false)});
})();
</script>
</body>
</html>
"""
open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(page)
print('index.html', os.path.getsize(os.path.join(HERE, 'index.html')))
