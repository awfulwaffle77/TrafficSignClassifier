# https://www.tensorflow.org/tutorials/keras/classification
import os
import random

import cv2
import matplotlib.pyplot as plt
import numpy as np
from numpy import asarray
import tensorflow as tf

# The path to the directory where all folders with images are stored
TRAIN_PATH = "F:\\Facultate\\Licenta\\SendIntroDeepLearning_October\\ParasitologyClassificationDemo\\GTSRB_Final_Training_Images\\GTSRB\\Final_Training\\Images"
TEST_PATH = "F:\Facultate\Licenta\SendIntroDeepLearning_October\ParasitologyClassificationDemo\GTSRB_Final_Test_Images\GTSRB\Final_Test\Images"
CHECKPOINT_PATH = "./cp.cpkt"
# The width and height of the resized image in pixels
IMAGE_HEIGHT = 128
IMAGE_WIDTH = 128
MAX_IMAGES_PER_LABEL = 50
MAX_TEST_IMAGES = 40

CLASS_NAMES = ["20", "30", "50", "60", "70", "80", "80_bar", "100", "120", "NoOvertake", "NoTruckOvertake",
               "RoadIntersected", "Priority", "GivePriority", "Stop", "ForbiddenAll", "NoTruck", "ForbiddenWay",
               "Warning", "LeftBend", "RightBend", "Twist", "LevelOscillation", "Sideslip", "ShallowRoad",
               "ConstructionWork", "TrafficLight", "Pedestrians", "School", "Bikes", "Frozen", "WildAnimals",
               "RemovedRestrictions", "OnlyRight", "OnlyLeft", "OnlyForward", "ForwardRight", "ForwardLeft",
               "DetourRight", "DetourLeft", "Roundabout", "CanOvertake", "TruckCanOvertake"]

LAST_LABEL = 11


def create_test_list():
    # Creates normalized arrays from images
    images = os.listdir(TEST_PATH)
    test_array = []
    count = 0
    for image in images:
        if count == MAX_TEST_IMAGES:
            return test_array
        full_path = TEST_PATH + "\\" + image
        img = cv2.imread(full_path)
        resized_img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
        test_array.append(asarray(resized_img) / 255.0)
        count += 1
    return test_array


def create_training_list():
    # Creates normalized arrays from images
    labels = os.listdir(TRAIN_PATH)

    train_array = []  # labeled_array[0] will be the pictures with label 0 and so on
    train_labels = []
    count = 0
    for label in labels:
        x = 0  # debugging purposes
        if int(label) == LAST_LABEL:
            break
        for picture_path in os.listdir(TRAIN_PATH + "\\" + label):
            if count == MAX_IMAGES_PER_LABEL:
                count = 0
                break
            full_path = TRAIN_PATH + "\\" + label + "\\" + picture_path
            img = cv2.imread(full_path)
            resized_img = cv2.resize(img, (IMAGE_WIDTH, IMAGE_HEIGHT))
            train_array.append(asarray(resized_img) / 255.0)
            train_labels.append(int(label))
            count += 1
    return {"TrainArray": train_array, "TrainLabels": train_labels}


def create_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(128, 128, 3)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(LAST_LABEL)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model


def plot_value_array(i, predictions_array):
    plt.grid(False)
    x = len(predictions_array[i])
    plt.xticks(range(x))
    plt.yticks([], rotation='vertical')
    # thisplot = plt.bar(range(x), predictions_array[i])
    thisplot = plt.bar(range(x), predictions_array[i])  #, tick_label=CLASS_NAMES[:x])
    for a, b in zip(range(x), predictions_array[i]):
        plt.text(a, b, CLASS_NAMES[a], rotation='vertical')
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array[i])

    thisplot[predicted_label].set_color('red')


def plot_pictures(test_array, predictions):
    for i in range(5):
        plt.figure(figsize=(10, 10))
        plt.subplot(1, 2, 1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        index = random.randint(0, len(test_array) - 1)
        plt.imshow(test_array[index], cmap=plt.cm.binary)
        plt.xlabel(CLASS_NAMES[np.argmax(predictions[index])])
        plt.subplot(1, 2, 2)
        plot_value_array(index, predictions)
        plt.show()


test_array = create_test_list()
test_array = asarray(test_array)
print(test_array.shape)
dict = create_training_list()
train_array = dict["TrainArray"]
train_labels = dict["TrainLabels"]

train_labels = asarray(train_labels)
train_array = asarray(train_array)
print(train_array.shape, train_labels.shape)
print(train_labels)

checkpoint_dir = os.path.dirname(CHECKPOINT_PATH)
cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH,
                                                 save_weights_only=True,
                                                 verbose=1)
model = create_model()
if os.path.isfile("checkpoint"):
    print("Found model")
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)
else:
    model.fit(train_array, train_labels, epochs=10, callbacks=cp_callback)

probability_model = tf.keras.Sequential([model,
                                         tf.keras.layers.Softmax()])
predictions = probability_model.predict(test_array)

plot_pictures(test_array, predictions)
