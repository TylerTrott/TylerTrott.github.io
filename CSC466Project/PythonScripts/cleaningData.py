import pandas as pd

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('./traffic_data.csv')


# Preview the data
print(df.head())

# Check for missing values
print(df.isnull().sum())

# Before cleaning
# OBJECTID              0
# Traffic_Volume        1
# Direction             1
# Segment_Length        0
# Year                 15
# Start_Coordinates     0
# End_Coordinates       0
# dtype: int64

# Fill missing data with the mean (or any other strategy)
#df = df.fillna(df.mean())

# Or drop rows with missing values
# df = df.dropna()

# Drop rows with missing 'Year' values
df = df.dropna(subset=['Year'])

# Fill missing 'Traffic_Volume' values with the median
df['Traffic_Volume'] = df['Traffic_Volume'].fillna(df['Traffic_Volume'].median())


 # Drop one of the categories to avoid multicollinearity
df = pd.get_dummies(df, columns=['Direction'], drop_first=True) 

print(df.isnull().sum())
# After cleaning
# OBJECTID             0
# Traffic_Volume       0
# Segment_Length       0
# Year                 0
# Start_Coordinates    0
# End_Coordinates      0
# Direction_one        0