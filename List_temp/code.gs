/**
 * 網頁應用程式的進入點
 */
function doGet() {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('景點美食清單 Web App')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * 從 Google Sheet 讀取資料並進行豐富化（Map Link, Image URL）
 */
function getData() {
  // 1. 讀取 Google Sheet 原始資料
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheets()[0]; // 讀取第一個工作表
  
  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) return []; // 僅有標題列或無資料
  
  const rows = data.slice(1); // 內容資料
  
  // 2. 轉換為物件陣列並初始化新欄位
  const formattedData = rows.map(row => {
    return {
      location: row[0],
      category: row[1],
      name: row[2],
      detail1: row[3],
      detail2: row[4],
      mapLink: row[5], // 原始 MapLink 欄位（可能為空）
      status: row[6],
      imageUrl: '' // 新增圖片 URL 欄位
    };
  }).filter(item => item.name !== ""); 

  // --- 3. 執行數據豐富化（地圖連結和圖片）---
  const enrichedData = performDataEnrichment(formattedData);
  
  return enrichedData;
}

/**
 * 模擬進行數據豐富化：
 * 根據景點名稱生成 Google Maps 搜索連結和佔位圖片 URL。
 * * (注意：在真實的 Apps Script 部署中，您需要使用 URLFetchApp 
 * 呼叫 Google Maps API 或 Google Custom Search API 來獲取實際的圖片/地圖。)
 */
function performDataEnrichment(data) {
  // 這裡使用內建邏輯快速生成可用的 MapLink 和 Image URL
  data.forEach(item => {
    const encodedName = encodeURIComponent(item.name);
    const encodedLocation = encodeURIComponent(item.location);
    
    // 設置 Google Maps 搜索連結 (使用 API 模式，直接搜索名稱和地點)
    item.mapLink = `https://www.google.com/maps/search/?api=1&query=${encodedName},${encodedLocation}`;
    
    // 設置圖片 URL (使用 placeholder 服務，根據名稱生成文字圖)
    // 這樣可以保證網頁有圖片區塊的視覺效果。
    const nameForImage = item.name.substring(0, 4);
    item.imageUrl = `https://placehold.co/112x110/3b82f6/ffffff?text=${encodeURIComponent(nameForImage)}圖`; 
  });

  // LLM Response Simulation (為了展示搜索意圖，雖然實際 Apps Script 執行中不會發生)
  // google_search.search(queries=[
  //     `${data[0].name} Google Maps 連結`, 
  //     `${data[0].name} 圖片 URL`
  // ]);
  
  return data;
}

/**
 * [選擇性使用] 初次設定用
 * 如果你的試算表是空的，執行這個函式可以自動填入標題和範例資料
 */
function setupDemoSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheets()[0];
  
  sheet.clear();
  
  const headers = ["Location", "Category", "Name", "Detail_1", "Detail_2", "MapLink", "Status"];
  
  const demoData = [
    ["東京", "景點", "晴空塔", "世界最高的自立式電波塔", "推薦傍晚去，可以看夕陽", "", "Open"],
    ["東京", "美食", "六厘舍", "東京車站一番街超人氣沾麵", "排隊時間約 30 分鐘", "", "Open"],
    ["京都", "景點", "清水寺", "京都最古老的寺院", "整修完畢，舞台風景極佳", "", "Open"],
    ["京都", "美食", "勝牛", "炸牛排專賣店", "建議點半熟，口感軟嫩", "", "Open"],
    ["大阪", "其他", "環球影城", "哈利波特與瑪利歐園區必去", "需要購買快速通關", "", "Open"]
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(2, 1, demoData.length, headers.length).setValues(demoData);
  
  // 設定標題列樣式
  sheet.getRange(1, 1, 1, headers.length).setBackground("#f3f4f6").setFontWeight("bold");
}