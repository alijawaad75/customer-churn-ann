# %%
import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt

# %%
df= pd.read_csv('D:\c desktop data\Python\Ann\Churn_Modelling.csv')

# %%
df

# %%
# now we asign the value of x and the value of y
x = df.iloc[:,3:13].values
# why i start from 3 and not 0
# because the first three columns are not features
# and the last column is not a feature
# the last column is the dependent variable
y = df.iloc[:, 13].values

# %%
print(x)

# %%
print(y)

# %%
# now we have the datset in whiich some feature that are catgorical so we convert into the numberic
from sklearn.preprocessing import LabelEncoder
# we use the LabelEncoder to convert the categorical data into numeric data
le = LabelEncoder()   # that are the object
# we convert the categorical data into numeric data
le.fit(df['Gender'])
df['Gender'] = le.transform(df['Gender'])


# %%
df

# %%
# now thw geography featuree have more than binary catory so we use the one hot encoding
# we use the get_dummies to convert the categorical data into numeric data
# give me the onehot encoder libary ad import
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
# we use the ColumnTransformer to convert the categorical data into numeric data

ct = ColumnTransformer([('encoder', OneHotEncoder(drop='first'), [1])], remainder='passthrough')
# 1 are we defined the columns
x = ct.fit_transform(x)

# %%
print(x)

# %%
### now we diivde the testing and thetraiining data
from sklearn.model_selection import train_test_split
# we use the train_test_split to split the data into training and testing data
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# %%
print(X_train.dtypes)
print(X_train.head())

# %%


# %%
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
import pandas as pd

# Assuming X_train and X_test are your datasets (pandas DataFrames)
# Identify categorical columns (e.g., 'Geography', 'Gender')
categorical_cols = ['Geography', 'Gender']  # Adjust based on your dataset
numerical_cols = X_train.select_dtypes(include=['int64', 'float64']).columns

# Create ColumnTransformer to encode categorical columns
ct = ColumnTransformer(
    transformers=[
        ('encoder', OneHotEncoder(drop='first', sparse_output=False), categorical_cols)
    ],
    remainder='passthrough'  # Keep numerical columns unchanged
)

# Create a pipeline to combine encoding and scaling
pipeline = Pipeline([
    ('encoder', ct),  # Apply one-hot encoding
    ('scaler', StandardScaler())  # Apply scaling to all columns
])

# Apply transformations to training and test data
X_train_scaled = pipeline.fit_transform(X_train)
X_test_scaled = pipeline.transform(X_test)

# %%
## now we do the feature standard scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train_scaled = sc.fit_transform(X_train)
X_test_scaled = sc.transform(X_test)

# %%
pip install keras

# %%
## we make the input layer and the first hidden layer
hidden_layer = tf.keras.layers.Dense(units=6, activation='relu', )
hidden_layer1 = tf.keras.layers.Dense(units=6, activation='relu')

# %%
%pip install tensorflow


from keras.layers import Dense, Dropout, Activation, Flatten,sequential



# %%
## we make the input layer and the first hidden layer
import tensorflow as tf

hidden_layer = tf.keras.layers.Dense(units=6, activation='relu', )
hidden_layer1 = tf.keras.layers.Dense(units=6, activation='relu')
# we make the output layer
output_layer = tf.keras.layers.Dense(units=1 , activation='sigmoid',kernel_initializer='uniform')
tf.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])



# %%
tf.fit(X_train_scaled, y_train, epochs=10, batch_size=32)

# %%



