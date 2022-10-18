import os
from queue import Empty 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import keras
import tflearn
import numpy as np
import matplotlib as plt
import cv2
import easyocr
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from random import shuffle
from tqdm import tqdm



os.chdir("C:/Users/7/Desktop/Python Work File")
TRAIN_DIR = 'C:/Users/7/Desktop/Python Work File/Platenumbers'
TEST_DIR = 'C:/Users/7/Desktop/Python Work File/Platenumbers'
lr = 1e-3


physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


plateCascade = cv2.CascadeClassifier("C:/Users/7/Desktop/Python Work File/PlateDetect/Haarcascades.xml")
minArea = 500

cap =cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    numberPlates = plateCascade.detectMultiScale(imgGray, 1.1, 4)
    print(numberPlates)
    for (x, y, w, h) in numberPlates:
        area = w*h
        if area > minArea:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            imgRoi = img[y:y+h,x:x+w]
            cv2.imshow("ROI",imgRoi)
    if cv2.waitKey(1) & 0xFF ==ord('s'):
        if numberPlates:
            cv2.imwrite("C:/Users/7/Desktop/Python Work File/Python Project/Saved Images"+str(count)+".jpg",imgRoi)
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
        cv2.putText(img,"Scan Saved",(15,265),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count+=1
    if cv2.waitKey(1) & 0xFF == ord('e'):
        cap.release()
        cv2.destroyAllWindows()
        break

ds_train = tf.keras.preprocessing.image_dataset_from_directory(
    TRAIN_DIR,
    labels='inferred',
    label_mode='int',
    class_names=None,
    color_mode='grayscale',
    batch_size=12,
    image_size=(28, 28),
    shuffle=True,
    seed=123,
    validation_split=0.1,
    subset='training',
    )


ds_test = tf.keras.preprocessing.image_dataset_from_directory(
    TEST_DIR,
    labels='inferred',
    label_mode='int',
    class_names=None,
    color_mode='grayscale',
    batch_size=32,
    image_size=(28, 28),
    shuffle=True,
    seed=123,
    validation_split=0.5,
    subset='validation',
    )


def convert():
    result = ''
    Files = os.listdir(path)
    for file in Files:
        imgPath = os.path.join(path, file)
        img_gray = cv2.imread(imgPath)
        cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
        cv2.destroyAllWindows()
        reader = easyocr.Reader(['en'], gpu = False)
        result = reader.readtext(imgPath)
        
        #if cv2.waitKey(1) & 0xFF == ord('e'):
        #   break
convert()



def augment(x,y):
    image = tf.image.random_brightness(x, max_delta = 0.05)
    return image, y
ds_train = ds_train.map(augment)





def my_model():
    input = layers.Input(shape = (28,28,1))
    x = layers.Conv2D(32,3)(input)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(64,3, padding = "same")(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.MaxPooling2D()(x)
    x = layers.Conv2D(128, 3)(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Conv2D(128, 3)(x)
    x = layers.BatchNormalization()(x)
    x = keras.activations.relu(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, activation = 'relu')(x)
    output = layers.Dense(10)(x)
    

    model = keras.Model(outputs = output, inputs = input)
    

    return model

model = my_model()
#model.save_weights('saved_model/')


model.compile(
    loss = keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    optimizer = keras.optimizers.Adam(learning_rate = 1e-3),
    metrics=["accuracy"],
)



model.fit(ds_train, epochs = 50, verbose =2)
model.evaluate(ds_test, verbose=2)