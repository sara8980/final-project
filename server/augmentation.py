import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import imread
from scipy import ndimage
import os

from keras.src.legacy.preprocessing.image import ImageDataGenerator
# Keras function to augment the image
image_gen = ImageDataGenerator(rotation_range=30,
         width_shift_range=0.1,
         height_shift_range=0.1,
         shear_range=0.15,
         zoom_range=[0.9, 1.1],
         horizontal_flip=True,
         vertical_flip=False,
         fill_mode='reflect',
         data_format='channels_last',
         brightness_range=[0.5, 1.5])

img_path = './marilyn_monroe.jpg'

outputImages = os.listdir('DB/train/Q80-120')

images = [img for img in outputImages]

i = 200

for img_name in images:
    img_path = f'DB/train/Q80-120/{img_name}'

    img = imread(img_path)

    if len(img.shape) == 3 and img.shape[2] == 3:
        img = np.dot(img[..., :3], [0.2989, 0.587, 0.114])

        # Add channel dimension
    img = np.expand_dims(img, axis=-1)

    # Add a batch dimension
    img = np.expand_dims(img, axis=0)

    # Generate batches of augmented images from the original image
    aug_iter = image_gen.flow(img, save_to_dir='DB/train/Q80-120', save_prefix='img', save_format='jpeg')

    # Get 9 samples of augmented images
    for _ in range(9):
        next(aug_iter)

    i += 1




