# 日本中部行程表 — 程式碼說明文件
---

### 包含以下九個區塊：
1.全域顏色變數 — 一次改色全頁套用  
2.背景漸層 — 角度與色票說明  
3.泡泡效果 — 數量、大小、速度參數  
4.外層容器 — 左右留白、上下間距  
5.頁首標題 — 各元素字體大小與間距  
6.按鈕列 — 滑動設定、按鈕大小、選中樣式  
7.行程卡片 — 卡片留白、圓角、頂部色條  
8.卡片內部元素 — 標題、時間欄、內文、標籤、提示框  
9.JS 切換邏輯 — 顯示隱藏原理說明

---
## 一、全域顏色變數（`:root`，第 9–18 行）

```css
:root {
  --ink: #1a2a3a;    /* 主要文字顏色（深藍黑）*/
  --paper: #dff0fb;  /* 背景紙色（目前未直接使用，備用）*/
  --aged: #c2e0f4;   /* 舊紙色（備用）*/
  --rust: #2e6fa3;   /* 強調色，用於交通資訊粗體、城市標籤 */
  --moss: #3a8a7a;   /* 綠色標籤（景點） */
  --mist: #5a87a8;   /* 次要文字色（時間欄、小標） */
  --gold: #3a9fc8;   /* 主色，用於卡片頂部色條、分隔線 */
  --line: #9ecde8;   /* 分隔線顏色（dashed line）*/
}
```
> 要改顏色主題，直接修改這裡即可，全頁套用。

---

## 二、背景漸層（`body`，第 22–30 行）

```css
background: linear-gradient(160deg, #a8d8f0 0%, #ceeafa 30%, #e0f4fd 60%, #b8e2f5 100%);
```
- `160deg`：漸層角度（0 = 由上到下，90 = 由左到右）
- 四個色票控制漸層深淺變化
- `background-attachment: fixed`：滑動時背景不跟著動

---

## 三、泡泡畫布（`#bubble-canvas`，第 32–37 行 CSS / 第 586–656 行 JS）

- `position: fixed`：固定在畫面上，不隨頁面捲動
- `pointer-events: none`：滑鼠事件穿透，不影響點擊
- JS 控制 **28 顆泡泡**（`length: 28`，第 596 行）
  - 泡泡大小：`Math.random() * 28 + 8` → 半徑 8–36px
  - 上浮速度：`Math.random() * 0.5 + 0.2` → 慢速漂移
  - 透明度：`Math.random() * 0.25 + 0.08` → 8%–33%

---

## 四、整頁的外層容器（`.container`，第 39–45 行）

```css
.container {
  max-width: 780px;   /* 最大寬度，超過此寬度置中顯示 */
  margin: 0 auto;     /* 水平置中 */
  padding: 60px 4px 80px;
  /*        ↑上  ↑左右  ↑下 */
}
```
> **左右留白**：改 `4px` 這個數字（目前左右各 4px）
> **上方留白**：改 `60px`
> **下方留白**：改 `80px`

---

## 五、頁首標題區（`.header`，第 47–110 行）

| 元素 | 說明 | 位置 |
|------|------|------|
| `.header` | `margin-bottom: 24px` 控制標題與按鈕列距離 | 第 50 行 |
| `.route-label` | 最上方英文小字，`font-size: 13px` | 第 63–71 行 |
| `.title-jp` | **主標題**，微軟正黑體 | 第 73–81 行 |
| `.cities-strip` | 城市名橫排列，`margin-top: 24px` | 第 89–96 行 |

```css
/* 主標題字體大小（響應式）*/
.title-jp {
  font-size: clamp(32px, 6vw, 52px);
  /* 最小 32px，最大 52px，中間依視窗寬度縮放 */
  font-weight: 700;       /* 粗體 */
  letter-spacing: 6px;    /* 字間距 */
  margin-bottom: 8px;     /* 與下方元素距離 */
}
```

---

## 六、按鈕列（`.tab-bar`，第 258–280 行）

```css
.tab-bar {
  display: flex;
  flex-wrap: nowrap;        /* 強制單列，不換行 */
  overflow-x: auto;         /* 超出寬度可橫向滑動 */
  -webkit-overflow-scrolling: touch; /* iOS 滑順滾動 */
  scrollbar-width: none;    /* 隱藏捲軸 */
  margin-bottom: 12px;      /* ← 按鈕列與卡片的距離 */
  position: sticky;
  top: 12px;                /* ← 捲動時距頂端固定距離 */
  padding: 6px 4px 10px;   /* 按鈕列內距 */
}
```

```css
.tab-btn {
  font-size: 15px;          /* 按鈕文字大小 */
  font-weight: 700;
  padding: 7px 20px;        /* 按鈕上下 7px / 左右 20px */
  border-radius: 8px;       /* 圓角矩形弧度（越大越圓）*/
}

.tab-btn.active {           /* 選中狀態 */
  background: linear-gradient(135deg, #3a9fc8, #5ab8e0);
  color: #fff;
  box-shadow: 0 4px 16px rgba(58,159,200,0.45);
  transform: translateY(-2px); /* 選中時微微上浮 */
}
```

---

## 七、每日行程卡片（`.day-card`，第 112–135 行）

```css
.day-card {
  margin-bottom: 24px;   /* 卡片與卡片之間的距離 */
  margin-left: 4px;      /* 卡片左側留白 */
  margin-right: 4px;     /* 卡片右側留白 */
  padding: 20px 24px 18px;
  /*        ↑上   ↑左右  ↑下  卡片內部留白 */
  border-radius: 10px;   /* 卡片圓角 */
  border-top: 4px solid var(--gold); /* 頂部彩色條 */
}
```

**每天頂部色條顏色**（第 129–135 行）：
```css
.day-card:nth-child(1) { border-top-color: var(--rust); } /* D1 藍 */
.day-card:nth-child(2) { border-top-color: var(--gold); } /* D2 水藍 */
.day-card:nth-child(3) { border-top-color: var(--moss); } /* D3 綠 */
/* 以此類推... */
```

---

## 八、卡片內部元素

### 卡片標題（`.day-num` / `.day-title`）
```css
.day-num {
  font-size: 13px;     /* "DAY 01" 小字大小 */
  color: var(--mist);  /* 灰藍色 */
}

.day-title {
  font-size: 20px;     /* ← 每天大標題字體大小 */
  font-weight: 700;    /* 粗體 */
  font-family: 'Microsoft JhengHei'; /* 微軟正黑體 */
}
```

### 交通資訊欄（`.transport`）
```css
.transport {
  padding: 10px 14px;    /* 內距 */
  margin-bottom: 14px;   /* 與行程列表的距離 */
  font-size: 14px;       /* ← 交通資訊文字大小 */
}
```

### 行程時間列表（`.schedule li`）
```css
.schedule li {
  grid-template-columns: 70px 1fr;
  /* 70px = 時間欄寬度，1fr = 活動內容欄 */
  padding: 10px 0;       /* 每列上下間距 */
  font-size: 18px;       /* ← 行程內文字體大小（主要內容）*/
  line-height: 1.7;      /* 行高 */
}

.time {
  font-size: 14px;       /* ← 時間欄（09:00）字體大小 */
  color: var(--mist);    /* 灰藍色 */
}
```

### 標籤（景點 / 美食 / 住宿）
```css
.activity .tag {
  font-size: 10px;       /* 標籤文字大小 */
  padding: 1px 6px;      /* 標籤內距 */
  border-radius: 10px;   /* 標籤圓角 */
}
/* 顏色分類：
   .tag-food  → 橘/棕（美食）
   .tag-sight → 綠（景點）
   .tag-stay  → 藍（住宿）
   .tag-nature → 深綠（自然）
*/
```

### 提示框（`.tip-box`）
```css
.tip-box {
  margin-top: 14px;       /* 與行程列表距離 */
  padding: 10px 14px;     /* 內距 */
  border-left: 3px solid var(--gold); /* 左側藍色線條 */
  font-size: 14px;        /* ← 提示文字大小 */
}
```

---

## 九、顯示切換邏輯（JS，第 568–584 行）

```javascript
// 點擊 D1~D7 按鈕時執行
function showDay(n) {
  // 1. 全部卡片加上 hidden（隱藏）
  document.querySelectorAll('.day-card').forEach(c => c.classList.add('hidden'));
  // 2. 全部按鈕移除 active 樣式
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  // 3. 找到對應天數的卡片，移除 hidden（顯示）
  document.querySelector(`.day-card[data-day="${n}"]`).classList.remove('hidden');
  // 4. 對應按鈕加上 active 樣式（變藍）
  document.querySelectorAll('.tab-btn')[n - 1].classList.add('active');
}

// 點擊「摘要」按鈕時執行（邏輯相同，改顯示 summary-panel）
function showSummary() { ... }
```

> **預設顯示 D1**：D1 卡片沒有 `hidden` class，D2~D7 和摘要都有 `hidden`

---

## 快速修改對照表

| 想改的項目 | CSS 屬性 | 位置 |
|-----------|---------|------|
| 行程內文字體大小 | `.schedule li { font-size }` | 第 213 行 |
| 時間欄字體大小 | `.time { font-size }` | 第 224 行 |
| 每天大標題大小 | `.day-title { font-size }` | 第 160 行 |
| 交通資訊文字大小 | `.transport-detail { font-size }` | 第 192 行 |
| 提示框文字大小 | `.tip-box { font-size }` | 第 248 行 |
| 卡片左右留白 | `.day-card { margin-left/right }` | 第 115–116 行 |
| 卡片內部留白 | `.day-card { padding }` | 第 121 行 |
| 頁面左右邊距 | `.container { padding }` | 第 42 行 |
| 按鈕與卡片距離 | `.tab-bar { margin-bottom }` | 第 267 行 |
| 標題與按鈕列距離 | `.header { margin-bottom }` | 第 50 行 |
| 背景顏色漸層 | `body { background }` | 第 23 行 |
| 泡泡數量 | `Array.from({ length: 28 }` | 第 596 行 |
