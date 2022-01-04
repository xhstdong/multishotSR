#  This code combines 16 images, each shifted by half pixel, to generate a final
#  image with 4x the resolution
#  INPUT: user must modify the folder path, and file names
#  OUPUT: tiff images


import cv2
#import numpy as np
#import rawpy
#import math
import onePS
import halfPS
    
#set the proper image folder
folder_name='D:/subpixel/sample_sonyPS/sony_pixel_shift_processor-master/nov25_2021/nov25_set1'
#set the proper image file name
prefix='20211125_132559_'

ps1_images=[]

for shift_index in [0,4,5,1]:    
    image_files = [prefix+str(0+shift_index)+'.raw', prefix+str(8+shift_index)+'.raw', prefix+str(10+shift_index)+'.raw', prefix+str(2+shift_index)+'.raw']
    print(image_files)
    ps1_images.append(onePS.produce_ps1_image(image_files, folder_name))

final_image, _ = halfPS.produce_ps2_image(ps1_images)

cv2.imwrite(folder_name+'_16shot.tiff', final_image)

