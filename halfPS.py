# Helper functions for half pixel shift

import numpy as np
import cv2
import gc


def unsharp_mask(image, kernel_size=(5, 5), sigma=3.0, amount=2.0, threshold=0):
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 2.0**16-1 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint16)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened


def produce_ps2_image_debug(input_images, folder_name):

    current_dim = input_images[0].shape
    
    #upsample    
    up_sampled=[]
    print('upsampling images')
    for index in range(len(input_images)):
        up_sampled.append(cv2.resize(input_images[index],(current_dim[1]*2, current_dim[0]*2), interpolation = cv2.INTER_NEAREST))

    
    # pixel shifting
    print('shifting and combining images')   
    up_sampled[1]=np.roll(up_sampled[1],-1,axis=0)
    
    up_sampled[2]=np.roll(up_sampled[2],(-1,1),axis=(0,1))
    
    up_sampled[3] = np.roll(up_sampled[3],1,axis=1)

    
    #compositing
    final_image_array = up_sampled[0].astype(np.uint16)
    for i in range(1, len(input_images)):
        cv2.imwrite(folder_name+'_16shot_'+str(i)+'.tiff', final_image_array)
        final_image_array = np.mean(up_sampled[0:i],0).astype(np.uint16)

    return final_image_array


def produce_ps2_image(input_images):

    current_dim = input_images[0].shape
    
    #upsample
    up_sampled=[]
    print('upsampling images')
    for index in range(len(input_images)):
        up_sampled.append(cv2.resize(input_images[index],(current_dim[1]*2, current_dim[0]*2), interpolation = cv2.INTER_NEAREST))
    
    # pixel shifting
    print('shifting and combining images')   
    up_sampled[1]=np.roll(up_sampled[1],-1,axis=0)
    
    up_sampled[2]=np.roll(up_sampled[2],(-1,1),axis=(0,1))
    
    up_sampled[3] = np.roll(up_sampled[3],1,axis=1)

    #compositing
    #final_image_array = np.median(up_sampled, 0).astype(np.uint16)
    final_image_array = np.mean(up_sampled,0).astype(np.uint16)
    ref_img = input_images[0]

    print('applying unsharp mask')
    final_image_array=unsharp_mask(final_image_array, amount=1)
    ref_img=unsharp_mask(ref_img, amount=1)
    
    return final_image_array, ref_img


def produce_ps3_image_debug(input_images, folder_name):

    current_dim = input_images[0].shape
    
    #upsample  
    up_sampled=[]
    print('upsampling images')
    for index in range(len(input_images)):
        up_sampled.append(cv2.resize(input_images[index],(current_dim[1]*3, current_dim[0]*3), interpolation = cv2.INTER_NEAREST))
    
    # pixel shifting
    print('shifting and combining images')

    up_sampled[1]=np.roll(up_sampled[1],-1,axis=0)
    up_sampled[2]=np.roll(up_sampled[2],-2,axis=0)
    up_sampled[3]=np.roll(up_sampled[3],1,axis=1)
    up_sampled[4]=np.roll(up_sampled[4],(-1,1),axis=(0,1))
    up_sampled[5]=np.roll(up_sampled[5],(-2,1),axis=(0,1))
    up_sampled[6] = np.roll(up_sampled[6],2,axis=1)
    up_sampled[7]=np.roll(up_sampled[7],(-1,2),axis=(0,1))
    up_sampled[8]=np.roll(up_sampled[8],(-2,2),axis=(0,1))    
    
    #compositing
    final_image_array = up_sampled[0].astype(np.uint16)
    for i in range(1, len(input_images)):
        cv2.imwrite(folder_name+'_36shot_'+str(i)+'.tiff', final_image_array)
        final_image_array = np.mean(up_sampled[0:i],0).astype(np.uint16)

    print('applying unsharp mask')
    final_image_array=unsharp_mask(final_image_array, kernel_size = (5,5), amount=1)

    return final_image_array


def produce_ps3_image(input_images):

    current_dim = input_images[0].shape
    
    #upsample   
    up_sampled=[]
    print('upsampling images')
    for index in range(len(input_images)):
        up_sampled.append(cv2.resize(input_images[index],(current_dim[1]*3, current_dim[0]*3), interpolation = cv2.INTER_NEAREST))
    
    # pixel shifting
    print('shifting and combining images')

    up_sampled[1]=np.roll(up_sampled[1],-1,axis=0)
    up_sampled[2]=np.roll(up_sampled[2],-2,axis=0)
    up_sampled[3]=np.roll(up_sampled[3],1,axis=1)
    up_sampled[4]=np.roll(up_sampled[4],(-1,1),axis=(0,1))
    up_sampled[5]=np.roll(up_sampled[5],(-2,1),axis=(0,1))
    up_sampled[6] = np.roll(up_sampled[6],2,axis=1)
    up_sampled[7]=np.roll(up_sampled[7],(-1,2),axis=(0,1))
    up_sampled[8]=np.roll(up_sampled[8],(-2,2),axis=(0,1))    
    
    #final_image_array = np.median(up_sampled, 0).astype(np.uint16)
    final_image_array = np.mean(up_sampled, 0).astype(np.uint16)
    ref_img = up_sampled[0]
    
    return final_image_array, ref_img


def produce_ps4_image(input_images):

    current_dim = input_images[0].shape
    
    #upsample
    up_sampled=[]
    print('upsampling images')
    for index in range(len(input_images)):
        up_sampled.append(cv2.resize(input_images[index],(current_dim[1]*4, current_dim[0]*4), interpolation = cv2.INTER_NEAREST))
    
    # pixel shifting
    print('shifting and combining images')

    up_sampled[1]=np.roll(up_sampled[1],-1,axis=0)
    up_sampled[2]=np.roll(up_sampled[2],-2,axis=0)
    up_sampled[3]=np.roll(up_sampled[3],-3,axis=0)
    up_sampled[4]=np.roll(up_sampled[4],1,axis=1)
    up_sampled[5]=np.roll(up_sampled[5],(-1,1),axis=(0,1))
    up_sampled[6]=np.roll(up_sampled[6],(-2,1),axis=(0,1))
    up_sampled[7]=np.roll(up_sampled[7],(-3,1),axis=(0,1))
    up_sampled[8] = np.roll(up_sampled[8],2,axis=1)
    up_sampled[9]=np.roll(up_sampled[9],(-1,2),axis=(0,1))
    up_sampled[10]=np.roll(up_sampled[10],(-2,2),axis=(0,1))    
    up_sampled[11]=np.roll(up_sampled[11],(-3,2),axis=(0,1))          
    up_sampled[12] = np.roll(up_sampled[12],3,axis=1)
    up_sampled[13]=np.roll(up_sampled[13],(-1,3),axis=(0,1))
    up_sampled[14]=np.roll(up_sampled[14],(-2,3),axis=(0,1))    
    up_sampled[15]=np.roll(up_sampled[15],(-3,3),axis=(0,1))     
    
 
    #compositing
    final_image_array = np.mean(up_sampled, 0).astype(np.uint16)
    #final_image_array = np.median(up_sampled, 0).astype(np.uint16)

    ref_img = up_sampled[0]
    
    return final_image_array, ref_img




