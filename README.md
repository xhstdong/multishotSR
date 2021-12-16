# multishotSR
Algorithm to significantly boost pixel count and image resolution

This code combines 16 images, each shifted by half pixel, to generate a final image with 4x the resolution

The only format it reads right now is pure RAW (no metadata). Specific vendor formats can be added by using rawpy instead of np.fromfile for reading in RAW data

The input images should be numbered from 0.raw to 15.raw. Additional characters can be added before the numbers, but they must be the same across all 16 shots. The order of the 16 images should be in this order:

![alt text](https://github.com/xhstdong/multishotSR/blob/main/16shot_table.PNG?raw=true)

Some test images can be found here: https://drive.google.com/drive/folders/1sa6bMHf8rWKW50FiqliDVW3IchvCdZMB?usp=sharing

These images have a Bayer grid that is considered "GR" according to the OpenCV convention: https://docs.opencv.org/3.4/d8/d01/group__imgproc__color__conversions.html#ga57261f12fccf872a2b2d66daf29d5bd0

Run pixel_shift_16shots.py to start. Depending on the size of the image, it may take some time. The user must change the directory in pixel_shift_16shots to the directory of the images. If the images are not the samples, the image size will need to be adjusted in OnePS.py, from the default 3024x4096. Throughout the code, 16bit unsigned int is assumed to be the data type. The data range is assumed to be 14 bit, but this can be changed in OnePS.py (in actuality, our sample images are 10bits left shifted by 4 bits, for more details, please request the manual from us). These can be improved for greater convenience at a later time.

Superresolution is achieved by taking the mean/median of all upsampled images. This is a simple yet effective way of achieving improvement.

Helper code include implementations for getting better result by combining 1/3 pixel (36 total shots) and 1/4 pixel (64 total shots) shifted images 
