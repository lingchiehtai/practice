
# 景點美食清單（Google Apps Script Web App）

本專案是一個以 **Google Apps Script (GAS)** 為後端、
**HTML + Tailwind CSS** 為前端的輕量 Web App，
用來從 **Google Sheet** 讀取資料並動態呈現景點／美食清單。

---

## 特點摘要

* 後端主機使用 Google Apps Script
* 資料即時來自 Google Sheet，方便維護與編輯
* 前後端分離，結構清楚
* 適合做為：
  * 旅遊清單
  * 私人資料庫
  * 行動裝置友善的清單型 Web App
  
---

## 整體架構

```
Browser
  ↓
Index.html（前端 UI / 篩選 / 搜尋）
  ↓ google.script.run
code.gs（後端 GAS）
  ↓
Google Sheet（資料來源）
```

---

## 前端（Index.html）

### 技術

* HTML + JavaScript
* Tailwind CSS（UI 樣式）
* Font Awesome（Icon）
* 由 Google Apps Script Web App 載入

### 功能

* 從後端取得景點／美食資料
* 卡片式清單顯示（含圖片、地圖連結）
* 篩選功能

  * 地區（location）
  * 分類（category）
  * 關鍵字搜尋（支援多關鍵字、空格或 `&`）
* 動態篩選狀態列顯示
* 分批渲染（Batch Render，避免一次渲染過多資料）
* 載入中動畫與錯誤處理

---

## 後端（code.gs）

### doGet()

* Web App 入口
* 載入 `Index.html`
* 設定頁面標題與 viewport
* 允許 iframe（方便嵌入）


### getData()

* 從指定的 Google Sheet 讀取資料

* 將每一列轉為前端可用的物件格式

* 欄位範例：

  * location（地區）
  * category（分類）
  * name（名稱）
  * detail1（簡介）
  * detail2（補充說明）
  * mapLink（地圖連結）
  * imageUrl（圖片）

* 若 Sheet 尚未初始化，會自動寫入示範資料（demo data）

* 回傳陣列給前端使用

---

## Google Sheet 資料格式

| location | category | name | detail1 | detail2 | mapLink  | imageUrl |
| -------- | -------- | ---- | ------- | ------- | -------- | ------ |

* 第一列為標題列
* 前端會自動忽略空白或標題列資料

---


