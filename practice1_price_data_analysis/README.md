# 飯店房價監控與分析系統 (Hotel Price Monitoring & Analysis System)

## 📝 簡介
一個整合了**網路爬蟲**與**數據分析**的工具，協助使用者自動化追蹤訂房平台（如 Booking.com）上的飯店價格波動。透過批次抓取特定月份的房價數據，進一步生成視覺化趨勢圖表，並利用統計邏輯計算「合理房價」的出現機率，作為出遊訂房的決策參考。

## 📂 專案內容
本專案主要由以下兩個核心模組組成：

1.  **數據採集模組 (`hotel-price-1month_v2.py`)**
    *   使用 `requests` 與 `BeautifulSoup` 針對 Booking.com 進行自動化爬取。
    *   支援按月份批次查詢特定飯店、特定房型的每日價格。
    *   將抓取結果自動存儲為結構化的 CSV 檔案，便於後續分析。

2.  **數據分析與視覺化模組 (`hotel-price-1month_plot.py`)**
    *   讀取 CSV 房價數據，並利用 `matplotlib` 繪製多間飯店的價格對比趨勢圖。
    *   **合理價計算**：實作特定演算法，統計價格落在「最低價的 1.3 倍」以內的區間，計算其出現頻率，幫助使用者識別特價時機。

---

## 🚀 重點分析

*   **自動化資料工程**：透過模擬 User-Agent 與 Cookie 處理，突破基礎爬蟲限制，獲取即時的房價資訊。
*   **彈性參數化設計**：爬蟲腳本支援傳入不同的 `hotelWebsite` 與 `dataBlockID`（房型編號），可輕易擴展至不同飯店的監控。
*   **趨勢洞察**：
    *   **視覺化對比**：直觀呈現不同日期、不同飯店間的價格震盪，協助找出旅遊淡旺季。
    *   **智慧統計模型**：不只是顯示價格，更透過「合理價出現機率」量化數據，讓使用者了解目前的價格是否值得入手。
*   **容錯處理**：爬蟲內建 `try-except` 機制，當特定日期無法獲取資料時會標記為 'None'，確保長時間跑批次任務時不會因單一請求失敗而中斷。

---

## 🛠️ 如何執行

### 1. 環境準備
請確保安裝了 Python 3.x 以及必要的套件：
```bash
pip install requests beautifulsoup4 matplotlib
```

### 2. 獲取房價數據 (Scraping)
編輯 `hotel-price-1month_v2.py` 中的參數（如飯店 URL 或月份），然後執行：
```bash
python hotel-price-1month_v2.py
```
*執行完成後，目錄下會生成對應飯店名稱的 `.csv` 檔案。*

### 3. 執行視覺化分析 (Analysis)
確保 CSV 檔案路徑正確，執行分析腳本：
```bash
python hotel-price-1month_plot.py
```
*系統將會：*
1.  在終端機輸出各飯店的「合理價出現機率」。
2.  產出一個 `hotel-price-1month_1.png` 圖表檔案，顯示房價走勢。



---
*Developed by Linda Tai*