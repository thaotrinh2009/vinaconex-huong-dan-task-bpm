# -*- coding: utf-8 -*-
"""Chú thích ảnh: ghim số đỏ (đốt thẳng vào ảnh), khung nhấn, làm mờ dữ liệu test.
Toạ độ theo khung chụp gốc 1280x665 (ảnh zoom theo khung riêng)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

SRC = os.path.join(os.path.dirname(__file__), 'img')
OUT = os.path.join(os.path.dirname(__file__), 'img_out')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
RED = (0, 71, 204)   # navy pin (cta-via)
BOX = (0, 104, 255)  # accent

def B(*boxes, blur=(), S=1.35):
    return dict(marks=[(n + 1, b[0], b[1]) for n, b in enumerate(boxes)], boxes=list(boxes), blur=list(blur), S=S)

A = {
 'b00_viec_cua_toi': B((8,108,211,140),(244,104,660,140),(256,172,640,202),(1140,236,1196,260),(614,58,878,89),(1045,58,1167,89), blur=[(296,432,570,476)]),
 'b01_luong_lien_ket': B((243,104,350,140),(232,155,354,212),(370,165,1130,640)),
 'b02_danh_sach': B((355,104,445,140),(244,166,500,192),(244,206,572,334),(930,58,1130,89),(8,190,211,520)),
 'b03_pipeline': B((244,104,320,140),(244,253,525,295),(546,308,806,450),(743,624,794,648),(495,104,600,140),(1122,58,1256,89)),
 'b04_quy_trinh_zoom': B((136,50,278,92),(145,118,272,136),(138,420,278,462),(142,490,272,510),(228,548,370,600), S=2.0),
 'b04_quy_trinh': B((495,104,594,140),(528,158,970,192),(1006,58,1114,89)),
 'b05_form_tao': B((50,150,1225,206),(50,222,1225,278),(50,316,140,356),(50,374,1225,545),(1018,560,1105,593),(1113,560,1231,593)),
 'b06_chon_don_vi': B((413,99,867,133),(413,184,861,223),(785,580,867,613)),
 'b07_form_bang': B((50,140,1225,358),(1062,140,1218,168),(55,372,130,395),(50,434,1225,468),(1018,560,1105,593),(1113,560,1231,593)),
 'b08_chi_tiet': B((244,158,640,182),(244,200,442,230),(244,252,832,288),(244,300,832,373),(872,346,1248,498),(872,560,1248,630)),
 'b09_thao_luan_sla': B((244,386,832,500),(244,528,832,645),(872,480,1248,545),(872,570,1248,632)),
 'b10_lich_su': B((394,112,442,146),(258,180,1234,295),(258,306,1234,485),(258,495,1234,600)),
 'b11_can_ban_duyet': B((244,192,880,214),(244,286,832,346),(637,302,722,332),(730,302,816,332),(1098,296,1243,321),(872,508,1248,570)),
 'b12_cong_viec_con': B((330,200,454,226),(637,308,800,345),(244,340,832,497),(258,460,818,484)),
 'b13_trinh_ky': B((244,251,832,290),(716,399,815,431),(258,455,818,491),(700,515,774,543)),
 'b14_phieu_thanh_toan': B((400,158,732,182),(660,320,800,372),(872,346,1248,498),(306,530,800,570)),
 'b15_menu_phieu': B((1058,268,1246,300),(1058,300,1246,332),(1058,334,1246,366),(1058,410,1246,442),(1058,486,1246,518),(1058,562,1246,594)),
 'b16_in_xuat': B((434,176,846,209),(434,250,846,287),(773,320,846,351)),
 'b17_ai_that_bai': B((261,384,815,436),(261,450,815,480),(261,505,600,530),(730,555,815,588)),
 'b18_buoc_xu_ly': B((434,305,636,352),(548,398,660,426),(260,452,816,470),(778,492,800,516),(872,346,1248,480)),
 'b19_ai_bang_vat_tu': B((306,180,800,208),(306,248,800,442),(778,224,800,242),(306,484,800,512)),
 'b20_bao_cao': B((926,58,1256,89),(244,120,433,267),(447,120,1248,267),(584,284,908,660)),
 'b21_tro_ly_ai': B((702,9,732,38),(1104,60,1266,87),(840,560,1260,655)),
 'b22_ai_tom_tat': B((890,90,1254,148),(842,160,1204,496),(930,618,1104,642)),
 'b23_bao_cao_dv': B((722,104,812,140),(916,168,1245,195),(246,209,1246,473)),
 'b24_bang': B((435,104,495,140),(244,155,560,186),(571,155,808,186),(820,155,951,186),(751,248,842,295), blur=[(300,592,560,630)]),
 'b25_ycvt_luong': B((262,40,360,80),(280,128,375,166),(40,318,134,355),(42,362,132,378), S=2.0),
 'b30_cai_dat_chung': B((266,140,466,240),(266,256,466,490),(520,270,1240,312),(1149,76,1251,105)),
 'b31_thanh_vien_quyen': B((517,206,1240,250),(517,266,1240,312),(517,326,1240,370),(517,386,1240,430)),
 'b32_thoi_han': B((517,221,1240,255),(517,313,1240,347),(517,400,1010,418)),
 'b33_mau_in': B((517,264,1240,334),(517,349,637,381),(517,410,690,435)),
 'b34_sua_luong': B((10,140,210,200),(10,240,210,340),(10,375,210,580),(1003,8,1120,40),(862,85,930,112)),
 'b35_khoi_duyet': B((252,200,318,226),(656,170,970,192),(670,358,1244,390),(686,470,1244,500),(686,566,1244,598)),
}

def font(sz):
    return ImageFont.truetype(FONT, sz)

def render(key, scale=1.0):
    a = A[key]
    src = os.path.join(SRC, key + '.jpg')
    if not os.path.exists(src):
        src = os.path.join(SRC, key + '.png')
    im = Image.open(src).convert('RGB')
    for (x0, y0, x1, y1) in a.get('blur', []):
        reg = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(9))
        im.paste(reg, (x0, y0))
    # nhẹ tay làm nét
    if a.get('S', 1.35) <= 1.35:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.1, percent=70, threshold=2))
    # phóng nhẹ cho nét chữ ghim
    S = a.get('S', 1.35)
    im = im.resize((int(im.width * S), int(im.height * S)), Image.LANCZOS)
    if S > 1.35:
        im = im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=90, threshold=2))
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for (x0, y0, x1, y1) in a.get('boxes', []):
        d.rounded_rectangle((x0*S-3, y0*S-3, x1*S+3, y1*S+3), radius=9, outline=BOX + (230,), width=2, fill=BOX + (16,))
    f = font(19)
    for (n, x, y) in a.get('marks', []):
        # ghim đặt lệch lên trên-trái của điểm để không che chữ
        cx, cy, r = x*S, y*S, 17
        bx = boxes_for(a, n)
        if bx:
            cx, cy = bx[0]*S - 4, bx[1]*S - 4
            cx = max(r + 2, cx); cy = max(r + 2, cy)
        d.ellipse((cx-r-3, cy-r-3, cx+r+3, cy+r+3), fill=(255, 255, 255, 255))
        d.ellipse((cx-r, cy-r, cx+r, cy+r), fill=RED + (255,))
        t = str(n)
        w = d.textlength(t, font=f)
        d.text((cx - w/2, cy - 12), t, font=f, fill=(255, 255, 255, 255))
    im = Image.alpha_composite(im.convert('RGBA'), ov).convert('RGB')
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, key + '.jpg')
    im.save(p, quality=90, subsampling=0, optimize=True)
    web = os.path.join(os.path.dirname(__file__), 'web')
    os.makedirs(web, exist_ok=True)
    im.save(os.path.join(web, key + '.webp'), 'WEBP', quality=84, method=6)
    return p, im.size

def boxes_for(a, n):
    bs = a.get('boxes', [])
    idx = [i for i, m in enumerate(a.get('marks', [])) if m[0] == n]
    if idx and idx[0] < len(bs):
        return bs[idx[0]]
    return None

if __name__ == '__main__':
    import sys
    for k in (sys.argv[1:] or A):
        print(render(k))
