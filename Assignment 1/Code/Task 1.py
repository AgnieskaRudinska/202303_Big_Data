import pandas as pd
import numpy as np
import multiprocessing as mp
import cv2
import os
import random
import time


def process_to_black_and_white(image: np.array, image_name: str):

    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # find the meadian value of pixels, since pixel is between 0 and 255
    median = np.median(image_grayscale)
    # set pixels lower than median to black, higher than median to white
    image_grayscale[image_grayscale > median] = 255
    image_grayscale[image_grayscale < median] = 0
    cv2.imwrite(f'Assignment 1/Data/Gray/{image_name}', image_grayscale)


def process_blur(image: np.array, image_name: str):
    # adding Gaussian blur to image
    blurred = cv2.GaussianBlur(image, (15, 15), 5)
    cv2.imwrite(f'Assignment 1/Data/Blurred/{image_name}', blurred)


def process_noise(image: np.array, image_name: str):
    # find number of black pixels. image is a list of list, where each list corresponds to r, g, b.
    # find positions, where each r, g, b is equal to 0.
    # we also can do this, be setting the image to grayscale and looking for 0
    # but since we want to add red noise, we decided to use original rgb
    bw_image_path = f'Assignment 1/Data/Gray/{image_name}'
    bw_image = cv2.imread(bw_image_path)
    black_pixels = np.where((bw_image[:, :, 0] == 0) & (
        bw_image[:, :, 1] == 0) & (bw_image[:, :, 2] == 0))
    number_of_black_pixels = len(black_pixels[0])
    # Calculate the 10% of black pixels and set that amount to red in random locations across the picture
    # There is a possibility, that the red pixels will be set twice,
    # But the probability is low and adding a check would take up more memory
    noise_pixels = int(number_of_black_pixels * 0.1)
    height, width = image.shape[:2]
    for _ in range(noise_pixels):
        random_x = random.randint(0, width-1)
        random_y = random.randint(0, height-1)
        image[random_y, random_x] = [0, 0, 255]

    cv2.imwrite(f'Assignment 1/Data/Noise/{image_name}', image)


def process_image(image_name: str):
    image_path = f'{IMAGE_DIR}/{image_name}'
    image = cv2.imread(image_path)
    process_to_black_and_white(image, image_name)
    process_blur(image, image_name)
    process_noise(image, image_name)

# execute each image im paralel


def scenario_1(images, cpu_count):
    with mp.Pool(cpu_count) as pool:
        pool.map(process_image, images)

# helper function


def assigment_split(arguments):
    assignment, image_name = arguments

    if assignment == 1:
        image_path = f'{IMAGE_DIR}/{image_name}'
        image = cv2.imread(image_path)
        process_to_black_and_white(image, image_name)
    elif assignment == 2:
        image_path = f'{IMAGE_DIR}/{image_name}'
        image = cv2.imread(image_path)
        process_blur(image, image_name)
    elif assignment == 3:
        image_path = f'{IMAGE_DIR}/{image_name}'
        image = cv2.imread(image_path)
        process_noise(image, image_name)


# execute tasks and images in paralel


def scenario_2(images, cpu_count):
    expanded_array = [(i, name) for name in images for i in range(1, 3)]
    case_3 = [(3, name) for name in images]
    with mp.Pool(cpu_count) as pool:
        pool.map(assigment_split, expanded_array)
    with mp.Pool(cpu_count) as pool:
        pool.map(assigment_split, case_3)

# testing image processing with different amount of cores


def test_function(images, function, file_name, order):
    print(f'Test {file_name} started')
    processors = mp.cpu_count()
    if order == 'asc':
        increment = 1
        start_pos = 3
        end_pos = processors+1
    else:
        increment = -1
        end_pos = 8
        start_pos = 9
    for processor_count in range(start_pos, end_pos, increment):
        print(f'Test with {processor_count} cpu')
        for _ in range(0, 10):
            start = time.perf_counter()
            # scenario_2(images, processors)
            function(images, processor_count)
            end = time.perf_counter()
            elapsed_time = end - start
            with open(f'Assignment 1/Results/{file_name}.txt', 'a') as f:
                f.write(f'{processor_count}, {str(elapsed_time)}\n')
            print(f'Test {processor_count} ended')


def test_bw(images, processor_count):
    args = [(1, image) for image in images]
    with mp.Pool(processor_count) as pool:
        pool.map(assigment_split, args)


def test_blur(images, processor_count):
    args = [(2, image) for image in images]
    with mp.Pool(processor_count) as pool:
        pool.map(assigment_split, args)


def test_noise(images, processor_count):
    args = [(3, image) for image in images]
    with mp.Pool(processor_count) as pool:
        pool.map(assigment_split, args)



IMAGE_DIR = "Assignment 1/Data/Images"
if __name__ == '__main__':
    print("Number of processors: ", mp.cpu_count())
    images = [image_name for image_name in os.listdir(IMAGE_DIR)]
    temp = [(3, image) for image in images]
    with mp.Pool(12) as pool:
        pool.map(assigment_split, temp)
