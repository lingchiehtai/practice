
# 從 JMA 獲取氣象資料分析

## 簡介
此專案從日本氣象廳 (JMA) 網站擷取特定地點和年份的氣象資料。處理資料為 CSV 檔案，並使用 matplotlib 生成趨勢圖表進行分析。

## 專案內容
- **weather_JMA.py**：主要腳本，功能包括：
  - 從 JMA 擷取四個城市的每月氣象資料：熊本、金沢、青森、札幌。
  - 將資料儲存為 CSV 檔案。
  - 繪製四個城市的每月平均溫度趨勢圖。
  - 繪製札幌多年雪量圖表（2020-2023 年）。

- **需要Library**： `requests`、`beautifulsoup4`、`pandas` 和 `matplotlib`。

- **輸出檔案**：
  - CSV 檔案：每個城市的 `weatherJMA_Data_{city}.csv`。
  - 圖片：`weatherJMA_cities_avg_Temp.png` 和 `weatherJMA_Snowfall.png`。

## 重點分析
- **平均溫度趨勢**：比較 2023 年四個城市的每月平均溫度，突出季節變化。
- **雪量分析**：專注於札幌從 10 月到 4 月的多年雪量，顯示冬季降雪的年際差異。
- 資料來源為 JMA 的每月統計，並處理缺失值（例如，將雪量資料中的 '--' 替換為 '0'）。