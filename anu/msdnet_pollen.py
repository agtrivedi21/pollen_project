import msdnet
import glob


import os
import random
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import models, layers
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras import datasets, models, optimizers
from tensorflow.random import set_seed
from sklearn.model_selection import train_test_split
import IPython
import kerastuner as kt


seed_value = 1
os.environ['PYTHONHASHSEED']=str(seed_value)

random.seed(seed_value)
np.random.seed(seed_value)
set_seed(seed_value)

train_path1 = open('../matthew/Pollen_Classifier/train/images/1/train_OBJ/paths.txt').read().splitlines()
train_path2 = open('../matthew/Pollen_Classifier/train/images/2/train_OBJ/paths.txt').read().splitlines()
train_path3 = open('../matthew/Pollen_Classifier/train/images/3/train_OBJ/paths.txt').read().splitlines()
train_path4 = open('../matthew/Pollen_Classifier/train/images/4/train_OBJ/paths.txt').read().splitlines()

print("Total class 1 images:", len(train_path1))
print("Total class 2 images:", len(train_path2))
print("Total class 3 images:", len(train_path3))
print("Total class 4 images:", len(train_path4))

train_images = []
train_labels = []

# first element for padding, classes begin at 1
label_counts = [len(train_path1), len(train_path2), len(train_path3), len(train_path4)] 

total_labels = label_counts[0] + label_counts[1] + label_counts[2] + label_counts[3]

type1, type2, type3, type4 = 0, 0, 0, 0

print("----- AUMGENTING DATA -----")

for i in range(total_labels):
    # Get random label that is still available
    while True:
        random_label = random.randint(1, 4)
        if (label_counts[random_label-1] > 0):
            label_counts[random_label-1] = label_counts[random_label-1] - 1 # decrement the label count
            break
    
    # append the label to the label list and add the corresponding image to the image list
    train_labels.append([random_label - 1])

    if random_label == 1:
        path = train_path1.pop(len(train_path1) - 1) # get the path at the end of the list
        image = Image.open(path)
        image_45 = image.rotate(45)
        image_90 = image.rotate(90)
        image = np.asarray(image, dtype=np.float64)
        image_45 = np.asarray(image_45, dtype=np.float64)
        image_90 = np.asarray(image_90, dtype=np.float64)
        train_images.append(image)
        train_images.append(image_45)
        train_images.append(image_90)
        label = [0]
        train_labels.append(label)
        train_labels.append(label)
        type1 += 3
    elif random_label == 2:
        path = train_path2.pop(len(train_path2) - 1) # get the path at the end of the list
        image = Image.open(path)
        image_45 = image.rotate(45)
        image_90 = image.rotate(90)
        image_60 = image.rotate(60)
        image_15 = image.rotate(15)
        image = np.asarray(image, dtype=np.float64)
        image_45 = np.asarray(image_45, dtype=np.float64)
        image_90 = np.asarray(image_90, dtype=np.float64)
        image_60 = np.asarray(image_60, dtype=np.float64)
        image_15 = np.asarray(image_15, dtype=np.float64)
        train_images.append(image)
        train_images.append(image_45)
        train_images.append(image_90)
        train_images.append(image_60)
        train_images.append(image_15)
        label = [1]
        train_labels.append(label)
        train_labels.append(label)
        train_labels.append(label)
        train_labels.append(label)
        type2 += 5
    elif random_label == 3:
        path = train_path3.pop(len(train_path3) - 1) # get the path at the end of the list
        image = Image.open(path)
        image = np.asarray(image, dtype=np.float64)
        train_images.append(image)
        type3 += 1
    elif random_label == 4:
        path = train_path4.pop(len(train_path4) - 1) # get the path at the end of the list
        image = Image.open(path)
        image_45 = image.rotate(45)
        image_90 = image.rotate(90)
        image_60 = image.rotate(60)
        image_15 = image.rotate(15)
        image = np.asarray(image, dtype=np.float64)
        image_45 = np.asarray(image_45, dtype=np.float64)
        image_90 = np.asarray(image_90, dtype=np.float64)
        image_60 = np.asarray(image_60, dtype=np.float64)
        image_15 = np.asarray(image_15, dtype=np.float64)
        train_images.append(image)
        train_images.append(image_45)
        train_images.append(image_90)
        train_images.append(image_60)
        train_images.append(image_15)
        label = [3]
        train_labels.append(label)
        train_labels.append(label)
        train_labels.append(label)
        train_labels.append(label)
        type4 += 5
    else:
        print("Issue...")

train_images = np.asarray(train_images)
train_labels = np.asarray(train_labels)

print("New training image count:", train_images.shape[0])

train_images, test_images, train_labels, test_labels = train_test_split(train_images,
                                                                       train_labels,
                                                                       test_size = 0.33,
                                                                       random_state = seed_value)

print("----- TRAIN/TEST SPLIT: 66% training, 33% testing -----")


train_1_count, train_2_count, train_3_count, train_4_count = 0, 0, 0, 0

for i in range(len(train_labels)):
    if train_labels[i,0] == 0:
        train_1_count += 1
    elif train_labels[i,0] == 1:
        train_2_count += 1
    elif train_labels[i,0] == 2:
        train_3_count += 1
    elif train_labels[i,0] == 3:
        train_4_count += 1
        
total = train_1_count + train_2_count + train_3_count + train_4_count

print("Out of", total, "training images, there are", train_1_count, "in class 1,", train_2_count, \
      "in class 2,", train_3_count, "in class 3,", "and", train_4_count, "in class 4")

test_1_count, test_2_count, test_3_count, test_4_count = 0, 0, 0, 0

for i in range(len(test_labels)):
    if test_labels[i,0] == 0:
        test_1_count += 1
    elif test_labels[i,0] == 1:
        test_2_count += 1
    elif test_labels[i,0] == 2:
        test_3_count += 1
    elif test_labels[i,0] == 3:
        test_4_count += 1

total = test_1_count + test_2_count + test_3_count + test_4_count

print("Out of", total, "testing images, there are", test_1_count, "in class 1,", test_2_count, \
      "in class 2,", test_3_count, "in class 3,", "and", test_4_count, "in class 4\n\n")

train_images = train_images / 255
test_images = test_images / 255

dilations = msdnet.dilations.IncrementDilations(10)

n = msdnet.network.MSDNet(100, dilations, 5, 4, gpu = True) # the 4 is the number of output channels, one for each label
#n = msdnet.network.MSDNet(100, dilations, 5, 1, gpu = False) #uncomment this to run on CPU

n.initialize()

flsin = train_images
flstg = train_labels

dats = []
for i in range(len(flsin)):
    d = msdnet.data.ImageFileDataPoint(flsin[i], flstg[i])
    d_oh = msdnet.data.OneHotDataPoint(d, [0,1,2,3])
    dats.append(d_oh)

dats = msdnet.data.convert_to_slabs(dats, 2, flip=True)
dats_augm = [msdnet.data.RotateAndFlipDataPoint(d) for d in dats]

#n.normalizeinout(dats)

bprov = msdnet.data.BatchProvider(dats, 1)

# Define validation data (not using augmentation)
flsin = test_images
flstg = test_labels
datsv = []

for i in range(len(flsin)):
    d = msdnet.data.ImageFileDataPoint(flsin[i], flstg[i])
    d_oh = msdnet.data.OneHotDataPoint(d, [0,1,2,3])
    datsv.append(d_oh)

datsv = msdnet.data.convert_to_slabs(datsv, 2, flip=False)

val = msdnet.validate.MSEValidation(datsv)

t = msdnet.train.AdamAlgorithm(n)

consolelog = msdnet.loggers.ConsoleLogger()
filelog = msdnet.loggers.FileLogger('log_pollen.txt')
imagelog = msdnet.loggers.ImageLabelLogger('log_pollen', chan_in = 2, onlyifbetter=True)
singlechannellog = msdnet.loggers.ImageLogger('log_pollen_singlechannel', chan_in = 2, chan_out = 3, onlyifbetter=True)

msdnet.train.train(n, t, val, bprov, 'pollen.h5', loggers=[consolelog, filelog, imagelog, singlechannellog], val_every=len(datsv))

os.makedirs('pollen_results', exist_ok = True)
n = msdnet.network.MSDNet.from_file('pollen.h5', gpu=True)
#n = msdnet.network.MSDNet.from_file('pollen.h5', gpu=False) #uncomment for CPU

flsin = train_images
dats = [msdnet.data.ImageFileDataPoint(f) for f in flsin]

dats = msdnet.data.convert_to_slabs(dats, 2, flip=False)

for i in range(flsin):
    output = n.forward(dats[i].input)
    tifffile.imsave('pollen_results/pollen_label_{:05d}.tiff'.format(i), np.argmax(output, 0,).astype(np.uint8))
    tifffile.imsave('pollen_results/pollen_prob_lab2_{:05d}.tiff'.format(i), output[2])

