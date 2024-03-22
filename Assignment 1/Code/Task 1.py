import pandas as pd
import numpy as np
import multiprocessing as mp
import cv2
import os
import random
import time

def process_to_black_and_white(image:np.array, image_name:str):
    # image =cv2.imread(image_path)
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = np.median(image_grayscale)
    image_grayscale[image_grayscale > mean] = 255
    image_grayscale[image_grayscale < mean] = 0

    # count_white = np.count_nonzero(image_grayscale == 255) 
    # count_black = np.count_nonzero(image_grayscale == 0) 
    # ratio = count_white/ count_black
    # print(f"Black to white ratio: {ratio}")
    # print(f"Number of black pixels {count_black}")
    # print(image_grayscale)
    # image_nm = image_name.split('.')[0]
    # with open(f'Results\\BW\\{image_nm}.txt', 'w') as f:
    #     f.write(f'{count_white}, {count_black}, {ratio}')
    # print(f'{image_name}')
    cv2.imwrite(f'Data/Gray/{image_name}', image_grayscale)

def process_blur(image:np.array, image_name:str):
    blurred = cv2.GaussianBlur(image, (15, 15), 5)
    cv2.imwrite(f'Data/Blurred/{image_name}', blurred)

def process_noise(image:np.array, image_name:str):
    # image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # print(image)
    # black_pixels = np.count_nonzero(image_grayscale == 0)
    black_pixels = np.where((image[:, :, 0] == 0) & (image[:, :, 1] == 0) & (image[:, :, 2] == 0))
    number_of_black_pixels = len(black_pixels[0])

    noise_pixels = int(number_of_black_pixels * 0.1)
    height, width = image.shape[:2]
    # x_max = width -1
    # y_max = height
    set_pixels = noise_pixels / number_of_black_pixels
    # print(f'Black pixels {number_of_black_pixels}')
    # print(f'Set pixels {noise_pixels}')

    # print(f"Set {set_pixels}% to red")

    for _ in range(noise_pixels):
        random_x = random.randint(0, width-1)
        random_y = random.randint(0, height-1)
        image[random_y, random_x] = [0, 0, 255]

    cv2.imwrite(f'Data/Noise/{image_name}', image)    
    # image_nm = image_name.split('.')[0]
    # with open(f'Results\\Noise\\{image_nm}.txt', 'w') as f:
    #     f.write(f'{number_of_black_pixels}, {noise_pixels}, {set_pixels}')
    # with open(f"Results\Noise\{str(image_nm)}.txt", 'w') as f:
    #     f.write(f'{number_of_black_pixels}, {noise_pixels}, {set_pixels}')
    # count of pixels
    # 10 percoent of black to int ~10 save to #all
    # np.random to pick a random pixel from 0 to count for every #all
    # change that pixel to red (76)
    # grayscale back to rgb



def process_image(image_name:str):
    image_path = f'{IMAGE_DIR}/{image_name}' 
    image =cv2.imread(image_path)
    process_to_black_and_white(image, image_name)
    process_blur(image, image_name)
    bw_image_path = f'Data/Gray/{image_name}'
    bw_image =cv2.imread(bw_image_path)
    process_noise(bw_image, image_name)


def scenario_1(images):
    processors = mp.cpu_count()
    pool = mp.Pool(processors)
    start = time.perf_counter()
    pool.map(process_image, images)
    pool.close()
    end = time.perf_counter()
    elapsed_time = end - start
    with open('Results\\scenario_1.txt', 'w') as f:
        f.write(str(elapsed_time))

def assigment_split(arguments):
    assignment, image_name = arguments
    if assignment == 1:
        image_path = f'{IMAGE_DIR}/{image_name}' 
        image =cv2.imread(image_path)
        process_to_black_and_white(image, image_name)
    elif assignment == 2:
        image_path = f'{IMAGE_DIR}/{image_name}' 
        image =cv2.imread(image_path)
        process_blur(image, image_name)
    elif assignment == 3:
        bw_image_path = f'Data/Gray/{image_name}'
        bw_image = cv2.imread(bw_image_path)
        process_noise(bw_image, image_name)

    
def scenario_2(images):
    processors = mp.cpu_count()
    start = time.perf_counter()
    for image in images:
        with mp.Pool(processors) as pool:
            pool.map(assigment_split, [(1, image), (2, image)])
        bw_image_path = f'Data/Gray/{image}'
        bw_image = cv2.imread(bw_image_path)
        process_noise(bw_image, image)
    end = time.perf_counter()
    elapsed_time = end - start
    with open('Results\\scenario_2.txt', 'w') as f:
        f.write(str(elapsed_time))

def split_functions(image_name):
    with mp.Pool(2) as p:
        p.map(assigment_split, [(1, image_name), (2, image_name)])
    bw_image_path = f'Data/Gray/{image_name}'
    bw_image = cv2.imread(bw_image_path)
    process_noise(bw_image, image_name)



def scenario_3(images, cpu_count):
    # processors = mp.cpu_count()
    start = time.perf_counter()
    expanded_array = [(i, name) for name in images for i in range(1, 3)]
    case_3 = [(3, name) for name in images]
    with mp.Pool(cpu_count) as pool:
        pool.map(assigment_split, expanded_array)
    with mp.Pool(cpu_count) as pool:
        pool.map(assigment_split, case_3)
    end = time.perf_counter()
    elapsed_time = end - start
    with open('Results\\scenario_3.txt', 'w') as f:
        f.write(str(elapsed_time))

def scenario_4(images):
    processors = mp.cpu_count()
    for processor_count in range(processors, 1, -1):
        print(f'Test {processor_count} started')
        mp.Pool(processor_count)
        start = time.perf_counter()
        #some function
        scenario_3(images, processors)
        end = time.perf_counter()
        elapsed_time = end - start
        with open('Results\\scenario_4.txt', 'a') as f:
            f.write(f'{processor_count}, {str(elapsed_time)}')
        print(f'Test {processor_count} ended')




IMAGE_DIR = "Data/Images/"
if __name__ == '__main__':
    # image_dir = "Data/Images/"
    # pic_list = os.listdir(dt_dir)
    # directory = [dt_dir+x for x in pic_list]

    print("Number of processors: ", mp.cpu_count())
    # images = ['667626_18933d713e.jpg']
    images = [image_name for image_name in os.listdir(IMAGE_DIR)]
    scenario_4(images)
    # print(images)
    
    # # images = [r'Data\Images\667626_18933d713e.jpg', r'Data\Images\3637013_c675de7705.jpg']
    
    # # # process_image(images[0])
    
    # sekam cpu vs time
    # sekam black and white pixelius
    # sekam red vs all 
    # scenario 1 - only images in paralel
    # scenario 2 - only functions in paralel
    # scenario 3 - images and functions in paralel
    # scenario 4 - best scanrio with different amount of cpus

    # process_image(images[0])


    

# Parallel Splitting of the Task:
# Objective: Strategize the division of image processing into parallelizable sub-tasks.
# Guidance: Focus on parallel computing concepts and workload balancing.