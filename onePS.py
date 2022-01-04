# Helper functions for one pixel shift


# a modification to do .raw files

import os
import cv2
import numpy as np
import gc as gc_import


# Function gamma correction
def gc(img, correction):
    img = img/(2.0**16-1)
    img = np.power(img, 1/correction)
    return np.uint16(img*(2.0**16-1))

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
    
def produce_ps1_image(image_files, folder_name):    
    bayr = []
    cm=[]
    for img in image_files:
        f=os.path.join(folder_name,img)
    
        npimg = np.fromfile(f, dtype=np.uint16)
        bayr.append( npimg.reshape((3024, 4096))) #the user may need to change file size
    
    
    cm.append(np.tile(np.array([[3, 2],[0, 1]]), [int(3024/2),int(4096/2)])) #the user may need to change file size
    # the user may also need to change colormap grid pattern depending on the Bayer grid used
    
    r=[]
    g1=[]
    b=[]
    g2=[]
    
    # Aligning 1-pixel sensor offsets of images and bayer RGB colors to picture 1
    print('Aligning 1-pixel sensor offsets of PSMS shots and bayer RGB colors to first shot')
    bayr[1]=np.roll(bayr[1],-1,axis=0)
    cm.append(np.roll(cm[0],1,axis=0))
    
    bayr[2]=np.roll(bayr[2],(-1,1),axis=(0,1))
    cm.append(np.roll(cm[0],(1,-1),axis=(0,1)))
    
    bayr[3] = np.roll(bayr[3],1,axis=1)
    cm.append(np.roll(cm[0],-1,axis=1))
    
    
    # Getting color pixels from all 4 images to RGB channels
    print('Getting color pixels from all 4 source RAW images for RGB channels')
    for i in range (0,4):
        r.append(bayr[i]*(cm[i] == 0).astype(int))
        g1.append(bayr[i]*(cm[i] == 1).astype(int))
        b.append(bayr[i]*(cm[i] == 2).astype(int))
        g2.append(bayr[i]*(cm[i] == 3).astype(int))
    
    # Combining pixels to color channels
    print('Combining pixels to color channels')
    r = r[0]+(r[1])+r[2]+r[3]    
    g1 = g1[0]+g1[1]+g1[2]+g1[3]
    g2 = g2[0]+g2[1]+g2[2]+g2[3]    
    g = np.median([g1,g2],axis=0)
    b = b[0]+b[1]+b[2]+b[3]
    
    r=np.float32(r)
    g=np.float32(g)
    b=np.float32(b)
    
    r=np.clip(r,0,65535)
    g=np.clip(g,0,65535)
    b=np.clip(b,0,65535)
  
    # Merging color channels to one picture
    print('Merging color channels to RGB image')
    img = np.dstack((b,g,r))
    
    ## create original image
    img0=cv2.demosaicing(bayr[0], cv2.COLOR_BAYER_GR2BGR)
    
    
    # Clearing temp color channels
    r=None
    g=None
    b=None
    
    img = np.float32(img)
    img0 = np.float32(img0)
    
    # Applying gamma correction
    print('Applying gamma correction')
    img = gc(img,1.4)
    img0 = gc(img0, 1.4)
    
    # Stretching brightness to cover 16 bit per channel range
    # note our images are 10bit, but left-shifted by 4, so this ends up working well
    #even if it's not technically correct
    print('Stretching brightness to 16 bit per channel range')
    img*=4
    img =np.clip(img,0,2**16-1)
    img = np.uint16(img)
    img0*=4
    img0 =np.clip(img0,0,2**16-1)
    img0 = np.uint16(img0)
    
    print('applying unsharp mask')
    img_sharp = unsharp_mask(img, amount=1)
    img0_sharp = unsharp_mask(img0, amount=1)
    
    #Write image to 16-bit TIFF file
    print('Writing the PSMS file to ',f.replace('.raw','_4shot.png'))
    #cv2.imwrite(f.replace('.raw','_4shot.png'),img_sharp)
    #cv2.imwrite(f.replace('.raw','_original.png'),img0_sharp)
    cv2.imwrite(f.replace('.raw','_4shot.tiff'),img_sharp)
    cv2.imwrite(f.replace('.raw','_original.tiff'),img0_sharp)    
    
    del r, g, b, g1, g2
    del bayr
    del cm
    del img0
    del img0_sharp
    gc_import.collect()

    return img_sharp
