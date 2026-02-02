# train_iris.py   ← 請新建一個檔案，名字隨便，內容直接複製下面

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import pickle

# 載入資料並訓練一個超簡單的模型
iris = load_iris()
X, y = iris.data, iris.target

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# 存成 pickle
with open("iris_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("iris_model.pkl 已成功產生！放在目前資料夾了～")