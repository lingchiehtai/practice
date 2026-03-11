# 匯入 CSV 檔案並列印內容
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 使用 pandas 讀取 CSV 檔案為 DataFrame
penguins = pd.read_csv('penguins.csv')
print(penguins.head()) # 印出前五行看看資料樣貌

# 檢查並處理缺失值
print("\n--- 缺失值統計 ---")
print(penguins.isnull().sum())

# 策略: 移除含有任何缺失值的資料列 (Drop rows with NA)
penguins = penguins.dropna()
print(f"\n移除缺失值後的資料筆數: {len(penguins)}")

# 配對圖 (Pair Plot)
plt.figure(figsize=(10, 8))
sns.pairplot(penguins, hue='species')
plt.title('Pair Plot of Penguin Dataset')
plt.savefig('penguins_pairplot.png', dpi=300, bbox_inches='tight')
#plt.show()

# 相關性矩陣 (correlation matrix)
plt.figure(figsize=(8, 6))
corr = penguins.corr(numeric_only=True)
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.savefig('penguins_correlation_matrix.png', dpi=300, bbox_inches='tight')
plt.show()
