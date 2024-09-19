# -*- coding: utf-8 -*-
"""SI_Zalando.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SswUUQkDPrE4ZL355RbkWR_ZlssxNp4O

## Zbiór danych
- musi się pobrać Zalando Fashion-MNIST
https://github.com/zalandoresearch/fashion-mnist
"""

# wczytanie potrzebnych bibliotek
import tensorflow as tf

# wczytanie danych
fashion_mnist = tf.keras.datasets.fashion_mnist
(X_train, y_train), (X_val, y_val) = fashion_mnist.load_data()

print(f'Zbiór uczący: {X_train.shape}, zbiór walidacyjny: {X_val.shape}')

import matplotlib.pyplot as plt

plt.figure(figsize=(7,7))
plt.imshow(X_train[0], cmap=plt.cm.binary)
plt.colorbar()
plt.show()

def plot_digit(digit, dem=28, font_size=8):
    max_ax = font_size * dem

    fig = plt.figure(figsize=(10,10))
    plt.xlim([0, max_ax])
    plt.ylim([0, max_ax])
    plt.axis('off')

    for idx in range(dem):
        for jdx in range(dem):
            t = plt.text(idx*font_size, max_ax - jdx*font_size,
                         digit[jdx][idx], fontsize=font_size,
                         color="#000000")
            c = digit[jdx][idx] / 255.
            t.set_bbox(dict(facecolor=(c, c, c), alpha=0.5,
                            edgecolor='#f1f1f1'))

    plt.show()

plot_digit(X_train[0])

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

plt.figure(figsize=(14,10))
for i in range(40):
    plt.subplot(5, 8, i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(X_train[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[y_train[i]])
plt.show()

"""## Przygotowanie danych"""

X_train = X_train.astype('float32') / 255.0
X_val = X_val.astype('float32') / 255.0

from tensorflow.keras.utils import to_categorical

y_train = to_categorical(y_train, len(class_names))
y_val = to_categorical(y_val, len(class_names))

"""## Pierwsza architektura"""

from tensorflow.keras.models import Sequential

model = Sequential()

from tensorflow.keras.layers import Flatten, add

model.add(Flatten(input_shape=(28, 28)))

"""Definiowanie pierwszej warstwy ukrytej"""

from tensorflow.keras.layers import Dense

model.add(Dense(128, activation='relu'))

"""Definiowanie warstwy wyjściowej"""

model.add(Dense(10, activation = 'softmax'))

"""Kompilacja modelu"""

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

"""Podsumowanie modelu"""

model.summary()

"""# Trenowanie modelu"""

history = model.fit(X_train,
                    y_train,
                    epochs=10,
                    verbose=1,
                    batch_size = 256,
                    validation_data = (X_val, y_val)
                   )

"""Wizualizacja z trenowania"""

def draw_curves(history, key1='accuracy', ylim1=(0.8, 1.00),
                key2='loss', ylim2=(0.0, 1.0)):
    plt.figure(figsize=(12,4))

    plt.subplot(1, 2, 1)
    plt.plot(history.history[key1], "r--")
    plt.plot(history.history['val_' + key1], "g--")
    plt.ylabel(key1)
    plt.xlabel('Epoch')
    plt.ylim(ylim1)
    plt.legend(['train', 'test'], loc='best')

    plt.subplot(1, 2, 2)
    plt.plot(history.history[key2], "r--")
    plt.plot(history.history['val_' + key2], "g--")
    plt.ylabel(key2)
    plt.xlabel('Epoch')
    plt.ylim(ylim2)
    plt.legend(['train', 'test'], loc='best')

    plt.show()

draw_curves(history, key1='accuracy', ylim1=(0.7, 0.95),
            key2='loss', ylim2=(0.0, 0.8))

model2 = Sequential()
model2.add(Flatten(input_shape=(28, 28)))
model2.add(Dense(128, activation='relu')) #FIX model -> model2
model2.add(Dense(10, activation = 'softmax'))

model2.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.summary()
model2.summary()

history2 = model2.fit(X_train,
                    y_train,
                    epochs=50,
                    verbose=1,
                    batch_size = 256,
                    validation_data = (X_val, y_val)
                   )

draw_curves(history2, key1='accuracy', ylim1=(0.7, 0.95),
            key2='loss', ylim2=(0.0, 0.8))

"""Predykcja"""

y_train_pred = model.predict(X_train) #TRY model -> model2
y_val_pred = model.predict(X_val) #TRY model -> model2

import numpy as np #FIX added

def plot_value_img(i, predictions, true_label, img):
    predictions, true_label, img = predictions[i], true_label[i], img[i]
    predicted_label = np.argmax(predictions)
    true_value = np.argmax(true_label)

    plt.figure(figsize=(12,5))

    plt.subplot(1, 2, 1)

    plt.yticks(np.arange(len(class_names)), class_names)
    thisplot = plt.barh(range(10), predictions, color="gray")
    thisplot[predicted_label].set_color('r')
    thisplot[true_value].set_color('g')

    plt.subplot(1, 2, 2)

    plt.imshow(img, cmap=plt.cm.binary)
    if predicted_label == true_value:
        color = 'green'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(class_names[predicted_label],
                                100*np.max(predictions),
                                class_names[true_value]),
                                color=color)
    plt.show()

plot_value_img(1, y_val_pred,  y_val, X_val) #FIX pierwszy parametr to indeks analizowanego obrazu 1 4 12