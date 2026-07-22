# -*- coding: utf-8 -*-
"""元僑科技官網原型建置腳本：python3 build.py 產生 site/*.html"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "site")

NAV = [
    ("index.html", "首頁"),
    ("netapp.html", "NetApp儲存"),
    ("lto.html", "LTO磁帶"),
    ("parts.html", "二手零件"),
    ("rental.html", "Storage租賃"),
    ("security.html", "資訊安全"),
    ("ai.html", "AI解決方案"),
    ("cases.html", "成功案例"),
    ("about.html", "關於我們"),
]

# ---- 單色線條 icon（取代 emoji，維持企業感與跨裝置一致）----
ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>',
    "server": '<rect x="2" y="3" width="20" height="7" rx="1.5"/><rect x="2" y="14" width="20" height="7" rx="1.5"/><path d="M6 6.5h.01M6 17.5h.01"/>',
    "tape": '<rect x="2" y="5" width="20" height="14" rx="2"/><circle cx="8.5" cy="12" r="2"/><circle cx="15.5" cy="12" r="2"/><path d="M8.5 14h7"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    "box": '<path d="m21 8-9-5-9 5v8l9 5 9-5V8z"/><path d="m3 8 9 5 9-5"/><path d="M12 13v8"/>',
    "shield": '<path d="M12 22s8-3 8-10V5l-8-3-8 3v7c0 7 8 10 8 10z"/>',
    "bot": '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4.5"/><circle cx="12" cy="3.5" r="1"/><path d="M9 14h.01M15 14h.01"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "ban": '<circle cx="12" cy="12" r="9"/><path d="m5.5 5.5 13 13"/>',
    "bolt": '<path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-2.64-6.36"/><path d="M21 3v6h-6"/>',
    "repeat": '<path d="m17 2 4 4-4 4"/><path d="M21 6H7a4 4 0 0 0-4 4v1"/><path d="m7 22-4-4 4-4"/><path d="M3 18h14a4 4 0 0 0 4-4v-1"/>',
    "disc": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/>',
    "monitor": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4"/>',
    "building": '<rect x="5" y="3" width="14" height="18" rx="1"/><path d="M9 7h1M14 7h1M9 11h1M14 11h1M9 15h1M14 15h1M10 21v-3h4v3"/>',
    "flask": '<path d="M9 3h6M10 3v6l-5.3 8.9A2 2 0 0 0 6.4 21h11.2a2 2 0 0 0 1.7-3.1L14 9V3"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9c.24.6.83 1 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M8 17v-6M13 17V7M18 17v-4"/>',
    "coins": '<circle cx="12" cy="12" r="9"/><path d="M12 6.5v11M15 9.2c0-1.2-1.3-1.9-3-1.9s-3 .7-3 1.9 1.2 1.7 3 2.1 3 .9 3 2.1-1.3 1.9-3 1.9-3-.7-3-1.9"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9.5h18M8 3v4M16 3v4"/>',
    "trend": '<path d="m3 17 6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
    "sparkle": '<path d="M12 3l1.9 5.8L20 10.5l-5.6 1.9L12 18l-2.4-5.6L4 10.5l6.1-1.7L12 3z"/>',
    "tag": '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><path d="M7.5 7.5h.01"/>',
    "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/><path d="M3 3h2l2.6 12.4a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.6L21 7H6"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 21v-1.5a5 5 0 0 1 5-5h4a5 5 0 0 1 5 5V21"/><path d="M16.5 4.6a3.5 3.5 0 0 1 0 6.8"/><path d="M22 21v-1.5a5 5 0 0 0-3.5-4.8"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3c2.5 2.6 4 5.7 4 9s-1.5 6.4-4 9c-2.5-2.6-4-5.7-4-9s1.5-6.4 4-9z"/>',
    "factory": '<path d="M2 21V9.5l6 3.5V9.5l6 3.5V4h8v17H2z"/><path d="M17 13h1M17 17h1M7 17h1M12 17h1"/>',
    "clipboard": '<rect x="5" y="4" width="14" height="17" rx="2"/><rect x="9" y="2" width="6" height="4" rx="1"/><path d="M9 11h6M9 15h6"/>',
    "bank": '<path d="M3 21h18M5 21v-11M19 21v-11M9 21v-8M15 21v-8"/><path d="M12 3 2 10h20L12 3z"/>',
    "door": '<path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><path d="m10 17 5-5-5-5"/><path d="M15 12H3"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
    "chat": '<path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.6 0-3.1-.4-4.4-1.2L3 20l1.2-5.1A8.5 8.5 0 1 1 21 11.5z"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
}

def I(name):
    return ('<svg class="i" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            + ICONS[name] + "</svg>")

# emoji → icon 名稱（build 時把內容裡的 emoji 換成 SVG）
EMOJI_MAP = {
    "📞": "phone", "✉": "mail", "🗄": "server", "📼": "tape", "🔧": "wrench",
    "📦": "box", "🛡": "shield", "🤖": "bot", "⏰": "clock", "🚫": "ban",
    "🔥": "bolt", "♻": "refresh", "💽": "disc", "🔀": "repeat", "🖥": "monitor",
    "🔄": "refresh", "🏢": "building", "🧪": "flask", "🛠": "gear", "📊": "chart",
    "💰": "coins", "🔒": "lock", "📅": "calendar", "📈": "trend", "🧹": "sparkle",
    "🏷": "tag", "🛒": "cart", "🤝": "users", "🌐": "globe", "🏭": "factory",
    "📋": "clipboard", "🏛": "bank", "🚪": "door", "🔐": "lock", "⚡": "bolt",
    "🧩": "grid", "👂": "chat", "💬": "chat", "📍": "pin", "⚙": "gear",
}

def iconify(html):
    html = html.replace("️", "")
    for d in "123456":
        html = html.replace(d + "⃣", d)  # 1️⃣ → 1（樣式交給 .ico）
    for emoji, name in EMOJI_MAP.items():
        html = html.replace(emoji, I(name))
    return html

def header(active):
    links = "".join(
        f'<a href="{h}" class="{"on" if h == active else ""}">{t}</a>' for h, t in NAV
    )
    return f"""<header>
<div class="topbar"><div class="wrap"><span>✉️ sales@datasys.com.tw</span><a href="tel:0226973311">📞 02-2697-3311</a></div></div>
<div class="navrow">
  <a class="logo" href="index.html">元僑科技<small>DATASYS TECHNOLOGIES</small></a>
  <nav>{links}</nav>
  <button class="burger" aria-label="開啟選單" onclick="this.closest('header').querySelector('nav').classList.toggle('open')">{I('menu')}</button>
  <a class="btn sm" href="contact.html">立即詢價</a>
</div>
</header>"""

FOOTER = """<section class="cta-band"><div class="wrap">
<h2>設備需求、零件急件、租賃詢價</h2>
<p>來電最快，或 Email 需求給我們，一個工作天內回覆</p>
<a class="phone" href="tel:0226973311">02-2697-3311</a>
<a class="btn" href="contact.html">填寫詢價表單</a>
</div></section>
<footer><div class="wrap"><div class="grid g3">
<div><h4>元僑科技有限公司</h4>
<p>新北市汐止區新台五路一段99號31樓之3<br>電話：02-2697-3311、02-2697-3312<br>Email：sales@datasys.com.tw<br>統一編號：28703966</p></div>
<div><h4>產品與服務</h4><a href="netapp.html">NetApp 儲存設備</a><a href="lto.html">IBM LTO 磁帶</a><a href="parts.html">二手零件與設備</a><a href="rental.html">Storage 短期租賃</a><a href="security.html">資訊安全</a><a href="ai.html">AI 解決方案</a></div>
<div><h4>公司</h4><a href="cases.html">成功案例</a><a href="about.html">關於我們</a><a href="contact.html">聯絡我們</a><a href="#">隱私權政策（待建）</a></div>
</div><div class="copy">© 2026 元僑科技有限公司 Datasys Technologies Co., Ltd.　｜　自 2007 年服務台灣企業與政府機關</div></div></footer>"""

def page(fname, title, desc, body):
    html = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
</head>
<body>
{header(fname)}
{body}
{FOOTER}
</body>
</html>"""
    html = iconify(html)
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("built", fname)

# ---------------------------------------------------------------- index
INDEX = """
<section class="hero hero-home"><div class="wrap">
<p class="kicker">SINCE 2007・企業儲存與備份專家</p>
<h1>企業儲存、備份與 IT 設備<br>的專業供應商</h1>
<p class="lead">NetApp 原廠認證工程師｜IBM LTO 磁帶代理｜自 2007 年服務台灣企業與政府機關</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 立即詢價 02-2697-3311</a><a class="btn ghost" href="contact.html">✉️ Email 需求給我們</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>六大業務</h2><p class="sub">從新機採購、租賃、維護到過保零件供應——企業 IT 設備的每個階段，我們都接得住。</p>
<div class="grid g3">
<a class="card" href="netapp.html"><div class="ico">🗄</div><h3>NetApp 儲存設備</h3><p>原廠認證工程師團隊，銷售、建置與長期維護。</p><span class="more">了解儲存方案 →</span></a>
<a class="card" href="lto.html"><div class="ico">📼</div><h3>IBM LTO 磁帶</h3><p>IBM LTO 磁帶代理，LTO-6/7/8/9 與備份媒體穩定供貨。</p><span class="more">查看磁帶產品 →</span></a>
<a class="card" href="parts.html"><div class="ico">🔧</div><h3>二手零件與設備</h3><p>NetApp、Cisco 等現貨庫存，過保與停產設備的維修救援，90 天保固。</p><span class="more">查詢庫存品項 →</span></a>
<a class="card" href="rental.html"><div class="ico">📦</div><h3>Storage 短期租賃</h3><p>NetApp FAS 系列短租，搬遷、測試、維修過渡的彈性選擇。</p><span class="more">了解租賃服務 →</span></a>
<a class="card" href="security.html"><div class="ico">🛡</div><h3>資訊安全</h3><p>Palo Alto Networks 防火牆與資安產品銷售與建置。</p><span class="more">了解資安方案 →</span></a>
<a class="card" href="ai.html"><div class="ico">🤖</div><h3>AI 解決方案</h3><p>AI Agent 導入、自動化流程開發與 SaaS 設計規劃。</p><span class="more">了解 AI 服務 →</span></a>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>為什麼選擇元僑科技</h2>
<div class="grid g2" style="margin-top:26px">
<div class="feat"><div class="n">1</div><div><h3>近 20 年的儲存備份專業</h3><p>自 2007 年起專注企業儲存與備份領域，服務台灣中小企業與政府部門。</p></div></div>
<div class="feat"><div class="n">2</div><div><h3>原廠認證與代理資格</h3><p>NetApp 合格工程師認證、IBM LTO 磁帶代理，原廠資源與技術支援有保障。</p></div></div>
<div class="feat"><div class="n">3</div><div><h3>現貨庫存，急件快速供應</h3><p>自有 FAS 系列、DS 硬碟櫃與 Cisco Nexus 庫存，故障急件不必苦等原廠交期。</p></div></div>
<div class="feat"><div class="n">4</div><div><h3>長期維護，不是一次性買賣</h3><p>指標客戶自建置後持續簽訂維護合約至今，對客戶環境的了解隨時間累積。</p></div></div>
</div>
<div class="badge-row" style="margin-top:14px">
<div class="badge">資誠聯合會計師事務所 PwC<small>維護合約持續中</small></div>
<div class="badge">華固建設<small>維護合約持續中・AI 合作進行中</small></div>
<div class="badge">台灣日立空調<small>維護合約持續中</small></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>常見詢問</h2>
<details class="faq"><summary>設備故障急需零件，多快可以供貨？</summary><p><span class="todo">待確認：實際供貨時效（例：常備庫存品項當日可出貨）</span></p></details>
<details class="faq"><summary>LTO 磁帶可以少量購買嗎？</summary><p>常備 LTO-6/7/8（LTO-9 少量供應），數量需求請來電確認。<span class="todo">待確認：最小訂購量</span></p></details>
<details class="faq"><summary>Storage 租賃最短租期是多久？</summary><p>最短租期 30 天，安裝設定費另計，詳見 <a href="rental.html">租賃服務</a>。</p></details>
<details class="faq"><summary>二手設備有保固嗎？</summary><p>有。二手零件與設備自交貨日起算 90 天內故障免費更換。</p></details>
</div></section>"""

# ---------------------------------------------------------------- parts
PARTS = """
<section class="hero"><div class="wrap">
<p class="kicker">現貨庫存・90 天保固</p>
<h1>NetApp、Cisco、HP、DELL、Oracle Sun<br>二手零件與設備供應</h1>
<p class="lead">設備過保、機型停產（EOL）、故障急件等不到原廠交期——來電報上型號或零件編號，快速確認供貨與報價。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 急件詢價 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>現貨庫存品項</h2><p class="sub">庫存即時變動，未列出的型號也歡迎詢問。</p>
<div class="grid g2 stock">
<div><h3>🗄 NetApp 儲存系統</h3><ul><li>FAS2700 系列</li><li>FAS2600 系列</li><li>FAS8200 系列</li><li>FAS8000 系列</li><li>各系列控制器、電源、風扇等零件</li></ul>
<h3>💽 NetApp 硬碟櫃（Disk Shelf）</h3><ul><li>DS224C</li><li>DS212C</li><li>相關硬碟、線材與模組</li></ul></div>
<div><h3>🔀 Cisco 網路設備</h3><ul><li>Nexus 9000 系列（N9K）Switch</li><li>Nexus 5000 系列（N5K）Switch</li></ul>
<h3>🖥 其他品牌伺服器零件</h3><ul><li>HP / DELL / Oracle Sun Server 零件供應 <span class="todo">待確認：常備或調貨</span></li></ul></div>
</div>
<div class="promise"><strong>90 天保固承諾</strong><br>所有二手零件與設備，自交貨日起算 90 天內故障免費更換。</div>
</div></section>

<section class="sec soft"><div class="wrap">
<h2>什麼情況下找我們</h2>
<div class="grid g2" style="margin-top:26px">
<div class="feat"><div class="n">⏰</div><div><h3>原廠保固已過期</h3><p>過保設備送原廠維修費用高、流程長，二手零件替換是務實的選擇。</p></div></div>
<div class="feat"><div class="n">🚫</div><div><h3>機型已停產（EOL / EOS）</h3><p>原廠已不再供貨的機型，我們的庫存可能還有料。</p></div></div>
<div class="feat"><div class="n">🔥</div><div><h3>故障急件，等不了原廠交期</h3><p>生產環境設備故障，每多停一天都是損失。常備庫存大幅縮短等料時間。</p></div></div>
<div class="feat"><div class="n">♻</div><div><h3>延長現有設備使用年限</h3><p>設備運作正常、暫不汰換，備妥關鍵零件讓它安心再戰幾年。</p></div></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>服務方式</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">1️⃣</div><h3>報型號</h3><p>來電或 Email 報上設備型號／零件編號。</p></div>
<div class="card"><div class="ico">2️⃣</div><h3>確認報價</h3><p>我們確認庫存與品況，回覆報價與交期。</p></div>
<div class="card"><div class="ico">3️⃣</div><h3>出貨</h3><p>交貨日起 90 天保固。<span class="todo">待確認：到府安裝更換服務</span></p></div>
</div>
<h2 style="margin-top:48px">常見詢問</h2>
<details class="faq"><summary>怎麼確認你們有沒有我要的零件？</summary><p>直接來電 02-2697-3311 報型號或零件編號，庫存有無當場告訴你。</p></details>
<details class="faq"><summary>二手零件品質如何把關？</summary><p><span class="todo">待確認：出貨前測試流程</span></p></details>
<details class="faq"><summary>有保固嗎？</summary><p>有。自交貨日起算 90 天內故障免費更換。</p></details>
<details class="faq"><summary>可以收購我們汰換下來的設備嗎？</summary><p><span class="todo">待確認：是否收購二手設備</span></p></details>
</div></section>"""

# ---------------------------------------------------------------- rental
RENTAL = """
<section class="hero hero-storage"><div class="wrap">
<p class="kicker">最短租期 30 天・認證工程師支援</p>
<h1>NetApp FAS Storage 短期租賃<br>臨時需求，不必買設備</h1>
<p class="lead">資料搬遷、專案測試、設備維修的過渡期，往往只需要用儲存設備幾週到幾個月。租用 NetApp FAS 系列，用完歸還，不必為臨時需求編列採購預算。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 租賃詢價 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>適合租賃的情境</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">🔄</div><h3>資料搬遷／設備汰換</h3><p>新舊設備交替期間，租一台 FAS 作為資料中繼，搬遷完成即歸還。</p></div>
<div class="card"><div class="ico">🏢</div><h3>機房搬遷</h3><p>搬遷期間需要臨時環境維持營運，短租比採購合理。</p></div>
<div class="card"><div class="ico">🧪</div><h3>專案需求與 POC 測試</h3><p>評估 NetApp 環境、開發測試專案，先租後買，降低決策風險。</p></div>
<div class="card"><div class="ico">🛠</div><h3>設備維修期間替代</h3><p>主要儲存設備送修期間，租賃設備暫代，維持服務不中斷。</p></div>
<div class="card"><div class="ico">📊</div><h3>預算年度限制</h3><p>資本支出（CAPEX）預算已滿，租賃走營運費用（OPEX），會計處理更彈性。</p></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>可租賃機型與方案</h2>
<div class="grid g2" style="margin-top:26px">
<div class="stock"><h3>可租機型</h3><ul><li>NetApp FAS2700 系列</li><li>NetApp FAS2600 系列</li><li>NetApp FAS8200 系列</li><li>NetApp FAS8000 系列</li><li>DS224C / DS212C 硬碟櫃（可搭配擴充容量）</li></ul></div>
<div class="stock"><h3>方案說明</h3><ul><li><b>最短租期：30 天</b></li><li>安裝設定費另計，由 NetApp 認證工程師執行</li><li>計費方式：來電洽詢</li><li>運送方式與費用：來電洽詢</li><li>歸還資料抹除機制：來電洽詢</li></ul></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>常見詢問</h2>
<details class="faq"><summary>最短可以租多久？</summary><p>最短租期 30 天。</p></details>
<details class="faq"><summary>租金包含安裝嗎？</summary><p>安裝設定費另計，由 NetApp 認證工程師到場執行；若貴公司自行上架設定，僅收租金。</p></details>
<details class="faq"><summary>租賃設備故障怎麼辦？</summary><p><span class="todo">待確認：建議承諾租期內故障由本公司負責更換</span></p></details>
<details class="faq"><summary>可以先租後買嗎？</summary><p><span class="todo">待確認：租金可否折抵購買</span></p></details>
</div></section>"""

# ---------------------------------------------------------------- lto
LTO = """
<section class="hero"><div class="wrap">
<p class="kicker">IBM LTO 磁帶代理</p>
<h1>IBM LTO 磁帶代理<br>企業備份與歸檔媒體穩定供應</h1>
<p class="lead">磁帶仍是每 TB 成本最低、離線保存最安全的備份媒體。元僑科技為 IBM LTO 磁帶代理，服務台灣企業與政府機關近 20 年。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 磁帶詢價 02-2697-3311</a><a class="btn ghost" href="contact.html">✉️ Email 詢價</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>為什麼企業還在用磁帶</h2>
<div class="grid g2" style="margin-top:26px">
<div class="feat"><div class="n">💰</div><div><h3>每 TB 成本最低</h3><p>大容量長期保存，媒體成本遠低於硬碟與雲端的長期費用。</p></div></div>
<div class="feat"><div class="n">🔒</div><div><h3>離線保存，天然防勒索</h3><p>磁帶離線（air gap）存放，勒索病毒加密不到、駭客碰不到。</p></div></div>
<div class="feat"><div class="n">📅</div><div><h3>保存年限長</h3><p>設計保存年限可達 30 年，適合金融、會計、醫療、政府等長期歸檔需求。</p></div></div>
<div class="feat"><div class="n">📈</div><div><h3>規格持續演進</h3><p>LTO 是開放標準，容量每一代持續倍增，不是過時技術。</p></div></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>供應品項</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">📼</div><h3>IBM LTO 資料磁帶</h3><p><b>LTO-6、LTO-7、LTO-8</b>：常備供應<br><b>LTO-9</b>：少量供應，請先來電確認。</p></div>
<div class="card"><div class="ico">🧹</div><h3>清潔帶</h3><p>磁帶機定期清潔必備，與資料磁帶一併採購最方便。</p></div>
<div class="card"><div class="ico">🏷</div><h3>條碼標籤（隨機號碼）</h3><p>自動化磁帶櫃管理用，磁帶出貨可搭配供應。</p></div>
</div>
<h2 style="margin-top:44px">LTO 各世代容量規格</h2>
<p class="sub">公開資料，以 IBM 官方規格為準</p>
<table class="spec"><tr><th>世代</th><th>原生容量</th><th>壓縮後容量（2.5:1）</th><th>供應狀態</th></tr>
<tr><td>LTO-9</td><td>18 TB</td><td>45 TB</td><td>少量供應</td></tr>
<tr><td>LTO-8</td><td>12 TB</td><td>30 TB</td><td>✔ 常備</td></tr>
<tr><td>LTO-7</td><td>6 TB</td><td>15 TB</td><td>✔ 常備</td></tr>
<tr><td>LTO-6</td><td>2.5 TB</td><td>6.25 TB</td><td>✔ 常備</td></tr></table>
<p style="margin-top:12px;color:var(--muted);font-size:14px">舊世代磁帶（LTO-5 以前）或其他品項需求，歡迎來電詢問。</p>
</div></section>

<section class="sec"><div class="wrap">
<h2>常見詢問</h2>
<details class="faq"><summary>可以少量購買嗎？</summary><p><span class="todo">待確認：最小訂購量</span></p></details>
<details class="faq"><summary>LTO 磁帶可以向下相容嗎？</summary><p>磁帶機一般可讀取前一至二個世代的磁帶，選購前歡迎來電確認您的磁帶機型號。</p></details>
<details class="faq"><summary>報價需要提供什麼資訊？</summary><p>磁帶世代（如 LTO-8）與數量即可；不確定規格的話，告訴我們磁帶機或磁帶櫃型號，我們協助確認。</p></details>
</div></section>"""

# ---------------------------------------------------------------- netapp
NETAPP = """
<section class="hero hero-storage"><div class="wrap">
<p class="kicker">NetApp Registered Partner・認證工程師</p>
<h1>NetApp 儲存設備<br>銷售、建置到維護的全生命週期服務</h1>
<p class="lead">自 2007 年專注 NetApp 儲存領域。無論是採購新機、短期租賃、還是讓過保設備繼續安心服役，儲存設備的每個階段我們都接得住。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 專案洽詢 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>我們提供的服務</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">🛒</div><h3>設備銷售與建置</h3><p>選型建議、報價、到府安裝建置與資料遷移。依實際容量與效能需求配置，不過度銷售。</p></div>
<div class="card"><div class="ico">🤝</div><h3>長期維護</h3><p>資誠 PwC、華固建設、台灣日立空調等客戶的維護合約自建置後持續至今。</p></div>
<div class="card"><div class="ico">🌐</div><h3>異地備援與資料保護</h3><p>備援架構規劃與建置。<span class="todo">待確認：SnapMirror 服務現況</span></p></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>主打產品：NetApp AFF C 系列全快閃儲存</h2>
<p class="sub">NetApp 現行主力產品線——容量型全快閃（Capacity Flash），以更合理的價格帶來全快閃效能與 ONTAP 完整資料管理能力。</p>
<div class="prodshot">
<div class="shot"><img src="image/aff-cseries.jpg" alt="NetApp AFF C 系列全快閃儲存設備"></div>
<div>
<ul>
<li>全快閃效能，容量型定價，取代傳統混合式儲存的務實選擇</li>
<li>ONTAP 資料管理：快照、複製、異地備援一套到位</li>
<li>適合檔案集中管理、虛擬化環境與資料保護應用</li>
<li>由 NetApp 認證工程師規劃配置與到府建置</li>
</ul>
<p style="margin-bottom:18px"><span class="todo">待確認：主推型號與容量配置（C250 / C400 / C800）</span></p>
<a class="btn" href="tel:0226973311">📞 索取 C 系列報價</a>
</div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>全生命週期支援</h2><p class="sub">多數經銷商只做採購與建置。我們自有 FAS 系列與 DS 硬碟櫃庫存，設備過保後不會被丟下。</p>
<table class="spec"><tr><th>階段</th><th>元僑提供</th></tr>
<tr><td><b>評估期</b></td><td><a href="rental.html">短期租賃 POC 測試</a>，先驗證再採購</td></tr>
<tr><td><b>採購建置</b></td><td>選型、報價、安裝、資料遷移</td></tr>
<tr><td><b>營運期</b></td><td>維護合約、故障排除</td></tr>
<tr><td><b>過保／延壽期</b></td><td><a href="parts.html">FAS 系列二手零件供應</a>，90 天保固</td></tr></table>
</div></section>

<section class="sec soft"><div class="wrap">
<h2>適合的客戶</h2>
<div class="grid g2" style="margin-top:26px">
<div class="feat"><div class="n">🏭</div><div><h3>中小企業</h3><p>檔案伺服器容量吃緊、需要集中儲存管理。</p></div></div>
<div class="feat"><div class="n">📋</div><div><h3>法規保存產業</h3><p>會計、金融、營建等有長期保存要求的產業。</p></div></div>
<div class="feat"><div class="n">🏛</div><div><h3>政府部門</h3><p>機關標案需要在地供應商與維護量能。</p></div></div>
<div class="feat"><div class="n">🔁</div><div><h3>既有 NetApp 用戶</h3><p>需要第二家維護供應商比價的企業。<span class="todo">待確認：是否接手他廠建置</span></p></div></div>
</div>
<h2 style="margin-top:48px">常見詢問</h2>
<details class="faq"><summary>你們是 NetApp 的什麼合作等級？</summary><p>我們是 NetApp Registered Partner，並持有 NetApp 合格工程師認證。比起合作等級，更實際的參考是：我們自 2007 年專注 NetApp 領域近 20 年，資誠 PwC 等指標客戶的維護合約持續簽訂至今。</p></details>
<details class="faq"><summary>可以只買設備不買維護嗎？</summary><p><span class="todo">待確認</span></p></details>
<details class="faq"><summary>建置需要多久？</summary><p><span class="todo">待確認：典型交期與建置時程</span></p></details>
</div></section>"""

# ---------------------------------------------------------------- security
SECURITY = """
<section class="hero"><div class="wrap">
<p class="kicker">Palo Alto Networks</p>
<h1>Palo Alto Networks 資安產品<br>網路防護與資料保護一次到位</h1>
<p class="lead">防火牆擋在前面，備份守在後面——企業資安是縱深防禦。我們提供 Palo Alto Networks 產品銷售與建置，並以近 20 年儲存備份專業，把「被打進來之後」的最後防線也建好。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 資安需求洽詢 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>產品與服務</h2>
<div class="grid g2" style="margin-top:26px">
<div class="card"><div class="ico">🛡</div><h3>次世代防火牆（NGFW）</h3><p>Palo Alto Networks 防火牆銷售與建置。<span class="todo">待確認：產品線範圍（PA 系列／授權續約等）</span></p></div>
<div class="card"><div class="ico">⚙️</div><h3>建置與服務</h3><p><span class="todo">待確認：政策規劃、教育訓練、定期健檢等服務範圍</span></p></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>防火牆＋備份＝完整的勒索病毒對策</h2><p class="sub">多數資安廠商只做第一層。元僑科技兩層都做，而且第二層做了近 20 年。</p>
<div class="grid g2">
<div class="card"><div class="ico">🚪</div><h3>第一層：擋在門外</h3><p>Palo Alto 次世代防火牆阻擋威脅進入內部網路。</p></div>
<div class="card"><div class="ico">🔐</div><h3>第二層：留好後路</h3><p>萬一被突破，離線的 <a href="lto.html">LTO 磁帶備份</a>與<a href="netapp.html">異地備援</a>讓資料救得回來、不必付贖金。</p></div>
</div></div></section>"""

# ---------------------------------------------------------------- ai
AI = """
<section class="hero hero-ai"><div class="wrap">
<p class="kicker">2026 新事業・AI AGENT</p>
<h1>讓 AI Agent 接手重複的工作<br>從你現有的系統開始</h1>
<p class="lead">企業導入 AI 最常失敗的原因，不是模型不夠聰明，而是 AI 接不上內部的系統與流程。我們做了近 20 年的企業 IT 基礎建設，我們做的 AI Agent，是能真正嵌進你日常營運的那種。</p>
<div class="cta-row"><a class="btn" href="contact.html">預約需求訪談</a><a class="btn ghost" href="tel:0226973311">📞 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>我們提供的服務</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">⚡</div><h3>自動化流程開發</h3><p>資料整理、報表產出、跨系統轉檔、通知追蹤——重複作業交給自動化，人力放回需要判斷力的工作。</p></div>
<div class="card"><div class="ico">🤖</div><h3>AI Agent 導入</h3><p>評估適合導入的環節、技術選型、開發部署到內部環境、教育訓練與後續調整。</p></div>
<div class="card"><div class="ico">🧩</div><h3>SaaS 設計規劃</h3><p>從需求訪談、系統規劃到開發落地，把內部流程或商業構想做成可營運的服務。</p></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>為什麼找一家「做儲存的公司」做 AI</h2>
<div class="grid g3" style="margin-top:26px">
<div class="feat"><div class="n">🖥</div><div><h3>我們懂企業 IT 環境</h3><p>AI Agent 要連上你的檔案伺服器、資料庫與內部系統——這些正是我們建置維護了近 20 年的東西。</p></div></div>
<div class="feat"><div class="n">📊</div><div><h3>我們懂資料</h3><p>AI 的原料是資料。從 2008 年起我們就以「資料」為核心提供服務。</p></div></div>
<div class="feat"><div class="n">🤝</div><div><h3>我們是長期合約型的公司</h3><p>AI 導入不是專案結案就結束，你需要一家會一直在的公司。</p></div></div>
</div>
<div class="promise" style="margin-top:30px"><strong>目前進行中</strong><br>我們正與長期合作的上市建設公司客戶進行 AI 導入合作。<span class="todo">待確認：可否具名露出與描述深度</span></div>
</div></section>

<section class="sec"><div class="wrap">
<h2>導入流程</h2>
<div class="grid g4" style="margin-top:26px">
<div class="card"><div class="ico">1️⃣</div><h3>需求訪談</h3><p>盤點營運流程，找出適合自動化的環節。</p></div>
<div class="card"><div class="ico">2️⃣</div><h3>可行性評估</h3><p>明確告訴你哪些做得到、哪些現階段不建議做。</p></div>
<div class="card"><div class="ico">3️⃣</div><h3>開發與測試</h3><p>小範圍先行，驗證效果後再擴大。</p></div>
<div class="card"><div class="ico">4️⃣</div><h3>部署與持續調整</h3><p>教育訓練，並隨使用回饋持續優化。</p></div>
</div>
<h2 style="margin-top:48px">常見詢問</h2>
<details class="faq"><summary>我們公司不大，適合導入 AI Agent 嗎？</summary><p>適合。中小企業人力精簡，重複性作業對營運的拖累反而更明顯。我們的方案以務實、可負擔為原則。</p></details>
<details class="faq"><summary>需要準備什麼才能開始？</summary><p>不需要事先準備技術文件。第一次訪談我們會一起盤點你的日常流程，從中找出投資報酬最高的切入點。</p></details>
</div></section>"""

# ---------------------------------------------------------------- cases
CASES = """
<section class="hero"><div class="wrap">
<p class="kicker">SUCCESS STORIES</p>
<h1>成功案例——用續約證明的服務品質</h1>
<p class="lead">以下客戶自建置完成後，維護合約持續簽訂至今。企業的資料放在誰手上顧，每年都可以重新選擇——被持續選擇，就是我們最好的案例。</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="case"><h3>資誠聯合會計師事務所 PwC</h3><div class="tag">專業服務／會計審計</div>
<p><b>客戶情境</b>　<span class="todo">暫時假設，請修正</span>　工作底稿與客戶資料有法定保存年限要求，資料量大、機密性高，備份與儲存的可靠度直接關係執業合規。</p>
<p style="margin-top:8px"><b>我們提供</b>　NetApp 儲存設備建置・備份系統規劃・長期維護服務</p>
<p class="ok">✔ 維護合約持續簽訂至今</p></div>

<div class="case"><h3>華固建設</h3><div class="tag">營建／上市公司</div>
<p><b>客戶情境</b>　<span class="todo">暫時假設，請修正</span>　建案圖說、合約與工程文件需長期保存，跨案場資料集中管理。</p>
<p style="margin-top:8px"><b>我們提供</b>　儲存與備份系統建置・長期維護服務・<b>AI 導入合作進行中</b></p>
<p class="ok">✔ 維護合約持續簽訂至今，並延伸至 AI 領域合作</p></div>

<div class="case"><h3>台灣日立空調</h3><div class="tag">製造／外商</div>
<p><b>客戶情境</b>　<span class="todo">暫時假設，請修正</span>　外商對 IT 供應商的服務水準與回應速度要求高，系統可用度標準嚴格。</p>
<p style="margin-top:8px"><b>我們提供</b>　儲存備份設備建置・長期維護服務</p>
<p class="ok">✔ 維護合約持續簽訂至今</p></div>
</div></section>"""

# ---------------------------------------------------------------- about
ABOUT = """
<section class="hero"><div class="wrap">
<p class="kicker">ABOUT DATASYS</p>
<h1>自 2007 年，做好企業資料儲存這件事</h1>
<p class="lead">將近 20 年專注一個領域：企業的資料儲存與備份。我們圍繞著「讓企業資料安全、可用、不中斷」建立完整的服務能力，並在 2026 年把累積的 IT 整合經驗延伸到 AI Agent 開發領域。</p>
</div></section>

<section class="sec"><div class="wrap">
<div class="grid g2">
<div><h2>公司歷程</h2>
<ul class="tl" style="margin-top:24px">
<li><b>2007</b>元僑科技成立，投入儲存備援系統整合與虛擬化管理領域</li>
<li><b>2008</b>以「資料」為核心重新定位服務方向，建立企業諮詢顧問團隊</li>
<li><b><span class="todo">年份待確認</span></b>取得 IBM LTO 磁帶代理資格・新增 Palo Alto Networks 產品線・開展二手零件與 FAS 短期租賃服務</li>
<li><b>2026</b>成立 AI Agent 開發與銷售業務</li>
</ul></div>
<div><h2>專業認證與代理資格</h2>
<div class="badge-row" style="margin-top:24px">
<div class="badge">NetApp Registered Partner<small>合格工程師認證</small></div>
<div class="badge">IBM LTO 磁帶代理<small>代理證明</small></div>
</div>
<h2 style="margin-top:36px">客戶怎麼看我們</h2>
<p style="margin-top:12px">資誠聯合會計師事務所 PwC、華固建設、台灣日立空調——這些客戶與我們的維護合約，自建置後持續簽訂至今。</p>
<p style="margin-top:8px;color:var(--muted)">維護合約每年續一次，客戶每年都有機會換掉我們。近 20 年來持續被續約，是我們最真實的服務證明。</p></div>
</div></div></section>

<section class="sec soft"><div class="wrap">
<h2>我們的服務原則</h2>
<div class="grid g3" style="margin-top:26px">
<div class="card"><div class="ico">👂</div><h3>傾聽需求，給務實的方案</h3><p>客戶多是中小企業與政府部門，預算有限是常態。我們在有限資源內做出最大效益的配置，不是把最貴的設備賣給你。</p></div>
<div class="card"><div class="ico">🤝</div><h3>長期關係，不是一次性買賣</h3><p>儲存設備一用就是五年、十年。我們的維護與零件供應能力，讓每一分投資用好用滿。</p></div>
<div class="card"><div class="ico">🔧</div><h3>技術紮實，講話直接</h3><p>認證工程師直接面對客戶。能做的說能做，不能做的直說，交期報價不灌水。</p></div>
</div></div></section>

<section class="sec"><div class="wrap">
<h2>公司資訊</h2>
<ul class="info-list" style="margin-top:20px;max-width:560px">
<li><b>公司名稱</b>元僑科技有限公司</li>
<li><b>成立時間</b>2007 年</li>
<li><b>統一編號</b>28703966</li>
<li><b>地址</b>新北市汐止區新台五路一段99號31樓之3</li>
<li><b>電話</b>02-2697-3311、02-2697-3312</li>
<li><b>Email</b>sales@datasys.com.tw</li>
</ul></div></section>"""

# ---------------------------------------------------------------- contact
CONTACT = """
<section class="hero"><div class="wrap">
<p class="kicker">CONTACT US</p>
<h1>聯絡我們</h1>
<p class="lead">設備採購、零件急件、租賃需求或 AI 導入評估，歡迎直接來電，或填寫表單，我們收到後會盡快與您聯絡。</p>
<div class="cta-row"><a class="btn" href="tel:0226973311">📞 02-2697-3311</a></div>
</div></section>

<section class="sec"><div class="wrap"><div class="grid g2">
<div>
<h2>聯絡資訊</h2>
<ul class="info-list" style="margin-top:18px">
<li><b>電話</b>02-2697-3311、02-2697-3312</li>
<li><b>Email</b>sales@datasys.com.tw</li>
<li><b>LINE 官方帳號</b><span class="todo">預留，開通後補上</span></li>
<li><b>地址</b>新北市汐止區新台五路一段99號31樓之3</li>
<li><b>服務時間</b><span class="todo">待確認（例：週一至週五 9:00–18:00）</span></li>
</ul>
<div class="map-ph">📍 Google 地圖嵌入位置（遠東世界中心，近汐科站）</div>
</div>
<div class="form">
<h2>詢價表單</h2>
<label>公司名稱 *</label><input type="text" placeholder="貴公司名稱">
<label>姓名 *</label><input type="text" placeholder="您的姓名">
<label>電話 *</label><input type="tel" placeholder="聯絡電話">
<label>Email *</label><input type="email" placeholder="email@company.com">
<label>需求類別 *</label>
<select><option>NetApp 儲存設備</option><option>IBM LTO 磁帶</option><option>二手零件／設備</option><option>Storage 短期租賃</option><option>資訊安全（Palo Alto）</option><option>AI Agent／自動化開發</option><option>其他</option></select>
<label>需求說明</label><textarea placeholder="請簡述您的需求，例如：需要 FAS8200 電源模組 2 個"></textarea>
<p style="font-size:12.5px;color:var(--muted);margin-top:10px">本表單資料僅用於回覆您的需求。</p>
<a class="btn" style="margin-top:14px;width:100%;text-align:center" href="#">送出詢問（原型示意）</a>
</div>
</div></div></section>"""

PAGES = [
    ("index.html", "元僑科技｜NetApp 儲存、IBM LTO 磁帶、二手伺服器零件與 Storage 租賃",
     "元僑科技自 2007 年起提供 NetApp 儲存設備、IBM LTO 磁帶與 Palo Alto Networks 資安產品，並供應二手零件與 NetApp FAS 短期租賃。詢價專線 02-2697-3311。", INDEX),
    ("parts.html", "NetApp、Cisco 二手零件與設備現貨供應｜90 天保固｜元僑科技",
     "NetApp FAS 系列、DS224C/DS212C 硬碟櫃、Cisco Nexus Switch 現貨庫存，交貨後 90 天保固。急件維修來電報型號快速報價：02-2697-3311。", PARTS),
    ("rental.html", "NetApp FAS Storage 短期租賃｜最短租期 30 天｜元僑科技",
     "NetApp FAS 系列儲存設備短期租賃，適用資料搬遷、機房搬遷、POC 測試、設備維修替代。最短租期 30 天。詢價：02-2697-3311。", RENTAL),
    ("lto.html", "IBM LTO 磁帶代理｜LTO-6/7/8/9 資料磁帶、清潔帶、條碼標籤｜元僑科技",
     "IBM LTO 磁帶代理，常備供應 LTO-6、LTO-7、LTO-8 資料磁帶（LTO-9 少量），並提供清潔帶與條碼標籤。詢價：02-2697-3311。", LTO),
    ("netapp.html", "NetApp 儲存設備銷售與建置｜認證工程師團隊｜元僑科技",
     "NetApp 儲存設備銷售、建置規劃與長期維護。從新機採購、短期租賃到過保零件供應，全生命週期支援。詢價：02-2697-3311。", NETAPP),
    ("security.html", "Palo Alto Networks 防火牆與資安產品｜銷售與建置｜元僑科技",
     "Palo Alto Networks 次世代防火牆銷售與建置，搭配儲存備份服務，建立從網路防護到資料保護的完整防線。詢價：02-2697-3311。", SECURITY),
    ("ai.html", "企業 AI Agent 導入與自動化流程開發｜元僑科技",
     "AI Agent 導入、自動化流程開發與 SaaS 設計規劃。近 20 年企業 IT 基礎建設經驗，做出真正接得上內部流程的 AI。", AI),
    ("cases.html", "成功案例｜資誠 PwC、華固建設、台灣日立空調｜元僑科技",
     "元僑科技服務資誠 PwC、華固建設、台灣日立空調等指標企業，儲存備份建置後維護合約持續至今。", CASES),
    ("about.html", "關於元僑科技｜自 2007 年深耕企業儲存與備份",
     "元僑科技有限公司成立於 2007 年，持有 NetApp 認證與 IBM LTO 磁帶代理資格，2026 年成立 AI Agent 開發業務。", ABOUT),
    ("contact.html", "聯絡我們｜詢價專線 02-2697-3311｜元僑科技",
     "NetApp 儲存、LTO 磁帶、二手零件、Storage 租賃詢價——電話 02-2697-3311，或填寫表單，我們將盡快回覆。", CONTACT),
]

for fname, title, desc, body in PAGES:
    page(fname, title, desc, body)
print("done:", len(PAGES), "pages ->", OUT)
