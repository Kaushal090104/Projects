import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load the Titanic dataset (modify as needed)
df = pd.read_csv("C:/Users/puroh/OneDrive/Desktop/8th sem major project/EDA APP with AI_FINAL/EDA APP with AI/example_dataset/titanic.csv")

# Preprocessing
# Drop irrelevant columns
df = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])
# Convert categorical variables to numeric
df = pd.get_dummies(df, columns=['Sex', 'Embarked'], drop_first=True)
# Fill missing values with median
df.fillna(df.median(), inplace=True)

# Separate features and target
X = df.drop(columns=['Survived'])  # Assuming 'Survived' is the target variable

# Standardize the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Display explained variance
print("Explained variance ratio:", pca.explained_variance_ratio_)

# Retrieve PCA loadings
loadings = pd.DataFrame(pca.components_, columns=X.columns, index=['PCA1', 'PCA2'])
print("PCA Loadings:")
print(loadings)

# Add PCA components to the dataset for analysis
df['PCA1'] = X_pca[:, 0]
df['PCA2'] = X_pca[:, 1]
