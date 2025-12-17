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
 * 從 Google Sheet 讀取資料
 * 假設資料在第一個工作表
 */
function getData() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheets()[0]; // 讀取第一個工作表
  
  // 取得所有資料範圍
  const data = sheet.getDataRange().getValues();
  
  // 如果沒有資料，回傳空陣列
  if (data.length === 0) return [];
  
  const headers = data[0]; // 標題列
  const rows = data.slice(1); // 內容資料
  
  // 將二維陣列轉換為物件陣列，方便前端使用
  // 對應欄位順序：Location(0), Category(1), Name(2), Detail_1(3), Detail_2(4), MapLink(5), Status(6)
  const formattedData = rows.map(row => {
    return {
      location: row[0],
      category: row[1],
      name: row[2],
      detail1: row[3],
      detail2: row[4],
      mapLink: row[5],
      status: row[6]
    };
  }).filter(item => item.name !== ""); // 過濾掉沒有名稱的空行
  
  return formattedData;
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
    ["東京", "景點", "晴空塔", "世界最高的自立式電波塔", "推薦傍晚去，可以看夕陽", "https://maps.google.com", "Open"],
    ["東京", "美食", "六厘舍", "東京車站一番街超人氣沾麵", "排隊時間約 30 分鐘", "https://maps.google.com", "Open"],
    ["京都", "景點", "清水寺", "京都最古老的寺院", "整修完畢，舞台風景極佳", "https://maps.google.com", "Open"],
    ["京都", "美食", "勝牛", "炸牛排專賣店", "建議點半熟，口感軟嫩", "https://maps.google.com", "Open"],
    ["大阪", "其他", "環球影城", "哈利波特與瑪利歐園區必去", "需要購買快速通關", "https://maps.google.com", "Open"]
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(2, 1, demoData.length, headers.length).setValues(demoData);
  
  // 設定標題列樣式
  sheet.getRange(1, 1, 1, headers.length).setBackground("#f3f4f6").setFontWeight("bold");
}