# 1. 指定 Python 環境
FROM python:3.10-slim

# 2. 設定容器內的工作目錄 (這會自動建立 /app 資料夾)
WORKDIR /app

# 3. 複製 requirements.txt 到容器的當前目錄 (即 /app/)
# 注意：這裡不加任何路徑，直接寫檔名
COPY requirements.txt ./

# 4. 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 5. 複製專案剩餘所有檔案
COPY . .

# 6. 設定啟動指令 (使用 CMD 格式)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]