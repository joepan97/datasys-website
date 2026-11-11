# DataSys 官網未完成事項與人工交接

日期：2026-11-11
Repo：`/Users/yen-chihpan/Datasys_website`
任務清單：iCloud `VScode/office/datasys-website-tasks.md`

## 目前狀態

這份文件列出尚未完成的人工工作、部署後驗收，以及尚未執行的 AI 工作。**目前所有本機修改尚未部署；不要把本機測試結果當成正式站已更新。** 目前未登入或操作 Cloudflare／主機後台，也未執行 Nginx reload。

AI 已準備：
- `404.html`：404 頁來源模板。
- `site/404.html`：可部署 404 頁。
- `server-config-snippet.conf`：T02 主機設定片段，請審閱後再合併至正確的 Tengine/Nginx `server` 區塊。
- `site/sitemap.xml`：已改用尾斜線法律頁網址並加上 `lastmod`。
- T03 Logo、T06 首頁連結、T07 preload、T08 首頁 JSON-LD、T11 色票有本機修改；其中 T06/T08 等仍有部署或來源同步驗收待辦，詳見下文。

備份位置：`/Users/yen-chihpan/Datasys-backup-20261111`（建立於本次修改前）。目前工作目錄原本已有未提交修改，部署／合併前請先檢查 `git status`，不要覆蓋既有變更。

---

## A. 請 Web Server／Cloudflare 同事處理

### T01｜根網域 DNS 與 301 轉址（人工）

1. Cloudflare → **DNS**，新增：
   - Type：`A`
   - Name：`@`
   - IPv4：`192.0.2.1`（任務書指定的佔位 IP）
   - Proxy status：**Proxied／橘色雲開啟**
2. Cloudflare → **Rules → Redirect Rules**，新增規則：
   - 條件：Hostname equals `datasys.com.tw`
   - Action：Dynamic redirect
   - Expression：`concat("https://www.datasys.com.tw", http.request.uri.path)`
   - Status code：`301`
   - 保留 query string。
3. 儲存後驗收：

```bash
curl -sI https://datasys.com.tw | grep -iE "^HTTP|^location"
curl -sI http://datasys.com.tw/lto.html | grep -iE "^HTTP|^location"
```

預期為 301，Location 目的地為 `https://www.datasys.com.tw/...`，並保留路徑與 query string。

### T02｜套用自訂 404／修正 500（人工部分）

AI 已建立 `site/404.html`，部署內容需一併上線。主機設定片段在 repo 根目錄 `server-config-snippet.conf`，內容如下：

```nginx
error_page 404 /404.html;
location = /404.html { internal; }

# 無副檔名網址轉到 .html，例如 /netapp → /netapp.html
location / {
    try_files $uri $uri.html $uri/ =404;
}

# 隱藏版本與主機資訊
server_tokens off;
```

套用前請：
1. 確認目前 `server` 區塊是否已有 `location /`、`error_page 404` 或 `server_tokens` 設定；避免重複 `location` 導致 `nginx -t` 失敗。將片段合併至現有設定，而非未檢查就整段覆蓋。
2. 確認站台 root 指向包含部署後 `404.html` 的目錄。
3. 檢查 500 的真正來源（任務書提到可能是錯誤頁指向不存在檔案）；`server_tokens off` 只隱藏版本資訊，不會修正 500 根因。
4. 先測試再 reload：`nginx -t`（依主機上的實際執行路徑／權限執行）；成功後才 reload，並記錄成功輸出。不要在測試失敗時 reload。

部署後驗收：

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://www.datasys.com.tw/404test
curl -s -o /dev/null -w "%{http_code}\n" https://www.datasys.com.tw/netapp
curl -s https://www.datasys.com.tw/404test | grep -c "18-hk-ls-vps01"
```

預期依序為 `404`、`200` 或 `301`、`0`。同時確認錯誤頁有品牌頁首／頁尾、服務入口可點，沒有洩漏主機名稱。

### T05｜關閉 Cloudflare Rocket Loader（人工）

Cloudflare → **Speed → Optimization → Content Optimization** → 關閉 **Rocket Loader**，接著 **Caching → Purge Everything**。

驗收：

```bash
curl -s https://www.datasys.com.tw | grep -c "rocket-loader"
```

預期 `0`。另用手機實測漢堡選單第一次點擊即可展開，並確認 GA 請求正常。

### T06｜`/index.html` 轉址（人工部分）

AI 已將 `site/` 十個主要頁面的 Logo 與「首頁」連結改為 `href="/"`，`build.py` 導覽列模板亦已調整。請在主機 `server` 區塊加入：

```nginx
location = /index.html { return 301 /; }
```

請確認站台的 `index index.html;` 等 index 設定，不會造成迴圈或讓根路徑失效；與既有精確匹配 location 合併後先執行 `nginx -t`，成功才 reload。

驗收：

```bash
curl -sI https://www.datasys.com.tw/index.html
curl -sI https://www.datasys.com.tw/
```

`/index.html` 應為 301 並導向 `/`，首頁應為 200。

### T09｜Cloudflare HTML 快取（人工）

Cloudflare → **Caching → Cache Rules** 新增規則：

- 條件：Hostname equals `www.datasys.com.tw`。
- 條件：URI Path does not start with `/cdn-cgi`。
- 排除表單 POST 路徑：先檢查部署版 `inquiry-form.js` 的實際 endpoint；若 POST 到本站路徑，務必排除該路徑，避免快取表單請求／回應。
- Cache eligibility：Eligible for cache。
- Edge TTL：4 小時。
- Browser TTL：遵循原站。

驗收：連續請求兩次，第二次應為 HIT：

```bash
curl -sI https://www.datasys.com.tw | grep -i cf-cache-status
curl -sI https://www.datasys.com.tw | grep -i cf-cache-status
```

更新網站後依流程 Purge；請確認 POST 排除規則和表單功能正常再結案。

### T10｜安全標頭與 UTF-8 charset（人工）

Cloudflare → **Rules → Transform Rules → Modify Response Header** 加入：

```text
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
X-Frame-Options: SAMEORIGIN
Permissions-Policy: camera=(), microphone=(), geolocation=()
```

另在主機設定 `charset utf-8;`。請先確認沒有重複或衝突標頭，再依主機程序測試設定並 reload。

驗收：

```bash
curl -sI https://www.datasys.com.tw
```

回應應包含以上四個標頭，且 `content-type` 為 `text/html; charset=utf-8`。

---

## B. 部署後由維護人員協助的網站驗收

以下驗收應在更新檔案已部署、Cloudflare cache 已 purge 後進行：

1. Sitemap 中每個 `<loc>` 都回 200（本機最新版共 12 個網址）：

```bash
B=https://www.datasys.com.tw
for u in $(grep -oE '<loc>[^<]+' site/sitemap.xml | sed 's/<loc>//'); do
  curl -s -o /dev/null -w "%{http_code} $u\n" "$u"
done
```

2. 首頁結構化資料：用 Google Rich Results Test 檢查正式 URL；本機 JSON 語法已通過，但正式測試尚未完成。
3. 頁面狀態與錯誤頁：依任務書第 6 節測試十個主頁、未知路徑、根網域轉址、Rocket Loader 標記；所有檔案部署前需確認實際 URL 路徑。
4. T07 Hero preload：正式站 Chrome DevTools → Network，確認 `hero-home.webp` 請求提早出現、Priority 為 High。本機已測過，正式站尚未部署驗收。
5. T12 導覽斷行：CSS 修改與自動測試已完成；仍需在寬度 `1280、1130、1100、900、768、375` 瀏覽器驗收。
6. PageSpeed Insights 手機版：記錄 Performance、LCP、CLS、SEO 修改前後數據；完成後重新提交 sitemap 至 Google Search Console。

---

## C. 尚未完成的 AI／內容任務（尚未開始或尚未完成）

### T08｜首頁 JSON-LD 正式驗收與產生來源

本機 `site/index.html` JSON-LD 已移除首頁 BreadcrumbList，補入 LocalBusiness 營業時間、`priceRange`、`image`、`parentOrganization`，JSON 語法測試通過；沒有自行填入 geo 座標。正式 Rich Results Test 尚待部署後執行。

需留意：目前 `build.py` 產生的 HTML 結構與已部署內容不一致，且其頁面模板沒有目前首頁 JSON-LD 區塊。不要直接跑全站 `python3 build.py` 覆蓋 `site/`；後續需先確認真正來源策略，再把 JSON-LD 修改納入可持續的生成流程。

### T11｜需補做快取版本參數更新及完整目視檢查

`site/style.css` 已改色票，但其 `<link rel="stylesheet">` 版本參數尚未按任務書更新。CSS 檔案本身目前在十個主要頁面及 404 頁有不同引用值，請後續以當天日期更新需要失效的引用，並再跑 grep 與逐頁檢查。任務清單目前 T11 已勾選，但完整逐頁驗收尚未完成；確認後再修正勾選／完成紀錄狀態。

### T12｜中寬度導覽斷行（AI 修改完成；驗收待完成）

`site/style.css` 已調整導覽列斷點至 1120px、桌機導覽不換行，並禁止按鈕文字換行；`tests/test_navigation_responsive_css.py` 已執行通過。仍需在瀏覽器按任務書指定的 `1280、1130、1100、900、768、375` 寬度驗收，且 CSS 引用版本參數需按當天日期更新後才可結案。

### T13｜手機版 Hero 高度（AI 修改完成；驗收待完成）

已將任務書的手機 Hero padding、標題與 CTA 規則加至 `site/style.css`。仍需用瀏覽器於 `375×812` 確認首頁第一屏可見「找到適合的服務」標題，並更新 CSS 引用版本參數後再結案。

### T14｜卡片 hover 與層次（AI 修改完成；驗收待完成）

已加入卡片 hover、焦點/動態降低支援及 `.card-new` 淡橘樣式；首頁情境卡片已使用放大 SVG 圖示。任務書指定的「2026 新服務」卡片目前不存在於首頁內容，因此未新增該標記；需確認是否保留此卡片樣式驗收。仍需桌面滑鼠及 reduced-motion 實測、更新 CSS 引用版本參數。

### 其餘未開始／部分完成任務

- **T15（AI+人工）**：任務書預設方案 B（未取得書面同意），依指示從 `cases.html` metadata/JSON-LD 移除具名客戶；完整盤點其他頁面的客戶名稱並交由人員確認。不要自行改寫案例事實。
- **T16（AI+人工）**：等待人員提供可使用的原廠 Logo 檔及經確認的數據。AI 不可編造服務客戶數、庫存數或合作標章；資料未提供前不可上線 placeholder/TODO。
- **T17（AI 修改完成；來源同步待處理）**：首頁區標題與三張情境卡片已重寫、加上 SVG 圖示；`data-track-cta` 為 4、`data-service` 為 3。需與修改前數量核對（未留存可比對的原始值），並將內容同步至適當的生成來源；勿直接跑全站 build 覆蓋既有頁面。
- **T18（AI）**：十頁頁尾營業時間、Google Maps 地址連結、隱私政策、LINE 圖片（檔案存在時）同步修改；驗收十頁 footer 一致。地址、電話、統編不得順手改寫。
- **T19（AI 修改完成；來源同步待處理）**：`site/cases.html` 的 3 個案例已改為挑戰／方案／成果欄位，只重排既有敘述；HTML 解析通過。尚需將變更納入可靠生成來源並核對修改前後所有文字。

### 本輪執行補充（2026-11-11）

- 已執行 `python3 -m unittest tests.test_navigation_responsive_css -v`，1 項測試通過；首頁與案例頁 HTML parser 驗證通過。
- 修正 `.case header` 被全域 `header{position:sticky}` 誤套用的捲動重疊；改以 `body>header` 僅讓主導覽固定，案例頁 CSS cache-busting 更新為 `20261111`。本機瀏覽器無快取重載後確認案例內層 header 為 `static`、主導覽仍為 `sticky`。
- 修正 `parts.html` 庫存清單 checkmark 與產品文字重疊：`.stock-card li` 現在保留 `26px` 左內距並設為相對定位；parts 頁 CSS 版本更新為 `20261111`。瀏覽器確認清單項目計算樣式正確。
- 本輪其他 CSS 變更尚未更新全部十個主要頁面及 404 頁的 stylesheet cache-busting 參數；不要宣稱正式站或部署驗收完成。
- `build.py` 仍與目前 `site/` 部署版結構不一致。T12–T14、T17、T19 的 CSS、首頁與案例頁尚未同步至可靠的持續生成來源；勿執行全站 build 覆蓋 `site/`。
- **T20（AI+人工）**：等人員提供庫存 CSV 後製作可搜尋清單；不可公開價格或數量，除非人員明確授權。
- **T21（AI+人工）**：建立文章專區與首批草稿；技術正確性需人員審核後才可上線。
- **T22（AI，選做）**：預設不做；只有人員要求品牌字型一致時才載入外部字型。

---

## D. 回覆 Web Server 同事時的結案記錄

請回覆以下項目，方便網站維護者更新主任務清單：

- T01 DNS／Redirect Rule 是否完成；驗收結果：
- T02 `site/404.html` 是否部署、Nginx 設定是否 `nginx -t` 通過及 reload；500 根因：
- T05 Rocket Loader 是否關閉／是否 purge；手機選單和 GA 驗收：
- T06 `/index.html` 是否 301 至 `/`；首頁狀態碼：
- T09 Cache Rule 設定及 POST 排除路徑；第二次請求是否 HIT：
- T10 四個安全標頭與 UTF-8 charset 是否生效：
- Sitemap 全部 URL HTTP 狀態：
- Google Rich Results、PageSpeed、Search Console 是否完成：
