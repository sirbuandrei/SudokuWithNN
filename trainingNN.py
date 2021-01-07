import cv2
import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

# LOAD THE DATA SET FROM MNIST
train_images = mnist.train_images()
train_labels = mnist.train_labels()
test_images = mnist.test_images()
test_labels = mnist.test_labels()

# MAKE THE PIXELS FROM [0, 255] TO [0, 1] TO TRAIN EASIER
train_images = (train_images / 255)
test_images = (test_images / 255)

# RESHAPE THE IMAGES (28*28 pixel images)
train_images = train_images.reshape((-1, 784))
test_images = test_images.reshape((-1, 784))

# CREATE THE MODEL WITH 2 HIDDEN LAYERS WITH 64 NEURONS AND RELU ACTIVATION FUNCTION
# AND LAST LAYER OF 10 NEURONS (10 digits 0-9) WITH SOFTMAX FUNCTION
model = Sequential()
model.add(Dense(64, activation='relu', input_dim=784))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='softmax'))

# COMPILE THE MODEL WITH 'adam' OPTIMIZER
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# TRAIN MODEL WITH 7 EPOCHS AND 32 BATCH-SIZE
model.fit(
    train_images,
    to_categorical(train_labels),
    epochs=7,
    batch_size=32
)

# EVALUATE MODEL
model.evaluate(
    test_images,
    to_categorical(test_labels)
)

# SAVE THE TRAINED MODEL
model.save('model')
