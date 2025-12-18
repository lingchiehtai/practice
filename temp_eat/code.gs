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
      location: row[0], // A 欄
      category: row[1],
      name: row[2],
      detail1: row[3],
      detail2: row[4],
      mapLink: row[5], // 原始 MapLink 欄位（可能為空）
      status: row[6],
      imageUrl: row[7]   // H 欄 - 新增圖片 URL 欄位
      //imageUrl: (row[7] && row[7].startsWith('http')) ? row[7] : 'https://via.placeholder.com/150?text=No+Image'  //空白或錯誤訊息，網頁就會顯示一張「No Image」的預設圖
    };
  }).filter(item => item.name !== ""); 

  // --- 3. 執行數據豐富化（地圖連結和圖片）---
  const enrichedData = performDataEnrichment(formattedData);
  
  return enrichedData;
}

/**
 * 根據景點名稱和地點生成 Google Maps 搜索連結和佔位圖片 URL。
 * * 注意：使用 Google Custom Search API 來獲取實際的圖片。
 */
function performDataEnrichment(data) {
  // 這裡使用內建邏輯快速生成可用的 MapLink 和 Image URL
  data.forEach(item => {
    const searchQuery = item.name + " " + item.location;
    const encodedSearch = encodeURIComponent(searchQuery);
    
    // 修正：只有當 MapLink 欄位 (row[5]) 是空的，才自動生成連結
    if (!item.mapLink || item.mapLink.toString().trim() === "") {
      // 使用您偏好的格式，並加上名字+地區，避免導航到其他縣市同名的店面
      item.mapLink = `https://www.google.com/maps/search/?api=1&query=${encodedSearch}`;
    }
        
    // 修正：當 H 欄 (imageUrl) 沒有有效網址時，使用佔位圖
    if (!item.imageUrl || !item.imageUrl.toString().startsWith('http')) {
      // 使用 gray 顏色 (e2e8f0) 配上深灰文字 (64748b)，看起來會像 App 的預設樣式
      item.imageUrl = `https://placehold.co/150x150/e2e8f0/64748b?text=No+Image`;
    }
  });
 
  return data;
}


// 在試算表上方新增一個自定義選單: 先選取的儲存格->抓取圖片網址
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('🔍 API 功能')
      .addItem('先選取C欄某一名稱->抓取圖片網址', 'runImageFetch')
      .addToUi();
}

//為了節省 API 額度並讓網址永久固定，不要直接在儲存格寫公式
//這邊是使用「按鈕」來「一次性」執行腳本
function runImageFetch() {
  var range = SpreadsheetApp.getActiveRange(); 
  var values = range.getValues();
  
  //const API_KEY = Search_API_KEY;
  const API_KEY = PropertiesService.getScriptProperties().getProperty('Search_API_KEY');
  const CX = "c781f3a08edd44ded"; //搜尋引擎 ID

  for (var i = 0; i < values.length; i++) {
    var keyword = values[i][0]; // C 欄的值
    // 取得同列 A 欄 (Location) 的值，C 往左移兩格是 A
    var location = range.getCell(i + 1, 1).offset(0, -2).getValue();
    if (keyword) {

      // 呼叫 API，搜尋關鍵字加上地區：例如 "YUGEN 京都"
      const combinedSearch = keyword + " " + location;
      const url = `https://www.googleapis.com/customsearch/v1?key=${API_KEY}&cx=${CX}&q=${encodeURIComponent(combinedSearch)}&searchType=image&num=1`;

      try {
        const response = UrlFetchApp.fetch(url);
        const data = JSON.parse(response.getContentText());
        if (data.items && data.items.length > 0) {
          
        // 關鍵修改點：從 C 欄往右移 5 格到 H 欄
        // 若選取的是 C 欄，offset(0, 5) 就會填入對應列的 H 欄
        // 原始圖片網址，畫質高但檔案大，網頁載入較慢。
        //range.getCell(i + 1, 1).offset(0, 5).setValue(data.items[0].link);
        // 改用縮圖網址，網頁顯示會更順暢
        range.getCell(i + 1, 1).offset(0, 5).setValue(data.items[0].image.thumbnailLink); 
        } else {
        range.getCell(i + 1, 1).offset(0, 5).setValue("找不到圖片");
        }
        } catch (e) {
        range.getCell(i + 1, 1).offset(0, 5).setValue("API 錯誤: " + e.toString());
        }
        
        // 建議：如果是大量執行，可以稍微停頓 0.1 秒避免 API 請求過快
        Utilities.sleep(100);
        
    }
  }
}


/**
 * [選擇性使用] 初次設定用
 * 如果你的試算表是空的，執行這個函式可以自動填入標題和範例資料
 */
function setupDemoSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheets()[0];
  
  sheet.clear();
  
  const headers = ["Location", "Category", "Name", "Detail_1", "Detail_2", "MapLink", "Status", "imageUrl"];
  
  const demoData = [
    ["東京", "景點", "晴空塔", "世界最高的自立式電波塔", "推薦傍晚去，可以看夕陽", "", "Open"],
    ["東京", "美食", "六厘舍", "東京車站一番街超人氣沾麵", "排隊時間約 30 分鐘", "", "Open"],
    ["京都", "景點", "清水寺", "京都最古老的寺院", "整修完畢，舞台風景極佳", "", "Open"],
    ["京都", "美食", "山元麺蔵", "烏龍麵專賣店", "冷麵,蔬菜天婦羅,可拿號碼牌", "", "Open"],
    ["大阪", "其他", "環球影城", "哈利波特與瑪利歐園區必去", "需要購買快速通關", "", "Open"]
  ];
  
  sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  sheet.getRange(2, 1, demoData.length, headers.length).setValues(demoData);
  
  // 設定標題列樣式
  sheet.getRange(1, 1, 1, headers.length).setBackground("#f3f4f6").setFontWeight("bold");
}