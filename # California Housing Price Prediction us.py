# California Housing Price Prediction using Artificial Neural Network
# Fixed and Debugged Version

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Load the dataset
print("Loading California Housing dataset...")
housing_data = fetch_california_housing()
X = housing_data.data
y = housing_data.target

print(f"Dataset shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Feature names: {housing_data.feature_names}")

# Split the data into training and testing sets
print("\nSplitting data into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Training set size: {X_train.shape[0]}")
print(f"Test set size: {X_test.shape[0]}")

# Standardize the features
print("\nStandardizing features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Features standardized successfully!")

# Build the ANN model
print("\nBuilding the ANN model...")
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_scaled.shape[1],)),
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(1)  # Output layer for regression
])

# Compile the model
model.compile(
    optimizer='adam',
    loss='mse',
    metrics=['mae']
)

print("Model architecture:")
model.summary()

# Train the model
print("\nTraining the model...")
history = model.fit(
    X_train_scaled, y_train,
    validation_data=(X_test_scaled, y_test),
    epochs=50,
    batch_size=32,
    verbose=1
)

# Evaluate the model
print("\nEvaluating the model...")
test_loss, test_mae = model.evaluate(X_test_scaled, y_test, verbose=0)
print(f"Test Loss (MSE): {test_loss:.4f}")
print(f"Test MAE: {test_mae:.4f}")

# Make predictions on test set
y_pred = model.predict(X_test_scaled)

# Calculate additional metrics
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nModel Performance Metrics:")
print(f"Mean Squared Error: {mse:.4f}")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"R² Score: {r2:.4f}")

# Plot training history
plt.figure(figsize=(15, 5))

# Plot training & validation loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='Training Loss', marker='o')
plt.plot(history.history['val_loss'], label='Validation Loss', marker='s')
plt.title('Model Loss Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.grid(True)

# Plot training & validation MAE
plt.subplot(1, 2, 2)
plt.plot(history.history['mae'], label='Training MAE', marker='o')
plt.plot(history.history['val_mae'], label='Validation MAE', marker='s')
plt.title('Model MAE Over Epochs')
plt.xlabel('Epoch')
plt.ylabel('Mean Absolute Error')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# Plot actual vs predicted values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Actual House Prices')
plt.ylabel('Predicted House Prices')
plt.title('Actual vs Predicted House Prices')
plt.grid(True)
plt.show()

# Make a prediction with custom input
print("\n" + "="*50)
print("MAKING A CUSTOM PREDICTION")
print("="*50)

# Sample input: [MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]
sample_input = np.array([[5.0, 20.0, 6.0, 1.0, 1000.0, 3.0, 34.0, -118.0]])

print("Sample input features:")
print("- Median Income: 5.0 (tens of thousands)")
print("- House Age: 20.0 years")
print("- Average Rooms: 6.0")
print("- Average Bedrooms: 1.0")
print("- Population: 1000.0")
print("- Average Occupancy: 3.0")
print("- Latitude: 34.0")
print("- Longitude: -118.0")

# Scale the input using the same scaler
sample_input_scaled = scaler.transform(sample_input)

# Make prediction
prediction = model.predict(sample_input_scaled, verbose=0)

print(f"\nPredicted house price: ${prediction[0][0]:.2f} (in hundreds of thousands)")
print(f"Predicted house price: ${prediction[0][0] * 100000:.2f} (actual dollars)")

# Feature importance analysis (simple approach)
print("\n" + "="*50)
print("FEATURE IMPORTANCE ANALYSIS")
print("="*50)

feature_names = housing_data.feature_names
feature_importance = []

# Calculate simple feature importance by training individual models
for i in range(len(feature_names)):
    # Train model with single feature
    single_feature_model = Sequential([
        Dense(32, activation='relu', input_shape=(1,)),
        Dense(16, activation='relu'),
        Dense(1)
    ])
    single_feature_model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Train on single feature
    single_feature_model.fit(
        X_train_scaled[:, i].reshape(-1, 1), y_train,
        epochs=20, batch_size=32, verbose=0
    )
    
    # Evaluate
    loss, mae = single_feature_model.evaluate(
        X_test_scaled[:, i].reshape(-1, 1), y_test, verbose=0
    )
    
    # Store inverse of loss (higher = better)
    feature_importance.append(1/loss if loss > 0 else 0)

# Normalize importance scores
feature_importance = np.array(feature_importance)
feature_importance = feature_importance / np.sum(feature_importance) * 100

# Display feature importance
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance (%)': feature_importance
}).sort_values('Importance (%)', ascending=False)

print(importance_df)

# Plot feature importance
plt.figure(figsize=(10, 6))
plt.barh(importance_df['Feature'], importance_df['Importance (%)'])
plt.xlabel('Relative Importance (%)')
plt.title('Feature Importance for House Price Prediction')
plt.gca().invert_yaxis()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "="*50)
print("ANALYSIS COMPLETE!")
print("="*50)