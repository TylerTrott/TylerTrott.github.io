import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'traffic_data.csv')
df = pd.read_csv(file_path)

# Data Cleaning
df = df.dropna(subset=['Year'])  # Drop missing 'Year'
df['Traffic_Volume'] = df['Traffic_Volume'].fillna(df['Traffic_Volume'].median())  # Fill missing target

# # 🔹 1. Line Plot - Traffic Volume Over Time
# plt.figure(figsize=(12, 6))
# sns.lineplot(x=df["Year"], y=df["Traffic_Volume"], marker="o", linestyle="-", color="b")
# plt.title("Traffic Volume Over the Years")
# plt.xlabel("Year")
# plt.ylabel("Traffic Volume")
# plt.grid(True)
# plt.show()

# # 🔹 2. Rolling Average (Smoother Trend Line)
# df["Rolling_Avg"] = df["Traffic_Volume"].rolling(window=5).mean()  # 5-year moving average

# plt.figure(figsize=(12, 6))
# sns.lineplot(x=df["Year"], y=df["Traffic_Volume"], alpha=0.3, label="Raw Data", color="gray")
# sns.lineplot(x=df["Year"], y=df["Rolling_Avg"], linewidth=2, label="Rolling Average", color="red")
# plt.title("Traffic Volume Trend with Rolling Average")
# plt.xlabel("Year")
# plt.ylabel("Traffic Volume")
# plt.legend()
# plt.grid(True)
# plt.show()

# 🔹 3. Box Plot - Distribution of Traffic Volume Per Decade
df["Decade"] = (df["Year"] // 10) * 10  # Convert years to decade bins

plt.figure(figsize=(12, 6))
sns.boxplot(x="Decade", y="Traffic_Volume", data=df)
plt.title("Traffic Volume Distribution by Decade")
plt.xlabel("Decade")
plt.ylabel("Traffic Volume")
plt.ylim(0, 25000)  # Set y-axis limit to max out at 50,000
plt.grid(True)
plt.show()

# 🔹 4. Correlation Heatmap - Find Factors Influencing Traffic Volume
correlation_matrix = df.drop(columns=["OBJECTID", "Start_Coordinates", "End_Coordinates"], errors="ignore").corr()

plt.figure(figsize=(10, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Heatmap of Features")
plt.show()
