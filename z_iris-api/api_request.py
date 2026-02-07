import requests
import time

url = "https://iris-fastapi-n0v1.onrender.com/predict"
data = {
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
}

print("正在連線到 API，可能需要幾十秒（第一次會較慢）... 請稍候")

# 可選：記錄開始時間，讓使用者知道等多久了
start_time = time.time()

response = requests.post(url, json=data)

end_time = time.time()
elapsed = end_time - start_time

print(f"連線完成！（花費約 {elapsed:.1f} 秒）")
print(response.json())