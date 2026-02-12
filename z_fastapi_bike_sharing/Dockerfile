# 1. 使用官方 Python 輕量版作為基礎鏡像
FROM python:3.10-slim

# 2. 設定容器內的工作目錄
WORKDIR /app

# 3. 先複製需求清單並安裝，利用 Docker 快取機制加速
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製專案所有內容到容器中
COPY . .

# 5. 暴露 FastAPI 預設埠號 (Render 會自動對應)
EXPOSE 8000

# 6. 啟動指令：使用 uvicorn 執行
# 注意：$PORT 是 Render 自動分配的環境變數
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}