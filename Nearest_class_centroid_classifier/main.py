#!/usr/bin/env python3
import numpy as np
from PIL import Image
from sklearn.neighbors import NearestCentroid


# Column = (vertical) =  1 colomn = 1200
# Rows = (horizontal) = 1 row = 400

def load_ORL_face_data_set_40x30():

    content = open("/Users/pmh/Desktop/classification_scheme/Attached_files/ORL_txt/orl_data.txt", 'r')
    readContent = content.read().split()
    
    matrix = np.zeros(shape=(1200,400))

    counterRow = 0
    counterColumn = 0
    for elem in readContent:
        if(counterColumn == 400):
            counterColumn = 0
            counterRow = counterRow + 1

        matrix[counterRow][counterColumn] = elem
        counterColumn = counterColumn + 1

    return matrix


def fetch_specific_image_in_binary(imageNumber, loaded_images):
    matrix = loaded_images
    return matrix[:,imageNumber]


def display_image(imageNumber):
    data = fetch_specific_image_in_binary(imageNumber)
    print(data)
    matrix = np.zeros(shape=(40,30,3), dtype=np.uint8)

    counterRow = 0
    counterColumn = 0
    for elem in data:
        if(counterRow == 40):
            counterRow = 0
            counterColumn = counterColumn + 1

        matrix[counterRow][counterColumn] = elem*255
        counterRow = counterRow + 1

    img = Image.fromarray(matrix, 'RGB')  
    img.save('my.png')
    img.show()


def load_ORL_labels():
    content = open("/Users/pmh/Desktop/classification_scheme/Attached_files/ORL_txt/orl_lbls.txt", 'r')
    readContent = content.read().split()
    return readContent

def fetch_label_by_image_id(image_id, loaded_labels):
    return loaded_labels[image_id]


def fetch_training_sets(loaded_images, loaded_labels):
    traing_list = []

    counter = 0
    x = 0
    total_images = 400
    while(x < total_images):
        if(counter == 7):
            x += 2
            counter = 0
        else:
            label_x = fetch_label_by_image_id(x, loaded_labels)
            image_x = fetch_specific_image_in_binary(x, loaded_images)
            traing_list.append((image_x, label_x))
            counter = counter + 1    
        x += 1
    return traing_list


def fetch_test_sets(loaded_images, loaded_labels):
    test_list = []

    counter = 0
    x = 0
    total_images = 400
    while(x < total_images):
        if(counter < 7):
            counter = counter + 1 
        elif(counter == 10):
            counter = 1
        else:
            label_x = fetch_label_by_image_id(x, loaded_labels)
            image_x = fetch_specific_image_in_binary(x, loaded_images)
            test_list.append((image_x, label_x))
            counter = counter + 1    
        x += 1
    return test_list


if __name__ == "__main__": 
    # prerequisites
    loaded_images = load_ORL_face_data_set_40x30()
    loaded_labels = load_ORL_labels()

    test01 = fetch_training_sets(loaded_images, loaded_labels)
    test02 = fetch_test_sets(loaded_images, loaded_labels)
    print(len(test02))