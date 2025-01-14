#!/usr/bin/env python3
import numpy as np
from PIL import Image
from sklearn.neighbors import NearestCentroid
from sklearn.decomposition import PCA
import sys
sys.path.append("/Users/pmh/Desktop/classification_scheme/Prerequisites") 
from LoadFiles import *

# Column = (vertical) =  1 colomn = 1200
# Rows = (horizontal) = 1 row = 400

def fetch_specific_image_in_binary(imageNumber, loaded_images):
    matrix = loaded_images
    return matrix[:,imageNumber]


def display_image(imageNumber, loaded_images):
    data = fetch_specific_image_in_binary(imageNumber, loaded_images)
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


def fetch_label_by_image_id(image_id, loaded_labels):
    return loaded_labels[image_id]


def fetch_NCC_training_set(loaded_images, loaded_labels):
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


def fetch_NCC_testing_set(loaded_images, loaded_labels):
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


def nearest_class_centroid(loaded_images, loaded_labels):
    training_data = fetch_NCC_training_set(loaded_images, loaded_labels)
    training_images = [training_data[i][0] for i in range(len(training_data))]
    training_labels = [training_data[i][1] for i in range(len(training_data))]

    pca = PCA(n_components=(2))
    training_images_pca = pca.fit_transform(training_images)

    clf = NearestCentroid()
    clf.fit(training_images_pca, training_labels)

    print(len(clf.centroids_))
    #print(clf.centroids_)
    
    test_data = fetch_NCC_testing_set(loaded_images, loaded_labels)
    test_images = [test_data[i][0] for i in range(len(test_data))]

    pca = PCA(n_components=(2))
    test_images_pca = pca.fit_transform(test_images)

    return clf.predict(test_images_pca)


def calculate_success_rate(loaded_images, loaded_labels):
    predicted_data_labels = nearest_class_centroid(loaded_images, loaded_labels)

    test_data = fetch_NCC_testing_set(loaded_images, loaded_labels)
    test_labels = [test_data[i][1] for i in range(len(test_data))]

    print("Predicted labes: \n", predicted_data_labels)
    print("Test labels: \n", test_labels)


    counter = 0
    success = 0
    for label in test_labels:
        if(label == predicted_data_labels[counter]):
            success = success + 1
        counter = counter + 1

    percentage = (success/counter)*100

    print("Total image labels: ", counter)
    print("Succeful matched image labels: ", success)
    print(f"Percentage: {percentage}%")


if __name__ == "__main__": 
    # prerequisites
    file_loader = LoadFiles()
    loaded_images = file_loader.load_ORL_face_data_set_40x30()
    loaded_labels = file_loader.load_ORL_labels()

    display_image(0,loaded_images)
    calculate_success_rate(loaded_images, loaded_labels)


    