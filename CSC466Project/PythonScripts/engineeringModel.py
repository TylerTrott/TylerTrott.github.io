import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.ensemble import RandomForestRegressor

# Load Data
# Python is a mentally ill child. Why do i need to dynamically look for this file
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'traffic_data.csv')
df = pd.read_csv(file_path)


# Data Cleaning
df = df.dropna(subset=['Year'])  # Drop missing 'Year'
df['Traffic_Volume'] = df['Traffic_Volume'].fillna(df['Traffic_Volume'].median())  # Fill missing target
df = pd.get_dummies(df, columns=['Direction'], drop_first=True)  # One-hot encode 'Direction'

# Feature Engineering: Compute Distance
def calculate_distance(row):
    start = eval(row['Start_Coordinates'])  # Convert string to tuple
    end = eval(row['End_Coordinates'])  # Convert string to tuple
    return np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)

df['Distance'] = df.apply(calculate_distance, axis=1)

# REMOVE SCALING (Decision Trees don’t need it)
X = df.drop(columns=['OBJECTID', 'Traffic_Volume', 'Start_Coordinates', 'End_Coordinates'])
y = df['Traffic_Volume']

# Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 🌳 Train a Decision Tree with controlled depth
tree_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)

tree_model.fit(X_train, y_train)

# Predictions
y_pred_tree = tree_model.predict(X_test)

# Evaluate
mse_tree = mean_squared_error(y_test, y_pred_tree)
r2_tree = r2_score(y_test, y_pred_tree)

print(f"Decision Tree Mean Squared Error: {mse_tree}")
print(f"Decision Tree R-squared: {r2_tree}")

# Feature Importance
feature_importances = tree_model.feature_importances_
features = X.columns

