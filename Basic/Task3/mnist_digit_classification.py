# -*- coding: utf-8 -*-
"""MNIST Digit Classification

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tlPN6egKvMlFkBguGIjCOQPZwokRCxzZ
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.datasets import mnist
from keras.utils import to_categorical

# Load and preprocess MNIST dataset
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape((x_train.shape[0], 28, 28, 1)).astype('float32') / 255
x_test = x_test.reshape((x_test.shape[0], 28, 28, 1)).astype('float32') / 255
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# Split the training data into training and validation sets
val_split = 0.1
val_samples = int(val_split * x_train.shape[0])
x_val = x_train[:val_samples]
y_val = y_train[:val_samples]
x_train = x_train[val_samples:]
y_train = y_train[val_samples:]

# Define CNN model architecture
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(x_train, y_train, epochs=5, batch_size=64, validation_data=(x_val, y_val))

# Define function to plot confusion matrix
def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

# Evaluate on validation data
val_loss, val_acc = model.evaluate(x_val, y_val)
print('\nValidation accuracy:', val_acc)

# Make predictions on validation data
val_predictions = model.predict(x_val)
val_predicted_labels = np.argmax(val_predictions, axis=1)

# Calculate confusion matrix for validation predictions
val_confusion_mtx = confusion_matrix(np.argmax(y_val, axis=1), val_predicted_labels)

# Plot confusion matrix for validation data
plt.figure(figsize=(8, 6))
plot_confusion_matrix(val_confusion_mtx, classes=range(10), title='Validation Confusion Matrix')
plt.show()

# Evaluate on test data
test_loss, test_acc = model.evaluate(x_test, y_test)
print('\nTest accuracy:', test_acc)

# Make predictions on test data
test_predictions = model.predict(x_test)
test_predicted_labels = np.argmax(test_predictions, axis=1)

# Calculate confusion matrix for test predictions
test_confusion_mtx = confusion_matrix(np.argmax(y_test, axis=1), test_predicted_labels)

# Plot confusion matrix for test data
plt.figure(figsize=(8, 6))
plot_confusion_matrix(test_confusion_mtx, classes=range(10), title='Test Confusion Matrix')
plt.show()

# Display random test images with predicted labels
plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(x_test[i].reshape(28, 28), cmap=plt.cm.binary)
    predicted_label = np.argmax(test_predictions[i])
    true_label = np.argmax(y_test[i])
    if predicted_label == true_label:
        color = 'green'
    else:
        color = 'red'
    plt.xlabel(f"Predicted: {predicted_label}, True: {true_label}", color=color)
plt.show()