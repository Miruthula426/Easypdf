import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical

# -----------------------
# LOAD DATA
# -----------------------
train_df = pd.read_csv("dataset/train.csv")
test_df = pd.read_csv("dataset/test.csv")

# First column = label (1–26), remaining = pixels
X_train = train_df.iloc[:, 1:].values
y_train = train_df.iloc[:, 0].values - 1   # 🔥 FIX (1–26 → 0–25)

X_test = test_df.iloc[:, 1:].values
y_test = test_df.iloc[:, 0].values - 1     # 🔥 FIX

# -----------------------
# PREPROCESS
# -----------------------
X_train = X_train / 255.0
X_test = X_test / 255.0

# Reshape to images (28x28 grayscale)
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

# Number of classes (A–Z)
num_classes = 26

# Convert labels to categorical
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

# -----------------------
# MODEL
# -----------------------
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
    MaxPooling2D(2,2),

    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# -----------------------s
# TRAIN
# -----------------------
model.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=128,
    validation_data=(X_test, y_test)
)

# -----------------------
# SAVE MODEL
# -----------------------
model.save("handwriting_model.h5")

print("✅ Model training completed and saved as handwriting_model.h5")
