# 使用官方 Python 輕量版映像（3.11）
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 先複製 requirements.txt 並安裝依賴（加速快取）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案所有檔案
COPY . .

# 暴露 FastAPI 預設埠
EXPOSE 8000

# 啟動指令（使用 uvicorn 執行）
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]